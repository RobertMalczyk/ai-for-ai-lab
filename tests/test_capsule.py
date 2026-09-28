import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from ai_for_ai_lab.capsule import CapsuleError, capture, check, loads


class CapsuleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "source.txt").write_text("evidence", encoding="utf-8")
        self.capsule = capture(self.root, "recover task", "run tests", ["source.txt"])

    def test_unchanged(self):
        self.assertTrue(check(self.root, self.capsule)["fresh"])

    def test_changed_same_size(self):
        (self.root / "source.txt").write_text("Evidence")
        result = check(self.root, self.capsule)
        self.assertFalse(result["fresh"])
        self.assertEqual(result["evidence"][0]["status"], "changed")

    def test_missing(self):
        (self.root / "source.txt").unlink()
        self.assertEqual(check(self.root, self.capsule)["evidence"][0]["status"], "missing")

    def test_touch_does_not_invalidate(self):
        os.utime(self.root / "source.txt", (1, 1))
        self.assertTrue(check(self.root, self.capsule)["fresh"])

    def test_unsafe_paths(self):
        for path in ("../outside", "/etc/passwd", "./source.txt", "a/../source.txt", "a\\b", ""):
            with self.subTest(path=path), self.assertRaises(CapsuleError):
                capture(self.root, "g", "n", [path])

    def test_symlink_rejected_at_check(self):
        (self.root / "target.txt").write_text("evidence")
        (self.root / "source.txt").unlink()
        (self.root / "source.txt").symlink_to("target.txt")
        with self.assertRaises(CapsuleError):
            check(self.root, self.capsule)

    def test_directory_replacement_is_error(self):
        (self.root / "source.txt").unlink()
        (self.root / "source.txt").mkdir()
        with self.assertRaises(CapsuleError):
            check(self.root, self.capsule)

    def test_invalid_documents(self):
        for key, value in (("version", True), ("version", 2), ("goal", " "), ("evidence", [])):
            bad = copy.deepcopy(self.capsule)
            bad[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(CapsuleError):
                check(self.root, bad)
        bad = copy.deepcopy(self.capsule)
        bad["evidence"].append(bad["evidence"][0])
        with self.assertRaises(CapsuleError):
            check(self.root, bad)

    def test_duplicate_json_keys(self):
        with self.assertRaises(CapsuleError):
            loads('{"version":1,"version":2}')

    def test_deterministic_capture(self):
        self.assertEqual(self.capsule, capture(self.root, "recover task", "run tests", ["source.txt", "source.txt"]))

    def test_cli_exit_contract(self):
        capsule_file = self.root / "capsule.json"
        capsule_file.write_text(json.dumps(self.capsule))
        def run():
            return subprocess.run([sys.executable, "-m", "ai_for_ai_lab", "check", "--root", str(self.root), str(capsule_file)], capture_output=True, text=True)
        self.assertEqual(run().returncode, 0)
        (self.root / "source.txt").write_text("changed")
        result = run()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["fresh"])
        capsule_file.write_text("{broken")
        result = run()
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
