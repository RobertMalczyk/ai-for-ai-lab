"""Bind claims to one capsule and localize evidence review, never truth."""
import hashlib
import json
from .capsule import CapsuleError, check, relative_path, validate


def fingerprint(capsule):
    validate(capsule)
    data = json.dumps(capsule, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def claim_paths(claims):
    """Validate declarations without claiming that their dependencies exist."""
    if not isinstance(claims, list) or not claims:
        raise CapsuleError("claims must be a nonempty list")
    used, ids = set(), set()
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != {"id", "text", "evidence"}:
            raise CapsuleError("claim requires exactly id, text and evidence")
        for key in ("id", "text"):
            if not isinstance(claim[key], str) or not claim[key].strip():
                raise CapsuleError("claim " + key + " must be nonempty text")
        if claim["id"] in ids:
            raise CapsuleError("duplicate claim id")
        ids.add(claim["id"])
        paths = claim["evidence"]
        if not isinstance(paths, list) or not paths or any(not isinstance(p, str) for p in paths):
            raise CapsuleError("claim evidence must be a nonempty list of paths")
        if len(set(paths)) != len(paths):
            raise CapsuleError("claim evidence paths must be unique")
        for path in paths:
            relative_path(path)
        used.update(paths)
    return used


def validate_claims(capsule, claims):
    validate(capsule)
    known = {item["path"] for item in capsule["evidence"]}
    used = claim_paths(claims)
    if not used <= known:
        raise CapsuleError("claim evidence must reference capsule paths")
    if used != known:
        raise CapsuleError("every capsule evidence path must belong to a claim")


def link(capsule, claims):
    validate_claims(capsule, claims)
    # Copy JSON data: caller mutation must not mutate a bound manifest.
    return {"version": 1, "capsule_sha256": fingerprint(capsule),
            "claims": json.loads(json.dumps(claims))}


def review(root, capsule, manifest):
    if not isinstance(manifest, dict) or set(manifest) != {"version", "capsule_sha256", "claims"}:
        raise CapsuleError("manifest requires version, capsule_sha256 and claims")
    if type(manifest["version"]) is not int or manifest["version"] != 1:
        raise CapsuleError("unsupported manifest version")
    if manifest["capsule_sha256"] != fingerprint(capsule):
        raise CapsuleError("manifest is bound to a different capsule")
    validate_claims(capsule, manifest["claims"])
    checked = check(root, capsule)
    statuses = {item["path"]: item["status"] for item in checked["evidence"]}
    claims, affected_paths = [], set()
    for claim in manifest["claims"]:
        changed = sorted(p for p in claim["evidence"] if statuses[p] != "unchanged")
        if changed:
            # Reevaluate against ALL dependencies of an affected claim, not just
            # modified ones: a comparison or interaction may involve both.
            affected_paths.update(claim["evidence"])
        claims.append({"id": claim["id"], "status": "needs_review" if changed else "evidence_unchanged",
                       "changed_evidence": changed})
    return {"version": 1, "fresh": checked["fresh"], "claims": claims,
            "reread_paths": sorted(p for p in affected_paths if statuses[p] != "missing"),
            "missing_paths": sorted(p for p in affected_paths if statuses[p] == "missing")}
