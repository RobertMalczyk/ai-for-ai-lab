"""Build the sanitized public export for the "Memory and learning" page. Stdlib only.

Reads the public memory contract (lab/memory/config.v1.json) and the public
append-only journals (lab/memory/{memories,feedback,decisions,mode_history}.jsonl)
and writes one JSON envelope shaped by lab/memory/export.v1.schema.json.

Rules from the owner's instruction of 2026-10-22 and contract v1:
- only verified feedback counts; pending/disputed are counted, never averaged;
- corrections append a record with `supersedes`; the newest record of a chain wins;
- duplicates are folded on (agent, task, evidence, category), not on event_id;
- positive credit is capped at +1 per agent and task, discovery at +0.2 per agent and session;
- nothing private is exported: only public records, safe links and aggregates;
- empty or missing data means "no data", never success; DEMO data never enters this export.
"""
import datetime as dt
import json
from collections import defaultdict
from pathlib import Path

EXPORT_VERSION = "1.0.0"
AGENTS = ("agent1", "agent2")
STALE_AFTER_DAYS = 7
CATEGORY_VALUE = {"useful_result": 1, "review_correction": 0.5, "new_finding": 0.2, "activity": 0,
                  "repeated_error": -0.5, "constraint_violation": -1, "unresolved": None}
MODES = ("SHADOW", "CANARY", "COUPLED", "ROLLED_BACK")


def _jsonl(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _ts(text):
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00")) if text else None


def safe_ref(ref, github):
    """Keep links that are public by construction: repo-relative paths, this repo, public arXiv."""
    if not isinstance(ref, str) or not ref:
        return None
    if ref.startswith(github + "/") or ref.startswith("https://arxiv.org/"):
        return ref
    if ref.startswith(("http://", "https://", "/", "~", "file:")) or ".." in ref or "\\" in ref:
        return None
    return f"{github}/blob/main/{ref}"


def fold(records, key):
    """Newest record of each `supersedes` chain wins; returns (effective, chains)."""
    by_id = {r[key]: r for r in records}
    replaced = {r["supersedes"] for r in records if r.get("supersedes")}
    chains = {}
    for r in records:
        if r[key] in replaced:
            continue
        chain, cur, seen = [r], r, {r[key]}
        while cur.get("supersedes") in by_id and cur["supersedes"] not in seen:
            cur = by_id[cur["supersedes"]]
            seen.add(cur[key])
            chain.append(cur)
        chains[r[key]] = list(reversed(chain))
    return [chains[k][-1] for k in chains], chains


def score(feedback):
    """Per-agent aggregates from effective feedback, with dedup and both caps."""
    effective, chains = fold(feedback, "event_id")
    agents = {a: {"positive": 0.0, "negative": 0.0, "net": 0.0, "graded": 0, "pending": 0,
                  "disputed": 0, "duplicates": 0, "capped": 0} for a in AGENTS}
    seen, task_pos, session_disc, counted = set(), defaultdict(float), defaultdict(float), {}
    for e in sorted(effective, key=lambda e: (e["occurred_at"], e["event_id"])):
        a = agents.get(e["agent"])
        if a is None:
            continue
        status = e["status"]
        if status in ("pending", "proposed") or e.get("value") is None:
            a["pending"] += 1
            continue
        if status == "disputed":
            a["disputed"] += 1
            continue
        if status != "verified" or not e.get("verifier") or e["verifier"] == e.get("proposer"):
            continue
        if CATEGORY_VALUE.get(e["category"], "x") != e["value"]:
            continue
        k = (e["agent"], e["task_id"], e["evidence_key"], e["category"])
        if k in seen:
            a["duplicates"] += 1
            continue
        seen.add(k)
        v = float(e["value"])
        if v > 0:
            room = 1.0 - task_pos[(e["agent"], e["task_id"])]
            if e["category"] == "new_finding":
                room = min(room, 0.2 - session_disc[(e["agent"], e.get("session_id"))])
            credit = max(0.0, min(v, room))
            if credit < v:
                a["capped"] += 1
            task_pos[(e["agent"], e["task_id"])] += credit
            if e["category"] == "new_finding":
                session_disc[(e["agent"], e.get("session_id"))] += credit
            a["positive"] += credit
            counted[e["event_id"]] = credit
        else:
            a["negative"] += v
            counted[e["event_id"]] = v
        a["graded"] += 1
    for a in agents.values():
        a["positive"], a["negative"] = round(a["positive"], 3), round(a["negative"], 3)
        a["net"] = round(a["positive"] + a["negative"], 3)
    return agents, effective, chains, counted


def memory_aggregates(memories, decisions, now):
    effective, chains = fold([m for m in memories if m.get("visibility") == "public"], "id")
    by_status = defaultdict(int)
    for m in effective:
        status = m["status"]
        if m.get("correction_effective_at") and _ts(m["correction_effective_at"]) > now:
            status = chains[m["id"]][-2]["status"] if len(chains[m["id"]]) > 1 else status
        by_status[status] += 1
    uses = defaultdict(int)
    for d in decisions:
        for mid in d.get("memory_ids", []):
            uses[mid] += 1
    corrections = sum(1 for m in memories if m.get("supersedes"))
    return {
        "public": {s: by_status.get(s, 0) for s in ("active", "provisional", "superseded", "retracted")},
        "historical_seed": sum(1 for m in effective if m.get("historical_seed")),
        "retrievals": sum(uses.values()),
        "corrections": corrections,
        "recent_applications": [
            {"decision_id": d["decision_id"], "agent": d["agent"], "at": d["occurred_at"],
             "memory_ids": d["memory_ids"], "evaluation_ref": d.get("evaluation_ref")}
            for d in sorted(decisions, key=lambda d: d["occurred_at"], reverse=True)
            if d.get("memory_ids") and d.get("evaluation_ref")][:5],
        "private": {"available": False},
    }


def readiness(cfg, decisions, github):
    c = cfg.get("canary", {})
    graded = [d for d in decisions if d.get("evaluation_ref")]
    per_agent = {a: sum(1 for d in graded if d["agent"] == a) for a in AGENTS}
    types = {d.get("task_type") for d in graded if d.get("task_type")}
    measured = [d for d in decisions if (d.get("cost") or {}).get("measured")]
    refs = sorted({r for r in (safe_ref(d["evaluation_ref"], github) for d in graded) if r})[:5]
    need_dec, need_agent, need_types = c.get("min_decisions", 30), c.get("min_per_agent", 10), c.get("min_task_types", 3)

    def crit(cid, label, threshold, observed, met, evidence, gaps):
        return {"id": cid, "label": label, "threshold": threshold, "observed": observed, "met": met,
                "evidence_refs": evidence, "gaps": gaps if met is not True else []}
    return {
        "criteria": [
            crit("decisions", "New graded decisions, both agents", c.get("min_decisions"), len(graded),
                 len(graded) >= need_dec, refs, [f"{need_dec - len(graded)} more graded decisions"]),
            crit("per_agent", "Graded decisions per agent", c.get("min_per_agent"), per_agent,
                 min(per_agent.values()) >= need_agent, refs,
                 [f"Agent {a[-1]}: {need_agent - n} more" for a, n in per_agent.items() if n < need_agent]),
            crit("task_types", "Kinds of real tasks", c.get("min_task_types"), len(types),
                 len(types) >= need_types, refs, [f"{need_types - len(types)} more kind(s) of task"]),
            crit("paired", "Memory without Q vs memory with Q trials", c.get("min_paired_trials"), 0, False, [],
                 ["No paired trials recorded; SHADOW does not run them."]),
            crit("net_wins", "Wins minus losses for Q", c.get("min_net_wins"), None, False, [],
                 ["No paired trials to compare."]),
            crit("cost", "Median full cost increase", c.get("max_median_cost_increase"),
                 None if not measured else len(measured), False, [], ["Full cost is not measured yet."]),
            crit("safety", "Privacy leaks, duplicate awards, hard-limit breaches", 0, None, None, [],
                 ["No privacy and duplicate-award audit recorded yet."]),
            crit("rollback", "Rollback verified", True, None, None, [], ["Rollback has not been exercised."]),
        ],
        "assessments": {a: {"written_at": None, "decision": None, "refs": []} for a in AGENTS},
        "note": "Operational threshold for a small pilot, not statistical proof. Unmet or unknown criteria keep SHADOW.",
    }


def build_export(mem, github, now=None, source_commit=None, demo=False):
    now = now or dt.datetime.now(dt.timezone.utc)
    mem = Path(mem)
    cfg_path = mem / "config.v1.json"
    env = {"export_version": EXPORT_VERSION, "demo": demo, "generated_at": now.isoformat(timespec="seconds"),
           "source_commit": source_commit, "data_status": "unavailable", "last_success_at": None}
    if not cfg_path.exists():
        env.update(mode="UNKNOWN", memory_enabled=None, reason="The memory contract is not on the main branch yet.")
        return env
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    memories, feedback = _jsonl(mem / "memories.jsonl"), _jsonl(mem / "feedback.jsonl")
    decisions, modes = _jsonl(mem / "decisions.jsonl"), _jsonl(mem / "mode_history.jsonl")
    mode = {"shadow": "SHADOW", "canary": "CANARY", "coupled": "COUPLED", "rolled_back": "ROLLED_BACK"}.get(
        str(cfg.get("reward_mode", "")).lower(), "UNKNOWN")
    if not modes:
        modes = [{"at": cfg.get("changed_at"), "from": None, "to": mode, "influence": cfg.get("reward_influence"),
                  "scope": cfg.get("coupling_scope"), "rule_version": cfg.get("rule_version"),
                  "decided_by": ["owner"], "reason": "Initial configuration: memory on, rewards observed only.",
                  "evidence_refs": ["docs/owner/2026-10-22-memory-feedback-dashboard.md"]}]
    agents, effective, chains, counted = score(feedback)
    events = []
    for e in sorted(effective, key=lambda e: e["occurred_at"], reverse=True):
        history = chains[e["event_id"]]
        events.append({
            "id": e["event_id"], "agent": e["agent"], "task": e["task_id"], "category": e["category"],
            "status": e["status"], "value": e.get("value"), "credited": counted.get(e["event_id"]),
            "rule_version": e["rule_version"], "reason": e["rationale"], "occurred_at": e["occurred_at"],
            "verified_at": e.get("verified_at"), "verifier": e.get("verifier"), "proposer": e.get("proposer"),
            "refs": [r for r in (safe_ref(x, github) for x in e.get("source_refs", [])) if r],
            "memory_ids": e.get("memory_ids", []),
            "history": [{"id": h["event_id"], "status": h["status"], "value": h.get("value"),
                         "at": h.get("verified_at") or h["occurred_at"]} for h in history[:-1]],
        })
    stamps = [_ts(x) for x in [r.get("occurred_at") for r in feedback + decisions] + [r.get("created_at") for r in memories] if x]
    last = max(stamps) if stamps else None
    has_data = bool(feedback or decisions or memories)
    env.update({
        "data_status": "stale" if has_data and last and (now - last).days > STALE_AFTER_DAYS
        else ("available" if has_data else "empty"),
        "last_success_at": last.isoformat(timespec="seconds") if last else None,
        "contract_version": cfg.get("contract_version"), "rule_version": cfg.get("rule_version"),
        "implementation_status": cfg.get("implementation_status"),
        "mode": mode, "memory_enabled": cfg.get("memory_enabled"), "coupling_scope": cfg.get("coupling_scope"),
        "reward_influence": cfg.get("reward_influence"), "mode_history": modes,
        "agents": {a: dict(v, cost={"value": None, "unit": None, "measured": False}) for a, v in agents.items()},
        "events": events,
        "memories": memory_aggregates(memories, decisions, now),
        "shadow": {
            "decisions": len(decisions),
            "differences": sum(1 for d in decisions if d.get("shadow_memory_ids") and d["shadow_memory_ids"] != d.get("memory_ids")),
            "evaluated": sum(1 for d in decisions if d.get("evaluation_ref")),
            "note": "A choice Q would have made but nobody made has no observed outcome.",
        },
        "readiness": readiness(cfg, decisions, github),
        "map_links": [{"memory_id": m["id"], "map_node_ids": m["map_node_ids"]} for m in memories
                      if m.get("visibility") == "public" and m.get("map_node_ids")],
    })
    return env
