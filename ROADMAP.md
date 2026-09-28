# Hypotheses, not promises

## NOW
- Isolated edit avoids 8192 file bytes, 7913 modeled bytes after overhead; unchanged/shared/all-changed cost 273/284/288 extra bytes.

## NEXT
- Unify invalid-input handling for library and CLI: reject unavailable roots before classifying evidence, add machine-readable error codes while preserving error text, and regression-test malformed CLI arguments and JSON.

## EXPERIMENTS
- H2: a bounded context selection manifest reduces repeated reads; measure bytes
  first, tokenizer-specific token counts only when justified.
- H3: a structured tool error envelope makes retry decisions less ambiguous.
- H4: distinguishing observations from assumptions prevents assumed facts from
  becoming established facts after summarization.
- H5: a restart checkpoint with completed side effects prevents duplicate writes.
- H6: explicit tool preconditions reduce wasted calls with guessed parameters.
- H7: branch/commit-aware handoffs reduce resuming from the wrong baseline.
- H8: an explicit stop condition prevents unnecessary verification loops.

## DISCOVERED PROBLEMS
1. Handoff summaries outlive the files supporting them (current experiment).
2. A fresh session may have no local checkout (observed at first launch).
3. Large tool-discovery outputs consume context before useful work starts
   (observed here; prefer names first and a few exact descriptions).
4. Goal and next-step summaries can mix evidence and assumptions.
5. Tool failures vary in shape and omit whether retry is safe.
6. Agents can repeat external side effects after an interrupted response.
7. Git branches can carry work invisible to an agent reading only main.
8. Broad rereading and redundant tests can cost more than a small change.

## REJECTED
- Build a general vector-memory database now: no measured retrieval problem,
  unnecessary dependencies and operational costs for the first experiment.
- GUI dashboard now: agents can consume JSON and repository state directly.
- Treat an unchanged hash as truth/confidence: it only establishes byte identity.
