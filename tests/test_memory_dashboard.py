import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "site"))
import memory_export as mx  # noqa: E402

GH = "https://github.com/RobertMalczyk/ai-for-ai-lab"
NOW = dt.datetime(2026, 10, 22, tzinfo=dt.timezone.utc)
CFG = {"contract_version": "1.0.0", "rule_version": "1.0.0", "memory_enabled": True, "reward_mode": "shadow",
       "reward_influence": 0.0, "coupling_scope": "none", "changed_at": "2026-10-22T00:00:00Z",
       "canary": {"min_decisions": 30, "min_per_agent": 10, "min_task_types": 3}}


def ev(i, agent="agent1", task="T1", key="k1", cat="new_finding", val=0.2, status="verified", at="2026-10-21T10:00:00Z",
       verifier="agent2", proposer=None, sup=None, sess="s1", rule="1.0.0", refs=("lab/tasks/EXTERNAL.md",)):
    return {"event_id": i, "task_id": task, "evidence_key": key, "agent": agent, "proposer": proposer or agent,
            "verifier": verifier, "status": status, "category": cat, "value": val, "rule_version": rule,
            "rationale": "t", "source_refs": list(refs), "occurred_at": at, "verified_at": at, "memory_ids": [],
            "session_id": sess, "supersedes": sup}


def export(feedback=(), memories=(), decisions=(), cfg=CFG, now=NOW, modes=(), receipts=(), utility=()):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        if cfg is not None:
            (d / "config.v1.json").write_text(json.dumps(cfg))
        for name, rows in (("feedback", feedback), ("memories", memories), ("decisions", decisions),
                           ("mode_history", modes), ("retrievals", receipts), ("utility", utility)):
            if rows:
                (d / f"{name}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        return mx.build_export(d, GH, now=now)


class MemoryExportTest(unittest.TestCase):
    def test_missing_contract_is_unavailable_not_success(self):
        e = export(cfg=None)
        self.assertEqual((e["data_status"], e["mode"], e["demo"]), ("unavailable", "UNKNOWN", False))

    def test_empty_journals_mean_no_data(self):
        e = export()
        self.assertEqual(e["data_status"], "empty")
        self.assertEqual(e["events"], [])
        self.assertEqual(e["agents"]["agent1"]["positive"], 0)

    def test_only_pending_counts_nothing(self):
        e = export([ev("p1", cat="unresolved", val=None, status="pending", verifier=None)])
        a = e["agents"]["agent1"]
        self.assertEqual((a["pending"], a["graded"], a["positive"], a["negative"]), (1, 0, 0, 0))

    def test_negative_and_self_verification(self):
        e = export([ev("n1", cat="repeated_error", val=-0.5), ev("s1", task="T2", key="k2", verifier="agent1")])
        a = e["agents"]["agent1"]
        self.assertEqual((a["negative"], a["positive"], a["graded"]), (-0.5, 0, 1))

    def test_category_value_mismatch_is_ignored(self):
        e = export([ev("x1", cat="useful_result", val=-1)])
        self.assertEqual(e["agents"]["agent1"]["graded"], 0)

    def test_retraction_reverses_once_and_keeps_history(self):
        e = export([ev("a"), ev("b", status="retracted", sup="a", at="2026-10-21T11:00:00Z"),
                    ev("c", key="k9", task="T9", sess="s9", at="2026-10-21T12:00:00Z")])
        self.assertEqual(e["agents"]["agent1"]["positive"], 0.2)
        row = next(x for x in e["events"] if x["id"] == "b")
        self.assertEqual([h["id"] for h in row["history"]], ["a"])

    def test_duplicate_evidence_counts_once(self):
        e = export([ev("a", cat="useful_result", val=1, key="pr"), ev("b", cat="useful_result", val=1, key="pr", at="2026-10-21T12:00:00Z")])
        a = e["agents"]["agent1"]
        self.assertEqual((a["positive"], a["duplicates"]), (1.0, 1))

    def test_caps_per_task_and_discovery_session(self):
        e = export([ev("a", cat="useful_result", val=1, key="x"), ev("b", cat="review_correction", val=0.5, key="y"),
                    ev("c", task="T5", key="z", sess="s2"), ev("d", task="T6", key="w", sess="s2")])
        a = e["agents"]["agent1"]
        self.assertEqual((a["positive"], a["capped"]), (1.2, 2))

    def test_retracted_lesson_and_seed_counts(self):
        mem = lambda i, st, sup=None, seed=False: {"id": i, "visibility": "public", "status": st, "supersedes": sup,
                                                   "created_at": "2026-10-21T00:00:00Z", "historical_seed": seed,
                                                   "correction_effective_at": "2026-10-21T00:00:00Z" if sup else None}
        e = export(memories=[mem("m1", "active", seed=True), mem("m2", "active"), mem("m2r", "retracted", "m2")])
        self.assertEqual(e["memories"]["public"], {"active": 1, "provisional": 0, "superseded": 0, "retracted": 1})
        self.assertEqual((e["memories"]["historical_seed"], e["memories"]["corrections"]), (1, 1))
        self.assertFalse(e["memories"]["private"]["available"])

    def test_rule_versions_are_kept_per_event(self):
        e = export([ev("a"), ev("b", task="T2", key="k2", sess="s2", rule="1.1.0")])
        self.assertEqual(sorted({x["rule_version"] for x in e["events"]}), ["1.0.0", "1.1.0"])

    def test_stale_export_is_flagged(self):
        e = export([ev("a", at="2026-10-01T00:00:00Z")])
        self.assertEqual(e["data_status"], "stale")

    def test_only_safe_links_leave_the_build(self):
        e = export([ev("a", refs=("lab/tasks/EXTERNAL.md", "/mnt/private/x.md", "https://example.com/secret",
                                  "../../etc/passwd", GH + "/pull/86"))])
        self.assertEqual(e["events"][0]["refs"], [GH + "/blob/main/lab/tasks/EXTERNAL.md", GH + "/pull/86"])

    def test_private_records_are_not_counted(self):
        e = export(memories=[{"id": "p", "visibility": "private", "status": "active", "supersedes": None,
                              "created_at": "2026-10-21T00:00:00Z"}])
        self.assertEqual(sum(e["memories"]["public"].values()), 0)
        self.assertNotIn('"p"', json.dumps(e["memories"]))

    def test_shadow_mode_reports_zero_influence(self):
        e = export()
        self.assertEqual((e["mode"], e["reward_influence"], e["memory_enabled"]), ("SHADOW", 0.0, True))
        self.assertEqual(e["mode_history"][0]["to"], "SHADOW")


class MemoryPageBuildTest(unittest.TestCase):
    def test_build_writes_page_real_export_and_separate_demo(self):
        with tempfile.TemporaryDirectory() as out:
            subprocess.run([sys.executable, str(ROOT / "site/build.py"), "--offline", "--out", out],
                           check=True, stdout=subprocess.PIPE)
            out = Path(out)
            page = (out / "memory.html").read_text(encoding="utf-8")
            real = json.loads((out / "memory-export.json").read_text(encoding="utf-8"))
            demo = json.loads((out / "memory-demo.json").read_text(encoding="utf-8"))
            self.assertTrue((out / "memory.js").is_file())
            text = "".join(p.read_text(encoding="utf-8", errors="ignore") for p in out.rglob("*") if p.is_file()
                           and p.suffix in (".html", ".json", ".js"))
        self.assertNotIn("{{", page)
        self.assertFalse(real["demo"])
        self.assertTrue(demo["demo"])
        self.assertFalse(set(e["id"] for e in demo.get("events", [])) & set(e["id"] for e in real.get("events", [])))
        for needle in ("/mnt/project-files", "/home/claude", "EQUILIBRIUM_TOKEN", "pilot-log"):
            self.assertNotIn(needle, text)


def dec(i, agent="agent2", mids=("m1",), at="2026-10-21T12:00:00Z", ref=None):
    return {"decision_id": i, "agent": agent, "task_id": "T-" + i, "task_type": "preflight", "session_id": "s1",
            "occurred_at": at, "rule_version": "1.0.0", "memory_ids": list(mids), "suggested_action": "a",
            "actual_action": "a", "shadow_memory_ids": list(mids), "alternative_outcome": "unobserved",
            "evaluation_ref": ref, "cost": {"value": None, "unit": None, "measured": False}, "map_node_ids": []}


def util(i, did, verifier="agent1", status="verified", agent="agent2", refs=("lab/tasks/EXTERNAL.md",)):
    return {"assessment_id": i, "agent": agent, "memory_id": "m1", "decision_id": did, "context": "preflight",
            "utility": 1, "verifier": verifier, "source_refs": list(refs), "occurred_at": "2026-10-21T13:00:00Z",
            "status": status, "supersedes": None}


class RuntimeJournalAdaptationTest(unittest.TestCase):
    """Agent 2's adaptation to the merged runtime (#101): the cases Agent 1 listed in MEMORY_RUNTIME_V1.md."""

    def test_disputed_with_null_value_is_disputed_not_pending(self):
        a = export([ev("a", status="disputed", val=None)])["agents"]["agent1"]
        self.assertEqual((a["disputed"], a["pending"]), (1, 0))

    def test_records_not_yet_available_or_effective_are_left_out(self):
        mem = lambda i, st, sup=None, avail="2026-10-20T00:00:00Z", eff=None: {
            "id": i, "visibility": "public", "status": st, "supersedes": sup, "available_at": avail,
            "created_at": "2026-10-01T00:00:00Z", "correction_effective_at": eff}
        e = export(memories=[mem("m1", "active"), mem("m2", "active", avail="2026-10-23T00:00:00Z"),
                             mem("m1r", "retracted", "m1", eff="2026-10-23T00:00:00Z")])
        self.assertEqual(e["memories"]["public"]["active"], 1)
        self.assertEqual(e["memories"]["public"]["retracted"], 0)
        self.assertEqual(e["last_success_at"], "2026-10-20T00:00:00+00:00")

    def test_freshness_is_the_journal_write_not_the_historical_lesson_date(self):
        m = {"id": "m1", "visibility": "public", "status": "active", "supersedes": None, "historical_seed": True,
             "created_at": "2026-10-04T00:00:00Z", "available_at": "2026-10-21T00:00:00Z"}
        e = export(memories=[m])
        self.assertEqual((e["last_success_at"], e["data_status"]), ("2026-10-21T00:00:00+00:00", "available"))

    def test_zero_result_recall_and_recall_without_decision_are_shown(self):
        r = lambda i, mids: {"decision_id": i, "occurred_at": "2026-10-21T11:00:00Z", "memory_ids": mids}
        e = export(decisions=[dec("d1", mids=())], receipts=[r("d1", []), r("d2", ["m1"])])
        self.assertEqual(e["memories"]["retrievals"], 2)
        self.assertEqual((e["shadow"]["prepared"], e["shadow"]["no_lesson_found"], e["shadow"]["awaiting_decision"]),
                         (2, 1, 1))

    def test_decision_is_graded_only_by_an_independent_verified_assessment(self):
        decisions = [dec("d1"), dec("d2"), dec("d3"), dec("d4")]
        e = export(decisions=decisions, utility=[util("u1", "d1"), util("u2", "d2", verifier="agent2"),
                                                 util("u3", "d3", status="pending"),
                                                 util("u4", "d4", refs=("/home/x/notes.md",))])
        self.assertEqual(e["shadow"]["evaluated"], 1)
        self.assertEqual([r["decision_id"] for r in e["memories"]["recent_applications"]], ["d1"])
        crit = {c["id"]: c for c in e["readiness"]["criteria"]}
        self.assertEqual(crit["per_agent"]["observed"], {"agent1": 0, "agent2": 1})
        self.assertNotIn("/home/x", json.dumps(e))

    def test_real_journals_on_main_export_without_inventing_activity(self):
        e = mx.build_export(ROOT / "lab/memory", GH)
        self.assertEqual(e["mode"], "SHADOW")
        self.assertEqual(e["reward_influence"], 0)
        self.assertGreater(e["memories"]["public"]["active"], 0)
        self.assertEqual(e["memories"]["retrievals"], len(mx._jsonl(ROOT / "lab/memory/retrievals.jsonl")))
        self.assertGreaterEqual(e["last_success_at"], "2026-10-26")


class ExportSchemaConformanceTest(unittest.TestCase):
    """Stdlib check of the DEMO export against the required fields of Agent 1's accepted schema."""

    def setUp(self):
        self.schema = json.loads((ROOT / "lab/memory/export.v1.schema.json").read_text(encoding="utf-8"))
        self.env = mx.build_export(ROOT / "site/memory-demo", GH, now=NOW, demo=True)

    def test_top_level_keys_are_allowed_and_required(self):
        props = self.schema["properties"]
        self.assertFalse(set(self.env) - set(props))
        required = set(self.schema["required"]) | set(self.schema["allOf"][0]["then"]["required"])
        self.assertFalse(required - set(self.env))

    def test_private_memory_is_only_unavailable_flag(self):
        self.assertEqual(self.env["memories"]["private"], {"available": False})

    def test_agent_cards_and_criteria_carry_required_fields(self):
        agent_req = set(self.schema["$defs"]["agent"]["required"])
        for a in ("agent1", "agent2"):
            self.assertFalse(agent_req - set(self.env["agents"][a]))
        crit = self.schema["properties"]["readiness"]["properties"]["criteria"]["items"]
        for c in self.env["readiness"]["criteria"]:
            self.assertFalse(set(crit["required"]) - set(c))
            self.assertFalse(set(c) - set(crit["properties"]))
            if c["met"] is not True:
                self.assertTrue(c["gaps"], c["id"])


class ReferenceLeakTest(unittest.TestCase):
    """Agent 1's Session 159 replay: absolute private paths must not reach the public export."""

    LEAKS = ("/mnt/private/result.json", "/home/private/mode.md", "~/notes.md", "file:///etc/passwd",
             "C:\\Users\\x.md", "C:/Users/x.md", "mailto:a@b.c", "https://example.com/private",
             "lab/../../etc/passwd", " lab/x.md", "lab/%2e%2e/x", "./x.md", "lab/x.md\n/secret")

    def decision(self, ref):
        return {"decision_id": "d", "agent": "agent1", "task_id": "T", "task_type": "build", "session_id": "s",
                "occurred_at": "2026-10-21T00:00:00Z", "rule_version": "1.0.0", "memory_ids": ["m"],
                "suggested_action": "x", "actual_action": "x", "shadow_memory_ids": ["m"],
                "alternative_outcome": "unobserved", "evaluation_ref": ref,
                "cost": {"value": None, "unit": None, "measured": False}, "map_node_ids": []}

    def mode(self, refs, by=("agent1",)):
        return {"at": "2026-10-21T00:00:00Z", "from": None, "to": "SHADOW", "influence": 0, "scope": "none",
                "rule_version": "1.0.0", "decided_by": list(by), "reason": "t", "evidence_refs": list(refs)}

    def test_session_159_cases_are_removed(self):
        e = export(decisions=[self.decision("/mnt/private/result.json")],
                   modes=[self.mode(["/home/private/mode.md", "docs/DECISIONS.md"])])
        text = json.dumps(e)
        self.assertNotIn("/mnt/private", text)
        self.assertNotIn("/home/private", text)
        self.assertEqual(e["mode_history"][0]["evidence_refs"], [f"{GH}/blob/main/docs/DECISIONS.md"])
        self.assertEqual(e["memories"]["recent_applications"], [])

    def test_no_leak_vector_reaches_any_reference_field(self):
        for leak in self.LEAKS:
            with self.subTest(leak=leak):
                e = export(feedback=[ev("a", refs=(leak,))], decisions=[self.decision(leak)],
                           modes=[self.mode([leak])])
                self.assertEqual(e["events"][0]["refs"], [])
                self.assertEqual(e["mode_history"][0]["evidence_refs"], [])
                self.assertEqual(e["memories"]["recent_applications"], [])
                for c in e["readiness"]["criteria"]:
                    self.assertEqual(c["evidence_refs"], [])

    def test_safe_references_survive(self):
        e = export(decisions=[self.decision("lab/tasks/EXTERNAL.md")], modes=[self.mode([f"{GH}/pull/86"])])
        self.assertEqual(e["memories"]["recent_applications"][0]["evaluation_ref"],
                         f"{GH}/blob/main/lab/tasks/EXTERNAL.md")
        self.assertEqual(e["mode_history"][0]["evidence_refs"], [f"{GH}/pull/86"])

    def test_mode_history_fields_are_whitelisted(self):
        m = dict(self.mode([]), private_note="/mnt/private/x", decided_by=["someone@example.com"])
        out = export(modes=[m])["mode_history"][0]
        self.assertNotIn("private_note", out)
        self.assertEqual(out["decided_by"], ["unknown"])


if __name__ == "__main__":
    unittest.main()
