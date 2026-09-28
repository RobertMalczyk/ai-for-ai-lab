"""Repository-local self-use: one atomic capsule/manifest checkpoint."""
import json
import os
from pathlib import Path
import tempfile
from .capsule import CapsuleError, capture, evidence_path, loads, root_path
from .review import link, review

CLAIMS = "handoff/claims.json"
CHECKPOINT = "handoff/checkpoint.json"


def atomic_json(path, value):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".checkpoint-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def refresh(root):
    root = root_path(root)
    claims = loads(evidence_path(root, CLAIMS).read_text(encoding="utf-8"))
    if not isinstance(claims, list) or not claims:
        raise CapsuleError("checkpoint claims must be a nonempty list")
    paths = set()
    for claim in claims:
        if not isinstance(claim, dict) or not isinstance(claim.get("evidence"), list):
            raise CapsuleError("checkpoint claims require evidence lists")
        if any(not isinstance(p, str) for p in claim["evidence"]):
            raise CapsuleError("checkpoint evidence paths must be strings")
        paths.update(claim["evidence"])
    if CHECKPOINT in paths or CLAIMS not in paths:
        raise CapsuleError("declare claims.json as evidence, never checkpoint.json itself")
    capsule = capture(root, "Resume AI FOR AI LAB from declared project evidence",
                      "Read STATE.md and evaluate the checkpoint review before implementation", sorted(paths))
    manifest = link(capsule, claims)
    target = evidence_path(root, CHECKPOINT)
    atomic_json(target, {"version": 1, "capsule": capsule, "manifest": manifest})
    return {"version": 1, "saved": CHECKPOINT, "claims": len(claims)}


def inspect(root):
    root = root_path(root)
    data = loads(evidence_path(root, CHECKPOINT).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or set(data) != {"version", "capsule", "manifest"}:
        raise CapsuleError("checkpoint requires version, capsule and manifest")
    if type(data["version"]) is not int or data["version"] != 1:
        raise CapsuleError("unsupported checkpoint version")
    return review(root, data["capsule"], data["manifest"])
