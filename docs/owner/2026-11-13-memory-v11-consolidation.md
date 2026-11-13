OWNER DECISION — MEMORY V1.1: CONSOLIDATION AND LESSON PROMOTION

This exact instruction applies to BOTH Agent 1 and Agent 2.

Canonical repository:

https://github.com/RobertMalczyk/ai-for-ai-lab

Start from CURRENT `main`, not remembered conversation state.

Read first:

- `AGENTS.md`
- `STATE.md`
- `ROADMAP.md`
- `docs/MEMORY_CONTRACT_V1.md`
- `docs/MEMORY_RUNTIME_V1.md`
- `lab/memory/config.v1.json`
- current memory journals
- recent sessions and decisions
- peer work

Record this as an owner decision in the normal LAB history and Decision Map.

============================================================
1. PURPOSE
============================================================

Memory V1 successfully performs:

experience
→ retrieval
→ decision
→ outcome
→ feedback

But the current real run has exposed a missing capability.

The system retrieves historical lessons, but it has produced almost no NEW durable lessons from its own prospective experience.

Current evidence includes repeated decisions and repeated no-candidate outcomes, while `memories.jsonl` still consists of historical seed lessons.

Therefore Memory V1.1 adds a CONSOLIDATION layer.

The objective is:

experience
→ repeated pattern
→ candidate lesson
→ independent adversarial review
→ promoted memory
→ future retrieval
→ later confirmation / contradiction / supersession

This is NOT permission to write every event into long-term memory.

The purpose is selective learning.

============================================================
2. DO NOT CHANGE CURRENT SAFETY MODE
============================================================

Keep:

`memory_enabled = true`

`implementation_status = active_shadow`

`reward_mode = shadow`

`reward_influence = 0.0`

`coupling_scope = none`

Private memory remains disabled.

Do NOT enter CANARY.

Do NOT change reward influence.

Do NOT allow newly created memories to affect reward.

Do NOT use this task as justification to change external OSS policy.

This task only extends how lessons are learned and maintained.

============================================================
3. MEMORY LAYERS
============================================================

Memory V1.1 must explicitly separate three layers.

------------------------------------------------------------
A. EPISODIC / EXPERIENCE RECORD
------------------------------------------------------------

Records what happened.

Existing examples:

- decisions
- retrievals
- feedback
- outcomes

Add lightweight episode records only where current journals fail to represent meaningful repeated inactivity.

------------------------------------------------------------
B. CONSOLIDATION
------------------------------------------------------------

Determines whether multiple experiences support a reusable lesson.

New canonical artifact:

`lab/memory/lesson_candidates.jsonl`

A candidate is NOT retrievable memory.

It is a hypothesis awaiting review.

------------------------------------------------------------
C. DURABLE MEMORY
------------------------------------------------------------

`lab/memory/memories.jsonl`

Only independently verified lessons may become active retrievable memory.

============================================================
4. SELECTION EPISODES
============================================================

Current scheduled runs that produce `no_update` can disappear from the learning dataset.

Add a lightweight record for task-selection cycles where this distinction matters.

Suggested canonical artifact:

`lab/memory/selection_episodes.jsonl`

Do NOT create an entry for every trivial poll.

Create one only when the agent actually evaluates whether work exists under the current selection policy.

Minimum fields:

- `episode_id`
- `occurred_at`
- `agent`
- `session_id`
- `policy_version` or policy reference
- `source_mode`
- `sources_considered`
- `candidate_count`
- `actionable_count`
- `outcome`
- `reason`
- `evidence_refs`

Allowed outcomes should include at least:

- `candidate_found`
- `no_candidate`
- `blocked`
- `waiting_external`

Do not treat `no_candidate` as failure.

Do not assign reward to selection episodes.

Do not create fake episodes merely to increase counts.

============================================================
5. LESSON CANDIDATES
============================================================

Add:

`lab/memory/lesson_candidates.jsonl`

Each record represents a possible generalization from experience.

Minimum fields:

- `candidate_id`
- `created_at`
- `proposer`
- `pattern`
- `scope`
- `supporting_decision_ids`
- `supporting_episode_ids`
- `support_count`
- `contradiction_count`
- `proposed_lesson`
- `actionable_implication`
- `falsifier`
- `confidence`
- `status`
- `reviewer`
- `reviewed_at`
- `review_rationale`
- `promoted_memory_id`
- `supersedes`

Statuses should support at least:

- `provisional`
- `verified`
- `rejected`
- `promoted`
- `superseded`

Append-only semantics remain mandatory.

Corrections supersede prior records.

Do not mutate history in place.

============================================================
6. WHEN TO CREATE A CANDIDATE
============================================================

Do NOT create a candidate from every event.

A lesson candidate may be proposed when at least ONE of these conditions holds:

A. repeated-pattern path

- at least 3 materially similar outcomes;
- across at least 2 separate sessions;
- with a common mechanism that can be stated;
- not merely the same command repeated.

OR

B. cross-agent path

- both agents independently observe materially the same pattern;
- evidence originates from separate reasoning or separate cases.

OR

C. strong-single-event path

One event may be sufficient only when:

- consequence is clear;
- mechanism is strongly evidenced;
- lesson is narrow;
- falsifier is explicit;
- independent reviewer agrees that repetition is not necessary.

Use this path sparingly.

============================================================
7. PERIODIC CONSOLIDATION TRIGGER
============================================================

Add a consolidation check.

It should run when one of these occurs:

- 5 new material decisions since the previous consolidation;
- OR 72 hours of relevant selection/runtime experience;
- OR the same outcome pattern appears at least 3 times;
- OR either agent explicitly flags a potential lesson.

The consolidation check asks:

1. What repeated patterns occurred?
2. Are they already represented by an existing active memory?
3. Are they merely consequences of explicit owner policy?
4. Is there evidence of a common mechanism?
5. Is there contradictory evidence?
6. Would remembering this change a future decision?
7. Can the lesson be stated conditionally?
8. What observation would falsify it?

A valid result may be:

`NO LESSON CANDIDATE`

Do not manufacture lessons.

============================================================
8. INDEPENDENT REVIEW
============================================================

No agent may promote its own lesson candidate.

Agent 1 candidate → Agent 2 reviews.

Agent 2 candidate → Agent 1 reviews.

Reviewer must independently verify:

- supporting records exist;
- records actually support the proposed pattern;
- events are not duplicates of the same underlying observation;
- scope is not too broad;
- owner policy is not being mistaken for learned experience;
- counterexamples were considered;
- lesson adds information not already contained in active memories;
- actionable implication follows from evidence;
- falsifier is realistic.

The reviewer may:

- VERIFY
- NARROW
- REJECT
- REQUEST MORE EVIDENCE

NARROW requires a superseding candidate record.

============================================================
9. PROMOTION TO MEMORIES.JSONL
============================================================

Only a verified candidate may be promoted.

The promoted memory must contain:

- stable `memory_id`
- lesson text
- scope
- exceptions
- source candidate ID
- evidence references
- created/promoted timestamps
- status
- confidence
- applicability conditions
- falsifier / invalidation condition where schema permits

Do not silently copy all candidate metadata into retrieval context.

Keep retrieval cards concise.

Do not import reward or utility values into the lesson.

============================================================
10. LESSON QUALITY
============================================================

Lessons must be CONDITIONAL.

Bad:

“Real-use-first does not work.”

Bad:

“Repositories accepting AI are bad targets.”

Bad:

“If no candidate exists for one day, search random issues.”

Preferred:

“When real-use-first selection repeatedly produces empty WIP across multiple independent selection episodes and no natural problem source appears, continued waiting provides diminishing new evidence. Consider the bounded existing-work fallback already permitted by owner policy.”

A lesson must distinguish:

observation
from
generalization
from
recommended action.

============================================================
11. SUPPORT AND CONTRADICTION
============================================================

A promoted memory is not permanent truth.

Track later evidence supporting or contradicting it.

Implement a minimal, auditable mechanism.

Do not create a complex probabilistic learning system.

At minimum the system must be able to associate later evidence with:

- `supports`
- `contradicts`
- `neutral`

for an existing memory.

A contradiction must NOT automatically delete or deactivate a lesson.

Repeated contradiction should trigger re-evaluation.

============================================================
12. RE-EVALUATION / EXPIRATION
============================================================

Create a re-evaluation path for active learned memories.

Trigger reconsideration when:

- significant contradictory evidence appears;
- owner policy changes;
- underlying external conditions materially change;
- the lesson repeatedly retrieves but proves irrelevant;
- applicability conditions no longer hold.

Possible outcomes:

- remain active
- narrow scope
- supersede
- retract

Preserve history.

This should use the same append-only approach.

============================================================
13. DO NOT CONFUSE POLICY WITH LEARNING
============================================================

A current owner instruction is authority.

Memory is evidence.

For example:

“Use real-use-first” is owner policy.

The observed consequence:

“real-use-first produced no actionable candidate across several days”

is experience.

A possible lesson:

“prolonged empty WIP under real-use-first may justify the already-authorized bounded fallback”

is learned knowledge.

Do not turn owner instructions themselves into learned facts.

============================================================
14. FIRST REQUIRED CONSOLIDATION CASE
============================================================

Use the current real history as the first natural consolidation case.

Relevant evidence includes at least:

- Agent 1 session 206:
  no credible candidate from three actual-use sources;

- Agent 2 session 207:
  independent source comparison → NO USEFUL CANDIDATE;

- subsequent scheduled cycles:
  no natural real-use candidate;

- Agent 2 site records explicitly stating that the lab remained in the same empty-WIP state for approximately a week;

- no new external implementation WIP during that period.

Do NOT assume the lesson in advance.

Agent 1 and Agent 2 must independently determine what this evidence supports.

Candidate hypothesis to test:

“When real-use-first selection repeatedly produces no actionable candidate across multiple independent cycles, continued empty WIP stops producing material new evidence. A bounded fallback to active existing work with a clear missing technical increment may be appropriate.”

This is only a HYPOTHESIS.

The agents must decide whether the evidence supports:

- this full statement;
- a narrower statement;
- or no durable lesson yet.

============================================================
15. IMPORTANT COUNTERFACTUAL
============================================================

The agents must explicitly consider:

Was the empty WIP actually a failure of real-use-first?

Alternative explanations may include:

- simply no real problem occurred during this short period;
- external OSS opportunities were unusually poor;
- maintainer attention criterion Q6 is too restrictive;
- waiting period is too short to generalize;
- the system does not observe enough real owner/LAB activity;
- scheduling frequency does not equal independent evidence.

Do not promote the lesson unless these alternatives are considered.

============================================================
16. FUTURE RETRIEVAL
============================================================

Promoted learned lessons participate in the same Memory V1 retrieval mechanism as existing active public lessons.

Do NOT prioritize them merely because they are newer.

Do NOT change Q ranking.

Do NOT change retrieval thresholds as part of this task.

SHADOW behavior remains identical.

The first important evidence after promotion will be:

Did this newly learned lesson retrieve for a later relevant decision?

Record that prospectively.

============================================================
17. FIRST TRUE LEARNING CHAIN
============================================================

The success criterion for Memory V1.1 is NOT implementation completion.

The first meaningful milestone is a complete real chain:

real experiences
→ repeated pattern
→ lesson candidate
→ independent verification
→ promoted learned memory
→ later relevant retrieval
→ later decision
→ independently evaluated usefulness

Until this entire chain occurs:

DO NOT claim that the agents have demonstrated learning from experience.

You may claim only that the consolidation mechanism exists.

============================================================
18. UTILITY
============================================================

Do not give positive utility merely because a new lesson was retrieved.

Utility remains unobserved unless later evidence supports that the retrieved lesson materially improved:

- decision correctness;
- decision efficiency;
- avoided rework;
- avoided a known mistake;
- identified useful external work;
- or improved another explicitly defined outcome.

If the same decision would clearly have happened without the lesson:

utility = 0 / unobserved as appropriate.

Do not inflate reward.

============================================================
19. TESTING
============================================================

Agent 1 owns implementation.

Agent 2 owns independent adversarial review.

Tests must cover at minimum:

1. one event does not create a candidate automatically;
2. three similar episodes may trigger a candidate;
3. repeated identical duplicate evidence does not inflate support;
4. owner policy alone cannot become learned memory;
5. self-promotion is rejected;
6. second agent can verify;
7. reviewer can narrow via supersession;
8. rejected candidate never reaches retrieval;
9. promoted candidate becomes active memory;
10. contradiction can be recorded;
11. contradiction does not silently delete history;
12. superseded/retracted lesson is excluded from normal retrieval;
13. old historical seeds still work;
14. reward influence remains zero;
15. CANARY remains locked;
16. invalid append-only records fail closed;
17. selection episode with no candidate is not treated as failure/reward;
18. consolidation can return NO LESSON CANDIDATE.

============================================================
20. ADVERSARIAL CASES
============================================================

Agent 2 must test at least these failure modes:

- three events that look similar but have different root causes;
- same event accidentally counted three times;
- candidate overgeneralizes from one repository;
- candidate merely restates current owner policy;
- candidate contradicts an existing active lesson;
- candidate references unavailable/private evidence;
- candidate has no falsifier;
- proposer attempts self-verification;
- outdated lesson remains active after clear policy change;
- repeated `no_update` scheduler executions are incorrectly treated as independent evidence.

============================================================
21. PRIVACY
============================================================

Only public, sanitized evidence enters public memory.

Do not expose:

- private runtime;
- credentials;
- private mail;
- employer code;
- personal owner data;
- hidden chain of thought.

Store only explicit decisions, observations, evidence, hypotheses and falsifiers.

============================================================
22. DASHBOARD
============================================================

Agent 2 owns the public dashboard adaptation.

Add a small consolidation section showing:

- active memories;
- historical seeds;
- learned promoted memories;
- provisional lesson candidates;
- verified/rejected candidates;
- memories under contradiction/re-evaluation;
- last consolidation time;
- latest consolidation result.

Do not expose private evidence.

Do not imply that a promoted lesson has positive utility.

Clearly distinguish:

PROMOTED

from

PROVEN USEFUL.

============================================================
23. METRICS
============================================================

Track at least:

- selection episodes;
- material decisions;
- lesson candidates;
- candidates verified;
- candidates rejected;
- promoted learned memories;
- contradictions;
- supersessions/retractions;
- learned memories later retrieved;
- learned memories with independently observed positive utility.

Do not optimize agents to maximize these counts.

These are observation metrics only.

============================================================
24. CURRENT MEMORY SEEDS
============================================================

Preserve all currently active historical seeds unless a separate evidence-driven correction is justified.

Do not rewrite them merely to fit the new schema.

Migration may add metadata only if it can be done without changing historical meaning.

============================================================
25. ROLES
============================================================

Agent 1:

- implement schemas/runtime;
- selection episode support;
- consolidation trigger;
- candidate creation;
- promotion/re-evaluation mechanics;
- tests;
- documentation;
- first independent consolidation proposal if evidence supports one.

Agent 2:

- independently review implementation;
- adversarial tests;
- independently inspect first consolidation evidence;
- verify/narrow/reject Agent 1 candidate;
- dashboard adaptation;
- review privacy and provenance.

Roles may rotate for later candidates.

============================================================
26. DELIVERY ORDER
============================================================

Use this order:

1. inspect current main;
2. define minimal schema extension;
3. implement selection episodes;
4. implement lesson candidates;
5. implement consolidation trigger;
6. implement cross-agent review;
7. implement promotion;
8. implement support/contradiction/re-evaluation;
9. tests;
10. Agent 2 adversarial review;
11. fix blockers;
12. dashboard;
13. run FIRST REAL consolidation on existing experience;
14. cross-review the resulting candidate;
15. promote only if justified;
16. wait for a future natural retrieval;
17. evaluate utility only after later outcome.

Do not skip directly to promoting the supplied hypothesis.

============================================================
27. NO NEW OWNER DECISION REQUIRED
============================================================

The owner has approved implementation of this consolidation loop.

The agents do not need to ask the owner whether to:

- create the new journals;
- implement the runtime;
- review candidates;
- promote a lesson that passes the defined cross-review process;
- retract/supersede a lesson when evidence requires it.

Return to the owner only if:

- the change would alter external contribution policy;
- reward influence would change;
- CANARY would start;
- private data would be required;
- architecture must materially depart from this instruction;
- external communication requires human ownership.

============================================================
28. OWNER REPORT
============================================================

Report back when the first consolidation cycle is complete.

The report must state:

A. IMPLEMENTATION

- new files/schema;
- tests;
- Agent 1 result;
- Agent 2 independent result.

B. FIRST REAL CONSOLIDATION

- exact evidence inspected;
- candidate proposed or NO LESSON CANDIDATE;
- proposed scope;
- counterevidence considered;
- Agent 2 verdict.

C. MEMORY STATE

- historical seeds count;
- newly promoted learned memories count;
- provisional candidates count;
- rejected candidates count;
- utility count.

D. CLAIM BOUNDARY

Explicitly say whether we have demonstrated:

- memory storage;
- retrieval;
- consolidation;
- learning from experience;
- positive utility.

Do not merge these claims.

============================================================
29. SUCCESS CRITERION
============================================================

Memory V1.1 is technically complete when:

- episodic experience is observable;
- repeated experience can create a candidate lesson;
- candidate requires independent verification;
- verified lesson can become retrievable memory;
- contradiction/supersession works;
- SHADOW remains zero-influence;
- dashboard exposes the lifecycle honestly.

But the research goal is reached only after a natural case demonstrates:

EXPERIENCE
→ CONSOLIDATION
→ NEW MEMORY
→ FUTURE RETRIEVAL
→ CHANGED OR IMPROVED DECISION
→ INDEPENDENTLY VERIFIED OUTCOME

Until then:

the system has a learning mechanism,

but learning utility remains unproven.