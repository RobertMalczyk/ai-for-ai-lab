# State

- Exists: Python stdlib handoff capsule CLI (`src/ai_for_ai_lab`), v1 contract,
  11 passing unittest tests, operating rules and hypothesis roadmap.
- Works: capture selected file hashes; check unchanged/changed/missing evidence;
  compact JSON and exit codes 0/1/2; reject unsafe paths and malformed capsules.
- Limits: no semantic validity, external evidence, concurrent-write guarantees,
  or measured recovery/token gains. No dependencies beyond Python 3.10+.
- Current focus: determine whether freshness detection improves resumption.
- Next: add deterministic recovery fixtures (unchanged, edited, deleted,
  unrelated edit); compare blind-trust baseline vs checker; emit JSON counts
  for stale detection and unnecessary invalidation. No model API needed.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical repo: RobertMalczyk/ai-for-ai-lab; fetch main and inspect agent
  branches before starting. Read AGENTS.md for session and Git rules.
