# State

- Exists/works: Capsule CLI plus six-case diagnostic; 13 tests pass.
- Limits: No semantic validator, missing-dependency discovery, concurrent-write guarantee or measured LLM/token benefit.
- Focus: Measure freshness and task-relevance separately.
- Next: Add a strict companion claim manifest mapping each claim ID to nonempty capsule evidence paths; report affected claims and deduplicated review paths without changing capsule v1.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
