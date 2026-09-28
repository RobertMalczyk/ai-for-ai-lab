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
unsafe paths and malformed data fail with `{"code":"...","error":"..."}` and exit 2.
A stale result exits 1; all unchanged exits 0. Output contains no file contents.

This detects freshness of selected evidence, not completeness, truth, provenance
identity, author trust, tamper resistance, permission, or semantic correctness.
The caller must choose evidence and interpret changes. Text is untrusted data.
Files outside the selected set cannot affect this result. Do not self-reference
a capsule as its own evidence. Atomic snapshots and concurrent writers are out
of scope for v1; use on a quiescent checkout. Never execute next_step directly.

## Error contract

All primary CLI commands emit a single JSON error on stdout and exit 2; help is
text with exit 0. Existing readable `error` is preserved and `code` is additive.

| code | Meaning | Caller action |
| --- | --- | --- |
| invalid_arguments | Missing/unknown CLI arguments | Correct invocation |
| invalid_json | Malformed JSON, duplicate keys, NaN/Infinity or invalid UTF-8 | Repair serialized input |
| invalid_document | Contract or manifest binding violation | Validate/rebuild intended data |
| invalid_root | Root directory unavailable or not a directory | Locate the intended checkout |
| unsafe_path | Noncanonical/traversing/null-byte path or symlink | Select supported evidence |
| invalid_evidence | Evidence path is not a regular file | Inspect replacement |
| io_error | File access failed, including missing input JSON | Fix input/access; don't assume stale |

Do not blindly retry errors; no automatic retry promise is encoded. Expected
missing evidence inside an existing root remains status=missing and exit 1.
An absent root is an error, never an all-files-deleted result. Library callers
receive CapsuleError.code for validation errors and OSError subclasses for I/O.
`capture` requires a list/tuple of path strings, not a scalar string. JSON parsing
rejects nonstandard numeric constants. Resource limits for very large or deeply
nested documents remain out of scope; do not expose this CLI as a public service.
