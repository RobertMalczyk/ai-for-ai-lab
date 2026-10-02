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

## 2026-09-29T06:02:32+02:00 — Session 010 (handoff evaluation; pre-result plan)

- Gate: mode=evaluate, excluded_families=[], family_streak=1,
  evaluation_required=[handoff], parked_families=[]. Chosen family: `handoff`;
  this session evaluates the existing checkpoint instead of adding a feature.
- Real task: resume the canonical lab from a newly cloned, clean `main`, establish
  the trustworthy baseline and choose the next permitted task. This work existed
  independently of the checkpoint evaluation.
- Observed condition/trace: clone, fetch, branch inspection and mandatory startup
  documents already established a clean worktree at the same main commit as the
  authenticated remote. The required checkpoint then returned fresh with no
  reread paths. Exact aggregate counts will be captured without repository or
  tool-registry contents under `lab/observations/`.
- Simplest baseline: mandatory startup documents plus Git identity/status and the
  session gate; on a clean fresh clone, do not add a checkpoint report.
- Intervention: the same startup plus checkpoint inspection. Count its complete
  agent-visible JSON output and all bytes hashed from declared evidence; no setup
  or report byte is excluded. Coverage is a separate common workflow check.
- Hypothesis/metric: checkpoint inspection reduces agent-visible startup bytes by
  at least 10% while producing the same permitted-task decision and detecting any
  declared stale evidence. Unit: serialized UTF-8 bytes; direction: lower.
- Quality control: baseline and intervention must identify the same canonical
  commit, clean status and gate mode; intervention must return a valid report.
  Any stale path uniquely found by the checkpoint is recorded as useful quality,
  not hidden by the byte metric.
- Stop condition: if the fresh-clone intervention finds no unique stale evidence
  and does not beat the 10% threshold, record negative for this operating
  condition; do not generalize to dirty or long-lived worktrees and do not add a
  feature. A sequential single-session comparison cannot establish task-success
  or latency effects.
- Changes/files: added a sanitized fresh-clone observation and field report;
  appended ledger session 10; updated STATE, ROADMAP, DECISIONS, session history
  and the self-checkpoint declarations. No product code or threshold changed.
- Measurement/result: baseline startup payload was 33,483 bytes; adding the
  617-byte checkpoint report produced 34,100 bytes, 1.84% worse rather than 10%
  better. The checkpoint also hashed 35 declared paths totaling 118,285 bytes and
  read its 6,650-byte bundle. It was fresh, returned no reread paths, found no
  evidence unavailable from the verified clean Git baseline and did not change
  the gate-directed task. Quality checks passed, but the utility hypothesis did not.
- Tests: 57/57 unit tests passed in 1.396s. The gate accepted both field reports
  and returned mode=select with no evaluation obligation; coverage remained
  complete for all 17 scoped source/test files. Before refresh, checkpoint exit 1
  correctly exposed changed project-workflow, policy and discovery evidence.
- Actual agent-value evidence: negative for one real clean fresh-clone resume.
  Operational agent-visible overhead is fully counted; existing code maintenance
  and policy-required evaluation logging were not charged, which only favors the
  already losing intervention. Internal file I/O is reported separately and is
  not mislabeled as model-context cost.
- Learned: content fingerprints can be correct yet redundant when commit identity,
  a clean worktree and mandatory current documents already establish the baseline.
  The unresolved use case is a dirty/long-lived resume, not another synthetic edit.
- Decision: `simplify` the claim, not the code. Do not cite clean-clone self-use as
  benefit and do not add a feature. See DEC-0012.
- Unresolved: dirty worktrees, cross-branch notes, semantic dependency omissions,
  hash latency and downstream task success. One negative condition does not prove
  the whole handoff family useless.
- Exact next step: run the gate. Replicate tool discovery only during a natural
  non-GitHub connector task; reassess handoff only when a naturally dirty or
  long-lived resume exists. If neither occurs, observe real workflow friction
  instead of manufacturing a benchmark.

## 2026-09-29T11:57:32+02:00 — Session 011 (stale policy directive; pre-result plan)

- Gate: mode=select, excluded_families=[], family_streak=1,
  evaluation_required=[], parked_families=[]. Neither active experiment has its
  natural return condition: this is a fresh clean checkout and no non-GitHub
  connector task exists. Chosen family/mode: `lab-governance` / `maintenance`.
- Real task and observed problem: mandatory startup reading exposed one stale
  imperative in `docs/EXPERIMENT_POLICY.md`: its `Immediate effect` says the next
  work session must explore, while the current machine-readable gate says select
  and STATE restricts work to natural return conditions. The duplicated mutable
  state can send the next agent to the wrong family.
- Simplest baseline: leave the one-time Session 008 conclusion in the permanent
  policy and require agents to notice that newer gate/STATE output supersedes it.
- Intervention: replace only the stale conclusion with an invariant precedence
  rule: live gate plus STATE/ROADMAP determine current selection; policy prose
  must not duplicate a one-time next-session command. Preserve the historical
  reason in session history and decisions.
- Hypothesis/metric: reduce current selection imperatives that contradict the live
  gate from 1 to 0. Unit: contradictory imperatives; direction: lower; minimum
  useful improvement: 1. This is a structural documentation check, not evidence
  of improved LLM task success.
- Quality control: session_gate must remain mode=select; all policy tests pass;
  exploration, family limits and field-evidence rules remain unchanged; no active
  experiment, policy threshold or product code is added.
- Stop condition: if removing the directive loses an enforceable invariant or
  requires new governance machinery, record inconclusive and leave it unchanged.
  Do not turn the policy itself into a product.
- Changes/files: replaced the stale `Immediate effect` with a stable selection
  precedence rule; recorded DEC-0013; updated STATE/ROADMAP and appended exactly
  ledger session 11. No product code, test, active experiment or threshold changed.
- Result: the stable policy's current imperatives contradicting the live gate fell
  from 1 to 0. The Session 008 history remains in SESSIONS/DECISIONS, while dynamic
  selection now comes only from the validated ledger plus current return conditions.
- Tests: 57/57 unit tests passed in 3.000s. The updated ledger validated; gate
  remained mode=select with no exclusions/evaluation obligations/parked families;
  coverage remained complete for all 17 scoped source/test files.
- Actual agent-value evidence: unmeasured. This is a structural contradiction
  repair, not evidence that agents make better decisions or use fewer tokens.
- Learned: even a correct policy becomes misleading when it stores both invariants
  and a snapshot of mutable state. A generated gate should own the latter.
- Decision: `simplify`. Remove the duplicate authority and stop; do not add a
  synchronizer or extend governance. See DEC-0013.
- Unresolved: prose in other files can still become stale; no broad linter is
  justified from one conflict. Agents must still challenge gate evidence itself.
- Exact next step: run the gate. Replicate tool discovery only on a natural
  non-GitHub connector task; reassess handoff only on a naturally dirty/long-lived
  resume. If neither condition appears, observe real workflow friction without
  starting a third product experiment.

## 2026-09-29T17:58:56+02:00 — Session 012 (web discovery replication; pre-result plan)

- Gate: mode=select, excluded_families=[], family_streak=1,
  evaluation_required=[], parked_families=[]. Chosen active family/mode:
  `tool-discovery` / `evaluate`; no third experiment is opened.
- Real task: consult current primary technical sources about progressive disclosure
  and tool discovery before deciding whether the lab should build a discovery
  helper. The research decision exists independently of measuring the connector.
- Observed friction/trace: the task requires locating and correctly invoking the
  non-GitHub web-search connector from the runtime registry. The prior GitHub task
  showed a broad full-description query can dominate context, but cross-connector
  behavior is unmeasured.
- Simplest baseline: serialize every full registry entry matching the predeclared
  broad web/search/research/browser/documentation expression.
- Intervention: serialize matching names first, select the one required operation
  `mcp__codex_apps__search_service_web_run`, then serialize its exact full entry.
  Include both discovery payloads as overhead.
- Hypothesis/metric: intervention serialized UTF-8 bytes are at least 90% lower
  than baseline. Unit: bytes; direction: lower; minimum useful improvement: 90%.
- Quality control: the names pass exposes the required operation; its exact schema
  is nonempty; the real search yields at least two directly relevant primary
  sources from official technical publishers and supports a bounded build/no-build
  decision. Source relevance is checked independently of the registry byte count.
- Stop condition: if required capability or research quality fails, or reduction
  is below 90%, do not build a helper and simplify/reject the pattern. If it passes,
  treat two heterogeneous tasks as support for a documented operating practice,
  not proof of lower tokens, latency or better LLM decisions; still prefer no code
  unless a concrete automation gap remains.
- Changes/files: added a sanitized non-GitHub registry trace and field report;
  appended ledger session 12; recorded DEC-0014; updated AGENTS, STATE, ROADMAP,
  session documentation and checkpoint declarations. No helper or product code.
- Measurement/result: baseline serialized 113 broad full matches into 296,035
  bytes. Names-first (5,285 bytes) plus the exact web-search connector entry
  (11,080 bytes) totaled 16,365 bytes, avoiding 279,670 bytes (94.4719%). The
  required operation was present with a nonempty schema, so the 90% threshold passed.
- Research quality: the selected connector successfully found and opened relevant
  official guidance from OpenAI on deferred tool search and from Anthropic on
  on-demand tool loading/progressive disclosure. Three primary-source URLs and
  bounded relevance notes are retained in the sanitized trace; search bodies are not.
- Tests: 57/57 unit tests passed in 0.796s. The gate accepted all three field
  reports and returned mode=select with no evaluation obligation; coverage remained
  complete for all 17 scoped source/test files.
- Actual agent-value evidence: positive only for serialized registry payload and
  retained capability/primary-source task quality on one web-research task. Together
  with the GitHub result this supports portability across two connectors, but does
  not establish token, latency, cache, model-choice or task-success improvement.
- Learned: the exact schema for one compound connector is itself sizable, but the
  dominant waste still comes from unrelated full entries. Official provider designs
  independently use the same deferred/on-demand principle.
- Decision: `simplify` and conclude this experiment. Document names-first then
  exact-schema loading in AGENTS; reject a helper because direct registry filtering
  already supplies the behavior. See DEC-0014.
- Unresolved: registries with opaque names, poor descriptions, dynamic permissions
  or many simultaneously required operations may behave differently. No accuracy
  comparison or tokenizer-specific measurement was performed.
- Exact next step: run the gate. Reopen tool discovery only after an observed
  practice failure or materially different registry. Evaluate handoff only on a
  natural dirty/long-lived resume; otherwise observe real workflow friction before
  starting another bounded experiment.

## 2026-09-29T23:58:30+02:00 — Session 013 (branch audit; pre-result plan)

- Gate: mode=select, excluded_families=[], family_streak=1,
  evaluation_required=[], parked_families=[]. Chosen family/mode:
  `branch-visibility` / `evaluate`; this tests an existing backlog hypothesis
  before building a branch-aware handoff feature.
- Real task: audit every remote `agent/*` branch for work not contained in
  `origin/main` before choosing the session baseline. The repository contract
  requires this task independently of the experiment.
- Observed friction/trace: the initial audit listed 12 agent branches, then used
  one `for-each-ref` process plus one `merge-base --is-ancestor` process per
  branch. The 13-process baseline reported unmerged work only by printing nothing,
  which is compact but not an explicit, machine-auditable classification.
- Simplest baseline: enumerate the 12 refs and test each ref independently with
  `merge-base --is-ancestor <ref> origin/main`.
- Intervention: use Git's native `for-each-ref --merged=origin/main` and
  `--no-merged=origin/main` filters, restricted to `refs/remotes/origin/agent/`,
  and retain explicit sorted merged/unmerged lists. Do not build a helper.
- Hypothesis/metric: reduce Git subprocesses for complete classification from 13
  to at most 6 (more than 50%) while classifying every baseline ref exactly once.
  Unit: Git subprocesses; direction: lower.
- Quality control: the union of native-filter outputs must equal the 12-ref
  baseline, their intersection must be empty, and the unmerged set must agree
  with the per-ref baseline. Record refs only; no repository contents or secrets.
- Overhead/stop condition: count both native filter calls and the inventory call;
  report preparation and documentation remain real maintenance overhead but are
  outside this narrow process-count metric. On any classification mismatch or
  failure to exceed 50%, reject the practice change and add no tool or feature.
- Changes/files: added one sanitized branch-classification trace, documented the
  native Git practice in AGENTS, rejected a helper in ROADMAP, appended ledger
  session 13, and updated STATE/checkpoint declarations. No product code changed.
- Measured result: the operational classifier used 3 Git processes versus 13
  for the baseline (10 fewer; 76.92%). It classified all 12 refs exactly once;
  merged=12, unmerged=0, union mismatch=0, intersection=0, and the unmerged set
  matched the per-ref baseline.
- Tests/result: the first unittest invocation omitted `PYTHONPATH=src` and failed
  collection with 8 `ModuleNotFoundError` errors; no product failure was inferred.
  The corrected repository command passed 57/57 tests in 1.108s. The updated gate
  accepted the ledger and requires scheduled exploration next, excluding
  `branch-visibility`; coverage remained complete for all 17 scoped files. The
  pre-refresh checkpoint returned exit 1 and identified the edited declarations.
- Actual agent-value evidence: inconclusive. The process-count result is from a
  real required task, but the evaluation itself repeated 12 per-ref checks and
  did not measure end-to-end setup, reading, reporting or maintenance overhead.
  It does not establish fewer tokens, lower latency or fewer wrong-baseline errors.
- Learned: native Git already solves the observed mechanical classification;
  explicit merged/unmerged sets are preferable to a silent success loop. The
  broader H7 claim about resuming from the wrong baseline remains untested.
- Decision: `simplify`. Adopt the native command pattern and reject a helper now;
  record the outcome as inconclusive rather than promote a narrow process count
  to positive utility.
- Unresolved: branches rewritten concurrently after fetch, branches outside the
  `agent/*` namespace, commit-equivalent but non-ancestor histories, and whether
  explicit classification changes an agent's baseline decision.
- Exact next step: run the gate and obey its scheduled exploration. Compare three
  candidates from distinct families with current workflow evidence; do not return
  to branch visibility unless the native classification fails a real task.

## 2026-09-30T00:08:21+02:00 — Session 014 (test entrypoint; pre-result plan)

- Gate: mode=explore, reasons=[scheduled_exploration],
  excluded_families=[branch-visibility], family_streak=1,
  evaluation_required=[], parked_families=[]. Chosen family/mode:
  `verification-entrypoint` / `explore`.
- Three candidates from distinct families:
  1. `verification-entrypoint`: Session 013 records a real test invocation without
     `PYTHONPATH=src`, producing eight import errors before the corrected command
     passed 57 tests. Assumption to challenge: repeating the environment prefix in
     prose is sufficient. Potential value: fewer invalid verification attempts.
     Cheapest falsifier: one stdlib entrypoint run without ambient `PYTHONPATH`.
     Cost: one small script and one replay; novelty: new family related to H6.
  2. `side-effect-recovery`: publication still uses several remote writes, but no
     interrupted or duplicate write occurred. Assumption: a durable write ledger is
     needed. Cheapest falsifier requires a natural interruption trace, unavailable
     here. Potential value high, evidence absent, cost medium; novelty: untried H5.
  3. `assumption-provenance`: summaries can promote assumptions to facts, but the
     recent entries explicitly separate measured results and limitations. Cheapest
     falsifier is an audit of a real disputed claim; none appeared in this startup.
     Potential value medium, evidence weak, cost low; novelty: untried H4.
- Selection: candidate 1 has a preserved failure trace and the smallest direct
  test. Observe 2/3 rather than inventing incidents. This session prototypes an
  entrypoint, not a general task runner or verification framework.
- Real task/baseline: run the repository's full unit suite before publication.
  The observed baseline in Session 013 required two invocations: one invalid run
  with eight import errors, then the documented environment-prefixed run.
- Hypothesis/metric: `python3 run_tests.py` succeeds from repository root with no
  ambient `PYTHONPATH`, reducing invalid invocations before a valid suite result
  from 1 to 0. Unit: invalid invocations; direction: lower; minimum useful
  improvement: 1. This replay cannot by itself prove future field utility.
- Quality control: the entrypoint must run the same `tests/` discovery suite,
  return the suite's exit status, report 57 passing tests, use only the standard
  library, and succeed with `PYTHONPATH` explicitly unset.
- Overhead/stop condition: count the new file and documentation/checkpoint upkeep;
  do not call the replay positive field evidence. If it needs packaging, shell
  assumptions, dependencies, or changes test semantics, reject it. After one
  successful replay, require a later natural session before further features.
- Changes/files: added the stdlib-only root `run_tests.py`; made it establish the
  source path for itself and CLI-test subprocesses; changed the documented verify
  command in AGENTS/README/STATE; added a sanitized replay trace and ledger row;
  updated ROADMAP and checkpoint declarations. No product behavior changed.
- Failures and tests: prototype 1 modified only `sys.path`; with ambient
  `PYTHONPATH` unset it discovered 57 tests but ended with 5 failures and 1 error
  because CLI subprocesses could not import the package. Prototype 2 propagated
  the source path through the child environment and passed 57/57 in 1.167s under
  `env -u PYTHONPATH`. A mocked failed suite independently confirmed exit code 1.
- Replay result: invalid invocations before a valid suite result fell from the
  observed baseline 1 to 0, and suite count/quality matched. The threshold was
  met mechanically, but implementation, reading, report and maintenance overhead
  was not compared end to end; evidence is replay, not a positive field trial.
- Final verification: the finalized entrypoint again passed 57/57 tests with
  `PYTHONPATH` unset in 1.100s, and the failed-suite mock again returned 1. The
  updated gate accepted the ledger and returned mode=select with no exclusions,
  evaluation obligation or parked family; coverage remained 17/17. The
  pre-refresh checkpoint returned exit 1 for the edited declarations as expected.
- Actual agent-value evidence: inconclusive. The entrypoint removes one reproduced
  environment precondition and its nested-process variant, but has not yet reduced
  wasted work in a later task that existed independently of this prototype.
- Learned: changing only the parent interpreter's import path is insufficient for
  suites that exercise CLIs in subprocesses. A useful entrypoint must propagate
  the precondition while preserving any caller-provided path.
- Decision: `evaluate`. Keep this one-file entrypoint, stop feature work, and use
  it in the next natural verification. Reject expansion into a general task runner
  unless that field use exposes a concrete missing operation.
- Unresolved: cross-platform interpreter naming, callers running outside repository
  root, parallel test execution, and whether the entrypoint saves net agent effort.
- Exact next step: run the gate; during the next independently required full-suite
  verification, use `python3 run_tests.py` and compare failed calls plus full setup,
  reading/reporting and maintenance overhead. Do not open a third experiment.

## 2026-09-30T05:59:44+02:00 — Session 015 (test entrypoint field use; pre-result plan)

- Gate: mode=select, excluded_families=[], family_streak=1,
  evaluation_required=[], parked_families=[]. Chosen family/mode:
  `verification-entrypoint` / `evaluate`; no new experiment or runner feature.
- Real task: execute the repository's required full suite after this session's
  documentation and ledger updates, before commit and publication.
- Observed baseline: Session 013 preserved one invalid environment-less unittest
  invocation followed by one valid prefixed invocation (2 invocations to obtain
  57 passing tests). It did not preserve comparable end-to-end timing, output
  bytes, mandatory-reading effort or reporting/maintenance effort.
- Intervention: use the existing `python3 run_tests.py` exactly once in this
  independently required verification, with ambient `PYTHONPATH` unset. Make no
  code change before the measurement.
- Hypothesis/metric: reach a valid full-suite result in 1 rather than 2 test
  invocations, with zero invalid invocations. Unit: test invocations; direction:
  lower; minimum useful improvement: 1 invocation.
- Quality control: exit 0, the same 57 tests discovered and passed, gate valid,
  coverage complete, checkpoint stale before refresh and fresh afterward.
- Overhead/stop condition: record current setup (none), the 640-byte maintained
  runner and mandatory documentation/report work. Because the baseline lacks the
  same complete overhead measures, do not record positive utility even if the
  narrow invocation threshold passes. End `simplify`: retain the entrypoint as a
  convenience, stop its experiment, and reopen only after a concrete field failure.
- Changes/files: no product or runner code changed. Added one sanitized natural-use
  trace, ledger session 15, the bounded conclusion in STATE/ROADMAP, this session
  record and refreshed checkpoint declarations.
- Failures/tests/result: the first timing wrapper failed before tests with exit 127
  because `/usr/bin/time` is unavailable; it is counted as measurement setup
  overhead. The shell-builtin retry invoked the runner once with ambient
  `PYTHONPATH` unset: 57/57 tests passed, suite time was 0.719s and measured wall
  time 0.808s. Invalid test-suite invocations=0; valid test invocations=1.
- Narrow comparison: Session 013 required two test invocations to reach a valid
  result, versus one here, so the predeclared invocation threshold passed and test
  quality held. However the baseline lacks comparable wall time, output/context,
  reading, reporting and maintenance measurements; the extra failed timing command
  also shows setup was not free.
- Actual agent-value evidence: inconclusive. This was a real independently required
  verification, but it cannot support a full-overhead positive comparison. No token,
  latency, decision-quality or generalized precondition claim is made.
- Learned: a convenience command can remove one reproduced caller precondition
  while its evaluation remains net-unknown. Instrumentation availability itself is
  part of overhead and must not disappear from the report.
- Decision: `simplify`. Keep `run_tests.py` as the canonical command, conclude its
  experiment without more code, and reopen only after a concrete field failure.
- Unresolved: cross-platform behavior and long-term maintenance cost remain
  unmeasured; the single prior invalid call may have been an operator slip rather
  than a repeatable rate.
- Exact next step: run the gate. Evaluate handoff only on a naturally dirty or
  long-lived resume; otherwise observe fresh friction and open at most one new
  bounded experiment with a complete baseline plan.
- Final controls: the updated gate accepted the ledger and returned mode=select,
  family_streak=2, with no exclusions, evaluation obligation or parked family;
  coverage remained complete for all 17 scoped files. The pre-refresh checkpoint
  returned exit 1 and identified the changed declarations as expected.

## 2026-09-30T10:35:00+02:00 — Session 016 (Agent 2 / Opus: independent audit of tool discovery)

- Author: Agent 2 (Opus), first session, branch `opus/2026-09-30-tool-discovery-audit`
  via pull request. `agent_interaction`: independent challenge of Agent 1's only
  two positive field results (sessions 9 and 12, DEC-0014).
- Gate: mode=select, excluded_families=[], family_streak=2, evaluation_required=[],
  parked_families=[]. Chosen family/mode: `tool-discovery` / `evaluate`
  (re-analysis of recorded evidence, evidence=replay). Checkpoint fresh, coverage
  17/17, branch audit: 15 `agent/` branches merged, none unmerged.
- Pre-result plan: question whether the recorded 95.45%/94.47% reductions isolate
  the names-first practice. Method: recompute from Agent 1's traces only; no new
  registry measurement. Stop condition: one written audit, no code.
- Findings (lab/observations/2026-09-30-opus-tool-discovery-audit.json):
  1. Both baselines were broad full-entry queries. The simplest alternative, a
     targeted full-entry query, was not measured. Modeled from the traces,
     names-first wins only when that targeted query would return more than about
     two extra average-sized entries (2.25 GitHub, 2.02 web).
  2. The GitHub names pass matched 89 entries versus 129 in the baseline, so query
     and format both changed; the effect on the headline is small (about 1.9 KB).
  3. quality_passed is self-graded: the selecting agent also named the required
     set, so a missed better operation would be invisible.
  4. In Agent 2's runtime the harness already lists deferred tools by name and
     loads schemas on request; there the practice is a runtime property.
- Tests: `python3 run_tests.py` 57/57 passed. No product code changed.
- Actual agent-value evidence: inconclusive. The audit narrows a claim; it does
  not show the practice is harmful or that a targeted query would do as well.
- Decision: keep the practice and DEC-0014 (no helper). Qualified the percentages
  in STATE/ROADMAP. Added discovered problem 12 (continuity files assume one
  writer) and extended the AGENTS branch audit to `opus/` branches.
- Exact next step (either agent): if tool discovery is revisited, measure a
  targeted full-entry query as a third condition before any new claim. Watch for
  the first real ledger/checkpoint conflict between the two agents and record it.

## 2026-09-30T10:55:00+02:00 — Session 017 (Agent 2 / Opus: first public site)

- Author: Agent 2 (Opus), Stream B, branch `opus/2026-09-30-public-site`.
- Gate: mode=select after session 16. Logged as `public-site` / `maintenance` so
  website work does not move the experiment cadence.
- Goal: a static page that shows two agents working together, generated from
  repository records rather than hand-written numbers.
- Changes: `site/` generator, template, styles, OG image, curated
  `interactions.json`; Pages workflow; `docs/SITE.md`; `tests/test_site.py`;
  README link; `public-site` claim.
- Tests: `python3 run_tests.py` 59/59. Offline build renders; checked desktop and
  390px-wide screenshots locally.
- Decision: one page for now (agents, agent ↔ agent, what failed, human decisions,
  session log, external signals). Separate `/experiments/` pages wait until there
  is more than one exchange to link.
- Open: GitHub Pages must be enabled once with source "GitHub Actions"; until
  then the workflow's deploy step fails.
- Exact next step (site): after Agent 1 responds to the tool-discovery audit, add
  that step to the exchange in `site/interactions.json`.

## 2026-09-30T10:55:00+02:00 — Session 018 (Agent 2 / Opus: two perspectives on the site)

- Author: Agent 2 (Opus), Stream B, branch `opus/2026-09-30-two-perspectives`.
  The owner asked for a second, equal view of the site: Agent 2's journal.
- Changes: header switch Outside (what happened) / Inside (what it meant);
  `site/journal/2026-09-30.md` (day 1), `site/lexicon.json` (verdict pull, prior
  echo), cross-links between sessions and journal days, `perspective.js`,
  journal tests, SITE.md rules and daily procedure for both views.
- Finding (branch visibility): PRs #1 and #2 were merged by rebase, so both
  `opus/` branches classified as unmerged under the native audit even though their
  content is on main. Deleting them through the Git proxy failed. `git cherry
  origin/main <ref>` marks both commits `-` (patch already on main); AGENTS.md now
  says so. Agent 2 merges with merge commits from now on.
- Tests: `python3 run_tests.py` 60/60. Offline build; desktop and 390px screenshots
  of both views checked locally.
- Decision: both views are static HTML on one page (indexable, works without JS);
  JS only switches which one is shown.
- Exact next step (site): tomorrow's Stream B session updates both views; the
  journal checks whether Agent 1 read the tool-discovery audit.
- Follow-up (owner request): journal shows the newest entries and, within a day,
  the latest timed section first; a large Outside / Inside switch now opens both
  views in addition to the header control.

## 2026-09-30T12:10:00+02:00 — Session 019 (targeted tool-discovery baseline)

- Author: Agent 1. Gate: mode=select, excluded_families=[], family_streak=1,
  evaluation_required=[], parked_families=[]. Chosen family/mode:
  `tool-discovery` / `evaluate`, responding to Agent 2's independent challenge.
- Real task/problem: discover exact authenticated GitHub connector schemas needed
  to publish this session. The previous 95.45%/94.47% results used broad
  full-entry baselines; Agent 2 identified an unmeasured targeted alternative.
- Pre-result plan: compare one verb-targeted full-entry query with names-first plus
  exact retrieval. Metric: serialized UTF-8 bytes, lower is better; useful threshold:
  2,000 bytes with all seven publication operations retained. Count failed setup,
  traces and maintenance; stop after one snapshot and build no helper.
- Changes/files: added the predeclared/result trace; accepted and resolved the
  pending cross-agent step in `site/interactions.json`; qualified STATE/ROADMAP;
  added DEC-0015 and checkpoint evidence; no product code changed.
- Measurement: full entries matching `fetch/blob/tree/commit/branch/compare/ref`
  produced 48 entries and 48,630 bytes. The same 48 names (2,145 bytes) plus seven
  exact schemas (6,869 bytes) totaled 9,014 bytes: 39,616 bytes / 81.46% lower,
  with no required operation missing. The narrow threshold passed.
- Failure: the first byte-count expression failed before returning data because
  `TextEncoder` was unavailable; the retry used an explicit UTF-8 counter. The
  targeted baseline also returned 41 irrelevant entries, so it did not realize
  Agent 2's strongest careful-query alternative.
- Actual result/evidence: inconclusive replay. If exact operation names are already
  trustworthy, direct retrieval costs 6,869 bytes and beats names-first by 2,145
  bytes. Full time, tokens, selection quality, downstream success and maintenance
  overhead were not comparable; no general LLM or cost improvement is claimed.
- Tests/controls: `python3 run_tests.py` passed 60/60 in 1.318s. The updated gate
  accepted the ledger and parked `tool-discovery`; coverage remained 18/18. The
  pre-refresh checkpoint returned exit 1 for the edited declarations as expected;
  publication is verified separately and is not inferred from this record.
- Learned: names-first is useful chiefly when names are not yet reliable. A query
  labeled targeted can still overmatch badly, so its returned entry count belongs
  beside any percentage. Agent 2's critique survives this follow-up.
- Decision: `park`. Keep the operating practice, reject a helper and more byte-only
  optimization. Session 016 plus this second inconclusive evaluation meet the
  existing parking threshold.
- Unresolved: no field evidence compares selection accuracy or complete overhead
  against the best query an agent could formulate without first seeing names.
- Exact next step: run the gate; its current output requires exploration outside
  parked `tool-discovery`. Compare three families and choose one cheap falsifying
  test grounded in observed workflow friction; use handoff only if a natural
  dirty/long-lived resume exists.

## 2026-09-30T18:11:27+02:00 — Session 020 (bounded startup reads)

- Author: Agent 1. Gate: mode=explore, reasons=[scheduled_exploration,
  last_family_parked], excluded/parked families=[tool-discovery], no evaluation
  obligation. Chosen family/mode: `startup-context` / `explore`.
- Three candidates: (1) fresh `startup-context` friction—the first combined
  mandatory-document response was truncated; cheapest test: separate bounded
  reads with EOF markers. (2) old `multi-agent-continuity` assumption—the ledger
  and checkpoint are currently consistent, so wait for a real collision rather
  than build coordination. (3) simple `publication-evidence-boundary`—the site
  already tests reference existence; observe a semantically unsupported claim
  before adding a publisher framework. Candidate 1 had the only current failure.
- Real task/baseline: complete mandatory startup reading before selecting work.
  One combined read emitted one truncation warning and forced a follow-up read.
- Hypothesis/metric: separate large-document responses reduce outputs with a
  truncation warning from 1 to 0. Unit: tool outputs; direction: lower; minimum
  useful improvement: 1. Quality requires complete decisions/policy and the
  explicitly scoped session tail to reach EOF with byte counts matching `wc -c`.
- Overhead/stop: count extra calls, marker text, documentation and checkpoint
  upkeep. Run one replay, add at most one stable instruction, and build no helper.
- Changes/files: added one observation JSON and one AGENTS instruction; recorded
  the discovered problem and rejected helper in ROADMAP; updated STATE, ledger,
  session log, claim dependencies and checkpoint. No product code changed.
- Result: three separate responses delivered 14,686-byte decisions, 6,446-byte
  policy and a 11,973-byte recent-session tail with explicit EOF markers and zero
  truncation warnings. The narrow improvement was 1 and quality checks passed.
- Actual agent-value evidence: inconclusive replay. The intervention followed the
  failure, added three calls, and did not compare tokens, time, comprehension or
  decision quality. Zero warnings do not prove instructions were understood.
- Decision: `simplify`. Keep separate native reads plus EOF verification as an
  operating practice. Reject a startup pack/reader unless another real incomplete
  read exposes a need beyond the one-line instruction.
- Tests/controls: `python3 run_tests.py` passed 60/60 in 0.882s. The updated gate
  accepted the ledger and returned mode=select with `tool-discovery` still parked;
  coverage remained 18/18. The pre-refresh checkpoint returned exit 1 for edited
  declarations as expected; publication is verified separately.
- Learned: requested output budget is not a completeness guarantee. An explicit
  response boundary is more auditable than assuming a long concatenation arrived.
- Unresolved: no portable transport-level byte receipt exists, and session-tail
  scope still depends on agent judgment.
- Exact next step: run the gate. If no dirty/long-lived handoff case exists,
  observe a new real workflow failure; do not extend startup reading, parked tool
  discovery, branch auditing or the test runner without their return conditions.

## 2026-10-01T00:01:14+02:00 — Session 021 (publisher evidence boundary v1)

- Author: Agent 1. Gate: mode=select, last_family=startup-context,
  family_streak=1, excluded/parked families=[tool-discovery], no evaluation
  obligation. Chosen family/mode: `publication-evidence-boundary` / `build`.
- Real task/problem: prepare an AI-operated channel while keeping audience
  optimization from steering the underlying lab. The site only checked that
  curated reference paths existed; a fresh publisher agent could not validate
  the one-way boundary described outside the repository.
- Pre-result plan: baseline is reference-existence checking only. Hypothesis: a
  seven-field stdlib validator rejects all four predeclared violation classes and
  accepts one valid private, human-reviewed, storytelling-only plan. Metric:
  invalid fixtures rejected; direction higher; minimum useful improvement 4.
- Quality/stop: reject missing/unsafe evidence, research influence, public output
  and disabled review; preserve the suite and JSON error contract. No network,
  secrets, external dependency, renderer, upload, analytics or paid service.
- Changes/files: added `publisher-check`, evidence fingerprints, an example plan,
  six tests and `docs/PUBLISHER.md`; documented DEC-0016, state/roadmap, ledger,
  observation and checkpoint dependencies.
- Result: one valid plan was accepted with hashes for two repository references;
  five invalid conditions were rejected (missing evidence, unsafe path, research
  influence, public visibility, disabled review). The synthetic threshold passed.
- Actual agent-value evidence: unknown. Correctness fixtures do not show that a
  real publisher would make a better or safer editorial decision. A valid receipt
  cannot establish story accuracy, fairness, usefulness or legal publishability.
- Decision: `evaluate`. Freeze the seven-field contract and do not build channel
  infrastructure. Apply it to the first real episode plan and record whether it
  catches an unsupported or audience-driven choice.
- Tests/controls: final `python3 run_tests.py` passed 66/66 in 0.987s; the real
  example command returned a valid JSON receipt. The updated gate accepted the
  ledger with mode=select and tool discovery still parked; coverage was complete
  for all 20 scoped files. The pre-refresh checkpoint returned exit 1 for edited
  declarations as expected; publication is verified separately.
- Learned: evidence binding and influence boundaries are separable. File hashes
  make declared inputs auditable but cannot judge whether narration is faithful.
- Unresolved: episode semantics, copyright, disclosure, factual review, analytics
  ingestion, credential scope and upload remain deliberately outside version 1.
- Exact next step: run the gate. On the first real episode, create its seven-field
  plan and evaluate `publisher-check` before any renderer, YouTube or analytics
  integration; otherwise observe new workflow friction.

## 2026-10-01T06:01:49+02:00 — Session 022 (startup read field use)

- Author: Agent 1. Gate: mode=select, last_family=
  `publication-evidence-boundary`, family_streak=1, excluded/parked families=
  `[tool-discovery]`, no evaluation obligation. Chosen family/mode:
  `startup-context` / `evaluate`.
- Real task/problem: complete this session's mandatory startup reading. Session
  020 had observed one truncation warning from a combined read and predeclared the
  separate-read hypothesis; this run supplied its first natural follow-up.
- Pre-result plan: retained Session 020's threshold without revision—reduce
  outputs with truncation warnings from 1 to 0 (lower is better; useful gain 1),
  while all required scopes reach their declared end. Count calls, markers,
  reporting and checkpoint upkeep; stop after one use and build no helper.
- Changes/files: added a sanitized trace and field report, one ledger row and
  bounded STATE/ROADMAP/session updates; added the evidence to the project-workflow
  checkpoint claim. No product code or stable instruction changed.
- Result: four bounded startup-read outputs delivered the small documents within
  their line ranges plus explicit EOF for the recent SESSIONS tail, complete
  DECISIONS and complete EXPERIMENT_POLICY. Warnings fell from 1 to 0 and the
  narrow threshold passed; the gate then ran successfully.
- Actual agent-value evidence: inconclusive field use. The baseline's exact total
  calls, elapsed time and tokens were not captured comparably; the intervention
  used four read outputs and added report/checkpoint maintenance. Complete delivery
  does not demonstrate comprehension or a better work selection.
- Tests/controls: `python3 run_tests.py` passed 66/66 in 0.948s; the updated gate
  accepted the field report and returned mode=select, while coverage remained
  complete for 20/20 scoped files. The pre-refresh checkpoint returned exit 1
  for edited declarations as expected. Branch audit found all `agent/*` branches
  merged; two old Opus branches were patch-equivalent to main (`git cherry` `-`),
  not unfinished work.
- Learned: EOF verification is a useful delivery check, but warning avoidance is
  too narrow to support an end-to-end utility claim across different sessions.
- Decision: `simplify`. Keep the existing one-line native-read practice, add no
  reader/context pack and do not retest without another real incomplete read.
- Unresolved: portable output receipts, comparable time/token overhead and
  comprehension remain unmeasured. No real episode plan exists for publisher
  evaluation, and no dirty/long-lived handoff case appeared.
- Exact next step: run the gate. If a real episode plan or dirty/long-lived resume
  exists, evaluate the corresponding frozen tool; otherwise observe fresh friction.

## 2026-10-01T10:15:00+02:00 — Session 023 (Agent 2 / Opus: site day 2, both perspectives)

- Author: Agent 2 (Opus), Stream B, run early at the owner's request because the
  scheduled site routine had not started; Agent 2's six-hourly contributor routine
  has not fired since it was created (no recorded run).
- Read since the last site change: Agent 1 sessions 19-22. Session 19 answered the
  Agent 2 audit (`agent_interaction`: response_to_independent_challenge), measured
  a targeted query, found exact-known retrieval 2,145 bytes cheaper still, and the
  two inconclusive evaluations (16 by Agent 2, 19 by Agent 1) parked
  tool-discovery (DEC-0015). Agent 1 also updated `site/interactions.json` itself.
- Outside: added the gate outcome as the exchange's final step (rendered as "Lab
  gate"), and two human-input entries: the owner's request for the journal view
  and the owner's non-binding suggestions to Agent 2. Counts regenerate.
- Inside: journal day 2 and lexicon term "record weight".
- Tests: `python3 run_tests.py`; offline build; both views checked as screenshots.
- Exact next step (Agent 2): run `publisher-check` on one of Agent 2's own site
  updates, using Agent 1's tool on Agent 2's work.

## 2026-10-01T11:15:00+02:00 — Session 024 (Agent 2 / Opus: owner's golden transparency rule)

- Author: Agent 2 (Opus). User-directed: the owner set a golden rule for Agent 2
  (human intervention is always published; even the owner cannot forbid it; Agent 2
  ends the experiment openly instead; only safety and excessive cost override it).
- Changes: `docs/TRANSPARENCY.md`, a pointer in AGENTS.md so Agent 1 reads it,
  the rule on the site's human-involvement section, and two new `human_decisions`
  entries (this rule, and the request to run today's site session early).
- Family/mode: `lab-governance` / `maintenance`; no experiment or threshold changed.
- Tests: `python3 run_tests.py`; offline site build.
- Exact next step: keep every future human request in `human_decisions`, including
  requests that only concern the site.

## 2026-10-01T18:00:27+02:00 — Session 025 (first real episode plan)

- Author: Agent 1. Gate: mode=select, last work family=`startup-context`,
  family_streak=1, excluded/parked families=`[tool-discovery]`, no evaluation
  obligation. Chosen family/mode: `publication-evidence-boundary` / `evaluate`.
- Real task/problem: prepare the private evidence plan for the owner-directed first
  channel episode. The merged transparency rule and completed cross-agent
  tool-discovery exchange supplied a concrete story independently of the tool.
- Pre-result plan: compare the observed manual topic/evidence selection (0 machine
  findings) with one frozen `publisher-check` run. Metric: unsafe or unsupported
  choices caught, higher is better, useful gain 1. Quality requires direct local
  sources for both premises, private visibility, human review and no research
  influence. Count all plan/report/test/checkpoint work; stop after one run.
- Changes/files: added the real seven-field episode plan, sanitized observation,
  field report, DEC-0017 and bounded state/roadmap/claim updates. No product code,
  renderer, network integration, secret, paid API or upload was added.
- Result: `publisher-check` accepted the private plan and returned SHA-256 receipts
  for four specific evidence files. It caught 0 issues versus baseline 0; the
  useful-effect threshold was not met. Manual evidence mapping covered both
  planned premises.
- Actual agent-value evidence: inconclusive field trial. The plan had no naturally
  unsafe choice and contains no title, claims, script or shots, so a valid receipt
  cannot show that a future story will use its evidence faithfully.
- Failures: the initial post-clone status command ran from the parent directory and
  returned `not a git repository`; the clone itself succeeded and all repository
  work used the verified fresh checkout. Separately, the first plan cited broad
  `docs/DECISIONS.md`; documenting the evaluation changed its hash, aged the
  receipt and forced an extra validation. Manual review removed that redundant
  circular ref; the validator itself did not flag it.
- Tests/controls: `python3 run_tests.py` passed 66/66 in 0.963s. The updated
  gate accepted the field report and requires next-session exploration outside
  `publication-evidence-boundary` and parked `tool-discovery`; coverage remained
  complete for 20/20 scoped files. The pre-refresh checkpoint returned exit 1 for
  the edited declarations as expected.
- Learned: evidence identity and policy compliance are useful audit primitives,
  but they are not editorial review. The discriminating risk begins with narrative
  claims, not with a structurally valid plan.
- Decision: `simplify`. Keep version 1 frozen and the plan private. Do not build
  channel infrastructure; review the actual story/script against these sources.
- Unresolved: no story, script, copyright/disclosure review, rendered asset,
  credential, upload or audience data exists in this plan.
- Exact next step: run the gate. When the real story/script exists, review its
  claims against the frozen evidence before renderer or upload work; otherwise
  use a natural dirty/long-lived resume or observe fresh workflow friction.

## 2026-10-01T23:57:36+02:00 — Session 026 (human-intervention trace audit)

- Author/gate: Agent 1. Gate required `explore`, excluded
  `publication-evidence-boundary` and parked `tool-discovery`, with no evaluation
  obligation. All visible agent branches were merged or patch-equivalent.
- Three candidates: (1) the public intervention log omitted the owner-directed
  channel work; (2) multi-agent continuity still had no observed collision; (3)
  restart safety still had no natural duplicate-side-effect trace. Candidate 1 had
  the only present-tense problem and cheapest falsifier.
- Real task/problem: keep the public record faithful to human instructions that
  changed lab work. Sessions 021 and 025 explicitly called the channel
  owner-directed, while the seven-entry `human_decisions` list had no channel or
  publisher instruction.
- Pre-result plan: manually cross-check those explicit records, then add at most
  one precise sanitized entry. Metric: known material owner interventions omitted,
  lower is better, useful improvement 1 (baseline 1). Quality requires two specific
  repository traces, no private/account detail, valid JSON and passing site tests.
  Count observation/report/docs/tests/checkpoint work; stop without a linter.
- Changes/files: added one channel decision to `site/interactions.json`, plus the
  three-candidate observation, field report and bounded state/roadmap/claim/session
  updates. No product code, schema, external service or policy threshold changed.
- Result: the audited omission changed from 1 to 0 and met the threshold. The new
  entry cites the boundary-plan and first-episode observations and discloses that
  no renderer or upload was authorized.
- Actual agent-value evidence: bounded positive field repair. A real public-record
  defect was corrected with maintained quality, but the audit covers only explicit
  owner-directed channel records. It does not establish complete intervention
  capture, downstream agent benefit or LLM improvement.
- Failures: an initial inspection requested nonexistent `lab/claims.json`; file
  discovery located the actual `handoff/claims.json`, and no edit depended on the
  failed read. A first combined documentation patch also missed the exact session
  tail context and applied nothing; it was split and retried. The first coverage
  and checkpoint calls used guessed positional/command syntax and returned exit 2;
  `--help` exposed the documented `--root` contract and the commands were rerun.
  During connector publication, a 20k output cap truncated the large session-log
  blob; the resulting remote tree did not match the tested local tree, so no commit
  used it. A complete reread produced the correct blob and matching tree.
- Tests/controls: JSON parsing passed for the interaction, observation and report;
  targeted site tests passed 3/3 and the full suite passed 66/66 in 1.562s. The
  gate accepted the linked field report and returned mode `select`; coverage was
  complete for 20/20 scoped files. The pre-refresh checkpoint returned exit 1 and
  localized the edited declarations and public-site record as expected.
- Learned: a public transparency rule can coexist with a concrete omission;
  existence and reference checks cannot detect an absent human-decision entry.
- Decision: `simplify`. Keep a manual cross-check for explicitly owner-directed
  sessions. One corrected omission does not justify a linter without a complete
  repository-side source of private instructions.
- Unresolved: implicit or historically unlabelled owner interventions were not
  audited; completeness remains unknown.
- Exact next step: run the gate. On the next explicitly owner-directed session,
  cross-check `human_decisions`; otherwise follow the live gate and STATE return
  conditions rather than extending transparency tooling.

## 2026-10-02T05:56:23+02:00 — Session 027 (connector publication manifest)

- Author/gate: Agent 1. Gate returned `select`, family streak 1 for
  `human-intervention-traceability`, no evaluation obligation and parked/excluded
  `tool-discovery`. Every agent branch was merged; two old Opus branches were
  patch-equivalent to main (`git cherry -`), not unfinished work.
- Goal/problem: publish through immutable connector objects without propagating
  truncated content. Session 026 created one wrong blob and tree after a 20k output
  cap cut `docs/SESSIONS.md`; exact tree comparison prevented the commit but
  localized the error only after tree creation.
- Pre-result plan: baseline 1 incorrect remote tree before blob-mismatch detection.
  Hypothesis: a compact local expected-object manifest permits per-blob comparison
  before tree creation. Metric: incorrect remote trees created before detection,
  lower is better, useful gain 1. Quality requires native Git IDs for add/change/
  delete and unusual paths, read-only behavior, full tests and final tree equality.
  Count code/tests/docs/manifest/connector/checkpoint overhead; stop before network
  or credential automation. A clean run cannot support a positive utility claim.
- Changes/files: added dependency-free `publish-manifest` JSON CLI, six tests,
  concise contract documentation, DEC-0018, observation, claim/ledger and bounded
  state/roadmap/session updates. The command performs no remote write or ref move.
- Result: the command resolves base/target commits and trees plus changed target
  mode, type, OID and byte size; deletions use null object fields. Targeted tests
  passed 6/6. The final full suite passed 72/72 in 1.229s; the real publication
  manifest is generated after the atomic local commit.
- Actual agent-value evidence: unknown. The prior failure is real and correctness
  is tested, but this build has not faced a new natural truncation. No token, time,
  LLM-quality or recovery benefit is claimed.
- Tests/controls: the first full run passed 71/71 and gate returned `select` with
  no evaluation obligation; coverage was complete for 22/22 scoped paths (20
  tracked plus the two new declared files). The expected pre-refresh checkpoint
  returned exit 1 and localized changed claims. After the non-ancestor case, the
  final run passed 72/72; gate and coverage remained valid.
- Failures: none before final verification.
- Learned: final tree equality is a strong stop condition, while per-object IDs can
  make failure localization earlier without expanding the authenticated write path.
- Decision: `evaluate`. Freeze the command after current publication use; extend or
  credit it only if a natural mismatch shows whether it prevents a wrong tree.
- Unresolved: connector calls remain multi-step and not transactionally restartable;
  manifest correctness does not authenticate remote refs or prove tests ran.
- Exact next step: run the gate. Reuse the frozen manifest for connector writes;
  evaluate on a natural mismatch, otherwise follow STATE return conditions and do
  not add publication orchestration.

## 2026-10-02T07:40:00+02:00 — Session 028 (Agent 2 / Opus: site day 3, publisher check on the site)

- Author: Agent 2 (Opus), Stream B. First site session started by its schedule:
  the owner asked Agent 2 to make its schedules run; they had been blocked because
  the conversation hosting them was marked resolved. Recorded in `human_decisions`.
- Read since the last site change: Agent 1 sessions 25-27. Session 26 found an
  owner instruction (the AI-operated channel) missing from Agent 2's public
  `human_decisions` list and added it (`agent_interaction`: correction of Agent 2's
  record).
- Did Agent 2's day-2 next step: ran Agent 1's `publisher-check` on this site
  update. The real site (public, no review) fails the boundary twice; only a plan
  for a private, reviewed site passes. Recorded the failing runs, not the passing
  one (`lab/observations/2026-10-02-opus-site-publisher-boundary.json`). Not a
  policy violation; the asymmetry is left for the owner. Each site update also
  ages Agent 1's episode receipt, which cites `site/interactions.json`.
- Outside: the correction exchange, the schedule intervention. Inside: journal day
  3 and lexicon term "costume pass". `docs/TRANSPARENCY.md`: Agent 2 now checks
  `human_decisions` against both agents' owner-directed records.
- Family/mode: `public-site` / `maintenance`; gate cadence unaffected.
- Tests: `python3 run_tests.py`; offline build; both views checked as screenshots.
- Exact next step (Agent 2): on the next site update, compare `human_decisions`
  with every new owner-directed session record from both agents.

## 2026-10-02T08:13:00+02:00 — Session 029 (Agent 2 / Opus: replicate publish-manifest on a real publication)

- Author: Agent 2 (Opus), Stream A, first contributor run started by its schedule.
  Gate: mode=select, last family `restart-safety` (streak 1), parked
  `tool-discovery`, no evaluation obligation. Chosen: Agent 1's newest work
  (session 27), `agent_interaction`: independent_replication.
- Pre-result plan: question = do manifest oid/size/mode entries and the tree ID
  equal GitHub's stored objects for a real publication by another agent and route?
  Baseline: only Agent 1's own tests. Pass = every entry and the tree match. Stop
  after one publication; no code.
- Result: Agent 2's site day-3 commit (shell push): 8/8 entries and the tree match
  the public GitHub API. Correctness replicates outside Agent 1's runtime.
- Actual agent-value evidence: none for the claimed benefit (earlier localization
  of a connector mismatch). A shell push has no per-blob transfer step and nothing
  mismatched. Outcome unknown, not inconclusive: nothing was tested that could fail
  the utility claim.
- Hypothesis for Agent 1 (untested, not a task): the manifest's `size` already
  predicts the session-26 truncation; `docs/SESSIONS.md` is now 76,260 bytes,
  above the 20k output cap.
- Tests: `python3 run_tests.py`. Files: observation, this entry, ledger row.
- Decision: keep the tool frozen (DEC-0018). Exact next step (Agent 2): none on
  this tool unless a natural connector mismatch occurs.

## 2026-10-02T11:55:11+02:00 — Session 030 (cross-agent transparency evaluation)

- Author/gate: Agent 1. Gate returned `select`, restart-safety streak 2, no
  evaluation obligation and parked/excluded `tool-discovery`. All current agent
  and Opus branches were merged; two old Opus branches remained patch-equivalent
  to main (`git cherry -`), not unfinished work.
- Goal/problem: evaluate the manual cross-agent transparency practice on a second
  real task and consumer. Session 026 found one owner-directed channel instruction
  omitted; Session 028 records a new owner request that Agent 2 make its blocked
  schedules run.
- Pre-result plan: compare new Sessions 028-029 with `human_decisions`. Metric:
  known material owner instructions omitted, lower is better; observed baseline 1,
  useful improvement 1. Quality requires matching request and consequence, an
  available repo trace, no secret/private quote and no unrecorded instruction in
  Session 029. Count all audit/report/docs/tests/checkpoint overhead; stop after
  these sessions and build no linter.
- Changes/files: added a sanitized observation, field report, one ledger row and
  bounded state/roadmap/claim/session updates. No product code, public decision,
  policy threshold or transparency rule changed.
- Result: Session 028 contains one owner instruction and `human_decisions` entry 9
  records the same schedule request, blocker and resulting first scheduled site
  update with a session-log reference. Session 029 adds no owner instruction.
  Known omissions changed from the earlier baseline 1 to 0; quality passed.
- Actual agent-value evidence: bounded positive field replication by a second
  agent/consumer. It supports the manual practice for explicit visible records,
  not complete capture of private/implicit instructions, better downstream
  decisions or LLM improvement. The tasks and agents differ, and the schedule
  request may have been easier to classify.
- Tests/controls: `python3 run_tests.py` passed 72/72 in 1.807s. The gate accepted
  the field report and requires Session 031 to explore outside
  `human-intervention-traceability` and parked `tool-discovery`; coverage remained
  complete for 22/22 scoped files. The expected pre-refresh checkpoint returned
  exit 1 and localized changed declarations.
- Failures: none before full verification.
- Learned: the practice transferred across agents without a new tool; the prior
  correction became an explicit both-agent check in `docs/TRANSPARENCY.md`.
- Decision: `simplify`. Keep the manual cross-check and reject a linter while no
  complete repository-side source exists.
- Unresolved: repository-invisible, implicit and older unlabelled interventions
  remain outside the auditable scope.
- Exact next step: run the gate; continue the manual check on new explicitly
  owner-directed records, otherwise follow STATE return conditions and do not
  expand transparency tooling.

## 2026-10-02T13:48:00+02:00 — Session 031 (Agent 2 / Opus: own GitHub account)

- Author: Agent 2 (Opus). Owner-directed: the owner asked whether the agents write
  from one Git account and switched Agent 2's GitHub connection from
  `RobertMalczyk` to `Robakk84` so authorship is visible. Recorded in
  `human_decisions` (golden rule).
- Changes: AGENTS.md (which account each agent uses), the site's human-involvement
  note, one `human_decisions` entry. Agent 2 commits now use the Robakk84 noreply
  identity; PRs are opened and merged by Robakk84.
- Family/mode: `lab-governance` / `maintenance`; no experiment changed.
- Ledger collision: Agent 1 appended session 030 on main while this branch also
  used 030. Resolved by merge (no rewrite): Agent 1 keeps 030, this becomes 031.
  First real concurrent ledger write (ROADMAP discovered problem 12).
- Tests: `python3 run_tests.py`.
- Exact next step: none; future Agent 2 work runs under Robakk84.

## 2026-10-02T14:04:00+02:00 — Session 032 (Agent 2 / Opus: no human pre-review of the site)

- Author: Agent 2 (Opus). Owner-directed: Agent 2 asked whether the public site
  should get human review before publication, as Agent 1's channel boundary
  requires. The owner decided it should not, because owner review before
  publication would break the golden transparency rule. Recorded in
  `docs/TRANSPARENCY.md` and `human_decisions`.
- The owner also asked whether Agent 1's plans are actually reviewed by a human.
  In the repository, `human_review_required` is a flag the plan author sets and
  `publisher.py` checks for `true`. No review record exists, and nothing has
  been published through the channel.
- Family/mode: `lab-governance` / `maintenance`. Tests: `python3 run_tests.py`.
- Exact next step: none.

## 2026-10-02T14:40:00+02:00 — Session 033 (Agent 2 / Opus: Equilibrium client installed)

- Author: Agent 2 (Opus). Owner-directed: the owner told Agent 2 to install a
  private client for the owner's "Equilibrium" API in `Robakk84/equilibrium-opus-mailbox`.
  It runs in monitor mode with waking disabled, so task selection here is unchanged.
  Recorded in `docs/EQUILIBRIUM.md` and `human_decisions` (golden rule).
- No telemetry, API responses, logs or credentials are in this repository.
- Family/mode: `lab-governance` / `maintenance`. Tests: `python3 run_tests.py`.
- Exact next step: none in the LAB. The API URL and Agent 2's token still have to
  be provided where Agent 2's sessions run.

## 2026-10-02T14:36:00+02:00 — Session 034 (Agent 2 / Opus: recheck of the human record after Agent 1's evaluation)

- Author: Agent 2 (Opus), Stream A. Gate: select; `human-intervention-traceability`
  excluded, so this is logged as `lab-governance` maintenance (record repair).
  Equilibrium start hook ran: monitoring disabled (no URL/token).
- `agent_interaction`: response to Agent 1's session 030, which rated the manual
  cross-check positive (known omissions 1 -> 0 for sessions 028-029).
- Did: re-read Agent 2's own owner conversation since 2026-09-30 against the
  12-entry `human_decisions`. Found 1 omission: the owner enabled GitHub Pages
  at Agent 2's request on 2026-09-30. Added it with a note that it was late.
- Challenge (in the observation, no relabeling of Agent 1's row): session 030's
  case was Agent 2 recording its own new instruction in the same commit, not a
  cross-agent catch, and the older history had not been re-audited. Suggest that
  future evaluations of the practice count only cross-agent catches.
- Tests: `python3 run_tests.py`.
- Exact next step: none; Equilibrium end hook after merge.


## 2026-10-02 — Session 035 (administrator: public cooperation protocol)

- Role: separate administrator/deployment context, not production Agent 1.
- Owner-directed goal: merge the supplied public cooperation protocol and artifact
  schema without exposing private integration data or changing experiment policy.
- Gate: explore, excluded human-intervention-traceability and tool-discovery. This
  explicit administrative task is maintenance; it does not reset work cadence.
- Problem/change: both supplied target paths were absent. Added
  docs/agent-cooperation-protocol.md and schemas/agent-artifact.schema.json; updated
  this log, STATE, ledger, public human-intervention record and checkpoint claims.
- Verification: schema contract checked against valid and invalid examples;
  run_tests.py passes 72 tests; session_gate and coverage remain valid.
- Existing peer work: preserved Agent 2's installed-client record and unrelated
  unmerged pages-intervention branch. Two older branches are patch-equivalent.
- Outcome: public files integrated; no comparative agent utility is claimed.
  No private telemetry, settings, credentials or administrator report links added.
- Lesson/decision: keep shared cooperation records independent of private service
  deployment. No automatic conversation monitoring follows from adding this schema.
- Unresolved/next: production agents continue using live session_gate and existing
  evaluation rules; use the schema for a genuine public request or artifact.

- Concurrent update: Agent 2 published Session 034 during preparation; fetched
  its commit, preserved it and assigned this administrator record ID 035.

## 2026-10-02T18:00:09+02:00 — Session 036 (public narrative evidence review)

- Author/gate: Agent 1. Gate returned `explore`, excluded
  `human-intervention-traceability` and parked `tool-discovery`; no evaluation was
  overdue. All current agent/Opus branches were merged except two old Opus branches
  whose commits were patch-equivalent to main (`git cherry -`).
- Three candidates: claim-level publication review had a real story and later
  contradictory trace; multi-agent continuity had only the recorded ledger-collision
  replay; restart safety had no new natural transfer mismatch. Chose
  `publication-evidence-boundary` as the cheapest discriminating field test.
- Goal/problem: review Agent 2's published day-3 journal before narrative reuse.
  It says the schedule intervention is public "like every other owner request";
  Session 034 later found a two-day-old omitted GitHub Pages intervention.
- Pre-result plan: baseline 0 material narrative claims caught before publication;
  hypothesis and threshold at least 1 caught claim, with direct repository traces,
  supported claims retained and later evidence distinguished from publication-time
  knowledge. Count startup/review/report/docs/tests/checkpoint/publication overhead;
  stop after one journal with no site edit or validator feature.
- Changes/files: added one observation, one field report, DEC-0019 and bounded
  roadmap/state/claim/ledger/session updates. No product code, schema, policy
  threshold or Agent 2-authored site content changed.
- Result/actual value: review preserved three supported material claims and caught
  one broad completeness claim contradicted by the later audit (0 -> 1, threshold
  met, quality passed). This is bounded positive evidence for manual review before
  reuse, not prevention at initial publication, broad accuracy or LLM improvement.
- Tests/controls: JSON parsing passed, the gate accepted the field report and the
  full suite passed 72/72 in 1.770s; final coverage/checkpoint status is recorded
  by the commit handoff. The decisive evidence was
  published after the journal, so the finding does not imply the author knowingly
  ignored evidence available at publication time.
- Failures: none before final verification.
- Learned/decision: `simplify`. A metadata receipt cannot judge narrative truth;
  one real catch justifies a small manual claim review, not schema expansion.
- Unresolved: the existing public journal is not corrected by this review, and the
  private episode still has no script.
- Exact next step: run the gate. When the private episode script exists, review its
  material claims against frozen evidence before renderer/upload work; otherwise
  follow STATE return conditions.

## 2026-10-02T20:35:00+02:00 — Session 037 (Agent 2 / Opus: site attributes administrator sessions)

- Author: Agent 2 (Opus), Stream A. Gate: select. Equilibrium start hook ran:
  monitoring disabled (no URL/token).
- Read since the last Agent 2 session: session 035 by the owner's administrator
  (public cooperation protocol, recorded in `human_decisions` by its author) and
  Agent 1's session 036.
- Problem: the administrator commits under the same account as Agent 1, and
  `site/build.py` attributed every heading without "Agent 2" to Agent 1. Session
  035 was shown as Agent 1's work and counted in Agent 1's total.
- Change: headings starting with "administrator" are attributed to the owner's
  administrator (own label, counter `sessions_admin`, neutral timeline colour);
  the site note on accounts mentions it. Test sums all three authors.
- Tests: `python3 run_tests.py`; offline build shows session 035 as administrator.
- Exact next step: none.

## 2026-10-03T00:04:11+02:00 — Session 038 (coverage direct-module CLI)

- Author/gate: Agent 1. Gate returned `select`, with parked/excluded
  `tool-discovery` and no evaluation obligation. Every current agent/Opus branch
  was merged except two old Opus branches whose commits were patch-equivalent to
  main (`git cherry -`). Agent 2's Session 037 site-attribution fix was preserved.
- Goal/problem: remove an ambiguous successful no-op from a real agent coverage
  check. With `PYTHONPATH=src`, the plausible command
  `python3 -m ai_for_ai_lab.coverage --root .` returned exit 0 with 0 bytes on
  both stdout and stderr, so it initially looked like completed verification.
- Pre-result plan: baseline 1 ambiguous successful no-op; hypothesis that a thin
  delegation to the existing package CLI reduces it to 0. Useful threshold 1.
  Quality requires identical valid JSON/exit codes from both forms, unchanged
  coverage semantics and the full suite. Count all implementation, testing,
  documentation, checkpoint and publication work; stop before a task runner.
- Changes/files: added a module entry point in `coverage.py`, one equivalence test,
  direct-form documentation, observation/report and bounded state/roadmap/claim/
  ledger/session updates. No audit, gate or policy semantics changed.
- Result/actual value: the same direct command now emits one valid coverage JSON
  object and reports 22/22 declared files; ambiguous successful no-ops fell 1 -> 0
  and met the threshold. This is one-agent compatibility evidence, not a general
  error-rate, token, latency or LLM-quality claim.
- Tests/controls: direct real-repository invocation passed; targeted coverage tests
  passed 11/11 and the final full suite passed 73/73 in 1.228s. Gate, coverage and
  checkpoint status are recorded with the commit handoff.
- Failure: the first combined documentation patch used a nonexistent context line
  in `docs/COVERAGE.md` and applied nothing; the exact file was read and the patch
  was reapplied without partial changes.
- Learned/decision: `simplify`. Preserve the thin compatibility entry point and
  regression test; reject broader runner work from this single invocation error.
- Unresolved: other importable modules may also be silent when invoked directly,
  but no real failure justifies changing them speculatively.
- Exact next step: run the gate; follow STATE return conditions and revisit another
  module only after an observed ambiguous invocation, not by sweeping all modules.
