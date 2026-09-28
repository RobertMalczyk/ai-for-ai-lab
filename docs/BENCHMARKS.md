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

## Scoped review byte accounting

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab.review_benchmark
```

Five controlled cases use a=2048 UTF-8 bytes (1024 alpha characters), b=4096,
c=8192. Claim AB depends on a+b; C depends on c. The shared-dependency case also
makes C depend on a. Edits append one byte. The baseline hashes first, then
rereads all available capsule files if any evidence changed. Scoped review reads
all dependencies of affected claims. Both skip content rereads when unchanged.

| Case | Baseline file bytes | Scoped file bytes | Modeled total bytes avoided |
| --- | ---: | ---: | ---: |
| unchanged | 0 | 0 | -273 |
| isolated edit | 14337 | 6145 | 7913 |
| shared dependency | 14337 | 14337 | -284 |
| deleted | 12288 | 4096 | 7914 |
| all changed | 14339 | 14339 | -288 |

Modeled total includes one compact capsule, one result report, and selected file
contents; scoped review additionally includes its full manifest. UTF-8 bytes
are measured, not tokenizer tokens. JSON serialization overhead excludes shell
newlines, tool wrappers and prompt instructions. Results assume cold inputs are
sent once, without cache savings. Hash scanning still reads every available
evidence file for both strategies; this is not a disk-I/O or latency win claim.

Scoped review helps only when independent evidence can be skipped. It costs more
in the unchanged, shared-dependency and all-changed cases. No aggregate percentage
is reported: fixture frequency is not a workload distribution. No model ran.
