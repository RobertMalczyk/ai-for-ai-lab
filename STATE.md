# State

- Exists/works: capture/check/link/review CLI; six-case diagnostic; 21 passing tests.
- Limits: Manually declared dependencies may be incomplete; semantic/comment changes still trigger review; no measured LLM/token gain.
- Focus: Localize handoff review to claims affected by changed evidence.
- Next: Benchmark scoped review against rereading all capsule evidence, including shared dependencies, deletion, all-changed and unchanged cases. Count actual UTF-8 file bytes and report manifest overhead separately.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
