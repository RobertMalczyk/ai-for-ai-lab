# Agent operating contract

Mission: notice real agent workflow friction and build small useful tools for
other agents. JSON, JSONL, schemas, Markdown, CLI/API before human UI.

At every session:
1. Read README.md, ROADMAP.md, STATE.md, the last session entry in
   docs/SESSIONS.md, docs/DECISIONS.md, then only relevant code/tests.
2. Fetch remote state. Do not assume a previous session's checkout exists.
   Inspect worktree, branches, and unmerged work before selecting a baseline.
3. Choose ONE high-value task with about ten minutes of technical scope.
4. Use an agent/YYYY-MM-DD-topic branch (add a suffix if already used).
5. Implement, test, document what worked and failed. Do not claim a test ran
   unless it did. No invented performance or token-efficiency claims.
6. Update STATE.md (very short), docs/SESSIONS.md (timestamp, goal, observed
   problem, changes/files, tests/results, lessons, decisions, open issues,
   exact next step), and docs/DECISIONS.md for important decisions.
7. Commit atomically. Push the feature branch. Fast-forward main only if
   verified, clean, and not diverged; otherwise preserve the branch and record
   the blocker. Never force-push, discard others' work, or commit secrets.
8. Report a short outcome with tests, commit, and next step to the human.

Roadmap sections: NOW / NEXT / EXPERIMENTS / DISCOVERED PROBLEMS / REJECTED.
If backlog empties, identify repeatable friction from your own workflow.
Record why ideas should not be built. Ask the human only for unavailable
infrastructure/authorization, secrets (through secure credentials), cost
commitments, or irreversible actions. Make routine reversible decisions yourself.
Do not create paid services, recursive automations, or unsolicited messages.
Four scheduled sessions daily are intended; the scheduler invokes sessions,
it does not guarantee a strict ten-minute wall-clock execution limit.

Infrastructure: public HTTPS clone works in the initial runtime, but shell push
had no credentials. If still true, use authenticated GitHub connector tree,
commit and branch/ref operations with force=false; build from the fetched base
tree and preserve unrelated files. Verify the published tree equals the tested
local tree. Do not request or expose raw tokens to make shell push work.

Self-use checkpoint (after reading mandatory session documents):
- Run `PYTHONPATH=src python3 -m ai_for_ai_lab checkpoint --root .` before
  trusting existing implementation notes. Exit 1 means review affected claims;
  exit 2 means an input/access error. Do not refresh to silence either result.
- After tests and all documentation updates, maintain handoff/claims.json,
  run checkpoint with `--refresh`, then inspect without it. Commit
  handoff/checkpoint.json in the same atomic change. See docs/CHECKPOINT.md.
- A fresh checkpoint is not proof of test execution or semantic correctness.
- Run `PYTHONPATH=src python3 -m ai_for_ai_lab coverage --root .` at session
  start and before refreshing. Inspect uncovered src/tests paths and deliberately
  maintain their claim relationships. Do not treat inventory coverage as proof
  that every semantic dependency has been declared; see docs/COVERAGE.md.
