# Scoped evidence review v1

A capsule's single fresh flag is too coarse for independent claims. Create a
companion manifest without changing capsule v1. Author claims as a JSON array:

```json
[{"id":"comparison","text":"A is compatible with B","evidence":["a.txt","b.txt"]},{"id":"independent","text":"C is configured","evidence":["c.txt"]}]
```

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab link /tmp/handoff.json /tmp/claims.json > /tmp/manifest.json
PYTHONPATH=src python3 -m ai_for_ai_lab review --root . /tmp/handoff.json /tmp/manifest.json
```

Use capsule paths matching your claims. Each claim has exactly id, text,
evidence. IDs are unique nonempty strings; text is nonempty. Evidence is a
nonempty array of distinct paths from the capsule. Every capsule path must be
assigned to at least one claim: no silently ignored evidence. Shared paths are
allowed across claims. Uncaptured dependencies are still unknowable.

The manifest is `{version:1,capsule_sha256:<digest>,claims:[...]}`. Digest:
SHA-256 of UTF-8 JSON using Python json.dumps with sort_keys=True,
separators=(',', ':'), ensure_ascii=True. Arrays retain order; object key order
and external JSON whitespace do not matter. This is a binding against accidental
mismatches, not a signature, semantic link, or authorization mechanism. Edit a
capsule only with deliberate reevaluation/relinking of claims.

Review returns version, fresh, claims (id/status/changed_evidence), reread_paths,
and missing_paths. Claim status is `evidence_unchanged` or `needs_review`, never
true/false or confirmed. For an affected claim, ALL its dependencies are included
in the review set: changes can invalidate comparisons involving unchanged files.
Paths are sorted/deduplicated. Missing files are separate; do not repeatedly try
to read a deleted file. Unchanged claims contribute no reread paths.

Exit codes remain 0 unchanged, 1 review required, 2 invalid/unreadable.
Manifest text is never executed and is not echoed into the review report.
