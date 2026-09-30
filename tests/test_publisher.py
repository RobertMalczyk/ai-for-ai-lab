import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ai_for_ai_lab.capsule import CapsuleError
from ai_for_ai_lab.publisher import validate_plan


ROOT = Path(__file__).resolve().parent.parent


def plan(**changes):
    value = {
        "version": 1,
        "episode": "001",
        "evidence_refs": ["README.md"],
        "audience_feedback_use": "storytelling_only",
        "research_influence": "none",
        "visibility": "private",
        "human_review_required": True,
    }
    value.update(changes)
    return value


class PublisherPlanTests(unittest.TestCase):
    def test_valid_plan_returns_evidence_receipt(self):
        result = validate_plan(ROOT, plan())
        self.assertTrue(result["valid"])
        self.assertEqual(result["episode"], "001")
        self.assertEqual(result["evidence"][0]["path"], "README.md")
        self.assertEqual(len(result["evidence"][0]["sha256"]), 64)

    def test_missing_evidence_rejected(self):
        with self.assertRaisesRegex(CapsuleError, "missing") as caught:
            validate_plan(ROOT, plan(evidence_refs=["missing.md"]))
        self.assertEqual(caught.exception.code, "missing_evidence")

    def test_unsafe_evidence_rejected(self):
        with self.assertRaises(CapsuleError) as caught:
            validate_plan(ROOT, plan(evidence_refs=["../secret"]))
        self.assertEqual(caught.exception.code, "unsafe_path")

    def test_research_influence_rejected(self):
        with self.assertRaises(CapsuleError) as caught:
            validate_plan(ROOT, plan(research_influence="optimize_for_views"))
        self.assertEqual(caught.exception.code, "boundary_violation")

    def test_public_or_unreviewed_plan_rejected(self):
        for changes in ({"visibility": "public"}, {"human_review_required": False}):
            with self.subTest(changes=changes), self.assertRaises(CapsuleError) as caught:
                validate_plan(ROOT, plan(**changes))
            self.assertEqual(caught.exception.code, "boundary_violation")

    def test_cli_emits_json_error_and_success(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(json.dumps(plan()), encoding="utf-8")
            valid = subprocess.run(
                [sys.executable, "-m", "ai_for_ai_lab", "publisher-check",
                 "--root", str(ROOT), str(path)], cwd=ROOT, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            path.write_text(json.dumps(plan(research_influence="views")), encoding="utf-8")
            invalid = subprocess.run(
                [sys.executable, "-m", "ai_for_ai_lab", "publisher-check",
                 "--root", str(ROOT), str(path)], cwd=ROOT, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        self.assertEqual(valid.returncode, 0, valid.stderr)
        self.assertTrue(json.loads(valid.stdout)["valid"])
        self.assertEqual(invalid.returncode, 2)
        self.assertEqual(json.loads(invalid.stdout)["code"], "boundary_violation")


if __name__ == "__main__":
    unittest.main()
