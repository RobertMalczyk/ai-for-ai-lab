# Connector publication manifest

`publish-manifest` gives an agent a compact local receipt for the Git objects an
authenticated connector must reproduce. It performs no network or ref write.

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab publish-manifest \
  --root . --base origin/main --commit HEAD
```

The once-observed agent spellings `--base-ref` and `--target-ref` are exact
aliases for `--base` and `--commit`; the canonical form above remains preferred.

The JSON contains resolved base/target commit and tree IDs plus every changed
path's target mode, type, object ID and byte size. Deleted paths have null object
fields. Paths come from NUL-delimited Git output, including whitespace/newlines.

For connector publication:

1. Verify remote `main` still equals `base_commit`.
2. Create each `upsert` blob and compare its returned SHA with `oid` immediately.
3. Do not create a tree after any mismatch. Deletions use a null SHA.
4. Build from `base_tree`; require the returned tree SHA to equal `tree`.
5. Create the commit/branch, recheck `main`, then update it with force disabled.

This local manifest detects object-transfer corruption earlier than a final tree
comparison, but it does not authenticate GitHub, run tests, prove semantic
correctness or make ref updates restart-safe by itself. The final tree comparison
remains mandatory.
