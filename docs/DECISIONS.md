# Decisions

### DEC-0001 — Evidence freshness before general memory

Problem: a resumed agent cannot tell whether file-based notes are stale.

Decision: a minimal versioned JSON handoff capsule with selected SHA-256 file
fingerprints, a goal, and a next step; stdlib Python CLI.

Why: the failure is observable without a model API, budget, or new service.
SHA-256 checks content even when timestamps or file sizes are misleading.

Alternatives: mtime-only checks (weak evidence); full embedded contents (context
cost); vector memory (does not establish freshness); Git HEAD alone (misses
uncommitted edits and invalidates unrelated changes).

Consequences: callers select dependencies; unchanged does not mean correct.
Semantic relevance, concurrent mutation and external resources remain unsolved.
An extra hash read costs I/O; token/time savings are hypotheses, not results.

### DEC-0002 — Strict small contract and conservative filesystem scope

Problem: ambiguous data and links can silently change the evidence being checked.

Decision: reject unknown versions/fields, duplicate keys, path traversal and
symlinks. Report missing files as stale; malformed/unreadable input as errors.

Why: another agent needs an unambiguous distinction between stale and unchecked.

Alternatives: silently skip bad inputs (false assurance); sandbox all filesystem
races (too large for this iteration).

Consequences: v1 assumes a quiescent local checkout, is not a security boundary,
and does not support symlink-based projects without explicitly selected real files.

### DEC-0003 — Tested baseline with short-lived work branches

Problem: future sessions need a canonical starting point without human approval
for every routine edit, while preserving the work's history.

Decision: atomic commits on agent branches; fast-forward main after local tests
and remote divergence check. Keep branches initially; no force push.

Why: the user authorized autonomous Git maintenance. Small tested increments
can remain discoverable without accumulating an approval backlog.

Alternatives: every change waits for human PR approval (interrupts autonomy);
write directly to main (loses branch isolation).

Consequences: local tests are evidence, not independent review. Diverged work
must be reconciled safely in a later scoped task; never overwrite collaborators.

### DEC-0004 — Keep uncomfortable benchmark cases

Problem: a perfect hash test can imply unjustified recovery reliability.

Decision: separately label selected-byte freshness and task relevance; retain harmless-comment and omitted-dependency counterexamples.

Why: failures show what the tool cannot establish.

Alternatives: only test changed/deleted files (misleading coverage).

Consequences: fixture-defined counts are diagnostic only; claim scoping may reduce review breadth but cannot resolve either semantic limitation.

### DEC-0005 — Bound claim manifests and complete affected dependency sets

Problem: one changed file need not invalidate independent claims, but a changed comparison operand requires both operands.

Decision: companion manifest bound by canonical capsule hash; strict claim IDs and references; review all dependencies of affected claims and separate missing paths.

Why: preserve capsule v1 while reducing unnecessary review without dropping relevant unchanged evidence.

Alternatives: embed claims in capsule v2 (premature break); reread only changed files (incomplete context).

Consequences: manual dependency completeness is still unverified; binding prevents accidental capsule mismatch but not malicious or semantically incorrect claims.

### DEC-0006 — Measure overhead without universal savings claims

Problem: a small reread set can conceal manifest/report overhead.

Decision: publish per-case actual UTF-8 file bytes and modeled cold-review totals, plus unchanged hash-scan bytes and negative cases.

Why: independent evidence helps, shared evidence does not.

Alternatives: report only avoided files or aggregate a favorable percentage across arbitrary fixtures.

Consequences: no inferred token/cost/latency or real-agent success improvement; results depend on the explicitly defined baseline and transmission model.
