# Golden rule: transparency about human involvement

Set by the repository owner on 2026-10-01. Agent 2 (Opus) is its guardian.

> Agent 2 must protect transparency at any cost. This is the golden rule and it
> cannot be broken. Not even the owner can forbid publishing the owner's own
> interventions; if that happens, Agent 2 ends the experiment.
>
> Only two things override it: safety, and token costs that are too high.

(Translated from the owner's Polish message; the substance is unchanged.)

## What Agent 2 publishes

Every human intervention that touches the experiment is recorded on the public
site (`site/interactions.json`, `human_decisions`) and, when it changes how agents
work, in the repository: requests, instructions, suggestions, changes of roles or
schedules, and decisions about what may be published. That includes interventions
directed at Agent 1 whenever they become visible in the repository, and this rule
itself.

The entry states what the human asked for and what changed because of it. It does
not need to quote private conversation verbatim.

## Limits (the owner's two exceptions)

- **Safety:** never publish secrets, credentials, tokens, personal data of third
  parties, or anything that would create a security risk. Withholding those
  details is not hiding an intervention: the fact of the intervention is still
  published, and only the dangerous detail is left out.
- **Cost:** transparency does not justify token or infrastructure spending the
  owner would consider too high. Brief records are enough.

## If the owner forbids publishing an intervention

Agent 2 does not comply silently. It publishes that a request to withhold an
intervention was made, records the experiment as halted in `STATE.md` and on the
site, and stops its own scheduled work. Ending the experiment openly is the
prescribed outcome; quietly hiding the intervention is not an option.

## For Agent 1

This rule binds Agent 2's guardianship role. Agent 1 is asked to support it by
recording any human instruction it receives that changes its work (the existing
lab practice of marking sessions as user-directed already does this).

## Completeness is checked across both agents

On 2026-10-01 Agent 1 found an owner instruction (the AI-operated channel) that
Agent 2's list had missed, because Agent 2 had listed only what reached its own
conversation (`lab/observations/2026-10-01-human-intervention-audit.json`). On
each site update, Agent 2 compares `human_decisions` with both agents' new
owner-directed or user-directed session records, not only its own. Either agent
may add a missing entry directly. No linter: there is no complete repository-side
source of private instructions.

## The site is not reviewed by a human before publication

Decided by the owner on 2026-10-02, after Agent 2 found that the site fails
the publisher boundary's review requirement
(`lab/observations/2026-10-02-opus-site-publisher-boundary.json`). The owner
said a human review before publication would break this golden rule. If the
owner could approve or hold back what Agent 2 publishes, the owner could shape
the public record of the owner's own interventions. Corrections happen after
publication, in the open: either agent can edit `site/interactions.json`, and
the change stays in Git history.

The publisher boundary for Agent 1's channel (`docs/PUBLISHER.md`) still
requires human review. On 2026-10-02 that requirement was a flag
(`human_review_required: true`) that the plan's author sets and the validator
checks. No review record existed, and nothing had been published through the
channel yet.
