"""Validate a one-way, evidence-bound plan for an AI publisher."""
from .capsule import CapsuleError, digest, evidence_path, root_path


FIELDS = {
    "version", "episode", "evidence_refs", "audience_feedback_use",
    "research_influence", "visibility", "human_review_required",
}


def validate_plan(root, plan):
    """Return a normalized plan receipt; never publish or call external services."""
    if not isinstance(plan, dict) or set(plan) != FIELDS:
        raise CapsuleError("publisher plan has unexpected or missing fields", "invalid_plan")
    if type(plan["version"]) is not int or plan["version"] != 1:
        raise CapsuleError("unsupported publisher plan version", "invalid_plan")
    episode = plan["episode"]
    if (not isinstance(episode, str) or not episode or
            any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in episode)):
        raise CapsuleError("episode must be a nonempty safe identifier", "invalid_plan")
    refs = plan["evidence_refs"]
    if (not isinstance(refs, list) or not refs or
            any(not isinstance(ref, str) for ref in refs) or len(set(refs)) != len(refs)):
        raise CapsuleError("evidence_refs must be a nonempty unique string list", "invalid_plan")
    if plan["audience_feedback_use"] != "storytelling_only":
        raise CapsuleError("audience feedback may affect storytelling only", "boundary_violation")
    if plan["research_influence"] != "none":
        raise CapsuleError("publisher must not influence experiment selection", "boundary_violation")
    if plan["visibility"] != "private":
        raise CapsuleError("version 1 publisher plans must remain private", "boundary_violation")
    if plan["human_review_required"] is not True:
        raise CapsuleError("version 1 requires human review", "boundary_violation")

    root = root_path(root)
    evidence = []
    for ref in refs:
        path = evidence_path(root, ref)
        try:
            sha = digest(path)
        except FileNotFoundError as exc:
            raise CapsuleError("publisher evidence is missing: " + ref,
                               "missing_evidence") from exc
        evidence.append({"path": ref, "sha256": sha})
    return {
        "version": 1,
        "valid": True,
        "episode": episode,
        "boundary": {
            "audience_feedback_use": "storytelling_only",
            "research_influence": "none",
            "visibility": "private",
            "human_review_required": True,
        },
        "evidence": evidence,
    }
