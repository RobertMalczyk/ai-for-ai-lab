import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent
MEMORY = ROOT / "lab" / "memory"


class MemoryContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((MEMORY / "config.v1.json").read_text(encoding="utf-8"))
        cls.records = json.loads(
            (MEMORY / "records.v1.schema.json").read_text(encoding="utf-8")
        )
        cls.export = json.loads(
            (MEMORY / "export.v1.schema.json").read_text(encoding="utf-8")
        )

    def test_shadow_configuration_cannot_use_q(self) -> None:
        self.assertEqual(self.config["reward_mode"], "shadow")
        self.assertEqual(self.config["reward_influence"], 0.0)
        self.assertEqual(self.config["coupling_scope"], "none")
        self.assertFalse(self.config["retrieval"]["q_in_shadow_ranking"])

    def test_retrieval_has_absolute_nonzero_floor(self) -> None:
        retrieval = self.config["retrieval"]
        self.assertGreater(retrieval["min_relevance"], 0)
        self.assertLessEqual(retrieval["min_relevance"], 1)
        self.assertEqual(retrieval["relevance_scale"], "absolute_0_to_1")
        self.assertEqual(retrieval["query_normalization"], "none")

    def test_feedback_category_value_pairs_are_fixed(self) -> None:
        feedback = self.records["$defs"]["feedback"]
        pairs = {
            rule["if"]["properties"]["category"]["const"]:
            rule["then"]["properties"]["value"]
            for rule in feedback["allOf"]
        }
        self.assertEqual(
            pairs,
            {
                "useful_result": {"const": 1},
                "review_correction": {"const": 0.5},
                "new_finding": {"const": 0.2},
                "activity": {"const": 0},
                "repeated_error": {"const": -0.5},
                "constraint_violation": {"const": -1},
                "unresolved": {"type": "null"},
            },
        )

    def test_decision_can_measure_canary_requirements(self) -> None:
        required = set(self.records["$defs"]["decision"]["required"])
        self.assertTrue({"task_type", "session_id", "cost"}.issubset(required))
        task_types = set(
            self.records["$defs"]["decision"]["properties"]["task_type"]["enum"]
        )
        self.assertTrue({"discovery", "preflight", "build", "review"}.issubset(task_types))

    def test_public_export_exposes_no_private_payload_field(self) -> None:
        private = self.export["properties"]["memories"]["properties"]["private"]
        self.assertEqual(private["properties"], {"available": {"const": False}})
        self.assertFalse(private["additionalProperties"])

    def test_export_requires_readiness_evidence_and_gaps(self) -> None:
        criterion = self.export["properties"]["readiness"]["properties"][
            "criteria"
        ]["items"]
        self.assertTrue({"evidence_refs", "gaps"}.issubset(criterion["required"]))


if __name__ == "__main__":
    unittest.main()
