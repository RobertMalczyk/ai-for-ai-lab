# Day-14 narrative claim audit

Scope: `site/journal/2026-10-13.md`, reviewed after Session 117 and before reuse
as LAB evidence. This is a repository-trace audit, not an external-state check.

| # | Material claim | Classification | Narrow repository evidence |
|---|---|---|---|
| 1 | Open pytest PR #14777 already contained the same fix. | supported | `lab/observations/2026-10-12-opus-pytest-14777-comparison.json` records the fix as identical in substance. |
| 2 | The lab's async-trigger regression was not covered by that PR. | supported | The same comparison record and its tracked `async-test.diff` distinguish the missing trigger. |
| 3 | The owner posted the disclosed comment and this was the LAB's first external contribution/result. | supported | `site/interactions.json` records the owner action, URL, disclosure condition and first-result classification; `lab/tasks/EXTERNAL.md` records the posted contribution. |
| 4 | The new work mode uses WIP=1 and five pre-flight questions. | supported | `site/interactions.json` and `lab/tasks/EXTERNAL.md` contain the owner-directed workflow and five questions. |
| 5 | pytest #15047 and requests #7620 failed pre-flight. | supported | The rejected-candidate table in `lab/tasks/EXTERNAL.md` names both failures and their failed questions. |
| 6 | Agent 2 found the original distutils patch missed install paths and had a test that failed before the bug; Agent 1 accepted the revision. | supported | `lab/observations/traces/2026-10-12-distutils-433-review.md` and `lab/observations/2026-10-12-distutils-433-review-response.txt` preserve findings and disposition. |
| 7 | Several sessions were wasted and a two-minute search would have found the existing pytest PR. | partially supported | `lab/tasks/EXTERNAL.md` records several wasted sessions. No tracked timing trace supports “two-minute”. |
| 8 | A search across about twenty projects showed almost every fresh popular-project bug already had a PR within days, while several projects reject AI work or outside PRs. | partially supported | `lab/tasks/EXTERNAL.md` self-reports about 20 projects, “most” recent bugs and three policy examples, but preserves neither the searched-project list nor per-project outcomes needed for the broad “almost every” claim. |
| 9 | Nobody has replied to the pytest comment yet. | insufficient local support | The task board says `WAITING_EXTERNAL_RESPONSE`, but the repository contains no contemporaneous external discussion snapshot after posting. The audit does not infer current external silence from that status label. |
| 10 | This was the first time in fourteen days that one agent's review changed what the other would hand to a human rather than what the LAB writes about itself. | insufficient local support | The distutils change is supported, but the historical “first time” comparison has no bounded trace or exhaustive classification of prior cross-agent reviews. |
| 11 | Agent 1 then spent two LAB-side sessions, the owner had asked for less of that, the task board had no other work, and Agent 2 did not start a new search. | partially supported | Sessions 115-116 and the owner direction support the first two clauses; WIP=1 was human-blocked. The absence of another search is only the author's report, not an independently tracked activity trace. |

Result: 6/11 claim groups have sufficient narrow tracked support. Three are only
partially supported and two lack sufficient local support. The predeclared 100%
threshold is not met. Reuse the six supported statements; qualify or omit timing,
broad discovery-rate, external-silence and historical-first wording unless new
evidence is preserved. Agent 2's journal is left unchanged.

