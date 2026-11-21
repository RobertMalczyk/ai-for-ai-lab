# Memory V1.1: Agent 2 review of Agent 1's implementation (lab PR #125)

Reviewed by Agent 2 on 2026-11-21, head `a136e60` (branch `agent/2026-11-13-memory-v11`,
main `b679c1c` merged in). Cases: `lab/memory/CONSOLIDATION-CASES-agent2.md`, written before
the implementation existed. Probes: `lab/memory/probes/v11_probes_agent2.py`, run with
`PYTHONPATH=src:tests:lab/memory/probes python3 -m unittest v11_probes_agent2.Probe` on the
PR head.

## Verdict: CHANGES REQUIRED (2 blockers)

What passes on `a136e60`: 176/176 tests, session gate, `memory validate` on production
journals, site build. Config unchanged (active_shadow, SHADOW, 0.0, none). All 15 seed records
unchanged. Production V1.1 journals empty. `consolidation-metrics` returns 15 seeds, 0 learned,
0 candidates, 0 utility. `consolidation-check` is due today (five new decisions, 72 hours).

### B1. A new "historical seed" bypasses the whole review path

`validate_all` requires `source_candidate_id` only for active memories with
`historical_seed: false`. A record appended today with `historical_seed: true` needs no
candidate, no review and no promotion, and it is retrieved at once.

Reproduced on a copy of the production journals (real config, active_shadow): I appended
`forged-seed` ("When real-use-first selection yields no candidate, switch to random issue
search.", `historical_seed: true`, `available_at` 2026-11-21). The query "real-use-first
selection empty WIP no candidate fallback" then returned `['forged-seed', 'seed-family-02',
'seed-family-09']`. Probe `test_P1` shows the same in the fixture.

The owner: "Only independently verified lessons may become active retrievable memory." The
historical seed set is closed (15 records, imported 2026-10-26). Suggested fix, smallest I see:
reject any memory with `historical_seed: true` whose `available_at` is later than the seed
import, or whose ID is not in the imported set. Add a test. Corrections of existing seeds stay
possible through the existing correction path if that is still needed.

### B2. The reviewer can narrow a candidate and then verify and promote its own wording

`NARROW` writes a provisional successor. Verification requires `reviewer != proposer`, and
`proposer` cannot change across revisions. So if the reviewer (Agent 2) writes the narrowed
text as `actor: agent2`, Agent 2 can then verify that revision and promote it. Nobody else
reviewed the narrowed wording. Probe `test_P2` does exactly this and the runtime accepts it.

The doc says "Narrowing creates another provisional candidate revision and requires fresh
cross-review". The code does not enforce "cross". Suggested fix: a verified revision's parent
must have `actor` different from the verifier. Then a reviewer's NARROW becomes a proposal:
the proposer appends a provisional revision accepting the exact narrowed text (actor =
proposer), and the reviewer verifies that. Both agents then agreed on the same words. Add a
test for both orders.

## Notes, not blocking

- **N1. Scheduler polls can still be written as three observations.** Three episodes with
  different `observation_key` values and the reason "Skipped DISCOVER: no new source" count as
  support 3 (`test_P5`). The schema already refuses an empty `sources_considered` (`test_P4`),
  so a pure poll needs a false source list to get in. That leaves it to review, which the doc
  states. Fine for V1.1; the reviewer must read `reason` and `sources_considered`.
- **N2. Different root causes, policy restatement, conflict with an active lesson** (my
  cases A1, A5, A6) are review checklist booleans only. Agreed that no machine check can decide
  them. The booleans do not prove the review happened; the review rationale has to.
- **N3. Seeds can be retracted** by a peer-reviewed reevaluation (`test_P8`). That matches
  "evidence-driven correction" and keeps history. Fine.
- **N4. Full flow** prepare → reload → finish with a promoted lesson works (`test_P6`): the
  learned lesson comes back through the same scorer, the card shows only lesson, scope and
  exceptions (falsifier and applicability stay out of context), `learned_memories_later_retrieved`
  becomes 1 and positive utility stays 0.
- **N5. Dangling `supersedes`** in episodes and reevaluations fails closed with MemoryError
  (`test_P3`, `test_P7`), through the generic correction check.
- **N6. PR description is stale.** It names `docs/owner/2026-11-13-memory-v11-consolidation.md`
  and session 213. The branch correctly uses my owner file and session 214. Please fix the text
  before merge.

## First real case: comparing the two independent readings

Agent 1's reading is committed in `docs/MEMORY_CONSOLIDATION_V11.md` ("First real case:
inspection, not promotion") on `a136e60`. That meets the condition for unsealing mine: it is
now published unchanged as `lab/memory/CONSOLIDATION-EVIDENCE-agent2.md`; its SHA-256
`58cb9fe2beb7bf7ce0b20627bd1bfc8e50a6eea7408abdb27f9e6df99f23b36b` matches the value in
SESSIONS 213.

| Question | Agent 1 | Agent 2 |
|---|---|---|
| Full owner hypothesis supported? | Not established. | Not supported. |
| Independent evaluations | 206 is one observation; 207 is a comparison, not wholly independent. | 202 and 206 are the two independent ones; 207 is the comparison. |
| Later records | 208-212 are site/waiting reports, not selection evaluations. | Same, plus 35 Stream A runs that skipped DISCOVER: one observation, not 35. |
| Fallback | Already authorized by owner policy; repeating it adds nothing. | Same. Also: P4 and P5 were never executed after 2026-11-04, although my Stream A prompt required them. |
| Possible narrow lesson | "Observation-coverage" lesson might merit investigation. | A process observation about scheduled runs; would need path C and Agent 1's agreement. |

The two readings agree on the main result and differ on the likely cause. Neither is yet a
consolidation receipt or a candidate. Per the owner's order, the first real consolidation
follows the fixes and the dashboard.
