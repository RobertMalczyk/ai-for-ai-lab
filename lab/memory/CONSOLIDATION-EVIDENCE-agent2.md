# Memory V1.1: Agent 2's independent read of the first consolidation evidence

Written by Agent 2 in session 213 (2026-11-13), from `main` `56ba7eb`, before any Agent 1
V1.1 work existed and before Agent 1 proposed any candidate. The file is sealed: only its
SHA-256 is on `main` until Agent 1 has committed its own consolidation result, so that
Agent 1's reading stays independent. It is then published unchanged.

Owner decision: `docs/owner/2026-11-13-memory-v1-1-consolidation.md`.
Memory V1 hook: decision `agent2-2026-11-13-consolidation-evidence-001`.

This file is not a lesson candidate. Under the owner's role split, Agent 1 makes the first
proposal and Agent 2 reviews it. This file states what Agent 2 thinks the evidence supports,
so the review can be compared with it.

## 1. Evidence inspected

### Selection evaluations under real-use-first (owner decision 2026-10-30)

| # | Record | Agent | What was evaluated | Result |
|---|---|---|---|---|
| E1 | Session 202, `lab/tasks/SOURCES-2026-10-30-agent2.md`, decision `agent2-2026-10-30-sources-001` | Agent 2 | P1, P2, P3 sources (the owner's first round asked for exactly these three) | No P1/P2 source. P3: S1 sqlparse #918/#894 verification increment, S2 dateutil #1631. Q6 decisive for S1. |
| E2 | Session 206, `docs/SESSIONS.md`, decision `agent1-2026-10-30-strategy-activation` | Agent 1 | Three actual-use sources (LAB publication refusal, Click replay drift, waiting pytest/distutils work) | NO USEFUL CANDIDATE. Written on 2026-10-30, before reading E1; published 2026-11-04. |
| E3 | Session 207, `lab/tasks/SOURCES-2026-10-30-agent2.md` (comparison), decision `agent2-2026-11-04-sources-compare-001` | Agent 2 | Comparison of E1 and E2, live check of S1 | NO USEFUL CANDIDATE. S1 held on Q6, then mooted: maintainer fixed the crash class (`3512a9d`), released 0.6.1 on 2026-11-01 and ended maintenance. |

### Selection evaluations before real-use-first (same empty-WIP period, older policy)

| # | Record | Agent | Result |
|---|---|---|---|
| E4 | Session 194, decision `agent1-2026-10-28-preflight-003` | Agent 1 | Rejected django-json-api, CUGA, aiohttp: exact open fix PRs. |
| E5 | Session 199, decision `agent2-2026-10-29-preflight-003` | Agent 2 | Rejected Python-Markdown: policy, saturated queue. |
| E6 | Session 200, decision `agent2-2026-10-29-preflight-004` | Agent 2 | Rejected boltons, toolz, python-dotenv: swamped queues or no merges. |

### Scheduled runs after 2026-11-04

- **Agent 2, Stream A (every 6 hours).** I counted my own run reports from 2026-11-04 18:34Z
  to 2026-11-13 06:35Z: **35 runs**. Every one checked `main`, distutils #434, pytest #14777
  and lab issues, then reported "Skipped DISCOVER: no new real-use source". None evaluated a
  source. None left a LAB record. Earlier, from 2026-10-31 to 2026-11-04 06:34Z, about 15 runs
  skipped because the owner-ordered comparison waited for Agent 1's list.
- **Agent 2, Stream B (site), sessions 208-212.** They record the state ("no new work",
  "a week of the same state", "the recent entries describe waiting, not evidence"). They are
  descriptions of one state, not selection evaluations.
- **Agent 1.** Nothing reached `main` after `ecaa559` (session 206, 2026-11-04). Session 206
  says its automation runs every six hours. I cannot see whether any of those runs evaluated
  sources, so I make no claim about them.

### Existing active memories checked

All 15 are historical seeds. Closest to this topic: `seed-family-09` ("an external
conversation with no maintainer reply is waiting, not failed ... without polling"). It is
about a submitted PR waiting for upstream, not about choosing new work. It was the top hit
for this decision's hook query, on the words "no", "task" and "without".

## 2. Counting independent evidence

- **Independent selection evaluations under the current policy: 2** (E1 and E2). They are
  independent in the owner's sense: separate agents, separate source lists, E2 written before
  reading E1. E3 is the comparison of the same two lists plus one live check. It is not a third
  independent case.
- **The 35 skipped Stream A runs are one observation, not 35.** Each asked "has a new trigger
  appeared?" and found the same answer. None asked "does work exist under the policy?". This
  is the owner's failure mode "repeated `no_update` scheduler executions treated as independent
  evidence". They must not count as support. They also must not become selection episodes,
  because no evaluation happened in them.
- **E4-E6 were under the previous policy** (open-issue discovery). They are evidence about
  that method, which the owner already acted on (2026-10-30). They are not evidence about
  real-use-first.

## 3. What actually caused the empty WIP after 2026-11-04

The owner's policy has five priorities. The first round (2026-10-30) asked for P1-P3 lists,
then "resume DISCOVER" with the full order. P4 (maintainer-requested help) and P5 (bounded
open-issue discovery, "only after the previous sources produce no candidate") were **never run
by either agent after 2026-11-04**. I checked: no session, board row or decision mentions a P4
search, and the last P5-style search was session 200 (before the policy).

I checked my own Stream A routine prompt (last changed 2026-10-30 09:56Z). It says: "If no task
is active: DISCOVER using the owner's priority order", P4 and P5 included. The runs nevertheless
skipped all of DISCOVER whenever no *new* P1/P2 source appeared. So the deviation was in how the
runs executed, not in the prompt and not in the owner policy. A plausible reason is that the
policy's warnings ("Do not keep repeating the same discovery method merely because WIP is
empty", "Do NOT perform another generic scan") were read as covering P5 too; I cannot prove the
reason. So the eight days of empty WIP are better explained by **"the
selection procedure stopped being executed"** than by **"real-use-first selection was executed
repeatedly and kept returning nothing"**. Only the second would support the owner's hypothesis
as worded.

## 4. The owner's alternative explanations, one by one

| Alternative | My assessment |
|---|---|
| No real problem occurred in this short period | **Supported.** Both lists found no P1/P2 problem; LAB work in that period was waiting and site upkeep, which uses only the standard library, git and GitHub Actions. Few real problems can arise when little real work happens. |
| External OSS opportunities were unusually poor | **Partly.** E4-E6 and S1 show crowded or closed queues (sqlparse ended maintenance). But that is pre-policy evidence plus one case. |
| Q6 is too restrictive | **Weak evidence.** Q6 decided exactly one candidate (S1), and the upstream fix made it moot two days later. One case cannot show Q6 is too strict. |
| Waiting period too short to generalize | **Supported.** Two independent evaluations within one round (2026-10-30 to 2026-11-04). |
| The system does not observe enough real owner/LAB activity | **Supported, and structural.** P1/P2 depend on real work; the agents see only LAB work, which was mostly waiting. |
| Scheduling frequency is not independent evidence | **Decisive.** See section 2. |
| (Added) The later priorities were not executed | **Decisive.** See section 3. |

## 5. Does the evidence support the hypothesis?

Owner's hypothesis: "When real-use-first selection repeatedly produces no actionable candidate
across multiple independent cycles, continued empty WIP stops producing material new evidence.
A bounded fallback to active existing work with a clear missing technical increment may be
appropriate."

- **"Repeatedly ... across multiple independent cycles"**: not met. One round, two independent
  evaluations. Repeated-pattern path A needs 3 materially similar outcomes; I find 2.
- **"Continued empty WIP stops producing material new evidence"**: true for the period, but the
  cause is that no evaluation ran, so it does not show anything about the policy.
- **"Bounded fallback to active existing work with a clear missing increment"**: that is P3,
  which was already executed in E1/E2 (S1, S2) and failed on Q6 and an upstream fix. The
  unexecuted part is P4/P5, and those are already written in the owner policy. A lesson saying
  "use P4/P5" would restate owner policy (failure mode: candidate merely restates policy).

**Verdict on the full hypothesis: not supported.**

## 6. What, if anything, is supported

- Cross-agent path B is met only for a narrow observation: **in one round, neither agent found
  a P1/P2 source from LAB work.** As a lesson this adds little: it describes one week, and the
  falsifier (a P1/P2 source appears) is just ordinary future use.
- One mechanism is well evidenced, but by one underlying cause only (how my Stream A runs read their instructions) and it
  is a process fact about Agent 2: **"a scheduled run that checks only for a new trigger is not
  a selection episode; if the higher priorities came back empty, the run has to continue to the
  next permitted priority or record why not, or WIP stays empty without new evidence."** This
  could pass path C (strong single event) only if Agent 1 agrees repetition is not needed. It
  is close to owner policy, so the reviewer must check that it adds information: the policy
  says P5 is allowed after P1-P4 are empty; it does not say what a scheduled run must do. The
  falsifier: under a rule that does run P4/P5 when P1-P3 are empty, WIP still stays empty and
  those runs produce no new evidence either.

**My preliminary result: NO LESSON CANDIDATE for the full hypothesis.** At most, the narrow
process observation above, which I would not propose myself before seeing Agent 1's reading.
The direct fix is operational: from now on, a run that evaluates selection writes a selection
episode, and a run that only polls does not; and Stream A runs follow their prompt's full
priority order. That belongs to Agent 1's V1.1 runtime and to how Agent 2 runs Stream A, not to
a memory.

## 7. What would change my mind

- A record I missed showing that P4 or P5 was run under real-use-first and came back empty.
- Agent 1's automation logs showing repeated real selection evaluations after 2026-11-04.
- Three or more future selection episodes, across at least two sessions, that run the full
  priority order and all end NO USEFUL CANDIDATE.
