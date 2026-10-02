"""Describe local Git objects an authenticated connector must reproduce."""
import os
from pathlib import Path
import subprocess

from .capsule import CapsuleError, root_path


def _git(root, *args):
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise CapsuleError("Git publication manifest failed; inspect revisions and repository", "git_error") from exc


def _commit(root, revision):
    return os.fsdecode(_git(root, "rev-parse", "--verify", f"{revision}^{{commit}}")).strip()


def _tree(root, commit):
    return os.fsdecode(_git(root, "show", "-s", "--format=%T", commit)).strip()


def build_manifest(root, base, commit):
    root = root_path(root)
    top = Path(os.fsdecode(_git(root, "rev-parse", "--show-toplevel")).rstrip("\n")).resolve()
    if top != root:
        raise CapsuleError("publication root must be the Git worktree root", "invalid_repository")

    base_commit = _commit(root, base)
    target_commit = _commit(root, commit)
    try:
        subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", base_commit, target_commit],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise CapsuleError("base must be an ancestor of commit", "invalid_history") from exc

    names = _git(root, "diff", "--no-renames", "--name-only", "-z", base_commit, target_commit, "--")
    entries = []
    for raw_path in sorted((item for item in names.split(b"\0") if item), key=os.fsdecode):
        path = os.fsdecode(raw_path)
        item = _git(root, "ls-tree", "-z", target_commit, "--", path)
        if not item:
            entries.append({"path": path, "operation": "delete", "mode": None,
                            "type": None, "oid": None, "size": None})
            continue
        metadata, listed_path = item.rstrip(b"\0").split(b"\t", 1)
        mode, object_type, oid = os.fsdecode(metadata).split(" ")
        if listed_path != raw_path:
            raise CapsuleError("Git returned an unexpected publication path", "git_error")
        size = int(os.fsdecode(_git(root, "cat-file", "-s", oid)).strip())
        entries.append({"path": path, "operation": "upsert", "mode": mode,
                        "type": object_type, "oid": oid, "size": size})

    return {
        "version": 1,
        "base_commit": base_commit,
        "base_tree": _tree(root, base_commit),
        "commit": target_commit,
        "tree": _tree(root, target_commit),
        "entries": entries,
    }
