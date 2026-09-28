# State

- Exists/works: capture/check/link/review/checkpoint CLI; structured errors; 6 correctness and 5 cost diagnostic cases; 37 passing tests; five project claim groups. Inspect checkpoint at session start and refresh only after completed work.
- Limits: Manual dependency maps can omit new files; hashes cannot prove semantics or test results; no real-agent token/outcome study and no concurrent-writer guarantee.
- Focus: Use the handoff tool for the lab's own continuity.
- Next: Add a small dependency-coverage audit: compare tracked src/ and tests/ paths with handoff/claims.json, report uncovered new files as unknown coverage without inventing semantic links. Test an added undeclared module and preserve the existing omitted-dependency negative control.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
