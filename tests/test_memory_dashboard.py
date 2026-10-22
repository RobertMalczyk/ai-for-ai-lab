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


def export(feedback=(), memories=(), decisions=(), cfg=CFG, now=NOW):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        if cfg is not None:
            (d / "config.v1.json").write_text(json.dumps(cfg))
        for name, rows in (("feedback", feedback), ("memories", memories), ("decisions", decisions)):
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


if __name__ == "__main__":
    unittest.main()
