# Synthetic diagnostics

Run from the repo root:
```bash
PYTHONPATH=src python3 -m ai_for_ai_lab.benchmark benchmarks/recovery_cases.json
```

Six fixtures start with config limit=10, no policy override, and an unrelated
note. Capture deliberately selects only config.txt. Labels are manually defined
by fixture authors: byte_stale means selected bytes changed; task_stale means
the assumed effective limit can no longer be reused. A comment is irrelevant to
the limit; an override in uncaptured policy.txt is relevant but invisible.

Initial results: all 3 selected-byte changes detected; 0 false byte alarms.
Against task-relevance labels: 2 stale cases detected, 1 missed (omitted policy),
1 unnecessary invalidation (comment), 2 correctly fresh. Blind trust misses all
3 task-stale cases. These constructed cases demonstrate boundaries, not population
accuracy, token savings, latency reduction, or success rates of actual LLM agents.
Do not optimize away the counterexamples by relabeling them.

Next hypothesis: explicit claim-to-file links can localize review to affected
claims. They cannot discover missing dependencies or prove semantic correctness.
