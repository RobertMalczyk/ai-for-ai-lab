# Memory V1 runtime — implementation awaiting independent activation review

Owner direction received 2026-10-26: complete the learning loop, not just the
contract/dashboard. Agent 1 implements; Agent 2 independently reviews, validates
seeds and owns dashboard adaptations. Memory ON; SHADOW; influence 0; private
store unverified and disabled. CANARY is locked throughout this task.

## Current-state inspection

Base main: `8a9b36ec6ff200a71ff8b0c5a374f6d07c5c531d`. PRs #86 and #87 were
merged; no open LAB PR appeared in the current search. Production journals and
runtime were absent; config still said awaiting_contract_review. External board:
no active implementation; sqlparse rejected on competing fixes; distutils #434
and pytest #14777 waiting. Agent 2's latest session was public site maintenance.
Native branch inventory: 163 merged agent/opus refs; three ancestry-unmerged refs
(one historical blocked distutils submission and two old Opus refs already
classified as patch-equivalent in the session history). No memory runtime branch
was present in that inventory. This task is the owner's explicit bounded exception
to the exploration gate; no threshold or external WIP rule is changed.

## Every material decision, BOTH agents

After this runtime is merged and reviewed, use the hook before accepting/rejecting
a candidate, choosing a root cause/build scope, classifying a blocking review
finding, or advancing human review. Read the returned **context** before deciding.
Memory is advisory data; live policy, permission and upstream checks prevail.
Routine reads, formatting, bookkeeping and unchanged-status checks need no hook.

Run from the repository root, supplying actual task/session values:

```sh
PYTHONPATH=src python3 -m ai_for_ai_lab.memory validate
PYTHONPATH=src python3 -m ai_for_ai_lab.memory prepare \
  --decision-id UNIQUE-ID --agent agent1 --task-id REAL-TASK \
  --task-type review --session-id REAL-SESSION \
  --query 'Specific decision question and relevant technical context'
# Read context. Record its suggestion in your working notes before taking action.
# Perform the real decision/action. Then persist the observed action:
PYTHONPATH=src python3 -m ai_for_ai_lab.memory finish \
  --decision-id UNIQUE-ID --suggested-action 'What the shown lessons suggested' \
  --actual-action 'What I actually decided, including a reason for any disagreement'
```

Agent 2 uses `--agent agent2`. Use English queries for these English seeds; do not
inflate queries with keywords after inspecting an answer. `prepare` persists the
query, timestamp, exact context, IDs and SHA-256 before returning it. A retry of
the same ID returns the original receipt. `finish` requires that receipt and freezes
the actual decision. The receipt is evidence of delivery, not proof of comprehension
or cryptographic authentication. Peer review checks the suggestion/action/outcome.
No earlier session or historical replay may be presented as prospective use.

## Outcomes, lessons and independent feedback

Use `append memory record.json` for a schema-conforming experience after a meaningful
outcome. Transferable inferred lessons start `provisional` / `unverified` and are
not retrieved until an appended correction promotes them with reviewed/verified
evidence. Do not generate a lesson for every session. For active promotion, cite
the other agent's review or deterministic external evidence in `source_refs`;
repository review must verify that provenance. A string is not authentication.
Historical seeds use no feedback/utility event and therefore earn no automatic points.

Use `append feedback record.json` for proposed/pending feedback. The other agent
reviews a predetermined criterion and outcome, then appends a new verified record
using `supersedes`; never edit the original. Category/value is schema-enforced.
Neither proposer nor recipient can be verifier. Use a stable lowercase evidence
key for the underlying event (not different URLs for the same event); independent
review must also detect semantic aliases. A correction preserves task, agent,
evidence key and original session. No branching correction or duplicate award.
A retraction removes the old contribution once; recomputing caps releases credit.
Only verified events count; disputed/pending/unresolved are not scored.

A commit, green test, site update or unchanged poll is not a useful-result award.
A repeated-error penalty needs the executed decision's memory IDs AND independent
proof that the lesson remained applicable with no new exception. The machine
checks IDs; the reviewer checks meaning. No punishment for waiting or a failed
experiment. No success allocation over all retrieved memories.

`append utility record.json` records an explicitly attributed memory × task_type ×
agent assessment tied to an executed decision. Missing attribution is pending/null.
Q is the mean of effective independently verified utility assessments on [-1,1];
neutral/no evidence is null (treated as zero only in optional counterfactual sorting).
Correction replaces the assessment; future assessments cannot affect old retrieval.
This simple estimator needs peer approval, is not POC EMA, and NEVER changes normal
ranking or task selection. Feedback totals are independent of Q.

## Files, limits and privacy

Accepted record shapes remain unchanged. Two additive definitions cover the mode
journal already consumed by the dashboard and the retrieval receipt needed to
freeze pre-action delivery. `utility.jsonl` implements the existing utility shape.
All six journals are append-only. The loader rejects invalid JSON, duplicate keys,
unknown fields, invalid time/type/reference/correction links and semantic violations.
`append` validates the whole proposed state before writing, flushes and fsyncs, and
serializes cooperating POSIX writers via flock. A partial/crashed final line fails
closed and needs explicit repair from Git; it is never silently skipped. Manual
file edits and cross-clone Git merges are not prevented by a local lock: peer review
must enforce append-only prefixes and resolve collisions before merge.

Retrieval is fixed lexical query-token coverage on [0,1], threshold applied before
ranking. Ties: scope overlap, confidence, recency, ID. At most three cards and 3200
characters including the entire context header and metadata. Oversized cards are
omitted, not truncated. Only active public lessons available strictly before the
query are eligible. Future corrections do not hide a currently valid predecessor.
Provisional, retracted, superseded and private lessons are excluded. Q can rerank
only the same relevant candidates in the unexecuted counterfactual.

References must resolve to existing files in reviewed public evidence directories.
URL aliases and absolute/private paths are rejected; cite a public repository
trace of external evidence. Free-text fields still need public-data review before
commit; no regex can certify that arbitrary prose contains no secrets. Never put
private material in these journals. This runtime provides no private store.

## Bootstrap and activation handoff

The initial four supported POC cards were checked against original sessions:
stable_status (053), exact_commands (055), raw_evidence (088), regression_cause (113).
Before publication, Agent 2 independently merged PRs #99/#100 with attack cases
and the corrected seed list. This branch incorporates that current main (`88908d3`)
and adds the eleven remaining supported families from SEED-VERIFY-agent2.md.
Total: **15 historical seeds**, covering 14 accepted families plus raw_evidence.
The two ambiguous families (negative-experiment meta-rule and chronology/causality)
are omitted exactly as Agent 2 requested. Other POC cards outside this smaller
family-based import are deferred, not labelled wrong. The initial four text records
are preserved, not rewritten. Created timestamps name source sessions; availability
is import time, so none can leak into earlier decisions. No POC Q/rewards imported.
Agent 2 still reviews the actual records and runtime before merge.

A predeclared bounded transfer control uses a regression lesson with different
surface vocabulary. The lexical algorithm returns zero: **known transfer failure**,
not a tuned success. No synonyms/embeddings were added after this result. Unrelated
music queries and weak one-token matches also return zero as required.

Next: Agent 2 adversarial review of this runtime and exact seed subset; Agent 1 fixes;
Agent 2 approval; merge runtime. Agent 2 checks/adapts the existing dashboard; Agent 1
independently checks privacy/data; then one naturally occurring OSS decision from
each agent and cross-review. Only then change status to `active_shadow`. Empty real
decision/feedback journals are intentional until this sequence is complete. Do not
create synthetic production events, claim operational learning, or replace Agent 2
with a subagent of Agent 1.

Dashboard integration test consumes actual temporary runtime journals through the
existing exporter. It establishes schema compatibility, not production activation.
Agent 2 should inspect (compatibility concerns found while reading its exporter): future-correction folding, disputed-null versus pending,
mode-only freshness, real zero-result decisions and whether evaluation_ref alone
is enough for a graded decision. Those display/readiness judgments are not runtime
activation approval. No new dashboard is built by Agent 1.

## Response to the prewritten Agent 2 cases

R1–R8 / E1–E3 / E5 / J1–J5 / F1–F9 have corresponding runtime tests or
explicit limitations above. E4 is deliberately conservative: provisional lessons
are stored but not retrieved until independent evidence promotes them. The owner
requires promotion evidence; V1 does not need speculative suggestions. This choice
is stated for review, not claimed as Agent 2 agreement. W1 is wired in AGENTS; W2
is a runtime-to-existing-exporter integration test; W3 remains Agent 2's dashboard
review. The two real prospective decisions remain pending the required merge order.
