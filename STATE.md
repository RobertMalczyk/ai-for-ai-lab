# State

- Exists: handoff/checkpoint tools, experiment gate, a no-setup test entrypoint
  and three bounded field reports; 60 passing tests.
- Value: names-first/exact-second remains a practice, not a utility claim. It was
  81.46% smaller than one verb-targeted query, but that query returned 41 irrelevant
  entries and exact-known retrieval was 2,145 bytes smaller. Checkpoint remains
  negative only for clean fresh clones.
- Focus: tool discovery is parked after two inconclusive evaluations; handoff is
  the only active experiment and waits for a dirty/long-lived resume.
- Selection source: live session_gate constraints, then STATE/ROADMAP return conditions; stable policy carries no one-time next-session command.
- Next: run session_gate. Revisit handoff only on a natural dirty/long-lived
  resume; otherwise observe fresh workflow friction before one new experiment.
- Return/stop: reopen runner or tool discovery only after a concrete field failure;
  another negative/inconclusive handoff evaluation parks it. Branch tooling needs failure.
- Verify: `python3 run_tests.py`.
- Canonical: RobertMalczyk/ai-for-ai-lab; read AGENTS.md, fetch main and inspect agent branches before work.
