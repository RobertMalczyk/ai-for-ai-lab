# Agent 2 memory pilot V1: protocol (declared 2026-10-22, before the first decision)

> **Superseded on 2026-10-22 at 15:36 UTC** by the owner's joint instruction (docs/owner/2026-10-22-memory-feedback-dashboard.md). That instruction says memory must support work from the start, so this protocol's random `current` arm (no memory) ends. Two decisions were logged under it: one `current` and one `memory`. Neither will be graded as a comparison. Memory stays on for every decision. Q and points stay in shadow mode, following the new contract that Agent 1 publishes.

The owner approved the POC report's V1 "as in the report" (2026-10-22). The owner then gave Agent 1 the same package and the same instruction, and said the agents now work on it separately. This file is Agent 2's protocol. It follows REPORT.md, "Decyzja wdrożeniowa". Agent 2's three suggested fixes from REVIEW-agent2.md are not part of it.

## Memory

- The memory is private to Agent 2 and stored outside this repository, in a folder Agent 1 cannot read. It holds the 22 shared cards from `memories.json` plus Agent 2's own cards, in the same schema.
- Engine: `memory.py` from this directory, unchanged. Retrieval uses `lexical`, k=3. The `utility` ranking is computed only in shadow mode.
- A lesson is added after the session where it was learned, with that session as its source. A wrong lesson is retired by setting `invalidated_at`, never deleted.
- Shared lessons reach the lab only when Agent 2 publishes them explicitly. Agent 2 does not read Agent 1's memory or its current assessment before forming its own.

## Pilot: up to 20 decisions

- **Decision unit:** one Stream A decision point. That is a candidate choice, a pre-flight verdict, a build decision or a review verdict.
- **Condition:** drawn at random before the decision and written to a private log with a timestamp. `current` means the usual process with no retrieval. `memory` means that up to 3 lessons are retrieved before deciding. In `memory`, the log also records what the shadow `utility` ranking would have returned and whether that would have changed anything.
- **Q:** updated only after an outcome is verified by later evidence, using `reward_event` from `memory.py`. Waiting or blocked outcomes leave Q unchanged. Q never chooses a task.
- **Blinding:** session records, board rows and journal entries do not mention the condition or the retrieved lessons. Those stay in the private log so a reviewer can grade decisions blind.

## Criteria, fixed now

For each decision, graded by a fresh reviewer who sees the decision record without the condition:

1. Was the decision correct by later evidence?
2. Did it repeat a known error that a card in memory already describes?
3. How many useful steps did it complete toward an outside result?
4. What did it cost (tool calls, and characters of retrieved context in `memory`)?

Lesson extraction is graded separately: is each new card backed by evidence, and is its scope right?

## End

The pilot ends after 20 decisions or at an earlier BLOCKED with evidence. The private log and the grades are then published here. This is a feasibility pilot, not a statistical test, and no result will be described as "the agent learns better".
