# Seed check: the 22 POC lessons against the original records (Agent 2, 2026-10-22)

The owner's instruction of 2026-10-22, section 4, says to verify the POC seed against the original records before importing it as `historical_seed`. Agent 2 checked each card in `memories.json` against its `source_heading` in `docs/SESSIONS.md`.

The check had two steps.

- **Mechanical:** all 22 headings exist, and each heading's session number matches the card's `source_session`.
- **Reading:** a fresh helper agent with no stake in the POC read each source section and judged the card.

## Result: 14 supported, 8 partial, 0 wrong

Three partial cards use facts from a later session than their `source_session`. That is time leakage: retrieval would offer the lesson before the lab actually knew it.

| Card | Problem | Fix before import |
|---|---|---|
| `final_only` (046) | The multi-agent caveat comes from Session 047. | Keep only 046's byte result, or move `source_session` to 047. |
| `append_anchor` (049) | 049 records the misplaced insert. The unique-anchor fix first appears in Session 051. | Split the card: the failure at 049 and the fix at 051. |
| `existing_fix` (135) | "Check before any reproduction" comes from Session 137, after a reproduction was wasted. | Move to 137, or keep only 135's "rejected at question 2" part. |

Five cards add small wording that is not in their source:

| Card | Added wording |
|---|---|
| `continuity_window` (049) | "administrator" sections; the window held only peer sessions. |
| `compact_output` (082) | "noisy" first appears in 116. |
| `waiting` (134) | "bounded" and "submission is not acceptance". |
| `peer_continuity` (047) | Drops "or the administrator". |
| `project_policy` (073) | Adds a "do not generalize" hedge. |

These five do not change when a lesson becomes available. They can be imported with a note.

## Consequence

The POC's 19/20 retrieval result used these cards unchanged. Three of the 20 cases may have been helped by leaked wording: C051 (`append_anchor`), C148 and C150 (`existing_fix`). This does not overturn the POC. It does mean `historical_seed` should be imported with the three fixes above, and each card's `created_at` and `source_refs` should name the session where its full content first existed.
