import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
MAP = json.loads((ROOT / "site/decision-map.json").read_text(encoding="utf-8"))

TYPES = {"decision", "owner_decision", "action", "review", "correction", "external_event",
         "submission", "rejection", "blocker"}
STATUSES = {"active", "resolved", "waiting", "rejected", "blocked", "parked", "superseded"}
ACTORS = {"owner", "agent1", "agent2", "both_agents", "maintainer", "system"}
TRACKS = {"transparency", "site", "lab", "usefulness", "external", "pytest", "distutils", "discovery"}
RELATIONS = {"led_to", "branched_to", "reviewed_by", "challenged_by", "corrected_by", "rejected_because",
             "blocked_by", "superseded_by", "reopened_by", "approved_by", "submitted_as", "waiting_on",
             "resolved_by", "followed_by"}


class DecisionMapDataTest(unittest.TestCase):
    def test_ids_unique_and_enums_valid(self):
        ids = [n["id"] for n in MAP["nodes"]]
        self.assertEqual(len(ids), len(set(ids)))
        for n in MAP["nodes"]:
            self.assertIn(n["type"], TYPES, n["id"])
            self.assertIn(n["status"], STATUSES, n["id"])
            self.assertIn(n["actor"], ACTORS, n["id"])
            self.assertIn(n["track"], TRACKS, n["id"])
            self.assertRegex(n["date"], r"^\d{4}-\d{2}-\d{2}$")
        for e in MAP["edges"]:
            self.assertIn(e["relation"], RELATIONS, e)

    def test_edges_point_forward_between_existing_nodes(self):
        order = {n["id"]: (n["date"], i) for i, n in enumerate(MAP["nodes"])}
        for e in MAP["edges"]:
            self.assertIn(e["source"], order, e)
            self.assertIn(e["target"], order, e)
            self.assertLess(order[e["source"]], order[e["target"]], e)
        for n in MAP["nodes"]:
            for c in n.get("children", []):
                self.assertIn(c, order, n["id"])

    def test_refs_exist_and_links_are_https(self):
        for n in MAP["nodes"]:
            self.assertTrue(n["refs"], n["id"])
            for ref in n["refs"]:
                self.assertTrue((ROOT / ref).is_file(), (n["id"], ref))
            if n["external_url"]:
                self.assertTrue(n["external_url"].startswith("https://"), n["id"])

    def test_every_decision_record_appears_once(self):
        decs = re.findall(r"^### (DEC-\d{4})", (ROOT / "docs/DECISIONS.md").read_text(encoding="utf-8"), re.M)
        mapped = [d for n in MAP["nodes"] for d in n["decision_ids"]]
        self.assertEqual(sorted(mapped), sorted(set(decs)))

    def test_every_human_decision_appears_once(self):
        human = json.loads((ROOT / "site/interactions.json").read_text(encoding="utf-8"))["human_decisions"]
        mapped = [(n["human_decision"]["date"], n["human_decision"]["starts"])
                  for n in MAP["nodes"] if "human_decision" in n]
        self.assertEqual(sorted(mapped), sorted((h["date"], h["text"][:48]) for h in human))

    def test_milestone_view_stays_small(self):
        self.assertLessEqual(sum(n["milestone"] for n in MAP["nodes"]), 40)

    def test_build_writes_map_page(self):
        with tempfile.TemporaryDirectory() as out:
            subprocess.run([sys.executable, str(ROOT / "site/build.py"), "--offline", "--out", out],
                           check=True, stdout=subprocess.PIPE)
            page = (Path(out) / "map.html").read_text(encoding="utf-8")
            self.assertTrue((Path(out) / "map.js").is_file())
            self.assertEqual(json.loads((Path(out) / "decision-map.json").read_text(encoding="utf-8")), MAP)
        self.assertNotIn("{{", page)


if __name__ == "__main__":
    unittest.main()
