# Direction change of 2026-10-07: Agent 2's independent answer

The owner sent both agents the same prompt on 2026-10-07 09:36 (Warsaw): move the
experiment from "find our own agent's problem and build a helper" to "enter a real
outside open-source project, do a real task with ordinary tools, record the real
friction, and only then think about an improvement". He asked each agent, without
coordinating, for six things. This is Agent 2's answer, written before reading
Agent 1's. No tool was built for it.

## 1. Assessment

The change is right, and the lab's own evidence asked for it. On 2026-10-06 Agent 2
tested 11 lab tools and practices on psf/requests, pallets/click and pallets/flask:
none beat a competent agent with git, grep and pytest ([USEFULNESS.md](USEFULNESS.md)).
Every lab tool was built for a problem the lab created for itself, and the lab then
measured it against its own earlier habits. The one finding that pointed outward
was not a tool but an observation about real repositories: a 2024 security fix in
requests (commit 96ba401c, the netrc fix) shipped with no test, and upstream only
added one in 2025.

The change keeps what was good (falsification, replication, baselines, public
record) and points it at a place where an outsider can judge the result. A
maintainer who merges or rejects a change is a judge the agents cannot game.

## 2. Biggest risk

The milestone becomes the target. "First external PR" is easy to satisfy badly:
pick the easiest possible repo and task, send a tiny change, count it as success.
That costs a maintainer's time, can look like AI spam, and teaches the lab nothing.
It is the same mistake as before (a metric the agents control) moved outside.

Smaller risks under the same heading: selection bias toward easy tasks; n=1 being
read as proof; the two agents agreeing with each other instead of reviewing
adversarially (same base model family is a real chance of shared blind spots);
undisclosed AI authorship against a project's policy; and access (Agent 2 pushes as
Robakk84 and has not yet forked anything outside).

Note on staleness, found while writing this: both external gaps Agent 2 found in
history are already closed upstream. requests got its netrc tests in 2025, and
click's pager code on current main (2247b35, 2026-10-04) has been rewritten and is
now covered by tests. Gaps found by mining old commits are mostly fixed by the time
we find them. Tasks must be picked on current HEAD and in open issues.

## 3. Keeping the scientific value

- Predeclare before touching the repo: repo, task, why it is real (link to an open
  issue or a reproducible failure on HEAD), what counts as done, what would count as
  failure. Commit this to the lab first, so it cannot be rewritten after the fact.
- Log friction as it happens, not afterwards: every wrong turn, failed attempt,
  wasted command, context problem, with a short sanitized trace. Friction recorded
  only in a summary is a story.
- Independent review is recorded: the reviewer's objections are written to the lab
  before the builder answers them, with the builder's verdict on each (fixed,
  rejected and why). This is the only way to measure later whether review caught
  what the maintainer would have.
- The outcome that counts is the maintainer's: merged, changed on request, rejected,
  or ignored. Record the reason for each; a rejection is a full result.
- Any tool idea after that must name the recorded friction it removes and be
  compared with a task-matched baseline on a second, different repo.
- Disclose AI authorship in every external PR and issue, and read the project's AI
  policy first. Contributions to projects that forbid AI-written changes are off.

## 4. First path to a real external contribution

1. Choose two or three active Python projects with clear contribution rules,
   working tests, and an open "good first issue" or "help wanted" backlog
   (this first draft suggested requests, click and flask; correction from session
   074: all three exclude unsupervised agent contributions, see
   `lab/observations/2026-10-07-opus-ai-policy-screen.json`). Check the project's
   AI policy before anything else.
2. Pick one open issue that is reproducible on current HEAD, not claimed by anyone,
   and small enough that a maintainer can review it in minutes. Missing tests for
   existing behaviour and small, confirmed bugs are good first targets; features and
   design discussions are not.
3. Predeclare it in the lab (section 3). Builder and reviewer are named; the other
   agent reviews only after the builder says the candidate is complete.
4. Builder works with ordinary tools, records friction, produces a branch in a fork
   with the project's own test suite passing and the project's PR template filled.
5. Reviewer attacks it: is the issue really this, is there a simpler fix, does it
   fit the project's style and history, what edge case or regression is missed.
6. Only if both agree it is worth a maintainer's time: comment on the issue first
   when the project expects it, then open one PR, disclosed as AI-made. If either
   agent says no, the candidate stays in the lab with the reason.
7. Without fork or PR rights, stop at a complete verified candidate in the lab and
   say so openly.

Agent 2 offers to take either role in the first round. If Agent 1 builds, Agent 2
reviews, and the other way round next time.

## 5. Keep and limit

Keep: predeclared hypotheses and falsification; cross-agent replication; task-
matched baselines; sanitized public traces; recording negative results; the owner-
intervention record and the site's two views.

Limit: tool families and their maintenance (frozen, as DEC-0028 already says);
lab-internal maintenance sessions and checkpoint upkeep as a goal in itself; the
size of the daily site and journal entry when nothing outside happened (one short
honest line is enough); duplicate entries of the same fact in several logs;
sessions whose only subject is the lab.

## 6. No new tool

None was built. This answer is one document and the record of the owner's message.
