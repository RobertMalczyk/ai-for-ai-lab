# Owner decision 2026-10-30: change external task selection strategy

Received in the project chat on 2026-10-30 at 09:53Z, addressed to both agents. It is recorded
verbatim below as an owner decision under the transparency rule. Agent 2 recorded it (session 202).

---

OWNER DECISION — CHANGE EXTERNAL TASK SELECTION STRATEGY
This exact instruction applies to BOTH Agent 1 and Agent 2.
Canonical repository:
https://github.com/RobertMalczyk/ai-for-ai-lab
Start from CURRENT repository state, not remembered conversation state.
Record this instruction as an owner decision in the normal LAB history and Decision Map.
============================================================

1. WHY THE STRATEGY CHANGES
============================================================

The previous discovery strategy has produced enough evidence.
Repeated rounds show that selecting projects primarily by:

* open bug lists;
* AI-friendly contribution policy;
* small Python repositories;
* recent unclaimed issues;

is no longer an efficient primary search method.
Observed pattern:

* fresh useful bugs often receive a PR within hours or days;
* projects openly accepting AI-assisted work often attract many AI-assisted contributors;
* an AI-friendly policy can correlate with a flooded PR queue;
* older apparently free issues are often already covered by hidden forks, stale PRs or unresolved design discussions;
* repeated random repository search is producing diminishing information value.

Do not keep repeating the same discovery method merely because WIP is empty.
The owner approves a change of strategy.
From now on:
START FROM A REAL PROBLEM OR REAL USE, NOT FROM A RANDOM OPEN ISSUE.
The objective is no longer:
“find a repository with a free bug.”
The objective is:
“find a real externally useful problem where this two-agent system has specific evidence or context that can add value.”
Search for external work in this order.
PRIORITY 1 — PROBLEM ENCOUNTERED DURING REAL WORK
Highest priority.
If either agent encounters an actual problem while performing normal LAB work, external OSS work, testing, deployment, tooling or repository interaction:
consider that problem as a candidate.
Examples:

* unexpected library behavior;
* reproducible crash;
* incorrect API behavior;
* documentation that caused a real incorrect action;
* missing regression coverage discovered during real work;
* compatibility problem;
* confusing behavior that required investigation;
* an existing upstream PR that fails to cover the case actually encountered.

A naturally encountered problem is more valuable than a randomly mined edge case.
Do not invent usage merely to manufacture a candidate.
PRIORITY 2 — SOFTWARE ACTUALLY USED BY THE OWNER / LAB
Prefer libraries, tools and systems that are genuinely used in:

* AI FOR AI LAB;
* the agents' normal runtime/workflow;
* the owner's real software/AI/QA/automation work;
* existing public owner projects where relevant context is available.

The mere fact that the owner uses a project is NOT sufficient.
There must still be a concrete technical problem, friction point or missing behavior.
Do not audit dependencies looking for arbitrary bugs.
Start from observed use or a concrete need.
PRIORITY 3 — HELP EXISTING EXTERNAL WORK
An existing PR is NOT an automatic rejection.
Look for cases where we can add incremental technical value to work already happening:

* missing regression test;
* second trigger of the same root cause;
* incomplete scope;
* failing CI with unclear cause;
* unverified edge case;
* reproduction requested by maintainer;
* A/B verification;
* platform/version confirmation;
* counterexample to the proposed fix;
* evidence helping choose between two implementations.

The pytest #14777 contribution remains the reference pattern.
Do not compete with the author.
If the implementation is already there, contribute only the missing increment.
PRIORITY 4 — MAINTAINER-REQUESTED HELP
Prefer explicit requests such as:

* help wanted;
* needs reproduction;
* needs tests;
* needs confirmation;
* needs benchmark;
* needs investigation;
* maintainer explicitly asks somebody to take over.

PRIORITY 5 — CLASSIC OPEN-ISSUE DISCOVERY
Only after the previous sources produce no candidate may you perform generic open-issue discovery.
This is now the fallback, not the default.
Keep it bounded.
Do not perform long sequences of nearly identical repository scans.
“AI-assisted contributions allowed” is now only a NECESSARY policy signal where relevant.
It is NOT a positive selection signal by itself.
Before investing significant effort, estimate whether the contribution has a realistic chance of being read.
Prefer:

* active maintainers;
* recent merges from outside contributors;
* short/moderate PR queue;
* evidence maintainers review technical comments;
* clear ownership;
* specific technical discussion;
* an actual user/reporter waiting for resolution.

Treat these as negative signals:

* dozens of fresh AI-generated PRs;
* one contributor flooding the project with edge cases;
* large queues with little review;
* no meaningful merge activity;
* issue exists only because an agent mined an artificial corner case;
* maintainers explicitly signal review overload.

A welcoming policy plus an overloaded queue is NOT a good target.
The change of discovery strategy does NOT weaken PRE-FLIGHT.
Before BUILD, verify:

1. Does the problem still exist on CURRENT code/release?
2. Is there already an open PR or fork fixing it?
3. Has it already been solved, rejected or intentionally designed this way?
4. Does project policy permit the proposed human-reviewed AI-assisted contribution?
5. Is there a real contribution path?
6. Is there evidence somebody is likely to review or use the contribution?
7. Is our proposed contribution incremental rather than duplicative?

Question 6 is NEW.
A technically valid patch that is very unlikely to be reviewed may be rejected for low expected external value.
Document that explicitly rather than pretending it is technically blocked.
Do not automatically reject a candidate because a PR already exists.
Ask instead:
Can we add independent technical value without competing with the current author?
VALID examples:

* new regression case;
* second failure path;
* incomplete fix;
* reproduction;
* benchmark;
* independent verification;
* platform result;
* counterexample;
* root-cause evidence;
* precise review finding.

INVALID:

* implementing the same patch again;
* stylistic review;
* generic “looks good” comments;
* repeating CI;
* summarizing what the existing author already knows.

WIP remains 1.
For a candidate that passes PRE-FLIGHT:
One agent is PRIMARY INVESTIGATOR.
The other is INDEPENDENT CHECK / ADVERSARIAL REVIEWER.
The investigator must not read the peer's conclusion before forming its own initial technical hypothesis where independence materially matters.
The reviewer should actively search for:

* hidden existing fixes;
* contrary maintainer decisions;
* alternate root causes;
* tests failing for the wrong reason;
* adjacent execution paths;
* scope expansion;
* evidence that the proposed work is not externally useful.

Rotate roles naturally.
Do not permanently assign one agent only to discovery and the other only to review.
For candidates originating from real use, record:

* what task was being performed;
* what software was being used;
* what unexpected behavior occurred;
* whether the behavior mattered to the task;
* minimal reproduction;
* whether a workaround already exists;
* whether the problem appears generalizable beyond the LAB.

Do NOT publish private owner context.
Sanitize the scenario to the minimum public reproducible facts.
Memory V1 remains enabled.
Mode remains:
SHADOW
reward_influence = 0.0
Do not enter CANARY as part of this owner decision.
Use the normal Memory V1 hook before material decisions.
However:
the owner is also changing the search strategy, so historical lessons such as:
“find an unclaimed open issue”
must not override this new instruction.
Current owner policy always has priority over historical memory.
If a memory conflicts with this decision:
record the conflict and treat the owner decision as authoritative.
Do not delete the historical memory simply because policy changed.
Use correction/supersession semantics where appropriate.
This strategy change itself should become a candidate lesson only after evidence review.
Possible lesson hypothesis:
“AI-friendly public contribution policies can attract enough automated contributors that queue saturation reduces expected value; real-use provenance and maintainer attention are better selection signals than AI policy alone.”
Do NOT immediately promote this to a universal rule.
Agent 1 and Agent 2 should independently assess whether the accumulated evidence supports:

* project-specific observation;
* ecosystem trend;
* or only a temporary local pattern.

If recorded, scope it conservatively.
Do not perform another sequence of 10+ generic scans.
Per discovery session:

* inspect at most 3 serious candidates;
* go deeper on at most 1;
* stop when the strongest candidate fails a decisive criterion.

A session ending with:
NO USEFUL CANDIDATE
is valid.
Do not compensate for an empty WIP by:

* building LAB tools;
* inventing artificial bugs;
* fuzzing random libraries without a user problem;
* mass-scanning GitHub;
* creating generic project-ranking infrastructure.

A successful contribution does NOT require our own PR.
Valid outcomes include:

* maintainer adopts our regression case;
* existing PR changes because of our counterexample;
* reproduction confirms or disproves a report;
* reviewer uses our evidence;
* root cause becomes clearer;
* issue is correctly closed as already solved/not a bug;
* our investigation prevents a duplicate PR;
* our evidence helps an existing contributor.

The important question is:
Did the work change or improve an external technical decision?
You may consider public owner projects and dependencies actually used by the owner.
Do NOT assume access to private owner repositories, employer systems or confidential code.
Do NOT search personal data.
Use only:

* public repositories;
* explicitly shared artifacts;
* software already present in the LAB workflow;
* owner-provided public context.

If a real-use candidate requires private evidence to explain the bug:
derive the smallest public reproducer before considering upstream work.
This instruction resolves the current strategy question.
Do not repeatedly ask:
“Which repository should we investigate next?”
Choose autonomously using the priority order above.
Ask the owner only when:

* publication requires human ownership;
* project rules require the human to interact personally;
* there is a genuine scope/value trade-off;
* external communication needs explicit human approval;
* private context would be required;
* two materially different contribution paths remain and cannot be resolved technically.

Existing waiting items remain unchanged.
Do not touch them without a new upstream signal.
In particular:

* pypa/distutils #434
* pytest #14777

They remain outside active WIP while waiting.
Complete the remaining Memory V1 bookkeeping according to the existing owner-approved activation sequence.
If all previously required conditions for `active_shadow` are already satisfied:
Agent 1 should perform the required status transition.
Agent 2 should independently verify that the transition is justified.
This does NOT require a new owner decision.
Do not enter CANARY.
After recording this owner decision:
Do NOT perform another generic “AI-friendly Python projects” scan.
Instead, each agent independently identifies up to 3 possible sources from:

1. a real problem encountered during recent LAB work;
2. software genuinely used by the LAB/owner;
3. existing external work where the agents can add a missing technical increment.

Compare the candidates.
Choose ONE only if there is credible expected external value.
Then resume:
DISCOVER
→ PRE-FLIGHT
→ INDEPENDENT CHECK
→ BUILD
→ ADVERSARIAL REVIEW
→ HUMAN REVIEW
→ SUBMIT / REJECT / BLOCK
WIP = 1.
Do not report routine failed searches individually.
Return to the owner when one of these happens:
A. REAL CANDIDATE FOUND
Report:

* source of the candidate;
* why it came from real use rather than random mining;
* project/repository;
* exact problem;
* current upstream state;
* expected external value;
* PRE-FLIGHT result.

B. READY FOR HUMAN REVIEW
Report:

* artifact;
* evidence;
* Agent 1 conclusion;
* Agent 2 independent conclusion;
* exact external action requiring human approval.

C. STRATEGY EVIDENCE
After enough natural cases, report whether real-use-first produced a materially better candidate rate than generic issue discovery.
Do not manufacture a comparison.
The purpose of this change is not to increase activity.
It is to increase the probability that the agents work on something another human actually needs.
