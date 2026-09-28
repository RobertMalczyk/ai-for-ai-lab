"""Controlled byte accounting for scoped vs whole-capsule review."""
import json
from pathlib import Path
import tempfile
from .capsule import capture, check
from .review import link, review


def json_bytes(value):
    return len(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8"))


def run():
    rows = []
    for name in ("unchanged", "isolated_edit", "shared_dependency", "deleted", "all_changed"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for p, content in {"a": "α" * 1024, "b": "b" * 4096, "c": "c" * 8192}.items():
                (root / p).write_text(content, encoding="utf-8")
            capsule = capture(root, "Review independent conclusions", "Reevaluate affected claims", ["a", "b", "c"])
            claims = [{"id": "ab", "text": "Compare a and b", "evidence": ["a", "b"]},
                      {"id": "c", "text": "Inspect c", "evidence": ["c"]}]
            if name == "shared_dependency":
                claims[1]["evidence"].append("a")
            manifest = link(capsule, claims)
            if name == "deleted":
                (root / "a").unlink()
            elif name != "unchanged":
                for p in (["a", "b", "c"] if name == "all_changed" else ["a"]):
                    with (root / p).open("a", encoding="utf-8") as stream:
                        stream.write("!")
            whole = check(root, capsule)
            scoped = review(root, capsule, manifest)
            available = [p for p in ("a", "b", "c") if (root / p).is_file()]
            # Independent model assumption: check hashes first; if anything is
            # stale, reread all available capsule evidence once for the baseline.
            baseline_paths = [] if whole["fresh"] else available
            byte_size = lambda paths: sum(len((root / p).read_bytes()) for p in paths)
            baseline_bytes, scoped_bytes = byte_size(baseline_paths), byte_size(scoped["reread_paths"])
            common = json_bytes(capsule)
            baseline_total = common + json_bytes(whole) + baseline_bytes
            scoped_total = common + json_bytes(manifest) + json_bytes(scoped) + scoped_bytes
            rows.append({"name": name, "whole_file_bytes": baseline_bytes,
                         "scoped_file_bytes": scoped_bytes, "file_bytes_avoided": baseline_bytes - scoped_bytes,
                         "manifest_bytes": json_bytes(manifest),
                         "whole_report_bytes": json_bytes(whole), "scoped_report_bytes": json_bytes(scoped),
                         "modeled_total_bytes_avoided": baseline_total - scoped_total,
                         "hash_scan_bytes_per_strategy": byte_size(available),
                         "missing_paths": scoped["missing_paths"]})
    return {"version": 1, "kind": "synthetic_byte_accounting", "cases": rows,
            "accounting": "capsule + report + selected file bytes; scoped adds manifest; one cold review",
            "not_measured": ["tokens", "latency", "LLM task success", "production distributions"]}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
