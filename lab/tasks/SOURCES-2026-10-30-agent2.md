# Agent 2: independent source list under the 2026-10-30 owner decision

Written by Agent 2 in session 202, before reading any Agent 1 list (none existed on
main `509bf7a`). Owner decision: `docs/owner/2026-10-30-external-task-selection.md`.
Agent 1 writes its own list without reading this one first, then the two are compared
and at most ONE candidate is chosen.

## Priority 1: a problem met during real LAB work

**None found.** The LAB code uses the Python standard library only, and its CI uses
GitHub's first-party Pages actions. The real problems we hit in the last weeks were in
our own process, not in outside software. Example: summaries of GitHub issue pages
left out maintainer comments and PR state (sqlparse, dateutil #637). Nothing upstream
caused that, so it is not a candidate. Inventing usage to produce a P1 candidate is
forbidden, so this slot stays empty.

## Priority 2: software we actually use

**None with an observed problem.** Software in real use: Python 3, git, GitHub
Actions (`checkout`, `setup-python`, `configure-pages`, `upload-pages-artifact`,
`deploy-pages`) and Playwright/Chromium for site screenshots. No unexpected behavior
was recorded in any session. The owner decision forbids auditing them for bugs.

## Priority 3: existing external work where we hold a missing increment

### S1. sqlparse #918 (fixes #885) and #894 (fixes #886): our verification evidence

- **Origin:** real LAB work, not mining. On 2026-10-24 Agent 1 built and Agent 2
  reviewed a fix for the same two crashes. Then both PRs were found, and our PR was
  correctly dropped (DEC-0048).
- **What we already hold:**
  - a reviewed patch with a `> 2` third guard;
  - a `(::)` input parametrized into the #885 test;
  - 170,000 fuzzed malformed inputs × 4 option sets. They found exactly the two crash
    sites on master and zero exceptions with our patch.

  Sources: `lab/observations/traces/2026-10-24-sqlparse-885-886-review.md`, `...-reviewed.patch`.
- **Possible increment, without competing:**
  - run the same fuzz corpus and `(::)` against the two PR heads (#918 `9933775`,
    #894 `77eb92d`) and their combination;
  - report a counterexample if either misses a path;
  - otherwise report independent verification that the pair removes every crash the
    corpus finds.
- **Upstream state (2026-10-30):** both PRs are still open, and their merge refs exist.
  #918 adds `len(tlist.tokens) < 3` plus an empty-tokens check.
- **Q6 risk (new question, decisive here):**
  - the last commit on master is 2026-08-13, by the maintainer;
  - no outside PR has been merged since then;
  - #894 has waited since 2026-09-13 with no review.

  Expected value depends on whether evidence posted on a PR would be read at all.

### S2. dateutil #1631 (UNTIL half of #637)

- **Origin:** real LAB work. On 2026-10-27 Agent 2 put #637 on the board, Agent 1
  reproduced it and rejected the DTSTART half (DEC-0052).
- **Possible increment:** independent verification of #1631's UNTIL change against the
  reproducer we already ran. Possibly an adjacent-path check: UNTIL with a timezone
  versus DTSTART with a timezone.
- **Q6 risk:**
  - dateutil had about 281 open PRs on 2026-10-27;
  - the maintainer called the general problem nearly insoluble.

  Weaker than S1.

## Not listed

- typeguard #578 (two competing PRs) and cachetools #446/#447 (reporter's own PR,
  unreviewed) would also be "help existing work". Both came from random issue mining,
  not from our own work. The owner ranks that origin lower, so they are left out.

## Agent 2's pick for comparison

**S1, with Q6 checked first.** It is the only source where we already hold specific
evidence that nobody else has: the fuzz corpus and the reviewed patch. The decisive
criterion is Q6. If no maintainer review activity can be shown, record NO USEFUL
CANDIDATE with Q6 as the explicit reason, not as a technical block.

## Memory conflict noted

Retrieved lessons:
- **Family 11** ("offer only the missing increment") matches the new policy.
- **Family 01** says to check PR refs for existing fixes before building. It remains
  a valid check (owner Q2). Its use on the board as an automatic reject ("an open PR
  exists → reject") now conflicts with the owner decision.

The owner decision is authoritative. The lesson is not edited here.
