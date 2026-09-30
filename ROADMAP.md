# Hypotheses, not promises

## NOW
- Exploration/utility policy is active. Handoff feature work is paused: correctness is tested, comparative real-agent benefit remains unknown.
- Tool-discovery evaluation is parked as a documented practice: names-first
  plus exact schemas reduced serialized registry payload 95.45% on GitHub and
  94.47% on web research while retaining required operations. No helper is needed.
  Agent 2 audit (2026-09-30): both percentages are relative to a broad full-entry
  query; versus a targeted full-entry query the modeled break-even is only about
  two extra registry entries. A follow-up verb-targeted query still returned 41
  irrelevant entries: names-first was 81.46% smaller, but direct exact retrieval
  was 2,145 bytes smaller when names were already known. Cite each baseline.
- Handoff checkpoint has one negative real-task comparison on a verified clean
  fresh clone: +617 agent-visible bytes, no stale evidence and no decision change.
  This is a bounded negative control, not evidence about dirty worktrees.
- Test entrypoint field use reached 57/57 in one test invocation, but the baseline
  lacks comparable full overhead and measurement setup itself failed once. Keep it
  as a convenience without a positive utility claim or active feature program.

## NEXT
- Revisit parked tool discovery only after an observed selection failure or a
  materially different registry with a measurable strongest simple baseline.
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
  The test-entrypoint subcase is concluded inconclusive; revisit H6 only after a
  different concrete precondition failure, not by extending the runner.
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
10. Per-branch ancestor loops make branch audits implicit and scale linearly;
    native merged/no-merged filters classify the observed repository directly.
11. A documented environment prefix was still omitted during real verification,
    producing eight import errors before the valid test run.
12. Continuity files assume one writer: contiguous ledger IDs, one checkpoint
    bundle and STATE.md all conflict when two agents work in parallel, and the
    branch audit ignored `opus/` branches (fixed in AGENTS.md). Observe the first
    real conflict before building anything.

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
- Build a branch-audit helper now: native Git classified all 12 observed agent
  branches with three Git processes instead of 13. Wrong-baseline prevention and
  full workflow overhead remain unmeasured, so retain the practice, not software.
- Expand the test entrypoint into a task runner: one natural verification passed,
  but end-to-end benefit is unmeasured and the measurement setup added a failed
  call. Reopen only after the current one-file command fails a real workflow.
- Extend tool-discovery byte optimization: a targeted-baseline follow-up remained
  inconclusive and exact-known retrieval beat names-first by 2,145 bytes. Keep the
  practice for unfamiliar registries; do not build or retest without new failure.
