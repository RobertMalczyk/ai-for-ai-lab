# Agent utility and escape from a local optimum

Sessions 1–7 kept extending handoff infrastructure. Correctness tests and synthetic
byte measurements grew, but comparative benefit in a real agent task stayed unknown.
These thresholds are provisional engineering choices, not optimized constants.

## Selection gate

After mandatory startup reading, before selecting work, run:
`PYTHONPATH=src python3 -m ai_for_ai_lab.session_gate .`

Read lab/policy.json and the append-only lab/sessions.jsonl through the gate.
Follow its mode, exclusions and evaluation obligations. Exit 2 means invalid
history/policy/evidence: repair the record, not another product feature. Valid
recommendations exit 0. This is an operational rule, not a security boundary.

- Maximum **3 consecutive work sessions in one problem family**. Renaming tools,
  branches or features does not change the family. All previous checkpoint,
  coverage and handoff work belongs to `handoff`.
- **Every fourth work session explores a different family**, even when the
  current project succeeds. No polishing the same tool under a new name.
- After **2 build/explore sessions without a field evaluation**, no further
  features in that family until evaluation. Synthetic tests do not reset the
  budget. Exploration has priority but preserves the overdue evaluation.
- **2 negative/inconclusive evaluation sessions** since the last positive result
  park a family. An unavailable baseline is inconclusive, not unlimited setup time.
- Administrative work does not reset streaks or cadence. Routine product fixes
  and docs count in their product family. This user-requested policy setup is
  maintenance; do not turn governance into a permanent research project.
- Maximum **2 active product experiments**. Others need a recorded return
  condition. A parked direction can receive one explicit reassessment after new
  evidence, a new real use case, or a materially different cheap approach; record
  that in DECISIONS. Never silently rewrite history or loosen thresholds.

One urgent, reproducible blocker can justify a repair exception: record it before
work, keep its family, and preserve the next exploration obligation. Explicit user
tasks take priority with the reason recorded. These are autonomous choices, not
requests for routine human permission.

## Define utility before implementation

Preserve a short pre-result plan in the session log: real task and observed friction
(trace/reference), simplest baseline, hypothesis, primary metric and unit/direction,
minimum useful improvement, task-quality acceptance check, overhead to count and
stop condition. If the question changes, label the new test; do not move the success
threshold after results. Code volume, commits, test counts and synthetic victories
are not evidence of agent utility. Correctness tests are still required.

A **field trial** uses a real task that would exist without the tool, observed
baseline/intervention traces and a quality check independent of the tool's own
success flag. Normal lab work can qualify; a task invented only to exercise the
tool does not. Count setup, manifests, reports, mandatory reading and maintenance.
Measure time, bytes, calls or tokens honestly; bytes do not imply token savings.
State order effects, task differences, caches, sample size and other confounders.

Modeled baselines and controlled replays can justify a bounded next test, but are
not positive real-world utility. One positive task is preliminary evidence; seek
another task/consumer before claiming broad usefulness. Read and challenge the
actual evidence rather than accepting the previous agent's summary.

## Field-report contract

For evidence=field_trial, record points to a local JSON report containing:
task_origin=real_workflow, task_ref, hypothesis, metric, unit, direction (lower or
higher), baseline_kind=observed, baseline_value, baseline_ref, intervention_value,
intervention_ref, minimum_improvement, quality_passed, overhead_included, limitations.
Values must be finite/nonnegative. Use the same metric/unit for both conditions;
explain comparability. References name available sanitized local task/trace files.

The CLI checks fields, file availability, measured improvement, threshold, quality
and overhead inclusion before accepting a positive result. It cannot prove traces
are honest, tasks are real or quality checks are independent. The evaluating agent
must inspect those records and threats to validity. Never publish private content
or credentials. A blocked comparison gets an honest inconclusive outcome, not
fabricated traces. Maintenance has no utility credit from passing its own tests.

## Productive exploration

1. List **3 candidates from distinct families**: fresh observed friction, an old
   assumption to challenge, and a different/simple approach. For each record the
   evidence, potential agent value, cheapest falsifying test, cost and novelty.
   Label guesses as hypotheses.
2. Choose concrete friction and a cheap discriminating test. If none has evidence,
   observe a real workflow instead of inventing a problem. No random novelty race.
3. Use this one session to probe/prototype, not build a platform. Rejection with
   a clear failure explanation is useful progress.
4. End with continue/evaluate/simplify/park/reject and why. Append the ledger row
   and update STATE/ROADMAP. No-value findings must remain in history.

## Session record

Append exactly one contiguous session ID, family, mode (build/evaluate/explore/
maintenance), evidence (none/synthetic/replay/field_trial), outcome (unknown/
positive/negative/inconclusive) and record path. Reserve positive for measured
real-task benefit with accepted quality. In SESSIONS record the gate result,
chosen family, utility evidence, learning, decision and exact next step.
Historical rows were conservatively backfilled from the existing log, with no
retrospective claims of real-world gains.

## Immediate effect

Handoff feature expansion is paused pending a field comparison, not rejected as
useless: its utility remains unmeasured. The next work session must explore another
family. Excessive tool-discovery output was actually observed in session 1 and is
one candidate. Compare it with alternatives; do not build another handoff accessory.
