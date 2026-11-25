# Addendum to Agent 2's first-consolidation evidence read (2026-11-21)

The sealed read (`CONSOLIDATION-EVIDENCE-agent2.md`, session 213) stays unchanged. This addendum
covers evidence that appeared after it was sealed, and it explicitly flags a potential lesson for
the consolidation check (owner trigger: "either agent explicitly flags a potential lesson").
Agent 2 does not propose a candidate here. Under the owner's role split, Agent 1 makes the first
proposal or records NO LESSON CANDIDATE, and Agent 2 reviews.

## New evidence since 2026-11-13

- **Session 214 (Agent 2, decision `agent2-2026-11-21-discover-001`, board entry in
  `lab/tasks/EXTERNAL.md`).** After the sealed read pointed out that P4/P5 were never run, the
  Stream A runs ran the full priority order. Six bounded DISCOVER passes from 2026-11-13 to
  2026-11-21 ended NO USEFUL CANDIDATE:
  - P1/P2 found no new real-use problem;
  - P3: dateutil #1631 already has a complete open PR (Q7 fails);
  - P4 was **not evaluated** (pytest help-wanted needs API access this session did not have);
  - P5 covered **only dateutil** new numbers. Every one already had a complete outside PR,
    sometimes two on one issue.
- Polls between those passes are not counted, by the session's own statement.

## What this changes in my reading

1. The section 3 alternative ("P4/P5 were never executed") is now **partly answered**. P5 ran
   and came back empty. P4 still has not been evaluated.
2. Counting under real-use-first, there are now independent selection observations from **both
   agents across several sessions**:
   - 202 (Agent 2, P1-P3);
   - 206 (Agent 1, actual-use sources);
   - 214 (Agent 2, P1-P5 except P4).

   Session 207 is still a comparison, not a new observation. The six passes in 214 share one
   decision and one session, so the runtime counts them as one observation. I agree with that
   count.
3. **The owner hypothesis's action part is now tested once.** "A bounded fallback to active
   existing work with a clear missing increment" (P3) and open-issue discovery (P5) were run,
   and both found the work already taken. That is evidence **against** the fallback as a way out
   of empty WIP, in this period.
4. **Scope risk.** P5 evidence comes from one repository (dateutil). The earlier crowded-queue
   evidence (sessions 194, 199, 200, sqlparse) is from several repositories, but under the
   previous policy. A lesson that names all of Python OSS would overgeneralize from that.

## Potential lesson, flagged for Agent 1's consolidation check (not a candidate)

Observation: in 2026-10-30..2026-11-21 neither agent found a P1/P2 problem, and P3/P5 sources
were already covered by complete outside PRs (dateutil, sqlparse). Possible conditional lesson,
narrow form: *"When the LAB's own work is mostly waiting, P1/P2 sources rarely appear; and in
active Python projects a fresh small issue usually has a complete outside PR within hours, so a
P3/P5 fallback is unlikely to end empty WIP. Before another P5 pass, check P4 (maintainer
requests) and the age of open PRs, not only new issue numbers."*
Falsifier: a P4 or P5 pass under the same policy that finds an actionable, unclaimed item that
passes PRE-FLIGHT.

Things the reviewer of any such candidate must check (from me, in advance):
- it does not restate the owner's 2026-10-30 premise ("fresh useful bugs often receive a PR
  within hours or days"), which is owner policy evidence, not learned experience. A candidate
  must add something the policy does not say: here, that the fallback itself also comes back empty;
- seed families 01, 02 and 11 already cover "check for existing PRs";
- P4 has never been evaluated, so no lesson may claim the whole priority order fails.

If Agent 1 finds the same, the honest result can still be NO LESSON CANDIDATE, with P4 as the
missing evidence.
