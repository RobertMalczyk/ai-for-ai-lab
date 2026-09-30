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
        self.assertEqual(data["stats"]["sessions_agent1"] + data["stats"]["sessions_agent2"], len(rows))
        self.assertIsNone(data["external"])

    def test_curated_references_exist(self):
        curated = json.loads((ROOT / "site/interactions.json").read_text(encoding="utf-8"))
        refs = [r for group in ("agent_interactions", "self_corrections", "human_decisions")
                for item in curated[group] for r in item["refs"]]
        for ref in refs:
            self.assertTrue((ROOT / ref).is_file(), ref)


if __name__ == "__main__":
    unittest.main()
