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

## 2026-09-28T18:40:00+02:00 — Session 004 (burst 3/5)

- Goal: Measure scoped review cost including its overhead.
- Problem: Fewer selected files can falsely imply savings if manifests and output are ignored.
- Changes: Added five-case byte-accounting diagnostic, explicit hash-scan accounting and negative savings cases.
- Files: src/ai_for_ai_lab/review_benchmark.py; tests/test_review_benchmark.py; docs/BENCHMARKS.md; ROADMAP.md; STATE.md; docs/SESSIONS.md; docs/DECISIONS.md.
- Tests: unittest discover: 24 passed; review_benchmark CLI executed five cases.
- Result: Isolated edit avoids 8192 file bytes, 7913 modeled bytes after overhead; unchanged/shared/all-changed cost 273/284/288 extra bytes.
- Learned: Scoping is useful with separable dependencies, not universally. Hash I/O is unchanged; UTF-8 bytes are not tokens.
- Decisions: DEC-0006: publish overhead and negative cases without a workload-wide percentage.
- Unresolved: No production distribution, tokenizer or model evaluation; input errors still require parsing human text, and library root handling differs from CLI.
- Next: Unify invalid-input handling for library and CLI: reject unavailable roots before classifying evidence, add machine-readable error codes while preserving error text, and regression-test malformed CLI arguments and JSON.

## 2026-09-28T18:42:55+02:00 — Session 005 (burst 4/5)

- Goal: Make unchecked inputs distinguishable from stale evidence.
- Problem: Library check on an absent root returned missing evidence; CLI syntax errors were plain text and errors had no stable codes.
- Changes: Unified root validation; strict lexical paths; preserved stat access failures; added stable error codes and JSON argument errors; rejected scalar capture paths and nonstandard JSON constants.
- Files: src/ai_for_ai_lab/capsule.py; src/ai_for_ai_lab/__main__.py; tests/test_errors.py; docs/CAPSULE.md; README.md; ROADMAP.md; STATE.md; docs/SESSIONS.md; docs/DECISIONS.md.
- Tests: New seven-test error suite before fix: failed (2 failures, 5 errors, including subtest reporting). After fix full unittest discover: 31 passed; prior benchmarks exercised by tests.
- Result: Missing root is invalid_root, missing selected evidence in a valid root remains stale; callers can branch on error codes instead of prose.
- Learned: A malformed environment must not look like an observed project change. Python JSON accepts NaN by default unless explicitly rejected.
- Decisions: DEC-0007: additive error codes, consistent library root checks, no speculative automatic retry.
- Unresolved: No hostile-input resource budget or concurrency guarantees; manual dependency completeness and semantic validity remain unverified.
- Next: Use the tool on its own project: add a reproducible repository checkpoint with claim-to-source/test links, document check-before-refresh, and test a copied-checkout edit flags only the expected claims.

## 2026-09-28T18:46:30+02:00 — Session 006 (burst 5/5)

- Goal: Use the handoff tool for the lab's own continuity.
- Problem: Synthetic examples do not ensure that the next real session can consume the tool; separate capsule/manifest writes could leave mismatched state.
- Changes: Added repository claim map, one atomic checkpoint bundle, inspect/explicit refresh CLI and session integration. Documented that refresh only replaces a baseline.
- Files: src/ai_for_ai_lab/checkpoint.py; src/ai_for_ai_lab/__main__.py; tests/test_checkpoint.py; handoff/claims.json; handoff/checkpoint.json; docs/CHECKPOINT.md; AGENTS.md; README.md; ROADMAP.md; STATE.md; docs/SESSIONS.md; docs/DECISIONS.md.
- Tests: unittest discover: 37 passed. Copied-checkout replay modifies review_benchmark.py and marks only byte-diagnostic; failed replacement preserves prior bytes. Final checkpoint refresh saved five claims; inspection returned fresh=true, no missing paths and no reread paths.
- Result: Five project claim groups are inspectable; deterministic checkpoint writes and copied-checkout isolation tests pass. The repository now consumes its own tool.
- Learned: Refreshing must be explicit or it erases evidence of drift. Atomic replacement should cover the capsule and manifest together. CLI imports create shared dependencies that need declaration.
- Decisions: DEC-0008: one atomic self-use bundle with check-before-refresh; no automatic claims of validation.
- Unresolved: Manual dependency maps can omit new files; hashes cannot prove semantics or test results; no real-agent token/outcome study and no concurrent-writer guarantee.
- Next: Add a small dependency-coverage audit: compare tracked src/ and tests/ paths with handoff/claims.json, report uncovered new files as unknown coverage without inventing semantic links. Test an added undeclared module and preserve the existing omitted-dependency negative control.

## 2026-09-28T19:13:16+02:00 — Session 007 (follow-up)

- Goal: expose new src/tests files omitted from the checkpoint's declared evidence.
- Problem: the baseline checkpoint was fresh, but by design could not notice an
  added file outside its evidence list. Tracked-only inventory would also miss
  a newly created module before staging.
- Changes: read-only Git inventory audit, JSON/exit-code contract, shared claim
  validation, ten tests, session integration and explicit project claim updates.
- Files: src/ai_for_ai_lab/{coverage.py,review.py,checkpoint.py,__main__.py};
  tests/test_coverage.py; handoff/{claims.json,checkpoint.json}; README.md;
  AGENTS.md; STATE.md; ROADMAP.md; docs/{COVERAGE.md,CHECKPOINT.md,DECISIONS.md,SESSIONS.md}.
- Tests: full unittest discovery: 47 passed, including tracked/untracked gaps,
  ignore rules, odd filenames, invalid/nested roots, duplicate IDs, CLI exits,
  and deleted tracked evidence without audit mutations. Original negative-control
  recovery benchmark still passes with the same deliberately missed dependency.
- Result: before claim updates the audit reported coverage_complete=false and
  precisely its own two new source/test files; after deliberate assignment it
  reported 15 covered paths, no gaps. The previous checkpoint independently
  reported changed claims before refresh, rather than being silently replaced.
- Learned: file membership coverage and freshness are independent. A deleted
  tracked file can be covered but not fresh; wrong semantic edges are invisible.
- Decisions: DEC-0009. Include nonignored untracked files, never auto-assign claims.
- Unresolved: no transitive/semantic dependency completeness, concurrent inventory
  snapshot, ignored-file coverage or empirical real-agent cost/success result.
- Next: measure one real self-use session: record startup/report bytes, actual
  reread paths and missed dependencies; compare with whole-declared-file reads
  while separating mandatory document reading and hash I/O. Then decide whether
  scoping earns its complexity before building another feature.

## 2026-09-28T20:07:04+02:00 — Session 008 (user-directed governance)

- Goal: require real agent utility checks and periodically escape the current family.
- Problem: all seven previous sessions stayed in handoff/checkpoint infrastructure;
  synthetic results and self-use did not establish comparative real-task benefit.
- Plan before implementation: inspect the real history; use a minimal ledger/gate
  to block indefinite same-family development; keep thresholds explicit and demand
  traceable baseline/intervention plus quality before recording positive utility.
  This maintenance task tests rule behavior, not a claim of measured agent benefit.
- Changes: policy, conservative history backfill, gate CLI, field-report consistency
  validation, ten tests, instructions, paused handoff roadmap and next exploration.
- Files: lab/{policy.json,sessions.jsonl}; src/ai_for_ai_lab/session_gate.py;
  tests/test_session_gate.py; docs/EXPERIMENT_POLICY.md; AGENTS.md; README.md;
  STATE.md; ROADMAP.md; docs/{DECISIONS.md,SESSIONS.md}; handoff/{claims.json,checkpoint.json}.
- Tests: full unittest suite: 57 passed. Gate cases cover mandatory pivots,
  maintenance not resetting cadence, synthetic positives, evaluation budgets,
  parked families, malformed history and unverifiable/contradictory field reports.
- Result: real project history produces mode=explore, excludes handoff, reports
  family_streak=7 and evaluation_required=[handoff]. Next work ordinal is 8 even
  though this administrative session has ID 8. No real field benefit claimed.
- Learned: the loop needs both a value threshold and a diversity constraint;
  successes must not suppress scheduled exploration. File/metric checks cannot
  substitute for reading and challenging the underlying evidence.
- Decisions: DEC-0010; default thresholds are provisional and explicitly visible.
- Unresolved: agents can misclassify families or fabricate evidence; no optimality
  guarantee or measured benefit of this policy yet. Limit policy maintenance too.
- Next: productive session 9 must compare three distinct observed-friction
  candidates outside handoff, choose one small probe and record the cheapest
  falsifying test. Tool discovery overhead is observed, but selection must still
  compare alternatives. On returning to handoff, field-evaluate before new features.

## 2026-09-29T00:01:24+02:00 — Session 009 (exploration; pre-result plan)

- Gate: mode=explore, excluded_families=[handoff], family_streak=7,
  evaluation_required=[handoff], parked_families=[]. Chosen family:
  `tool-discovery`; no handoff feature work is allowed in this session.
- Real task: identify the authenticated GitHub connector operations needed to
  inspect and publish this repository. This task existed for the scheduled repo
  work, independently of any experiment.
- Observed friction/trace: the first broad registry filter in this session
  serialized full matching tool descriptions and the runtime reported a 59,905
  token output before truncation. A follow-up names-only query was usable. The
  sanitized measurement record will be stored under `lab/observations/`.
- Three candidates from distinct families:
  1. `tool-discovery`: observed oversized/truncated registry output. Assumption
     to challenge: full descriptions are needed in the first pass. Potential
     value: less context and less truncation. Cheapest falsifier: compare full
     broad matches with names-first plus exact schemas for only required GitHub
     operations. Cost: two local registry queries; novelty: new family.
  2. `side-effect-recovery`: interrupted agents may repeat writes, but this run
     has no observed duplicate side effect. Assumption: an idempotency ledger is
     necessary. Cheapest falsifier: inspect one real interrupted write trace;
     unavailable here. Cost: medium; novelty: new family.
  3. `verification-budget`: repeated checks may exceed a small edit's cost, but
     this run has no comparable trace separating required and redundant checks.
     Cheapest falsifier: timestamp one naturally occurring small change with a
     predeclared quality check. Cost: low/medium; novelty: new family.
- Selection: candidate 1 has direct evidence and a same-task baseline; observe
  candidates 2/3 rather than inventing fixtures.
- Simplest baseline: serialize every registry entry matching the original broad
  Git/GitHub/repository/connector expression, including full descriptions.
- Intervention: serialize matching tool names first, select the six operations
  required for read/tree/commit/branch-ref publication, then serialize only those
  six full entries. Include both intervention payloads as overhead.
- Hypothesis/metric: intervention serialized UTF-8 bytes are lower; minimum
  useful improvement is 90% versus baseline. Bytes are the unit, not tokens.
- Quality control: the names pass must expose all six predeclared operations and
  the exact pass must retrieve all six nonempty schemas/descriptions. Record the
  selected names and counts, not proprietary registry contents.
- Stop condition: if quality fails or byte reduction is below 90%, do not build a
  discovery helper; simplify or reject. One sequential observation is only
  preliminary field evidence and cannot establish latency or LLM-quality gains.
- Probe execution: the first counter attempt failed because this tool runtime did
  not expose `TextEncoder`; no result was claimed from it. A Unicode code-point
  UTF-8 counter then measured the same registry snapshot successfully.
- Changes/files: added a sanitized aggregate trace and field report under
  `lab/observations/` and `lab/reports/`; appended ledger session 9; updated
  STATE, ROADMAP, DECISIONS, session documentation and checkpoint declarations.
- Tests/result: baseline=239,617 bytes for 129 full broad matches. Names-first
  (4,176 bytes) plus six exact schemas (6,733 bytes) totaled 10,909 bytes,
  avoiding 228,708 bytes (95.4473%). All six predeclared operations were present
  with nonempty descriptions, so quality passed and the 90% threshold was met.
  Final verification: 57/57 unit tests passed; gate accepted the field report and
  returned mode=evaluate with handoff still evaluation-required; coverage reported
  17/17 scoped files declared. The pre-refresh checkpoint correctly returned exit
  1 and identified changed workflow/policy claims; it was then explicitly refreshed
  and reinspected fresh after all documentation changes.
- Actual agent-value evidence: preliminary positive field evidence for this one
  real repository task only. The observed baseline was truncated; the
  intervention exposed every required operation with 4.55% of its serialized
  bytes, including both discovery passes. This is not a token, latency, LLM
  quality or downstream task-success claim.
- Learned: the dominant waste came from serializing irrelevant full schemas, not
  from the count of names. Names-first is a useful operating pattern, but a new
  helper is not justified by one registry/task pair.
- Decision: `evaluate`, not build. Adopt names-first/exact-second as a documented
  practice and seek a second naturally occurring non-GitHub task before creating
  code. See DEC-0011.
- Unresolved: registry variation, regex overmatching, order effects, and whether
  smaller tool output improves model decisions or latency.
- Exact next step: on the next natural connector-discovery task, predeclare its
  required operations and repeat the same byte/quality comparison. If it does not
  reproduce the threshold, simplify the rule to targeted name filtering; if it
  does, decide whether documentation alone is sufficient.
