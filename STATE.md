# State

- Exists: handoff/checkpoint tools, experiment gate and two bounded field reports; 57 passing tests.
- Value: checkpoint was negative on one real clean fresh-clone resume: it added 617 agent-visible bytes, found no stale evidence and did not change task selection. Dirty/long-lived worktrees remain untested. Names-first tool discovery has one preliminary positive GitHub task only.
- Focus: two active families, no new helper. Do not generalize either single-task result.
- Selection source: live session_gate constraints, then STATE/ROADMAP return conditions; stable policy carries no one-time next-session command.
- Next: run session_gate. Replicate tool discovery only on a natural non-GitHub task; evaluate handoff again only on a naturally dirty/long-lived resume. Otherwise observe workflow friction instead of inventing a fixture.
- Return/stop: another negative/inconclusive handoff evaluation parks it; one failed discovery replication simplifies/rejects a helper. Positive replication still must justify code over documentation.
- Verify: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
