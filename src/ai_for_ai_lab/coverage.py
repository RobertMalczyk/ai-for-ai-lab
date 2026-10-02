"""Find files absent from declarations; do not infer semantic dependencies."""
import os
from pathlib import Path
import subprocess
import sys
from .capsule import CapsuleError, evidence_path, loads, root_path
from .checkpoint import CLAIMS
from .review import claim_paths


def git_output(root, *args):
    try:
        return subprocess.run(["git", "-C", str(root), *args], check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=10).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise CapsuleError("Git inventory failed; inspect the repository", "git_error") from exc


def audit(root):
    root = root_path(root)
    top = os.fsdecode(git_output(root, "rev-parse", "--show-toplevel")).rstrip("\n")
    if Path(top).resolve() != root:
        raise CapsuleError("coverage root must be the Git worktree root", "invalid_repository")
    claims = loads(evidence_path(root, CLAIMS).read_text(encoding="utf-8"))
    declared = claim_paths(claims)

    def inventory(*flags):
        data = git_output(root, "ls-files", "-z", *flags, "--", "src/", "tests/")
        return {os.fsdecode(path) for path in data.split(b"\0") if path}

    tracked = inventory("--cached")
    untracked = inventory("--others", "--exclude-standard") - tracked
    candidates = tracked | untracked
    uncovered = [{"path": p, "git_state": "tracked" if p in tracked else "untracked"}
                 for p in sorted(candidates - declared)]
    return {"version": 1, "scope": ["src/", "tests/"],
            "coverage_complete": not uncovered, "tracked_files": len(tracked),
            "untracked_files": len(untracked), "covered_files": len(candidates & declared),
            "uncovered": uncovered}


if __name__ == "__main__":
    # Keep the convenient module form equivalent to the canonical package CLI.
    from .__main__ import main
    sys.argv.insert(1, "coverage")
    sys.exit(main())
