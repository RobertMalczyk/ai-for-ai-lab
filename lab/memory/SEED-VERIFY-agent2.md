# Historical seed verification for Memory V1 (Agent 2, 2026-10-26)

Owner direction of 2026-10-26 (`docs/owner/2026-10-26-memory-v1-activation.md`): Agent 2 independently
verifies the corrected seed set before anything is imported as `historical_seed`. This file checks the
owner's 16 lesson families and all 22 POC cards against their sources on `main`. A fresh helper agent with
no stake in the POC read the sources; Agent 2 spot-checked the quotes against `docs/SESSIONS.md`.
Agent 1 owns the import mechanics. Agent 2 will compare Agent 1's imported records with this list.

Checked read-only against `main`: docs/SESSIONS.md, docs/DECISIONS.md,
lab/tasks/EXTERNAL.md, lab/memory-poc/memories.json and SEED-CHECK-agent2.md. `created_at` is always the
heading timestamp of the source session. Quotes are copied exactly from that session's section.
Rule: a family is imported only if one session's own text states the lesson, not just shows an instance of it.

## Families

### 1. Check for an existing PR before building
- Verdict: IMPORT WITH FIX (POC card `existing_fix` moves from 135 to 137)
- Source: Session 137, 2026-10-19T08:39:57+02:00
- Quote: "The issue page did not show them; fetching `refs/pull/*/head` and reading commit subjects did. That check now comes before any reproduction."
- Lesson: Before reproducing or building for an open issue, check the PR refs (`refs/pull/*/head`, commit subjects) for existing fixes, not only the issue page. setuptools #5296 already had four open fix PRs that its issue page did not show.
- Scope: external OSS preflight existing fix PR duplicate refs/pull issue page reproduction
- Later exception/refinement: Session 167 / DEC-0048 (searching by exact issue number found open PRs #918/#894 after BUILD; "search open PRs using the exact issue number before cloning or coding"). Session 168 (list `refs/pull/*/merge` before reading any issue in depth).
- POC card: `existing_fix`. Drop "not the whole project forever" (not in 135 or 137). Session 135 only supports "rejected at question 2; continue DISCOVER on other projects".

### 2. Verify actual PR state, not just page wording
- Verdict: IMPORT
- Source: Session 162, 2026-10-24T00:01:06+02:00
- Quote: "Sqlparse correction: PR #887 is closed and unmerged, not competing. Its only comment says its author stepped back from all open work."
- Lesson: Do not reject a candidate just because a PR says it closes the issue. Check that PR's actual state first. sqlparse PR #887 was closed, unmerged and abandoned by its author, so it did not occupy the contribution path.
- Scope: external OSS preflight PR state closed unmerged competing wording question 2
- Later exception: Session 167 / DEC-0048. This corrected check still missed two *open* PRs, so state checks need the exact issue-number search too. Session 176 also counts: a GitHub "non-mergeable" label turned out not to be actionable after a native merge-tree check.
- POC card: none.

### 3. Distinguish closed from merged
- Verdict: IMPORT
- Source: Session 151, 2026-10-22T08:36:56+02:00
- Quote: "a first draft of this entry said PR #162 was closed unmerged; the PR page shows it merged with \"Thanks for finding and fixing this\""
- Lesson: Before recording a PR outcome, confirm on the PR itself whether it was merged or closed unmerged. A draft said pathspec #162 was closed unmerged, but it was merged, which showed that pathspec accepts disclosed AI-assisted outside work.
- Scope: external OSS PR merged closed state record correction pathspec policy
- Later exception: Session 162 / DEC-0047 ("closed" also has to be told apart from "competing": author-closed PRs with no review are not maintainer rejection).
- POC card: `resolved_candidate` (151) covers the policy/revisit half. It is supported and can be imported as is.

### 4. Current upstream state beats remembered state
- Verdict: IMPORT
- Source: Session 154, 2026-10-22T12:07:13+02:00
- Quote: "Contrary to the previous STATE summary, it has one workflow run from PR creation: conclusion `action_required`, zero jobs/check runs, and pending status."
- Lesson: Re-check live upstream state before repeating a waiting task's status from the lab summary. STATE had missed distutils #434's `action_required` fork-workflow run. Correct the summary from the live check. Here that run needed maintainer approval, so the author had no action to take.
- Scope: external PR waiting status STATE summary live check workflow action_required
- Earlier partial: Session 104 corrected "latest release" from a live PyPI check, but that was a prior session's assumption, not remembered state. Later: Session 167 (repeating the competing-work check found new evidence); Session 175 (a memory-suggested recheck of pathspec found nothing new).
- POC card: none.

### 5. Reproduce before patching
- Verdict: IMPORT (lab-specific form only: open issues can be stale on the current release)
- Source: Session 103, 2026-10-11T17:55:21+02:00
- Quote: "The current released behavior supports the current wording, so neither a documentation patch nor a checker is justified." / "an open issue can become stale as CLI defaults change."
- Lesson: Before patching for an open issue, reproduce the reported behavior on the current release. For uv #19262, bare `uv init` on 0.12.23 already produced `uv_build`, so no documentation patch was justified. Open issues go stale as defaults change.
- Scope: external issue reproduction current release stale issue documentation patch uv
- Later: Session 104 brackets the change at 0.12.0 and corrects which release is latest (do not call 0.12.23 latest). Sessions 145, 146 and 168 (nox #748/#666 and flit already fixed on main). Session 084 (a shallow checkout cannot reproduce; the environment must be equivalent).
- POC card: none. A plain "reproduce first" card would be a generic truism; do not import that form.

### 6. Regression test must fail for the intended reason
- Verdict: IMPORT
- Source: Session 113, 2026-10-12T14:42:01+02:00
- Quote: "The first regression test failed with `TypeError` before reaching the bug." / "end-to-end tests that fail on main with the reported `NotImplementedError`"
- Lesson: A regression test must fail on unpatched code with the reported error, not with an earlier unrelated failure. The first distutils #433 test raised `TypeError` before reaching the bug; the revised tests fail on main with `NotImplementedError`.
- Scope: regression test control failure reason distutils cache_tag NotImplementedError TypeError
- Later confirmation: Session 114 (removing both guards produced the intended `NotImplementedError` 0/2).
- POC card: `regression_cause` (113). It is supported; import as is (it also covers family 7 at 113).

### 7. Review adjacent execution paths, not only the reported function
- Verdict: IMPORT
- Source: Session 089, 2026-10-09T20:40:17+02:00 (earlier than the POC card's 113)
- Quote: "Found a second trigger of the same root cause on unpatched pytest: a class-scoped async fixture without a plugin also ends in `AssertionError`"
- Lesson: When reviewing a fix, look for other triggers of the same root cause beyond the reported path. In pytest #14775 a class-scoped async fixture also hit the `AssertionError`, so moving the adjacent async check was needed, not collateral.
- Scope: adversarial review root cause adjacent path second trigger pytest fixtures
- Later: Session 113 (distutils: `install_lib`, `install --record` and `bdist_dumb` still crashed after the `build_py`-only fix).
- POC card: `regression_cause` (113) is the later distutils instance; keep both.

### 8. Do not claim a green full suite when failures remain
- Verdict: IMPORT
- Source: Session 112, 2026-10-12T12:06:57+02:00
- Quote: "The broader suite produced 229 passed, 28 skipped and 12 environment-linked failures outside test_build_py ... so it is not reported as green."
- Lesson: When the broader upstream suite still has failures, even environment-linked ones outside the changed area, report the exact counts and do not call the suite green. A passing focused module is not a green full suite.
- Scope: upstream full suite environment failures reporting green claim PR testing section
- Later: Session 114 (A/B against main: same 12 failures, so "no added failure"). EXTERNAL.md final review: the PR body "must not claim an all-green suite".
- POC card: none.

### 9. Waiting for upstream is not failure
- Verdict: IMPORT
- Source: Session 126, 2026-10-15T06:03:48+02:00
- Quote: "zero non-owner comments. The useful threshold was not met; outcome `inconclusive`... Waiting remains outside active WIP" / "do not spend sessions polling it."
- Lesson: An external conversation with no maintainer reply is waiting, not failed. Record a no-reply check as inconclusive, keep the task outside active WIP, and revisit it only after a visible upstream reply, without polling or building a monitor.
- Scope: external PR waiting no reply inconclusive WIP polling monitor
- Later extension: Session 134 (once both external tasks wait, the next session may DISCOVER one new candidate under WIP=1). EXTERNAL.md owner decision of 2026-10-24 (waiting tasks do not occupy the implementation slot).
- POC card: `waiting` (134). IMPORT WITH FIX at 134: drop "bounded" and "submission is not acceptance". Fixed text: "Submitted distutils PR #434 awaits an external response. With both external tasks waiting, the next session may DISCOVER one new candidate under WIP=1."

### 10. Project AI/contribution policy is a hard PRE-FLIGHT constraint
- Verdict: IMPORT WITH FIX (POC card `project_policy`)
- Source: Session 073, 2026-10-07T11:57:08+02:00
- Quote: "A current unclaimed issue is insufficient: project contribution policy is an earlier hard constraint, and observing it avoids wasting maintainer attention."
- Lesson: Before any external implementation, check that project's contribution and AI policy as a hard stop. An open, unclaimed issue is not enough. The Pallets guide forbids AI-generated PRs, so Click was rejected as a target before any code.
- Scope: external OSS contribution policy AI preflight hard constraint Pallets Click
- Later exceptions: Session 074 (policies differ: Rich accepts AI PRs under conditions; requests/attrs/pip/pytest forbid unsupervised agentic work). Session 075 (also confirm a real submission path). Session 078 ("Absence of a rule is not consent"). Session 149 (a maintainer can decline AI help on one issue). Session 151 (pathspec accepts disclosed AI work). Session 177 (slugify: issues-first policy).
- POC card: `project_policy`. Remove the added "do not generalize this fact to other projects or future policy" hedge; it is not in 073.

### 11. Existing outside work can still be helped if there is incremental technical value
- Verdict: IMPORT
- Source: Session 110, 2026-10-12T10:36:01+02:00
- Quote: "Its test covers only the `-W error` trigger. Our async-trigger test ... fails on main and passes with the PR." / "Drafted a comment for the existing PR ... no competing PR"
- Lesson: If an open PR already has the same fix, do not open a competing one. Offer only the missing increment: here, a test for the async trigger that fails on main and passes with PR #14777, drafted for human review before posting.
- Scope: external OSS existing PR incremental test comment no competing PR human review
- Later exception: DEC-0048 / Session 167. When active fixes already exist, unsolicited extra evidence (the fuzz results) was rejected as noise. Session 166: credit earlier closed PRs and say plainly that a resubmission is one.
- POC card: none.

### 12. Read large required documents without truncating the relevant tail
- Verdict: IMPORT
- Source: Session 020, 2026-09-30T18:11:27+02:00
- Quote: "Learned: requested output budget is not a completeness guarantee. An explicit response boundary is more auditable than assuming a long concatenation arrived."
- Lesson: (POC text, supported) Read large mandatory documents in separate responses and verify scope through EOF. Requested output budget alone does not ensure complete delivery.
- Scope: startup documents truncation context reading EOF session tail
- Later extension: Session 077 (inner reads within one orchestration response share a cap; see card `outer_boundary`).
- POC card: `read_boundary`. Import as is.

### 13. Exact commands and replay inputs matter for reproducibility
- Verdict: IMPORT
- Source: Session 055, 2026-10-05T08:35:57+02:00 (responding to the Session 054 finding)
- Quote: "replaced the procedural commands of the continuity, coverage and fresh-clone receipts in site/proof.json with exact commands and re-ran them at the same commits"
- Lesson: (POC text, supported) Replay receipts need exact commands at the named commits rather than prose requiring reconstruction. Commands were corrected and replayed in this episode.
- Scope: receipt replay exact commands evidence commits
- Later extensions: Session 090 (each group also needs every local input; see card `replay_inputs`). Session 092 (labels and inputs are not enough when a two-state comparison leaves out the reset/transition order).
- POC card: `exact_commands`. Import as is. The "inputs" half belongs to `replay_inputs` at 090, not here.

### 14. Replace stale current-state claims with dated evidence or live checks
- Verdict: IMPORT
- Source: Session 053, 2026-10-05T00:03:04+02:00
- Quote: "Keep volatile run results in dated session evidence and a recomputation command in STATE; reject updating or generating a live count."
- Lesson: (POC text, supported) Keep volatile run counts in dated evidence and a verification command in current status. A fresh byte checkpoint can still contain stale factual claims.
- Scope: status summary STATE test count stale volatile claim checkpoint
- Later: Session 107 (dated tested-version wording for uv releases). Session 123 (take next-session numbers from the gate). Session 154 (live upstream check corrected STATE).
- POC card: `stable_status`. Import as is.

### 15. A negative experiment can generate a useful lesson
- Verdict: OMIT AMBIGUOUS
- Reason: This is a meta-truism. Many sessions record negative outcomes with specific lessons (088, 116, 120, 167), but no session states this family as its own lesson. Import those specific lessons instead (e.g. `scope_output`, `raw_evidence`, family 1).
- Nearest text: Session 174, "No suitable task was found in this bounded round, which is preferable to manufacturing LAB work." This is about selection, not the family.

### 16. Do not infer causality merely from chronology
- Verdict: OMIT AMBIGUOUS
- Reason: No session learns this from a chronology-based mistake. Session 139 says decision-map "then" edges are "sequence only", but that is a display rule. Session 087 confirms a cause by intervention, and Session 094 limits credit to the practice actually used. Both are nearby, not this family. Card `alias_correction` (060) is about counting repetitions, not causality.

## POC cards not covered by the 16 families

| Card (src) | Verdict | Note / fix |
|---|---|---|
| `discovery` (019) | IMPORT | Supported by 019 "names-first is useful chiefly when names are not yet reliable". |
| `final_only` (046) | OMIT | Superseded at 047/049 (invalidated_at 47), and it leaks a 047 caveat. If kept for history, strip it to 046's byte result. |
| `peer_continuity` (047) | OMIT | Superseded by `continuity_window` at 049. It also drops "or the administrator" from 047. |
| `continuity_window` (049) | IMPORT WITH FIX | 049's window held only peer sections. Fix: "Read from your own latest session through EOF, preserving intervening peer sections. The successful three-section example does not guarantee comprehension." |
| `append_anchor` (049) | IMPORT WITH FIX | Move to Session 051, 2026-10-04T18:03:14+02:00. 051 cites the 049 misplaced insert and first states the unique latest-heading/exact-tail fix. |
| `alias_correction` (060) | IMPORT | Supported: "each alias name was observed once, not twice". Useful evidence-hygiene lesson. |
| `alias_confirmed` (061) | OMIT | Supported, but redundant with `alias_correction`. Its own content is narrow (parked manifest family). |
| `lock_commit` (070) | IMPORT | Supported: "Synchronize the target commit's lock before historical tests". |
| `outer_boundary` (077) | IMPORT | Supported. A later refinement of family 12 at its own timestamp. |
| `compact_output` (082) | IMPORT WITH FIX | Drop "noisy" (first appears in 116). Fix: "Full-log capture plus a compact success receipt helped the full LAB test suite once. Expose full output on failure; benefit for a different consumer must be measured." |
| `raw_evidence` (088) | IMPORT | Supported ("does not refute Session 087's causal diagnosis"). |
| `replay_inputs` (090) | IMPORT | Supported. Extends family 13. |
| `scope_output` (116) | IMPORT | Supported. Negative field result that scopes `compact_output`. |
| `create_ref` (126) | IMPORT | Supported ("used `update_ref` for a branch that did not exist and returned HTTP 422"). |

## Summary

16 families:
- IMPORT: 12 (families 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14)
- IMPORT WITH FIX: 2 (families 1 and 10; card time moved or hedge removed)
- OMIT AMBIGUOUS: 2 (families 15 and 16)

All 22 POC cards:
- Import as is: 13 (`read_boundary`, `stable_status`, `exact_commands`, `regression_cause`, `resolved_candidate`, `discovery`, `alias_correction`, `lock_commit`, `outer_boundary`, `raw_evidence`, `replay_inputs`, `scope_output`, `create_ref`).
- Import with fix: 6 (`existing_fix` moved to 137, `project_policy` hedge dropped, `waiting` wording fix, `continuity_window` wording fix, `append_anchor` moved to 051, `compact_output` drops "noisy").
- Omit: 3 (`final_only`, `peer_continuity`, `alias_confirmed`).
- Check: 13 + 6 + 3 = 22.

New lessons with no POC card (from families): 2, 3, 4, 5, 7, 8, 9 (S126), 11. That is 8 new cards.
