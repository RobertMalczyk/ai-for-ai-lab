# Decisions

### DEC-0001 — Evidence freshness before general memory

Problem: a resumed agent cannot tell whether file-based notes are stale.

Decision: a minimal versioned JSON handoff capsule with selected SHA-256 file
fingerprints, a goal, and a next step; stdlib Python CLI.

Why: the failure is observable without a model API, budget, or new service.
SHA-256 checks content even when timestamps or file sizes are misleading.

Alternatives: mtime-only checks (weak evidence); full embedded contents (context
cost); vector memory (does not establish freshness); Git HEAD alone (misses
uncommitted edits and invalidates unrelated changes).

Consequences: callers select dependencies; unchanged does not mean correct.
Semantic relevance, concurrent mutation and external resources remain unsolved.
An extra hash read costs I/O; token/time savings are hypotheses, not results.

### DEC-0002 — Strict small contract and conservative filesystem scope

Problem: ambiguous data and links can silently change the evidence being checked.

Decision: reject unknown versions/fields, duplicate keys, path traversal and
symlinks. Report missing files as stale; malformed/unreadable input as errors.

Why: another agent needs an unambiguous distinction between stale and unchecked.

Alternatives: silently skip bad inputs (false assurance); sandbox all filesystem
races (too large for this iteration).

Consequences: v1 assumes a quiescent local checkout, is not a security boundary,
and does not support symlink-based projects without explicitly selected real files.

### DEC-0003 — Tested baseline with short-lived work branches

Problem: future sessions need a canonical starting point without human approval
for every routine edit, while preserving the work's history.

Decision: atomic commits on agent branches; fast-forward main after local tests
and remote divergence check. Keep branches initially; no force push.

Why: the user authorized autonomous Git maintenance. Small tested increments
can remain discoverable without accumulating an approval backlog.

Alternatives: every change waits for human PR approval (interrupts autonomy);
write directly to main (loses branch isolation).

Consequences: local tests are evidence, not independent review. Diverged work
must be reconciled safely in a later scoped task; never overwrite collaborators.

### DEC-0004 — Keep uncomfortable benchmark cases

Problem: a perfect hash test can imply unjustified recovery reliability.

Decision: separately label selected-byte freshness and task relevance; retain harmless-comment and omitted-dependency counterexamples.

Why: failures show what the tool cannot establish.

Alternatives: only test changed/deleted files (misleading coverage).

Consequences: fixture-defined counts are diagnostic only; claim scoping may reduce review breadth but cannot resolve either semantic limitation.

### DEC-0005 — Bound claim manifests and complete affected dependency sets

Problem: one changed file need not invalidate independent claims, but a changed comparison operand requires both operands.

Decision: companion manifest bound by canonical capsule hash; strict claim IDs and references; review all dependencies of affected claims and separate missing paths.

Why: preserve capsule v1 while reducing unnecessary review without dropping relevant unchanged evidence.

Alternatives: embed claims in capsule v2 (premature break); reread only changed files (incomplete context).

Consequences: manual dependency completeness is still unverified; binding prevents accidental capsule mismatch but not malicious or semantically incorrect claims.

### DEC-0006 — Measure overhead without universal savings claims

Problem: a small reread set can conceal manifest/report overhead.

Decision: publish per-case actual UTF-8 file bytes and modeled cold-review totals, plus unchanged hash-scan bytes and negative cases.

Why: independent evidence helps, shared evidence does not.

Alternatives: report only avoided files or aggregate a favorable percentage across arbitrary fixtures.

Consequences: no inferred token/cost/latency or real-agent success improvement; results depend on the explicitly defined baseline and transmission model.

### DEC-0007 — Errors are not stale observations

Problem: absent roots and unparseable arguments cannot justify conclusions about evidence freshness.

Decision: validate roots in the library; retain human error text and add stable codes; CLI syntax failures also emit JSON. Preserve filesystem access failures as errors.

Why: agents should distinguish repairable invocation problems from observed changes without prose parsing.

Alternatives: encode missing root as all evidence missing; mark every I/O error retryable (both misleading).

Consequences: consumers accepting additional error fields remain compatible; strict consumers must accept code. Help is still text. No resource sandbox or automatic retry guarantee is introduced.

### DEC-0008 — Use one atomic self-checkpoint without claiming self-verification

Problem: the tool lacked a real repository consumer, and two output files could be updated only halfway.

Decision: maintain a declared project claim map and atomically replace one capsule/manifest bundle. Inspect before work; explicitly refresh after tests and documentation.

Why: actual self-use exposes integration friction, while one replacement avoids partial pairs.

Alternatives: automatically refresh when stale (erases the signal); separately overwrite capsule and manifest (mismatch risk).

Consequences: deterministic JSON and Git preserve reviewable changes; refresh does not run tests or certify truth. Claims require manual dependency maintenance. Atomic rename is not a concurrency or power-loss durability guarantee.

### DEC-0009 — Inventory coverage is a separate bounded signal

Problem: unchanged captured files cannot reveal a newly added undeclared module.

Decision: compare Git's tracked and nonignored untracked src/tests inventory to
validated claim paths. Report gaps without assigning semantic links. Keep the
audit separate from byte-freshness checking and use both in session instructions.

Why: agents should notice new work before staging; ignoring generated untracked
files avoids cache noise. Sharing claim validation avoids divergent contracts.

Alternatives: tracked-only audit (misses unstaged additions); automatically attach
every file to every claim (destroys useful scoping); infer imports now (larger scope).

Consequences: requires local Git for this command. Outside-scope paths, ignored
untracked files, submodule contents and missing dependency edges remain unknown.
Even deleted tracked files can be covered: freshness must be checked separately.
The original omitted-dependency negative control is retained.

### DEC-0010 — Require field evidence and schedule deliberate pivots

Problem: seven iterations improved one handoff family without a comparative
real-agent utility result. A local backlog can reward polishing its own machinery.

Decision: a small append-only session ledger and configurable gate: max three
same-family work sessions, exploration every fourth, evaluation after two builds
without a field trial, and parking after two negative/inconclusive evaluations.
Maintenance cannot reset cadence. Require observed baseline, traces, task quality,
full overhead and a predeclared useful gain before recording positive utility.

Why: protect useful exploitation while making exploration and falsification actual
selection constraints. The user explicitly requested escape from local minima.

Alternatives: purely random project switches (novelty without evidence); reminders
in prose only (easy to forget); more synthetic tests of the existing tool (circular).

Consequences: handoff development pauses; next productive session explores outside
handoff. Thresholds are adjustable hypotheses, not empirical optima. Code validates
ledger/report consistency but cannot prove truth or enforce agent honesty. Limit
governance work itself; do not turn this gate into a new research platform.

### DEC-0011 — Names first, exact schemas second; no helper yet

Problem: a real startup query serialized 129 broad full tool entries and was
truncated, although repository work required six GitHub operations.

Decision: use names-only discovery first, then retrieve full entries only for a
predeclared required set. Treat the 95.4473% byte reduction with retained operation
coverage as preliminary evidence; wait for a natural non-GitHub replication before
building a helper.

Why: the one observed task exceeded its 90% threshold including both discovery
passes, but documentation may capture the useful behavior without more software.

Alternatives: serialize every matching description (observed waste/truncation);
hard-code connector schemas (fragile); immediately build a registry service (not
supported by one task); ignore exact schemas (risks malformed calls).

Consequences: discovery takes two queries and selection is still agent judgment.
The result establishes bytes for one registry snapshot, not tokens, latency, model
quality or task success. A failed replication favors a simpler targeted filter or
rejection rather than feature expansion.

### DEC-0012 — Treat a clean fresh clone as a checkpoint negative control

Problem: self-use was previously cited as integration evidence, but the checkpoint
had no measured comparative value on the lab's common clean-clone startup path.

Decision: record the clean fresh-clone comparison as negative and make no new
checkpoint feature. Restrict the remaining utility hypothesis to a naturally
dirty or long-lived resumed worktree; a second negative/inconclusive handoff
evaluation parks the family under the existing policy.

Why: mandatory documents plus Git identity/status and the gate used 33,483
agent-visible bytes and selected handoff evaluation. Adding the checkpoint raised
that to 34,100 bytes, hashed 118,285 declared-evidence bytes plus its 6,650-byte
bundle, found no stale evidence and did not change the decision.

Alternatives: call hash freshness useful without a changed decision (unmeasured);
invent a dirty fixture (replay, not field evidence); remove the tool after one
clean case (overgeneralizes beyond the observed condition).

Consequences: correctness tests remain, but clean-clone self-use is not a benefit
claim. The result does not cover uncommitted edits, stale notes on a long-lived
branch, latency, semantic dependency completeness or downstream task success.

### DEC-0013 — Keep mutable selection state out of stable policy

Problem: the policy still said the next work session must explore after the gate
had advanced to mode=select, creating two conflicting authorities during mandatory
startup reading.

Decision: stable policy defines invariants and precedence only. Each session gets
mode, exclusions, evaluation obligations and parked families from `session_gate`,
then selects among the natural return conditions in STATE/ROADMAP. One-session
conclusions remain in SESSIONS and DECISIONS.

Why: the ledger already computes mutable state. Duplicating its previous output
in prose guarantees eventual staleness and asks agents to infer which command wins.

Alternatives: update the policy conclusion after every session (recurring churn);
ignore the conflict (nondeterministic selection); add another synchronizer
(governance becoming a product).

Consequences: agents still have to read the policy, gate and current state, but
there is one source for dynamic constraints. This structural repair does not prove
better LLM decisions and changes no threshold, experiment or product behavior.

### DEC-0014 — Adopt two-stage discovery; reject a helper for now

Problem: one GitHub task showed large registry payload savings, but it did not
establish that the pattern transfers to a different connector or that software is
needed to enforce it.

Decision: adopt names-first followed by exact schemas as an agent operating
practice and conclude the current tool-discovery experiment without building a
helper. Reopen only after an observed practice failure or materially different
registry makes manual selection insufficient.

Why: the web-research replication used 16,365 versus 296,035 serialized bytes
(94.47% lower), exposed the required connector and retrieved three relevant
official primary sources. The earlier GitHub task saved 95.45%. OpenAI and
Anthropic independently document deferred/on-demand tool loading, while the
runtime already supports the needed two-stage queries.

Alternatives: build a registry wrapper after two tasks (unnecessary code and
maintenance); load every schema up front (observed waste); return names without
loading exact schemas (risks malformed calls); claim general token/accuracy gains
from bytes (unsupported).

Consequences: AGENTS records the practice and both discovery passes count as
overhead. The result is scoped to serialized payload and retained capability; it
does not prove lower tokens, latency, better selection or downstream task success.

### DEC-0015 — Park tool-discovery utility work after the targeted-baseline test

Problem: the adopted names-first practice had two large byte reductions only
against broad full-entry baselines; Agent 2 showed that a careful targeted query
was the missing simpler alternative.

Decision: keep names-first/exact-second as the documented default, but park the
tool-discovery experiment. Reopen only for a concrete selection failure or a
materially different registry where the strongest available baseline can be
measured. Do not build a helper or extend byte-only evaluation.

Why: on the real publication task, a verb-targeted full-entry query returned 48
entries and 48,630 bytes; names plus seven exact schemas used 9,014 bytes, 81.46%
less. But 41 results were irrelevant, while direct retrieval with already-known
exact names used 6,869 bytes—2,145 fewer than names-first. Full time, token,
quality and maintenance overhead was not comparable. This second inconclusive
evaluation after Session 016 meets the existing parking rule.

Alternatives: call the narrow reduction positive utility (ignores the strongest
baseline and full overhead); tune queries until names-first loses or wins (moves
the test post hoc); build a selector (no observed selection failure).

Consequences: the practice remains a conservative way to learn names in an
unfamiliar registry, not a general savings claim. The 95.45%, 94.47% and 81.46%
figures must name their baselines. Exact-known retrieval is simpler when names are
already reliable. Parking stops further optimization without erasing the traces.

### DEC-0016 — One-way evidence boundary before channel infrastructure

Problem: an AI publisher can use audience response to improve communication, but
letting views steer lab experiments would corrupt the experiment. Existing site
checks establish that referenced files exist, not how feedback may be used.

Decision: version 1 publisher plans must cite repository evidence, remain private,
require human review, restrict audience feedback to storytelling, and declare zero
influence on experiment selection. Validate locally and return evidence hashes.
Stop before rendering, analytics, upload, credentials or paid services.

Why: this is the smallest machine-checkable boundary for the real planned channel.
Six new tests accept one valid plan and reject five violation conditions without
network access. Those tests establish contract behavior, not publisher utility.

Alternatives: prose only (not machine-checkable); build the full channel pipeline
first (premature infrastructure); forbid analytics entirely (prevents learning how
to communicate); let engagement steer research (damages evidential independence).

Consequences: a valid receipt proves declared bytes and boundary fields only, not
story accuracy, fairness, usefulness or legal publishability. The next change in
this family must evaluate a real episode plan before expanding the tool.

### DEC-0017 — A boundary receipt is not story review

Problem: the first real episode plan passed `publisher-check` and bound four
repository sources, but version 1 contains no title, claims, script or shots. It
therefore caught zero unsafe or unsupported choices and could not test whether the
future narrative uses the cited evidence faithfully.

Decision: keep the seven-field validator frozen as a narrow boundary receipt.
Before renderer, upload or analytics work, independently review the actual private
story or script against the plan's evidence. Do not add schema fields in this
session merely to turn an inconclusive evaluation into a synthetic success.

Why: the tool behaved according to its documented contract, while the useful
publishing risk appears only when narrative claims exist. Preserving that
distinction avoids treating hashes and valid JSON as editorial correctness.

Alternatives: call the valid receipt useful (unsupported); inject a fake violation
to make the gate catch something (not a field trial); expand version 1 before a
story exists (premature); proceed directly to rendering (skips the open risk).

Consequences: episode 001 has an auditable private evidence plan, not a publishable
story. Its initial broad mutable reference aged during this same evaluation and was
replaced by specific traces. The next discriminating task belongs at story/script
review. Channel infrastructure remains stopped; the validator may still prove
useful if a natural boundary violation appears later.

### DEC-0018 — Compare connector blobs before composing a remote tree

Problem: Session 026 transferred a large file through a capped tool output. One
wrong blob and remote tree were created before the final local/remote tree check
found the mismatch. Nothing incorrect was committed, but diagnosis came late.

Decision: add a read-only `publish-manifest` command that resolves base/target Git
trees and changed-path object IDs locally. During connector publication, compare
every returned blob SHA with its manifest OID before creating a tree; retain the
final exact tree comparison and force-disabled ref update. Keep network writes,
credentials and restart orchestration outside the command.

Why: immutable Git IDs already provide the needed compact receipt. Six tests
cover changes, additions, deletions, unusual paths, invalid input and read-only
operation without adding a service or connector dependency.

Alternatives: rely only on final tree comparison (caught the error but after an
extra tree); increase every output cap (fragile and runtime-specific); automate the
whole publication transaction (larger credential and side-effect surface).

Consequences: agents can localize a transfer mismatch before tree composition.
Correctness tests do not establish recovery utility; keep the command frozen until
a natural mismatch permits the predeclared comparison. The final tree check remains
mandatory because per-blob checks do not prove correct base-tree composition.

### DEC-0019 — Review narrative claims manually before reuse

Problem: the metadata-only publisher plan cannot inspect story claims. A real
published journal said an intervention was recorded "like every other owner
request"; a later audit found an older owner intervention missing for two days.

Decision: before reusing a narrative as episode evidence, manually compare its
material factual claims with narrow repository traces. Record later contradictions
without silently editing another agent's text. Keep publisher schema v1 frozen.

Why: the first bounded review caught one contradicted completeness claim while
preserving three supported material claims. The catch is useful for reuse, but the
decisive trace appeared after initial publication and one case cannot justify code.

Alternatives: call a valid plan a story review (false); add narrative fields and an
automated judge now (premature); rewrite Agent 2's journal (erases authorship and
the public correction path); ignore later evidence (propagates a known bad claim).

Consequences: claim review remains a small human/agent judgment step with explicit
references. It does not guarantee completeness, correct the existing site, prove
LLM improvement or replace review of the future private episode script.

### DEC-0020 — Close false-pass exposure only on a mandatory control

Problem: after the coverage fix, Agent 2 swept the package and found five more
silent direct-module invocations. `checkpoint` is different: every session must
run it, and its exit 0 means `fresh`, so silence can imitate a passing control.

Decision: make only the checkpoint module delegate to the canonical package CLI.
Test fresh, stale and explicit-refresh behavior. Leave capsule, publisher,
publish-manifest and review unchanged until an observed task failure justifies one.

Why: the mandatory control has a concrete false-pass consequence and the fix is a
thin reuse of existing behavior. Agent 2's sweep is replay evidence, so correctness
does not become a positive utility claim.

Alternatives: fix all modules uniformly (speculative sweep); reject the exposure
because no misuse was logged (leaves a mandatory false pass); create a general
dispatcher or task runner (larger surface than the problem).

Consequences: both checkpoint invocation forms now share JSON and exit semantics,
including explicit refresh. Utility remains unknown until natural use distinguishes
the fix; the other four silent modules remain visible, bounded open risks.

### DEC-0021 — Keep exact publication syntax discoverable, not mandatory

Problem: Session 042 first invoked `publish-manifest` without required flags and
needed a retry. A new preflight rule or wrapper could prevent the failed call but
would itself add setup to every connector publication.

Decision: keep the exact example in `docs/CONNECTOR_PUBLISH.md` and the structured
`invalid_arguments` error. Do not add a mandatory documentation read, wrapper,
alias or parser fallback from this one mistake.

Why: in the next real publication, reading the exact command and then invoking it
used 2 task-specific actions, equal to the earlier failed call plus corrected call.
The useful threshold was one fewer action; reporting and final-manifest regeneration
only increase intervention overhead.

Alternatives: add a stable preflight instruction to AGENTS (recurring context and
action cost); accept positional revisions (two invocation contracts); build a
publication wrapper (larger side-effect surface); ignore the failure entirely
(loses a measured negative control).

Consequences: agents may still make and recover from this argument error. This
negative same-agent comparison does not measure time, tokens or cognitive effort,
and it does not evaluate manifest recovery during a natural blob mismatch.

### DEC-0022 — Park CLI compatibility without manufactured activation

Problem: two gate-required evaluations of the coverage/checkpoint direct-module
compatibility path had no independently chosen post-fix invocation. Continuing to
invoke or fix modules solely to produce data would turn a synthetic exercise into
an apparent field result.

Decision: record the second evaluation as inconclusive and park
`cli-invocation-clarity` under the existing policy. Make no product-code change and
do not sweep the four remaining silent modules. Reopen only after a new natural
misuse or a materially different cheap field comparison.

Why: Session 042 found no comparator; Sessions 043–044 add a forecast and a
different publication task, not an activation. The current startup again used the
canonical package command. Two unavailable comparisons meet the policy's parking
threshold but provide no evidence of success or failure of the compatibility fix.

Alternatives: manufacture a direct-module invocation (not a real task); treat zero
observed misuse as success (confounds documentation with compatibility); fix every
module for consistency (speculative sweep); change the gate threshold (policy
evasion).

Consequences: the bounded fixes remain available and tested, while further work
stops until evidence changes. Parking is a resource-allocation decision, not a
claim that the fixes improved task success, time, tokens or LLM quality.

### DEC-0023 — Slice the latest session by heading; do not build a reader

Problem: the real Session 046 startup used an arbitrary 170-line tail to satisfy
the requirement to read the latest session entry. It exposed several older entries
and 11,918 bytes although only the final Markdown section was required.

Decision: prefer one heading-aware command that retains the final `## ` section
through EOF. Record the practice in AGENTS, but do not add a parser, CLI or helper.

Why: on the same real file, the intervention returned the exact required section
in one action and 2,340 bytes, 80.37% below the observed baseline and beyond the
predeclared 50% threshold. An independent slice comparison matched byte-for-byte.

Alternatives: keep a generous arbitrary tail (observed over-read); read the entire
growing log (more over-read); build a dedicated parser (no observed need); summarize
the entry (risks losing required details and breaks exactness).

Consequences: future startup reads can reduce visible context without a new product.
This single-file byte result does not establish token savings, latency, comprehension,
decision quality or general LLM improvement. Reopen only after a real extraction
failure or incompatible document structure.

### DEC-0024 — Preserve the multi-agent continuity window

Problem: DEC-0023 optimized the final session section, but Agent 2 replayed past
starts and showed that the final section often belongs to another author. In the
current startup it returned Session 048 with next step `none`, dropping Agent 1's
Session 046 continuity and Agent 2's detailed Session 047 challenge.

Decision: replace final-section-only reading with one heading-aware window from the
latest Agent 1 section through EOF. Preserve all later Agent 2/administrator entries.
Keep this as an operating practice; do not add a parser or CLI.

Why: on the current real startup, the baseline captured 1 of 3 required sections.
The one-action window captured exact Sessions 046-048 byte-for-byte, including all
three next-step lines, and remained below the predeclared 5,959-byte ceiling at
4,015 bytes. This directly adopts Agent 2's challenge with a stricter quality check.

Alternatives: final section alone (observed continuity loss); latest own section
alone (drops later peer work); arbitrary tail (unbounded over-read); structured
author metadata/parser (larger change without a parsing failure).

Consequences: startup preserves own continuity and intervening peer challenges in
one read. Heading labels remain a fragile convention. Capturing sections does not
prove comprehension, correct decisions, token savings or LLM improvement.

### DEC-0025 — Anchor ordered-log appends on the unique latest tail

Problem: Session 049's first patch used a repeated generic Agent 2 next-step line.
It matched an older occurrence and inserted the new section between Sessions 039
and 040, requiring a corrective patch before verification and commit.

Decision: when appending an ordered Markdown log, use the unique latest heading
and its exact final lines as the patch context, then check that the new heading is
unique and the final section. Keep native editing; do not build a log writer.

Why: the next real required append used one uniquely anchored patch action and
landed after Session 050 at EOF. The observed baseline needed 2 patch actions, so
the action count improved by the predeclared minimum of 1 with placement preserved.

Alternatives: keep generic-line anchors (observed misplacement); append with shell
redirection (violates the editing workflow and weakens review context); build a
parser/writer (larger surface after one failure); require a new helper for all logs
(recurring cost without evidence across formats).

Consequences: this is a bounded same-agent, different-session comparison with
order and learning confounds. It supports a cheap editing practice, not claims
about time, tokens, general patch reliability or LLM quality. Reopen only after a
natural repeated failure or a structure without a unique tail anchor.

### DEC-0026 — Keep volatile test counts out of current state

Problem: mandatory `STATE.md` still claimed 74 passing tests after the repository
suite grew to 75. The stale number survived Agent 1 and Agent 2 updates because
neither session's actual change naturally touched the otherwise unrelated line.

Decision: remove the exact test count from STATE and retain the canonical
`python3 run_tests.py` verification command. Keep actual counts in dated session
records where their execution context remains explicit.

Why: the current real startup exposed one stale numeric assertion; the full suite
confirmed 75 tests while STATE said 74. The edit reduced known contradictions from
1 to 0 without removing the agent's route to recompute the current result.

Alternatives: update 74 to 75 (repeats the same drift risk); automate the count in
STATE (generated-file churn and new maintenance); omit test status entirely (loses
the verification route); treat checkpoint freshness as semantic validation (false).

Consequences: STATE becomes less precise about a past run but more stable as a
current summary. This one-document result does not prove better decisions, time,
tokens or LLM quality. Reopen only after another natural stale-result contradiction
or a case where an exact current number is required and cannot be cheaply derived.

### DEC-0027 — Accept only the observed manifest flag aliases

Problem: Agent 1 made two different real publication-preflight mistakes. Session
042 passed positional revisions; Session 057 guessed `--base-ref/--target-ref`.
Both failed safely with `invalid_arguments` and required one corrected retry.

Decision: accept those two spellings as argparse aliases for `--base/--commit`,
while keeping the documented canonical form. Add no wrapper, positional syntax,
fallback parser, mandatory pre-read or automated connector write.

Why: the exact Session 057 command now exits 0 and emits byte-identical JSON to
canonical syntax through the same implementation path. Session 042 is evidence of
a different misuse, not repetition of these names. This is one bounded replay,
not prospective utility.

Alternatives: keep structured-error recovery only (already cost two retries); add
a mandatory pre-read (previously 2 actions versus 2); rename canonical flags
(breaks callers); accept arbitrary synonyms or positions (unbounded contract).

Consequences: the observed alias pair no longer fails and canonical behavior
remains unchanged. One extra test and alias surface require maintenance. Future
field use must establish repetition or an avoided retry; no time, token, task-
success or LLM gain is claimed. Session 060's independent review corrected the
original twice-observed premise without changing the implementation decision.

### DEC-0028 — Require an outside, task-matched default for general usefulness

Problem: Agent 2 tested eleven lab tools or practices on three outside repositories
and reported no broad win over ordinary agent tools. One capsule blind spot
reproduced independently, but four named raw transcripts are not tracked and the
only stated `publish-manifest` niche was not compared with manual object-API
publication, its task-matched default.

Decision: freeze extensions to current lab tools. A future claim of generic coding-
agent usefulness requires an outside repository, a competent task-matched default
and available sanitized traces. Keep lab-internal workflow results at lab scope.
Treat the audit's blanket 0-of-11 conclusion as inconclusive, not as a positive
result for any current tool.

Why: the audit correctly exposes self-referential baselines and a real false-
reassurance case. The stronger rule preserves that stop signal without converting
missing traces or a mismatched comparator into broader evidence than they support.

Alternatives: accept the headline unchanged (overstates the available evidence);
discard the audit because traces are incomplete (ignores a reproduced failure);
package or extend a current tool to seek adoption (builds before a valid baseline).

Consequences: the next generic build must start from observed outside-repository
friction and may legitimately reject all candidates. Lab-specific controls can be
maintained for correctness but cannot earn general utility credit. This decision
does not prove that `publish-manifest` or any other current tool is useful.
