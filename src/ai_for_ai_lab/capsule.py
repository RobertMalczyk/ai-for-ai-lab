"""Evidence freshness for agent handoffs. Python standard library only."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat


class CapsuleError(ValueError):
    """Validation failure with a stable machine-readable code."""

    def __init__(self, message, code="invalid_document"):
        super().__init__(message)
        self.code = code


def root_path(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise CapsuleError("root must be an existing directory", "invalid_root")
    return root


def relative_path(relative):
    if not isinstance(relative, str) or not relative or "\\" in relative or "\x00" in relative:
        raise CapsuleError("evidence path must be a nonempty POSIX relative path", "unsafe_path")
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != relative or relative == ".":
        raise CapsuleError("evidence path must be canonical and remain inside root", "unsafe_path")
    return path


def evidence_path(root, relative):
    path = relative_path(relative)
    root = root_path(root)
    candidate = root / path
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise CapsuleError("symlink evidence is unsupported", "unsafe_path")
    if not candidate.resolve().is_relative_to(root):
        raise CapsuleError("evidence path escapes root", "unsafe_path")
    return candidate


def digest(path):
    # stat preserves permission failures instead of treating them as absence.
    if not stat.S_ISREG(path.stat().st_mode):
        raise CapsuleError("evidence must be a regular file", "invalid_evidence")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate(capsule):
    if not isinstance(capsule, dict) or set(capsule) != {"version", "goal", "next_step", "evidence"}:
        raise CapsuleError("expected version, goal, next_step, evidence fields")
    if type(capsule["version"]) is not int or capsule["version"] != 1:
        raise CapsuleError("unsupported capsule version")
    for key in ("goal", "next_step"):
        if not isinstance(capsule[key], str) or not capsule[key].strip():
            raise CapsuleError(key + " must be a nonempty string")
    evidence = capsule["evidence"]
    if not isinstance(evidence, list) or not evidence:
        raise CapsuleError("evidence must be a nonempty list")
    seen = set()
    for item in evidence:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise CapsuleError("each evidence entry requires path and sha256")
        path, sha = item["path"], item["sha256"]
        if not isinstance(path, str) or path in seen:
            raise CapsuleError("evidence paths must be unique strings")
        relative_path(path)
        seen.add(path)
        if not isinstance(sha, str) or len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise CapsuleError("invalid SHA-256")


def capture(root, goal, next_step, paths):
    root = root_path(root)
    if not isinstance(paths, (list, tuple)) or any(not isinstance(p, str) for p in paths):
        raise CapsuleError("paths must be a list or tuple of strings")
    result = {"version": 1, "goal": goal, "next_step": next_step,
              "evidence": [{"path": p, "sha256": digest(evidence_path(root, p))}
                           for p in sorted(set(paths))]}
    validate(result)
    return result


def check(root, capsule):
    validate(capsule)
    root = root_path(root)
    results = []
    for item in capsule["evidence"]:
        path = evidence_path(root, item["path"])
        try:
            actual = digest(path)
            status = "unchanged" if actual == item["sha256"] else "changed"
        except FileNotFoundError:
            status = "missing"
        results.append({"path": item["path"], "status": status})
    return {"version": 1, "fresh": all(r["status"] == "unchanged" for r in results),
            "evidence": results}


def loads(text):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise CapsuleError("duplicate JSON key: " + key, "invalid_json")
            obj[key] = value
        return obj
    def reject_constant(value):
        raise CapsuleError("nonstandard JSON constant: " + value, "invalid_json")
    try:
        return json.loads(text, object_pairs_hook=unique, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        raise CapsuleError(str(exc), "invalid_json") from exc
