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
