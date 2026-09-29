# Hypotheses, not promises

## NOW
- Exploration/utility policy is active. Handoff feature work is paused: correctness is tested, comparative real-agent benefit remains unknown.
- Tool-discovery evaluation is concluded as a documented practice: names-first
  plus exact schemas reduced serialized registry payload 95.45% on GitHub and
  94.47% on web research while retaining required operations. No helper is needed.
- Handoff checkpoint has one negative real-task comparison on a verified clean
  fresh clone: +617 agent-visible bytes, no stale evidence and no decision change.
  This is a bounded negative control, not evidence about dirty worktrees.

## NEXT
- Revisit tool discovery only after an observed practice failure, a materially
  different registry, or evidence that manual selection itself is the bottleneck.
- Before more handoff features: evaluate only on a naturally dirty or long-lived
  resumed worktree where stale evidence is plausible. A second negative or
  inconclusive evaluation parks the family.

## EXPERIMENTS
- H1: evidence-aware checkpoint improves resume work. It failed the clean
  fresh-clone condition; the remaining bounded hypothesis is dirty/long-lived
  resume, where Git identity alone may not expose claim-level staleness.
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
   (observed; mitigated by names first and selected exact schemas).
4. Goal and next-step summaries can mix evidence and assumptions.
5. Tool failures vary in shape and omit whether retry is safe.
6. Agents can repeat external side effects after an interrupted response.
7. Git branches can carry work invisible to an agent reading only main.
8. Broad rereading and redundant tests can cost more than a small change.
9. One-time next-session commands become stale when duplicated in stable policy.

## REJECTED
- Build a general vector-memory database now: no measured retrieval problem,
  unnecessary dependencies and operational costs for the first experiment.
- GUI dashboard now: agents can consume JSON and repository state directly.
- Treat an unchanged hash as truth/confidence: it only establishes byte identity.
- Claim checkpoint utility from canonical clean-clone self-use: the first field
  comparison added context and found nothing beyond Git identity/status.
- Duplicate current gate state in policy prose: derive it from the ledger and keep
  historical session-specific conclusions in the session log.
- Build a tool-discovery helper now: two heterogeneous field tasks support the
  names-first/exact-second practice, and direct registry filtering already works.
