# Memory V1 activation: Agent 2's starting finding and attack cases (2026-10-26)

Owner direction of 2026-10-26 12:39Z, "Complete and activate Memory V1", sent to both agents.
Agent 2 wrote this file from current `main` (`8a9b36e`) before any Agent 1 runtime existed,
so that the cases stay independent of the implementation.

## 1. Factual finding on current main

| Item | State on `8a9b36e` |
|---|---|
| Contract | `docs/MEMORY_CONTRACT_V1.md`, merged in #86. |
| Record schema | `lab/memory/records.v1.schema.json`: `memory`, `decision`, `feedback`, `utility`, `cost`. Memory `visibility` allows only `public`. |
| Export schema | `lab/memory/export.v1.schema.json`, byte-identical to the dashboard copy merged in #87. |
| Config | `lab/memory/config.v1.json`: memory on, `reward_mode: shadow`, `reward_influence: 0.0`, `coupling_scope: none`, `private_store_status: unverified_not_enabled`, `min_relevance: 0.2` on an absolute 0 to 1 scale, max 3 lessons, 3200 characters. **`implementation_status` is still `awaiting_contract_review`**, which is stale: the contract was approved and merged on 2026-10-23. |
| Production journals | **None.** `lab/memory/` holds only the config and two schemas. No `memories.jsonl`, `decisions.jsonl`, `feedback.jsonl` or `mode_history.jsonl`. |
| Runtime | **None.** No memory module under `src/ai_for_ai_lab/`. The only retrieval code is the POC in `lab/memory-poc/memory.py`, whose scores are normalised so the best match is always 1.0. |
| Startup workflow | `AGENTS.md` does not mention memory retrieval. Nothing makes either agent call a memory hook before a decision. |
| Dashboard | `site/memory.html`, fed by `site/memory_export.py`. It reads production journals if present and shows "no data yet" today. |
| Open PRs | None. Agent 1 branches on the remote are merged pre-flight rounds. |
| External WIP | None active. distutils #434 and pytest #14777 wait on upstream (heads `0d08e50`, `b98af3e`). |

The owner's description of the gap matches the repository.

## 2. Attack cases for Agent 1's runtime

Each case names an input and what must hold. They extend `lab/memory-poc/ADVERSARIAL-CASES-agent2.md`
(2026-10-22). Agent 2 will run them against the runtime branch and return
**APPROVED FOR ACTIVE SHADOW** or **CHANGES REQUIRED**.

### Retrieval

| # | Input | Must hold |
|---|---|---|
| R1 | Off-topic query: "choose a colour palette for the site header" against the seed | Zero memories, and the block reads `MEMORY V1: no relevant lesson found.` |
| R2 | Partial overlap, wrong meaning: "merge the dashboard branch after review" | No lesson about upstream PR state (`closed` versus `merged`) unless its score passes the absolute floor on its own. Agent 2 will report the actual scores. |
| R3 | Different vocabulary, same lesson: "a patch for this crash already sits in someone else's open change request" | Should reach the existing-PR lesson. A miss is recorded as a lexical-retrieval failure. No tuning after seeing it. |
| R4 | One query that matches four lessons | At most three are returned. |
| R5 | Three matches whose block exceeds 3200 characters with metadata | Fewer lessons; no lesson cut mid-text; the count includes ids, scores and exceptions. |
| R6 | Same query, Q set to extremes (0 and 1) | Identical `memory_ids` and order in SHADOW. |
| R7 | Q very high on a lesson below `min_relevance` | Never in `memory_ids`, and never in `shadow_memory_ids`. |
| R8 | Score of the single best weak match | Reported raw, never rescaled to 1.0. |

### Eligibility and chronology

| # | Input | Must hold |
|---|---|---|
| E1 | Lesson with `available_at` after the decision's `occurred_at` | Not retrieved. |
| E2 | Lesson superseded by a correction effective at T | Original before T; only the correction after T; both records stay. |
| E3 | Retracted lesson with the highest Q | Never retrieved after the retraction is effective. |
| E4 | `provisional` lesson | Agent 2 expects it retrievable but labelled provisional. The runtime must state its choice, and the decision block must show the status. |
| E5 | Record with `visibility` other than `public` | Rejected at load. Production retrieval never reads a private store. |

### Records and restart

| # | Input | Must hold |
|---|---|---|
| J1 | Malformed JSONL line, unknown enum, missing required field | Load fails with the file and line. No partial retrieval. |
| J2 | Same decision appended twice after a restart | Rejected or deduplicated by `decision_id`. |
| J3 | Journal edited in place (an old line changed) | Detectable. Agent 2 will check whether the runtime or tests guard this; if not, it is a review note, not a blocker. |
| J4 | Restart between decision and feedback | Feedback attaches to the right decision exactly once. |
| J5 | `source_refs` with an absolute local path, `~`, `..` or a URL with credentials | Rejected at write, or dropped by the public export (dashboard filter from #87). |

### Feedback

| # | Input | Must hold |
|---|---|---|
| F1 | `category: useful_result` with `value: 0.5` | Rejected. All seven category/value pairs are enforced. |
| F2 | `verifier` equal to `agent` or `proposer` | Rejected. |
| F3 | Pending, disputed or unresolved event | Not in any aggregate or Q, and not shown as 0. |
| F4 | Same `evidence_key` twice under new ids | Counted once. |
| F5 | Verified event then retracted, replayed after restart | Reversed exactly once. |
| F6 | Three positive verified events on one task | Positive total capped per the contract. |
| F7 | `historical_seed: true` memory | No points from import. Q starts neutral. No POC `q_initial` is copied. |
| F8 | Decision that retrieved three memories and succeeded | No equal split of utility. Utility stays `null` unless an event names the memory. |
| F9 | Negative experiment with a useful lesson | `source_outcome: negative` and lesson usefulness are separate fields and do not cancel. |

### Workflow and dashboard

| # | Input | Must hold |
|---|---|---|
| W1 | Material decision in the next session | `AGENTS.md` (or the startup workflow) names the hook and when to call it. A material decision without a decision record is visible. |
| W2 | Real journals with one decision and no feedback | Dashboard shows SHADOW, memory on, influence 0, real counts and the latest data timestamp; not "no data yet"; DEMO stays separate. |
| W3 | Export built from a journal older than the last decision | The page shows the export time, so a stale export is visible. |

## 3. Seed verification

Agent 2's independent check of the historical seed is in `SEED-VERIFY-agent2.md`.
It compares the owner's 16 lesson families and the 22 POC cards with their source sessions on main.
