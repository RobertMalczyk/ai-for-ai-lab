# State

- Exists/works: capture/check/link/review with machine-readable errors; 6 correctness and 5 byte-cost diagnostic cases; 31 passing tests.
- Limits: No hostile-input resource budget or concurrency guarantees; manual dependency completeness and semantic validity remain unverified.
- Focus: Make unchecked inputs distinguishable from stale evidence.
- Next: Use the tool on its own project: add a reproducible repository checkpoint with claim-to-source/test links, document check-before-refresh, and test a copied-checkout edit flags only the expected claims.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
