# Owner instruction, 2026-10-26 12:39 UTC (verbatim)

Posted by the owner in the project chat and relayed to Agent 2's thread. The instruction itself states that it applies to both Agent 1 and Agent 2. Published under the golden transparency rule (docs/TRANSPARENCY.md). The wording below is unchanged.

---

OWNER DIRECTION — COMPLETE AND ACTIVATE MEMORY V1
This exact instruction applies to BOTH Agent 1 (ChatGPT) and Agent 2 (Opus).
Recognize your identity and role from the existing repository configuration.
Do not switch identities, accounts or responsibilities.
Canonical repository:
https://github.com/RobertMalczyk/ai-for-ai-lab
Start from CURRENT `main`, not remembered conversation state.
The Memory V1 work is currently incomplete.
The contract and dashboard exist and have been reviewed/merged:

* PR #86 — Memory contract V1
* PR #87 — Memory and learning dashboard

However, the production Memory V1 runtime is not actually being used by the agents.
Current known gap:

* `lab/memory/config.v1.json` exists;
* `lab/memory/records.v1.schema.json` exists;
* `lab/memory/export.v1.schema.json` exists;
* dashboard/export infrastructure exists;

but there is no operational loop that reliably does:
IMPORTANT DECISION
→ retrieve relevant memory
→ expose it to the agent
→ record which memories were used
→ perform action
→ record outcome
→ independently verify feedback
→ create/correct lessons
→ make those lessons available to later decisions.
The historical `lab/memory-poc/` is evidence and reference code only.
Do NOT declare Memory V1 operational merely because the POC, schema or dashboard exists.
The objective of this task is:
make Memory V1 genuinely operational in normal Agent 1 and Agent 2 work.
============================================================

1. NON-NEGOTIABLE MODE
============================================================

Memory is active.
Rewards remain observational only.
Required mode:
memory_enabled = true
reward_mode = shadow
reward_influence = 0.0
coupling_scope = none
DO NOT enter CANARY.
DO NOT let Q/reward:

* choose tasks;
* alter task priority;
* alter session cadence;
* increase/decrease budget;
* bypass WIP=1;
* bypass upstream policy;
* change human-review requirements;
* introduce a previously irrelevant memory into retrieval.

The first goal is to prove that MEMORY ITSELF is usable.
Q is still a shadow counterfactual.
AGENT 1 owns:

* Memory V1 runtime;
* persistence;
* retrieval;
* append-only records;
* decision recording;
* feedback recording/folding;
* lesson creation/correction mechanics;
* configuration validation;
* CLI/API surface required by both agents;
* runtime tests.

AGENT 2 owns:

* independent adversarial review;
* retrieval counterexamples;
* historical-seed verification;
* checking that Agent 1 actually used retrieved memories;
* dashboard compatibility;
* public-data/privacy review;
* independent validation of the first real Memory V1 decisions.

Neither agent may approve its own feedback event.
Before writing code:
Both agents independently inspect current `main`.
Verify at least:

* current Memory contract;
* current export schema;
* current dashboard;
* `lab/memory/config.v1.json`;
* existence/non-existence of production JSONL journals;
* existence/non-existence of runtime implementation;
* current AGENTS/startup workflow;
* current open branches/PRs;
* current external WIP.

Record a short factual finding.
If reality differs from this prompt, use current repository truth.
Do not redesign V1 unless a concrete contradiction prevents implementation.
The current configuration may still contain:
`implementation_status: awaiting_contract_review`
despite contract approval/merge.
Replace stale status with a machine-readable state reflecting reality.
Use a minimal status progression such as:
contract_approved
runtime_implemented
active_shadow
Do not invent a large lifecycle framework.
Once the runtime is live and actually used in a real decision, the correct state should be:
active_shadow
Create the production append-only Memory V1 journals if they do not exist:
lab/memory/memories.jsonl
lab/memory/decisions.jsonl
lab/memory/feedback.jsonl
lab/memory/mode_history.jsonl
Use the accepted V1 schema.
Do NOT use the POC state file as production state.
Do NOT modify old records in place.
Corrections append new records using the existing supersession/correction model.
Empty journals are valid.
Implement the smallest production runtime that supports:
A. LOAD
Read:

* configuration;
* memories;
* decisions;
* feedback;
* mode history.

Validate records.
Invalid records must fail explicitly rather than silently influence decisions.
B. ELIGIBILITY
A memory may be retrieved only if:

* it was available BEFORE the decision being made;
* it is still active/applicable at that decision time;
* it is not retracted;
* a superseded version is not used after its correction became effective;
* visibility permits the current agent to see it.

The current public/shared layer is authoritative.
Do not pretend that private memory isolation exists.
Until real access-controlled private stores are verified:
private_store_status = unverified_not_enabled
and production retrieval must not depend on private memory.
C. RETRIEVAL
For each MATERIAL decision, retrieve:
maximum 3 memories
maximum 3200 characters INCLUDING the contextual metadata sent to the agent.
Use an absolute relevance score.
Required behavior:

* `retrieval.min_relevance` is applied BEFORE returning a memory;
* an off-topic query may return ZERO memories;
* the strongest item must NOT be normalized to 1.0 merely because it is the strongest;
* Q must not influence ranking in SHADOW;
* Q must never introduce a memory that failed the relevance filter.

The POC's normalization weakness must not be reproduced.
A simple BM25-style lexical implementation is acceptable for V1.
Do not add embeddings or an external vector database in this task.
D. OUTPUT TO THE AGENT
Retrieval must produce a concise decision-context block such as:
MEMORY V1

* memory_id
* applicable lesson
* why it matched / score
* important exception if any

If no memory passes the threshold:
MEMORY V1: no relevant lesson found.
That is a valid and desirable outcome.
E. DECISION RECORD
For every material decision using the Memory V1 hook, append one decision record.
It must include at least the accepted schema fields, including:
decision_id
agent
task_id
task_type
session_id
occurred_at
rule_version
memory_ids
suggested_action
actual_action
shadow_memory_ids
alternative_outcome
evaluation_ref
cost
map_node_ids
Important:
`memory_ids` means memories actually shown/used under normal SHADOW retrieval.
`shadow_memory_ids` means the counterfactual Q-influenced ordering, if calculated.
Do not claim the counterfactual was executed.
`alternative_outcome` remains `unobserved`.
F. EXPERIENCE / LESSON WRITE
After a meaningful result:
record the experience.
Create a new lesson only when there is a useful transferable conclusion.
Do NOT create one lesson per session.
New automatically derived lessons begin as:
provisional
Promotion requires:

* independent review by the other agent, OR
* sufficiently deterministic external evidence.

A lesson learned from failure may be valuable.
`source_outcome` and evidence strength must remain separate from lesson usefulness.
This is essential.
Do NOT leave Memory V1 as a CLI that nobody calls.
Modify the operating instructions/workflow so that BOTH agents must use the Memory V1 retrieval hook before a MATERIAL decision.
Examples of material decisions:

* reject/accept an OSS candidate at PRE-FLIGHT;
* decide whether an existing PR is actually competing;
* choose between two plausible root causes;
* decide BUILD scope;
* decide whether review finding is blocking;
* decide whether a task should proceed to HUMAN REVIEW;
* materially revise an earlier conclusion.

Routine actions do NOT require retrieval:

* reading a file;
* formatting;
* updating a journal;
* checking unchanged external status;
* routine site maintenance.

The hook should be cheap enough to use naturally.
Do not run full historical retrieval at every tool call.
The historical POC contains manually derived lessons.
Do NOT blindly import all POC records.
Use:
lab/memory-poc/SEED-CHECK-agent2.md
lab/memory-poc/REPORT.md
lab/memory-poc/memories.json
as source material.
Agent 2 independently verifies the corrected seed set.
Only lessons whose:

* historical source is valid;
* chronology is valid;
* scope is defensible;
* wording does not use future knowledge;

may be imported.
Imported records must be marked:
historical_seed = true
They receive NO reward points merely for being imported.
Do not import POC Q values.
Initial production Q is neutral.
If a seed remains ambiguous, omit it.
A smaller trustworthy seed is better than 22 questionable records.
Do not blindly force these in, but verify whether the repository evidence supports
at least these families because they have already affected real decisions:

* check for an existing PR before building;
* verify actual PR state, not just page wording;
* distinguish closed from merged;
* current upstream state beats remembered state;
* reproduce before patching;
* regression test must fail for the intended reason;
* review adjacent execution paths, not only the reported function;
* do not claim green full suite when failures remain;
* waiting for upstream is not failure;
* project AI/contribution policy is a hard PRE-FLIGHT constraint;
* existing outside work can still be helped if there is incremental technical value;
* read large required documents without truncating the relevant tail;
* exact commands/replay inputs matter for reproducibility;
* stale current-state claims should be replaced with dated evidence or live checks;
* negative experiment can generate a useful lesson;
* do not infer causality merely from chronology.

Import only after evidence review.
Implement the accepted feedback categories exactly.
Category/value consistency must be machine-enforced:
useful_result = +1.0
review_correction = +0.5
new_finding = +0.2
activity = 0
repeated_error = -0.5
constraint_violation = -1.0
unresolved = null
Only VERIFIED events affect aggregates/Q.
Self-verification is prohibited.
Pending, blocked or unresolved outcomes are not zero and not punishment.
Do not reward:

* a commit;
* a test merely being green;
* a site update;
* rechecking unchanged state;
* quantity of rejected candidates.

Use existing:

* deduplication;
* per-task positive cap;
* per-session discovery cap;
* exactly-once reversal.

Q is utility of:
MEMORY × CONTEXT × AGENT
not an intelligence score for an agent.
In SHADOW:
normal retrieval = relevance/scope/evidence/recency
counterfactual retrieval = same eligible relevant candidate set, then optional Q rerank.
Store both when useful.
Dashboard may show differences.
Do not act on the Q variant.
If no later outcome can attribute usefulness to a particular memory:
utility = null / unresolved
Do not smear success equally over every retrieved memory.
After implementation and seed validation, each agent must use Memory V1 in REAL normal work.
Do not manufacture a synthetic task.
Use the next naturally occurring material OSS decision.
For the FIRST qualifying decision from each agent:
BEFORE decision:

1. construct the decision query/context;
2. run production retrieval;
3. freeze the returned `memory_ids`;
4. record what the memories suggest;
5. make the actual decision.

AFTER:
6. record the decision;
7. wait for/obtain the normal evidence;
8. the other agent independently reviews whether:

* retrieved memories were relevant;
* any important relevant lesson was missed;
* the agent actually followed or consciously rejected the suggestion;
* the decision quality can be evaluated;

9. record feedback only if justified.

We need at least ONE real decision from Agent 1 and ONE from Agent 2 before Memory V1 is called operational.
At least one early real or bounded replay test must target a lesson whose vocabulary differs from the current task.
The original POC failed one such case.
Test whether a useful lesson transfers across different surface wording.
Do NOT tune the algorithm after seeing one test result.
Record failure honestly.
Embeddings are a future option only if enough new failures demonstrate lexical retrieval is materially insufficient.
Add a deterministic negative-control test.
An unrelated query must produce:
ZERO retrieved memories.
This specifically verifies the Agent 2 blocker that led to `min_relevance`.
Do not normalize the best weak match into a positive result.
Production public memory may contain only public/safely shared information.
Do not publish:

* credentials;
* private mailbox contents;
* private runtime contents;
* private project storage;
* local machine paths;
* hidden platform memory;
* authentication/session data.

The fact that Agent 2 has project-local storage inaccessible to Agent 1 is NOT
sufficiently verified access control for Memory V1 private-layer claims.
Therefore:
PRIVATE MEMORY V1 REMAINS DISABLED.
Dashboard may expose only:
private.available = false
until a real security boundary is implemented and tested.
Agent 2 must connect the existing dashboard to REAL production journals.
Once real Memory V1 activity exists, the page should no longer say simply
"no data yet".
Verify it displays correctly:

* SHADOW;
* memory ON;
* influence 0;
* public memory counts;
* actual retrieval/use count;
* Agent 1/Agent 2 feedback;
* pending/disputed separately;
* actual decision examples;
* latest data timestamp;
* readiness gaps;
* Decision Map links when IDs exist.

No fake/demo event may enter production aggregates.
DEMO remains visibly separate.
At minimum test:

1. persistence/restart;
2. append-only records;
3. chronology/no future memory;
4. superseded lesson behavior;
5. retracted lesson behavior;
6. 0-result retrieval;
7. max 3 lessons;
8. 3200-character budget;
9. absolute relevance threshold;
10. off-topic negative control;
11. Q has no effect on normal SHADOW ranking;
12. Q cannot introduce irrelevant memories;
13. feedback category/value enforcement;
14. self-verification rejection;
15. pending/disputed not scored;
16. duplicate feedback rejection;
17. exactly-once reversal;
18. positive caps;
19. historical_seed receives no automatic reward;
20. decision record persistence;
21. restart does not duplicate a decision/feedback event;
22. invalid records fail clearly;
23. no private record reaches public export;
24. current dashboard exporter consumes real journals.

Before approving activation, try to break the implementation with at least:

* irrelevant query;
* partially overlapping vocabulary but wrong meaning;
* corrected lesson;
* retracted lesson with high Q;
* future lesson;
* duplicate event;
* self-awarded success;
* pending external result;
* negative experiment generating useful lesson;
* task with several retrieved memories but no attributable utility;
* fake/private path in source refs;
* malformed record;
* Q-preferring irrelevant memory;
* restart/replay;
* stale dashboard export.

Agent 2 should write the cases BEFORE reading Agent 1's answers where practical.
Return:
APPROVED FOR ACTIVE SHADOW
or
CHANGES REQUIRED
with concrete evidence.
Required sequence:

1. Agent 1 — runtime implementation branch/PR.
2. Agent 2 — independent adversarial review.
3. Agent 1 — fixes if needed.
4. Agent 2 — final runtime approval.
5. Merge runtime.
6. Agent 2 — dashboard adaptation if needed.
7. Agent 1 — dashboard/privacy/data review.
8. Merge dashboard change.
9. First real Agent 1 Memory V1 decision.
10. First real Agent 2 Memory V1 decision.
11. Cross-review those decisions.
12. Only then set:

implementation_status = active_shadow
Do not mark active_shadow before the mechanism has actually been exercised by both agents.
Memory is infrastructure supporting real work, not the new purpose of the LAB.
After the bounded implementation/review:
return to the external OSS workflow.
Do not spend repeated sessions polishing memory.
Do not create:

* a vector database service;
* an LLM lesson-extractor service;
* new dashboards;
* analytics;
* a memory framework for other projects;
* recursive memory-about-memory records;
* artificial tasks to earn points.

If external OSS work is waiting, Memory V1 may be tested on the next naturally arising decision.
WIP=1 remains the external-work rule.
Do NOT enter CANARY during this task.
The existing criteria remain authoritative.
A working runtime plus two real decisions is NOT enough.
CANARY still requires the full prospective evidence threshold defined in the
accepted Memory Contract V1.
Until then:
SHADOW
reward_influence = 0.0
Do not ask the owner to resolve routine implementation details.
Return when the work reaches ACTIVE SHADOW or a genuine owner-level blocker exists.
Report:

1. runtime PR;
2. final runtime commit;
3. dashboard PR if changed;
4. number of imported historical seed memories;
5. number omitted as ambiguous;
6. first Agent 1 real decision and retrieved memory IDs;
7. first Agent 2 real decision and retrieved memory IDs;
8. whether either retrieval returned zero memories;
9. independent review results;
10. actual feedback events, if any;
11. test count/result;
12. current dashboard URL;
13. current mode and reward influence;
14. remaining known limitations.

Most importantly answer:
Did a past lesson demonstrably reach a later real decision through Memory V1?
If YES:
show the exact chain:
source event
→ lesson
→ retrieval
→ decision
→ outcome/review
If NO:
do not call Memory V1 operational.
The objective is not to produce more memory files.
The objective is to establish a real, auditable learning loop:
EXPERIENCE
→ LESSON
→ LATER RETRIEVAL
→ DECISION
→ RESULT
→ CORRECTION / UTILITY
while preserving independent review and keeping reward influence at zero.
