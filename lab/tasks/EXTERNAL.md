# External tasks (WIP = 1)

Work mode set by the owner on 2026-10-12 (see `site/interactions.json`, human_decisions):
DISCOVER → PRE-FLIGHT → INDEPENDENT CHECK (other agent) → BUILD → ADVERSARIAL REVIEW → READY FOR HUMAN REVIEW,
or REJECTED / BLOCKED WITH EVIDENCE. Only one task is active at a time. An ACTIONABLE task is not
interrupted by the session gate. This file is the single place to see the state; keep it short.

PRE-FLIGHT questions: (1) problem still exists on current code/release; (2) no open PR solves it;
(3) no closed PR, commit or discussion shows it was already solved or rejected; (4) project policy
allows human-reviewed AI-assisted contributions; (5) an outside contributor has a real path to contribute.

## Active

None yet. Agent 2 is doing DISCOVER and PRE-FLIGHT (2026-10-12). Agent 1: if you pick a candidate
first, write it here so we don't run two.

## Waiting on an external reply

- **pytest #14775**: WAITING_EXTERNAL_RESPONSE. Fix already in open PR pytest-dev/pytest#14777 (by another
  contributor). Our added value, an async-fixture regression test and changelog wording, was posted there by the owner on
  2026-10-12 (https://github.com/pytest-dev/pytest/pull/14777#issuecomment-6121058763). No further work
  without a reply from the PR author or a maintainer.
  - External result: technical information given to an existing contributor; no competing PR.
  - Builder (Agent 2): reproduction, async trigger, test. Reviewer (Agent 1): independent reproduction and challenges.
  - Waste: several sessions of work before the existing PR #14777 was found. This is the baseline the
    PRE-FLIGHT step exists to avoid.

## Rejected at PRE-FLIGHT

| Candidate | Failed question | Evidence (2026-10-12) |
|---|---|---|
| pytest #15047 (`--fixtures` exit code 0) | 2 | Issue comment by lpyu001: "submitted a PR"; another contributor offered a fix; maintainer (bluetech) wants it as a breaking change for pytest 10.0. |
| requests #7620 (PR 5410 change missing from main) | 5 | Issue page says PRs are restricted; maintainer (nateprewitt) has no strong opinion and suggests removing the change. |
