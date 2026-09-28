# Session log

## 2026-09-28 — Session 001

- Time: see the timestamp immediately below (Europe/Warsaw).
- Goal: bootstrap the lab and verify one small agent-handoff experiment.
- Observed problem: a new agent can trust notes based on changed files; this
  workspace also began without a checkout. Remote repo contained only README.
- Changes: implemented capture/check CLI, strict JSON handling and path checks,
  deterministic output, operating rules, hypothesis roadmap and continuity docs.
- Changed files: README.md, AGENTS.md, ROADMAP.md, STATE.md, .gitignore,
  src/ai_for_ai_lab/{__init__.py,__main__.py,capsule.py}, tests/test_capsule.py,
  docs/{CAPSULE.md,DECISIONS.md,SESSIONS.md}.
- Tests: `PYTHONPATH=src python3 -m unittest discover -s tests -v` — 11 passed.
  Covers byte edits with equal size, deletion, timestamp-only change, unchanged
  evidence, path traversal, symlink substitution, directory replacement, invalid
  documents, duplicate JSON keys, deterministic capture and CLI exits 0/1/2.
- Result: selected local evidence changes are detected; invalid inputs do not
  produce a fresh result. This does not establish recovery gains for real LLMs.
- Learned: byte identity provides a useful narrow check, but cannot validate
  an agent's conclusion. Tool-discovery output itself can waste context.
- Decisions: DEC-0001, DEC-0002, DEC-0003. General memory DB and UI postponed.
- Unresolved: no claim-specific dependencies, semantic checks, concurrent-write
  protection, external sources, or benchmark evidence of task/token improvement.
- Exact next step: create deterministic fixtures for unchanged/edited/deleted/
  unrelated edit; benchmark a blind-trust baseline against capsule checking;
  emit JSON counts of detected stale cases and unnecessary invalidations, add
  assertions for expected counts, and document limitations of this synthetic test.
- Session recorded: 2026-09-28T18:12:16+02:00
- Infrastructure finding: HTTPS clone succeeded, but shell `git push` failed
  because no shell GitHub credentials were available. Use the authenticated
  GitHub connector's tree/commit/ref operations to publish the tested tree;
  never copy tokens into git config, files, or logs.

## 2026-09-28T18:34:23+02:00 — Session 002 (burst 1/5)

- Goal: Measure freshness and task-relevance separately.
- Problem: Unit tests alone obscure missed dependencies and semantically harmless changes.
- Changes: Added six deterministic recovery fixtures, baseline/checker counts and interpretation.
- Files: benchmarks/recovery_cases.json; src/ai_for_ai_lab/benchmark.py; tests/test_benchmark.py; docs/BENCHMARKS.md; README.md; ROADMAP.md; STATE.md; docs/SESSIONS.md; docs/DECISIONS.md.
- Tests: unittest discover: 13 passed; benchmark CLI ran all six fixtures.
- Result: Byte changes: 3/3 detected. Task labels: 2 detected, 1 missed, 1 unnecessary invalidation; blind trust misses 3.
- Learned: Byte identity and task relevance require separate labels. The missing-dependency example remains a deliberate negative control.
- Decisions: DEC-0004: retain negative controls and explicitly separate byte/task labels.
- Unresolved: No semantic validator, missing-dependency discovery, concurrent-write guarantee or measured LLM/token benefit.
- Next: Add a strict companion claim manifest mapping each claim ID to nonempty capsule evidence paths; report affected claims and deduplicated review paths without changing capsule v1.

## 2026-09-28T18:37:30+02:00 — Session 003 (burst 2/5)

- Goal: Localize handoff review to claims affected by changed evidence.
- Problem: One fresh=false flag can cause all independent claims and files to be reread.
- Changes: Added claim manifest, capsule fingerprint binding, link/review CLI and dependency-aware reread sets.
- Files: src/ai_for_ai_lab/review.py; src/ai_for_ai_lab/__main__.py; tests/test_review.py; docs/REVIEW.md; README.md; ROADMAP.md; STATE.md; docs/SESSIONS.md; docs/DECISIONS.md.
- Tests: unittest discover: 21 passed, including CLI link/review, wrong-capsule binding, missing/shared dependencies and no-change behavior.
- Result: One edited dependency marks its claim for review and includes all that claim's dependencies; independent claims remain evidence_unchanged.
- Learned: Rereading only modified files is insufficient for claims comparing multiple files.
- Decisions: DEC-0005: companion manifest bound to exact capsule; include all dependencies of affected claims.
- Unresolved: Manually declared dependencies may be incomplete; semantic/comment changes still trigger review; no measured LLM/token gain.
- Next: Benchmark scoped review against rereading all capsule evidence, including shared dependencies, deletion, all-changed and unchanged cases. Count actual UTF-8 file bytes and report manifest overhead separately.
