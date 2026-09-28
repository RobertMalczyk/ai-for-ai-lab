import json
from pathlib import Path
import unittest
from ai_for_ai_lab.benchmark import run

CASES = Path(__file__).resolve().parents[1] / "benchmarks/recovery_cases.json"


class RecoveryBenchmarkTests(unittest.TestCase):
    def test_expected_byte_and_task_outcomes(self):
        result = run(json.loads(CASES.read_text()))
        self.assertEqual(result["byte_freshness"], {"detected_stale": 3, "missed_stale": 0,
            "unnecessary_invalidations": 0, "correct_fresh": 3})
        self.assertEqual(result["task_relevance"]["checker"], {"detected_stale": 2,
            "missed_stale": 1, "unnecessary_invalidations": 1, "correct_fresh": 2})
        self.assertEqual(result["task_relevance"]["blind_trust"]["missed_stale"], 3)

    def test_fixture_cannot_write_outside_sandbox(self):
        with self.assertRaises(ValueError):
            run([{"name": "bad", "after": {"../escape": "no"}}])
