# The lab uses its own handoff tool

Start after the required session documents, before trusting implementation notes:
```bash
PYTHONPATH=src python3 -m ai_for_ai_lab checkpoint --root .
```

Exit 0: declared evidence unchanged, not an assertion that the code is correct.
Exit 1: inspect affected claims and their dependencies. Keep the old baseline
while investigating. Exit 2: repair the input/access error; don't silently refresh.

After the scoped work, tests, and ALL documentation updates:
```bash
PYTHONPATH=src python3 -m ai_for_ai_lab checkpoint --root . --refresh
PYTHONPATH=src python3 -m ai_for_ai_lab checkpoint --root .
```

Commit handoff/checkpoint.json with the same change. Refresh is an explicit
baseline replacement, not a validation step; it neither runs tests nor certifies
claims. Never refresh merely to silence a stale result. Claims are maintained in
handoff/claims.json and the manifest stores the old declarations, so editing the
claim map itself is detectable before refresh. Add newly relevant paths there.
Run `coverage --root .` before refresh to find undeclared src/tests files;
see docs/COVERAGE.md. Checkpoint freshness alone cannot detect such additions.

One deterministic JSON bundle contains version=1, capsule and manifest. The
writer stages a temporary file in the same directory, flushes it, then replaces
the target atomically. This avoids a half-updated capsule/manifest pair on process
failure. Concurrent writers and power-loss durability are not guaranteed. Git is
the history; no timestamps or redundant commit IDs are embedded in the bundle.
The checkpoint must never reference itself. All dependency maps are manually
maintained, not automatically complete. Session history is read separately; only
current state/roadmap/decisions and declared code/tests enter this checkpoint.

This is a real project integration, but edited-checkout tests are still controlled
replay, not proof of lower costs or better success for autonomous agents.
