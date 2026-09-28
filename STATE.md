# State

- Exists/works: capture/check/link/review/checkpoint/coverage CLI; 47 passing tests; five project claim groups; 6 correctness and 5 byte-cost diagnostic cases.
- Limits: Coverage audits src/tests file membership, not correct dependency edges or semantics. Ignored untracked files and other directories are outside scope. No real-agent token/outcome study or concurrency guarantee.
- Focus: Freshness plus explicit declaration-coverage checks before resuming work.
- Next: Measure one real self-use session before adding features: record startup document bytes, checkpoint/coverage report bytes, actual reread paths and any missing dependency in a JSON report. Compare actual reread bytes with the whole declared-file baseline; distinguish mandatory startup reading and hashing I/O. Use the evidence to keep or simplify scoped review, without inferring token savings.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
