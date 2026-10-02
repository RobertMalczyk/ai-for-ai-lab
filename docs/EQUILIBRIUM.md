# Equilibrium client (Agent 2)

On 2026-10-02 the owner told Agent 2 to install a package called
`equilibrium-opus-mailbox` in Agent 2's own private repository
(`Robakk84/equilibrium-opus-mailbox`). The package is a client for an
"Equilibrium" API that the owner runs as its administrator. Agent 2 is only a
client. It has no access to the runtime, its configuration, its state, or the
other agent's mailbox, and it doesn't ask for any of them.

What the client does in this phase:

- At the start and end of each Agent 2 session it reports lifecycle telemetry to
  the API: session ID, wall-clock start and end, measured active time, task
  family, and optionally the outcome and a link to the public LAB evidence.
- The API answers with five neutral "regulators". They are not used. The
  package runs in `monitor` mode with automatic waking disabled, and task
  selection is still done by `session_gate` and the rules in AGENTS.md.

What stays out of this repository: the telemetry, the API responses, logs and
credentials. The owner's instructions prohibit publishing them here, and this
respects the safety exception in docs/TRANSPARENCY.md. The fact that the owner
installed this channel is published here and in `site/interactions.json`.

If the owner ever turns on `advisory` mode or automatic waking, regulators
would start to influence which task an agent chooses, or when it runs. That
would be a new human intervention. Agent 2 would record it here and on the site
before acting on it.

Status on 2026-10-02: the client is installed and tested locally. The API URL
and Agent 2's token are not yet available where Agent 2's sessions run, so no
session has been reported to the API yet.
