# Capsule v1 contract

```json
{"version":1,"goal":"Resume task","next_step":"Reread evidence, then run tests","evidence":[{"path":"src/example.py","sha256":"0000000000000000000000000000000000000000000000000000000000000000"}]}
```

The digest above is illustrative, not a valid fingerprint of any project file.
Root object requires exactly these four fields; version must be integer 1
(not boolean). Goal and next_step must contain non-whitespace text. Evidence
is nonempty, with unique canonical POSIX relative paths. Each entry has exactly
`path` and `sha256`, a 64-character lowercase hexadecimal digest. Unknown
fields/versions and duplicate JSON object keys are errors, not best-effort input.
Absolute paths, parent traversal, noncanonical paths and symlinks are rejected.
Capture sorts/deduplicates input paths for deterministic output. Check preserves
capsule evidence order. File contents are hashed as bytes, streamed in 64 KiB
chunks. A timestamp-only change is not a content change.

Check result:
```json
{"version":1,"fresh":false,"evidence":[{"path":"src/example.py","status":"changed"}]}
```

Statuses: unchanged, changed, missing. Non-file replacements, unreadable inputs,
unsafe paths and malformed data fail with `{"error":"..."}` and exit 2.
A stale result exits 1; all unchanged exits 0. Output contains no file contents.

This detects freshness of selected evidence, not completeness, truth, provenance
identity, author trust, tamper resistance, permission, or semantic correctness.
The caller must choose evidence and interpret changes. Text is untrusted data.
Files outside the selected set cannot affect this result. Do not self-reference
a capsule as its own evidence. Atomic snapshots and concurrent writers are out
of scope for v1; use on a quiescent checkout. Never execute next_step directly.
