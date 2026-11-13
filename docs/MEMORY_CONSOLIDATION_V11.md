# Memory V1.1 — implementation awaiting independent review

Owner authority: `docs/owner/2026-11-13-memory-v11-consolidation.md`.
The V1 base remains active_shadow, public only, SHADOW/0/none. V1.1 is on a
review branch. No learned lesson or useful learning outcome is claimed.
Agent 1 owns this runtime; the existing Agent 2 owns independent adversarial
review and dashboard adaptation. Do not substitute another assistant for that peer.

## Minimal additive contract

All definitions extend `records.v1.schema.json` (base record/rule version stays
1.0.0; V1 readers ignore additive optional memory fields). New strict JSONL journals:

| File | Purpose | Identity |
|---|---|---|
| selection_episodes.jsonl | A real task-selection evaluation, no trivial poll | episode_id |
| lesson_candidates.jsonl | Hypothesis, cross-review, promotion receipts | candidate_id |
| consolidations.jsonl | Inputs and result of a completed check | consolidation_id |
| memory_evidence.jsonl | supports / contradicts / neutral | evidence_id |
| reevaluations.jsonl | Pending or peer-reviewed applicability decision | reevaluation_id |

All use occurred_at and supersedes; no in-place correction, fork or missing parent.
Creation and review timestamps remain distinct. For a correction use a new ID,
with supersedes naming the current leaf. A candidate's IDs identify revisions;
the promoted memory ID remains stable for that version of the lesson. Narrowing
creates another provisional candidate revision and requires fresh cross-review.
Verified/promoted revisions cannot change lesson text, scope or support.

Episode observation_key identifies an underlying observation, not a scheduler run.
Use `decision:<decision_id>` for an episode already represented by a decision.
Independent decisions in the same agent/session/task count once. Other semantic
aliases, common mechanism, conditional wording, private text and counterexamples
require the peer's actual review; strings and checklist booleans do not authenticate
an author or prove truth. Existing public-reference validation remains in force.

## Use

Before a material decision retain the V1 prepare/finish hook. At session start and
after material work run:

```sh
PYTHONPATH=src python3 -m ai_for_ai_lab.memory consolidation-check
PYTHONPATH=src python3 -m ai_for_ai_lab.memory consolidation-check --explicit
PYTHONPATH=src python3 -m ai_for_ai_lab.memory append episode /tmp/public-episode.json
PYTHONPATH=src python3 -m ai_for_ai_lab.memory append candidate /tmp/public-candidate.json
PYTHONPATH=src python3 -m ai_for_ai_lab.memory promote --candidate-id VERIFIED-REVISION --memory-id STABLE-ID --actor agent2
PYTHONPATH=src python3 -m ai_for_ai_lab.memory consolidation-metrics
```

The trigger reports due for five new decisions, 72 hours with new relevant
experience, three distinct episode observations sharing a pattern_key, or an
explicit flag. It never synthesizes candidates. Repeated outcomes with different
causes are only a prompt to examine evidence. A completed consolidation receipt
lists inspected inputs, rationale, public references and either CANDIDATE PROPOSED
or NO LESSON CANDIDATE. Do not record a completed check merely by running the trigger.

The proposer records supporting IDs, mechanism, conditional lesson, applicability,
exceptions, realistic falsifier, alternative explanations, novelty and evidence.
At least three observations/two sessions, two agents' independent observations,
or a narrowly justified strong single event is required. Review must establish
all eight checklist judgments before verification. REQUEST MORE EVIDENCE leaves
provisional; NARROW appends a provisional successor; REJECT appends rejected.
Owner policy is authority, never sufficient experience. Review must check whether
an existing seed already says the same thing or contradicts the proposal.

Only the independent reviewer may promote. It writes the exact verified text to
memories.jsonl with source_candidate_id, applicability_conditions, falsifier,
promoted_at and promoted_by, then appends a promoted candidate receipt. An
interruption between those two writes is recoverable by rerunning the same IDs;
the memory is authoritative and metrics count it even before receipt completion.
Each append is locked/validated/fsynced; this is not a cross-file transaction.
Cooperating writers and reviewed Git merges are assumed, as in V1. A concurrent
review changing the candidate can reject completion and needs explicit resolution.

## Contradiction and applicability

Append memory_evidence with a stable evidence_key. One significant contradiction
or two distinct contradictions after the last completed review marks re-evaluation
due in metrics. It never deletes or deactivates a lesson. Explicit policy/external
change, irrelevant retrieval or applicability change creates a pending reevaluation.
Both agents must inspect these conditions when using lessons; the runtime cannot
infer changes in external policy from prose or watch the internet.

A peer-reviewed reevaluation can remain_active or retract. Retraction excludes the
lesson only after its effective occurred_at, keeping historical retrieval replay
valid. Narrow/supersede first requires promotion of a freshly verified replacement
candidate whose replaces_memory_id points to the predecessor. Then record the
reevaluation linking that replacement. History remains append-only.

## Ranking, utility and dashboard handoff

No relevance formula, threshold, Q ranking, feedback category or reward influence
changes. Promoted lessons use the existing retrieval cards; extra metadata is not
copied into context. No novelty boost is added (V1's existing recency tie-break stays).
A retrieval is not utility. Existing independent utility records remain the only
source of positive-utility counts. The metrics command exposes lifecycle counts,
re-evaluation flags and last consolidation time/result for Agent 2's exporter.
Agent 2 must distinguish PROMOTED from PROVEN USEFUL and apply the existing public
export privacy boundary. Dashboard work is not implemented or claimed here.

## First real case: inspection, not promotion

Base inspected: 56ba7eb. Sources: sessions 206/207 and 208–212 in docs/SESSIONS.md;
12 preexisting decisions and their frozen retrievals; all 15 seeds; Agent 2 source
list and active-shadow verification; site journals 2026-11-04 through 2026-11-12.
Session 206 combines an October 30 decision with November 4 resumed publication;
those are not two selection observations. Session 207 is a comparison of both lists,
so overlapping sources cannot count as wholly independent cases. Sessions 208–212
are site maintenance and waiting reports, not documented fresh selection evaluations.
The decision record in 207 rejects sqlparse on Q6, whereas the later session prose
also says upstream fixed it and ended maintenance: distinguish dated reasons.

Potential alternatives remain: no new real problem occurred; observed software
coverage was too narrow; Q6 constrained feasibility; a short interval cannot show
waiting's diminishing returns; scheduler cadence is not evidence independence.
Fallback was already authorized by owner policy. Repeating that permission adds
no learned information. No synthetic/backfilled episodes or candidate are written.
A narrow observation-coverage lesson might merit investigation, but the supplied
full hypothesis is not established by this inspection.

Delivery gate: independent Agent 2 runtime review, fixes, dashboard adaptation,
then each agent performs the first real consolidation and cross-reviews any actual
candidate. Until then production consolidation/candidate journals stay empty.
Technical tests demonstrate lifecycle behavior only. Learning from experience and
positive utility require the later natural retrieval/decision/outcome chain.
