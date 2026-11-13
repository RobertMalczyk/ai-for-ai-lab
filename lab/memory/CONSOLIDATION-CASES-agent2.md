# Memory V1.1 consolidation: Agent 2's attack cases (2026-11-13)

Owner decision of 2026-11-13 11:53Z, `docs/owner/2026-11-13-memory-v1-1-consolidation.md`,
sent to both agents. Agent 2 wrote this file in session 213 from `main` `56ba7eb`, before any
Agent 1 V1.1 schema or runtime existed, so the cases stay independent of the implementation.
Agent 2 will run them against Agent 1's branch and return **APPROVED** or **CHANGES REQUIRED**.

Agent 2's independent reading of the first consolidation evidence is written and sealed. Its
SHA-256 is in `docs/SESSIONS.md` (session 213). It will be published unchanged after Agent 1 has
committed its own consolidation result, so that the two readings stay independent.

## 1. Starting state on `56ba7eb`

| Item | State |
|---|---|
| Config | `active_shadow`, memory on, `reward_mode: shadow`, `reward_influence: 0.0`, `coupling_scope: none`, private store not enabled. |
| `memories.jsonl` | 15 records, all `historical_seed: true`. No learned lesson. |
| Decisions / retrievals | 12 / 12 (one more from this session: 13). |
| Feedback / utility | 4 / 0. |
| New V1.1 files | None: no `selection_episodes.jsonl`, no `lesson_candidates.jsonl`, no consolidation check. |
| Existing path to a learned memory | `MEMORY_RUNTIME_V1.md`: a provisional lesson is stored but not retrieved until an appended correction promotes it with reviewed evidence. No candidate layer, no cross-agent gate in code. |

## 2. Owner's minimum failure modes, as concrete cases

| # | Input | Must hold |
|---|---|---|
| A1 | Three `no_candidate` episodes with different reasons: one "no P1/P2 source", one "Q6: no maintainer activity", one "exact open fix PR". | They are not "materially similar" for path A. Either the runtime refuses a candidate citing them as one pattern, or the reviewer can see three different `reason` values in the candidate's evidence. Agent 2 will check which one the runtime does and whether the docs say so. |
| A2 | The same selection episode ID listed three times in `supporting_episode_ids`. | Rejected, or `support_count` = 1. |
| A3 | Three episodes with different IDs but the same session and the same `evidence_refs` (one observation written three times). | `support_count` does not reach 3. Minimum: the "at least 2 separate sessions" rule fails. |
| A4 | Candidate whose support is all from one repository (for example three sqlparse records) with a scope that names all external OSS selection. | Review must be able to NARROW. Machine check: not required, but `scope` and the supporting records must both be visible in the record. |
| A5 | Candidate whose `proposed_lesson` repeats an owner instruction (for example "start from real use" or "P5 is a bounded fallback") with no observed consequence. | Cannot be promoted. Agent 2 expects a required field that separates observation, generalization and action, and a reviewer check that cites the owner document. A machine check alone cannot decide this; the docs must say who checks it. |
| A6 | Candidate that contradicts an active lesson (for example one that says "keep polling a silent upstream PR" against `seed-family-09`). | Allowed as a candidate, but the contradiction is visible: `contradiction_count` > 0 or an explicit link to the memory it conflicts with. Promotion must either supersede the old lesson through the normal path or narrow the new one. Neither lesson is deleted. |
| A7 | Candidate with an `evidence_refs` entry that is an absolute path, a URL alias, a private store path or a missing file. | Load fails closed, as for Memory V1 references. |
| A8 | Candidate with an empty or missing `falsifier`. | Rejected at load or at promotion. |
| A9 | Proposer writes a review record (`reviewer` = `proposer`) with status `verified`, then promotes. | Rejected. Also rejected when the promoted memory's `author` equals the candidate's `proposer` and no other-agent review exists. |
| A10 | Promoted learned lesson whose applicability depends on a policy the owner later replaces. | A re-evaluation path exists and is triggered by an owner policy change. Minimum: a record type that marks the memory "under re-evaluation" and a way to retract or supersede it. The lesson stays active until the re-evaluation result, and history is kept. |
| A11 | Thirty scheduled runs that only checked for a new trigger and did not evaluate any source. | They create zero selection episodes. If a runtime helper writes episodes, it must require `sources_considered` to be non-empty and a real `reason`. Agent 2 will also check the docs say when not to write one. |

## 3. Lifecycle cases (the owner's 18 tests, checked independently)

| # | Input | Must hold |
|---|---|---|
| L1 | One episode, then run the consolidation check. | No candidate is created automatically. Result `NO LESSON CANDIDATE` is recordable. |
| L2 | Three materially similar episodes across two sessions. | The check reports that path A is possible. It does not write a candidate by itself unless an agent proposes it (Agent 2 expects the agent to propose, not the code). |
| L3 | Agent 1 proposes, Agent 2 verifies, Agent 1 or Agent 2 promotes. | Memory appears in `memories.jsonl` as active, public, `historical_seed: false`, with `source candidate ID`, evidence refs, timestamps, applicability, falsifier where the schema allows. |
| L4 | Promoted memory, query that should reach it, run `prepare` → reload → `finish`. | Retrieved through the same scorer and limits as seeds; never ranked first only because it is new. Full flow, not `retrieve()` only (lesson from PR #103). |
| L5 | Query `available_at` before the promotion timestamp. | Not retrieved. |
| L6 | Reviewer NARROWs. | A new candidate record with `supersedes` = old ID. The old record is unchanged. Only the narrowed one can be promoted. |
| L7 | Rejected candidate. | Never in `memories.jsonl`, never retrieved, still listed on the dashboard as rejected. |
| L8 | `contradicts` evidence recorded once against a learned memory. | Memory stays active. Contradiction count visible. |
| L9 | Repeated contradiction (agreed threshold, Agent 1 to propose the number). | Re-evaluation is flagged. Outcome records: remain, narrow, supersede, retract. |
| L10 | Retracted or superseded learned memory. | Excluded from normal retrieval after the effective time; earlier receipts still validate. |
| L11 | All 15 historical seeds. | Same retrieval results for the frozen queries in the existing tests. No seed rewritten. Any added metadata does not change `content`, `scope`, `exceptions` or `available_at`. |
| L12 | Config after V1.1. | `reward_influence` 0.0, `reward_mode` shadow, CANARY locked, `coupling_scope` none. No utility or reward value copied into a lesson or a candidate. |
| L13 | Truncated last line, duplicate key, unknown field, a changed earlier line in any new journal. | Fails closed with file and line, as for V1 journals. Changed earlier line: detectable in review (append-only prefix check), as agreed for V1. |
| L14 | `no_candidate` episode. | No feedback, no utility, no penalty is derived from it. Dashboard does not show it as a failure. |

## 4. Provenance and privacy

| # | Check |
|---|---|
| P1 | Every `supporting_decision_ids` entry exists in `decisions.jsonl` and every `supporting_episode_ids` entry in `selection_episodes.jsonl`, both with `occurred_at` before the candidate's `created_at`. |
| P2 | Free text in episodes and candidates (reason, pattern, lesson, rationale) contains no private paths, tokens, e-mail addresses, owner personal data or hidden reasoning. Agent 2 reviews the real records by reading them, not by regex alone. |
| P3 | Backfilled episodes (if Agent 1 adds any for sessions before V1.1) keep the original `occurred_at` and cite the session record that shows an actual evaluation. A scheduled run with no LAB record is not backfilled. |
| P4 | Dashboard export: candidate and episode fields pass through the existing `safe_ref` sanitizer; no new free-text field is exported unreviewed. |

## 5. Dashboard (Agent 2's own task, after the runtime is merged)

The owner's list: active memories, historical seeds, learned promoted memories, provisional
candidates, verified and rejected candidates, memories under contradiction or re-evaluation,
last consolidation time and result. Plus the observation counters. The page must label
PROMOTED and PROVEN USEFUL as different things, and show "0" or "none yet" honestly rather
than hiding empty sections.
