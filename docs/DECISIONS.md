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
