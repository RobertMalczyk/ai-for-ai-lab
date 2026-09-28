"""Synthetic diagnostic, not an LLM evaluation or a token-saving claim."""
import json
from pathlib import Path
import sys
import tempfile
from .capsule import capture, check


def counts(rows, prediction, label):
    result = {"detected_stale": 0, "missed_stale": 0,
              "unnecessary_invalidations": 0, "correct_fresh": 0}
    for row in rows:
        predicted, actual = row[prediction], row[label]
        key = ("detected_stale" if predicted else "missed_stale") if actual else (
            "unnecessary_invalidations" if predicted else "correct_fresh")
        result[key] += 1
    return result


def run(cases):
    rows = []
    for case in cases:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in {"config.txt": "limit=10\n", "notes.txt": "old note\n",
                                "policy.txt": "override=none\n"}.items():
                (root / name).write_text(value, encoding="utf-8")
            capsule = capture(root, "Recover effective limit", "Reevaluate effective limit", ["config.txt"])
            for name, value in case["after"].items():
                # Fixture input is restricted to the three sandbox files.
                if name not in {"config.txt", "notes.txt", "policy.txt"}:
                    raise ValueError("unsupported fixture path")
                if value is None:
                    (root / name).unlink()
                else:
                    (root / name).write_text(value, encoding="utf-8")
            rows.append({"name": case["name"], "byte_stale": case["byte_stale"],
                         "task_stale": case["task_stale"], "blind_stale": False,
                         "checker_stale": not check(root, capsule)["fresh"]})
    return {"version": 1, "kind": "synthetic_diagnostic", "cases": rows,
            "byte_freshness": counts(rows, "checker_stale", "byte_stale"),
            "task_relevance": {method: counts(rows, key, "task_stale") for method, key in
                               (("blind_trust", "blind_stale"), ("checker", "checker_stale"))}}


if __name__ == "__main__":
    print(json.dumps(run(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))), sort_keys=True))
