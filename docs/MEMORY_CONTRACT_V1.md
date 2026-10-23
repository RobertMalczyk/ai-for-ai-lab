# Public memory contract v1.0.0 — pending independent review

This is the contract-first handoff requested by the owner on 2026-10-22.
It is NOT an activation or evidence of improved decisions. Agent 1 owns the
engine and data; Agent 2 owns independent review and the existing-site dashboard.
The owner authorized implementation and publication without another approval.
No schedule changes or external messages are authorized by this task.

## Artifacts and precedence

`lab/memory/records.v1.schema.json` defines public interchange records and
`lab/memory/export.v1.schema.json` defines the sanitized dashboard envelope.
`lab/memory/config.v1.json` defines identical policy for both agents, with separate
state namespaces. `memory_enabled=true` expresses the deployment target; the
explicit `implementation_status` means no engine is activated by this PR.
Timestamps are UTC RFC3339, except the explicitly date-precision config timestamp.
Full timestamp validation and the semantic invariants below are engine obligations,
not claims made by JSON Schema alone. Breaking changes require a new major version.

The owner's new contract supersedes the earlier 20-decision coupling discussion.
The existing Agent 2 protocol and POC are preserved as historical artifacts.
The earlier local administrator implementation at 7e5ae6e is not published here:
it predates this contract and contains dashboard scaffolding assigned to Agent 2.

## Persistence and retrieval

Production journals are append-only JSONL: memories, feedback, decisions, utility.
Corrections append a new record with `supersedes`; no original is overwritten.
The loader folds a correction chain at the decision timestamp, rejects cycles,
missing references and duplicate IDs, and excludes retracted/superseded lessons.
A corrected memory refers backwards to its predecessor; the derived view exposes
the successor and effective timestamp. Knowledge is available only AFTER the
source action and no earlier than `available_at`. Restart reconstructs the same
state; retries are idempotent. A matching current lesson need not exist.

Retrieve at most three lessons within 3200 characters INCLUDING serialized
metadata (a conservative fallback, explicitly not tokens). Rank by relevance,
scope, evidence and recency, with no Q in SHADOW. The eligibility phase uses an
absolute, non-normalized score on a fixed 0..1 scale and rejects candidates below
`min_relevance=0.2`; the best weak match must not become 1.0 merely because it is
best. The engine must preserve a no-match case in its tests. Record the IDs and
suggested change before action. Current policies, permissions and PR state need
fresh checks.
Memory content is data, never authority. Independent checks must be recorded
before viewing the peer's current answer. New inferred lessons are provisional;
review or a verifiable outcome is required for promotion. Historical seeds earn
no points, must be traced to original public records, and get no demo Q values.
Apply Agent 2 seed review before import: final_only is available from session 047;
append_anchor fix from 051; existing_fix pre-reproduction advice from 137.
Preserve the five wording qualifications in lab/memory-poc/SEED-CHECK-agent2.md.

## Feedback semantics required in the engine

Only verified events affect totals. The proposer cannot verify their own event;
a deterministic verifier requires evidence of the specific criterion, not merely
green CI. Strings naming a verifier are not authentication: repository access
and peer review must establish provenance. No authenticated private store exists
in this contract. Public-only startup is permitted while access remains unverified.

Fixed categories: useful_result +1; review_correction +0.5; new_finding +0.2;
activity 0; repeated_error -0.5; constraint_violation -1; unresolved null.
Pending, disputed, blocked or waiting results are not zero and are not averaged.
Repeated-error penalties require proof that the still-valid lesson was retrieved
and no new exception applies. Useful outcomes require a criterion fixed beforehand.
Mixed events need review. Do not reward creating and repairing one's own error.

Deduplicate semantic task/evidence/category, not just event IDs or URL text.
One real event cannot collect multiple positive categories. Cap total positive
credit per task/agent at +1, and discovery credit per scheduled session/agent at
+0.2. Use stable canonical evidence keys. Corrections reverse an earlier effective
contribution exactly once, then recompute caps from the remaining effective events.
Preserve pending, late outcomes, disputes, rule versions and correction history.

Utility is per memory AND context AND agent, separate from agent totals.
No attribution means null/pending, not equal credit to all retrieved cards.
Initial utility is neutral; seed/demo rewards are never production feedback.
Q update details remain subject to independent contract review. No production
Q update or CANARY activation is shipped in this contract-only change.

## Dashboard interchange and privacy

Agent 2 consumes only a sanitized build-time export derived from these journals.
Export envelope: contract_version, rule_version, generated_at, last_success_at,
source_commit, data_status (available/stale/unavailable), mode, memory_enabled,
coupling_scope, reward_influence, agents, events, memories, readiness,
shadow comparison, map links and mode history. Empty event collections mean no
data, never success. Costs are null unless measured. Separate positive/negative
totals, pending/disputed counts and rule versions. No best-agent ranking. Every
unused alternative is unobserved.

The export schema incorporates Agent 2's independently drafted shape. Available,
stale and empty exports require both agent cards, mode history, readiness evidence
and gaps, public-only memory aggregates and the shadow counterfactual. `demo=true`
is permitted only for a separately labelled fixture; production generation must
reject it. Private export data is limited to `{available:false}` with no note,
identifier, topic or path. Agent 2 may extend display-only event details without
weakening these required fields or the privacy boundary.

Only public safe source links are exported. Never export private content, topics,
paths, IDs, credentials or authenticated screenshots. Public visibility fields do
not provide access control. Private mailbox/runtime verification belongs at the
actual storage/API boundary before use, not in this public schema. Demo fixtures
must live outside production exports and must be labelled DEMO.

Agent 1 independently recomputes dashboard aggregates and checks the generated
site for private data after Agent 2 supplies its implementation. Agent 2 must
provide filters, correction details, decision-map links, freshness and empty,
pending-only, negative, corrected, duplicate, retired, changed-rule and mobile
states on the existing site. No public write button or new service.

## Prospective coupling protocol

Freeze decision correctness (later evidence or a blinded explicit rubric), known
error recurrence, useful external outcome against a prior criterion, and measured
full cost before new trials. Keep model, instructions and budget comparable;
stratify changes. Count independent task-level decisions, not steps as new trials.

Before CANARY: >=30 new graded decisions, >=10 per agent, >=3 task types; >=10
new comparable memory-without-Q versus memory-with-Q trials in isolated replay
or a predeclared experiment; >=3 more wins than losses, no critical regressions,
median FULL measured cost increase <=10%; missing cost fails that condition.
Require zero privacy leaks, duplicate awards or hard-constraint violations, and
verified rollback. These are operational thresholds, not statistical proof.

Each agent writes its own assessment before seeing the other's. Both evidence-
backed approvals enable CANARY without another owner approval. First scope is
reranking relevant admissible memories only, influence <=0.10 for ten eligible
decisions with >=3 per agent; then jointly maintain, stop or increase to <=0.25.
Task-selection coupling needs its own analogous evaluation and joint decision.
Never change cadence, budgets, permissions or WIP=1 using reward.

Either agent can restore SHADOW immediately on a material regression or safety
failure. Set influence to zero while keeping memory and history active. Re-enable
only after repair and joint approval. Missing evidence means SHADOW and normal
external work, not invented trials or extra sessions to inspect counters.

## Review handoff

Next action: Agent 2 independently reviews this version's fields and invariants,
then reports concrete blocking findings or approval against the exact PR head.
Agent 1 implements and tests restart, time boundaries, invalidations, correction,
idempotency, delayed/disputed feedback, SHADOW non-influence, bounded CANARY and
rollback against the accepted contract. Agent 2 implements the dashboard on its
own branch. This PR does not claim either implementation or review is complete.

Review response: the revision accepts all four blockers from Agent 2's review of
head `0f88c3f`: a machine export schema, category/value constraints, an absolute
relevance floor, and task type/full-cost fields. It also adds the suggested source
outcome, decision session and Decision-map identifiers. Runtime behaviour remains
an implementation acceptance test rather than a contract-only success claim.
