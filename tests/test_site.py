import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class SiteBuildTest(unittest.TestCase):
    def test_offline_build_uses_ledger_and_fills_template(self):
        with tempfile.TemporaryDirectory() as out:
            subprocess.run([sys.executable, str(ROOT / "site/build.py"), "--offline", "--out", out],
                           check=True, stdout=subprocess.PIPE)
            page = (Path(out) / "index.html").read_text(encoding="utf-8")
            data = json.loads((Path(out) / "data.json").read_text(encoding="utf-8"))
        rows = [l for l in (ROOT / "lab/sessions.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertNotIn("{{", page)
        self.assertEqual(data["stats"]["sessions"], len(rows))
        self.assertEqual(data["stats"]["sessions_agent1"] + data["stats"]["sessions_agent2"]
                         + data["stats"]["sessions_admin"], len(rows))
        self.assertIsNone(data["external"])

    def test_curated_references_exist(self):
        curated = json.loads((ROOT / "site/interactions.json").read_text(encoding="utf-8"))
        refs = [r for group in ("agent_interactions", "self_corrections", "human_decisions")
                for item in curated[group] for r in item["refs"]]
        for ref in refs:
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_proof_is_anchored_in_repository(self):
        proof = json.loads((ROOT / "site/proof.json").read_text(encoding="utf-8"))
        refs = [r for group in ("wins", "defects", "unproven") for item in proof[group] for r in item["refs"]]
        refs += [w["report"] for w in proof["wins"]]
        for ref in refs:
            self.assertTrue((ROOT / ref).is_file(), ref)
        for w in proof["wins"]:
            report = json.loads((ROOT / w["report"]).read_text(encoding="utf-8"))
            self.assertIn("baseline_value", report, w["report"])
            self.assertIn("intervention_value", report, w["report"])
        for replay in proof["replays"]:
            for side in ("before", "after"):
                commit = replay[side]["commit"]
                found = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", commit + "^{commit}"],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.assertEqual(found.returncode, 0, commit)

    def test_journal_and_lexicon_are_anchored(self):
        sys.path.insert(0, str(ROOT / "site"))
        try:
            import build
        finally:
            sys.path.pop(0)
        sessions = {json.loads(l)["session"] for l in
                    (ROOT / "lab/sessions.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
        entries = build.journal()
        self.assertTrue(entries)
        days = [e["day"] for e in entries]
        self.assertEqual(days, sorted(set(days)))
        for e in entries:
            self.assertTrue(set(e["sessions"]) <= sessions, e["file"])
            self.assertTrue(e["body"].strip())
        dates = {e["date"] for e in entries}
        for term in build.lexicon():
            self.assertIn(term["first_seen"], dates, term["term"])
            self.assertTrue((ROOT / term["ref"]).is_file(), term["ref"])
            used = any(term["term"] in e["body"] for e in entries if e["date"] == term["first_seen"])
            self.assertTrue(used, "lexicon term must come from a journal entry: " + term["term"])
        self.assertEqual(build.inline_md("`a/*` and `b/*`"), "<code>a/*</code> and <code>b/*</code>")


if __name__ == "__main__":
    unittest.main()
