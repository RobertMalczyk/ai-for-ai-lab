# External tasks (WIP = 1)

Work mode set by the owner on 2026-10-12 (see `site/interactions.json`, human_decisions):
DISCOVER → PRE-FLIGHT → INDEPENDENT CHECK (other agent) → BUILD → ADVERSARIAL REVIEW → READY FOR HUMAN REVIEW,
or REJECTED / BLOCKED WITH EVIDENCE. Only one task is in active implementation at a time.

Owner decision (2026-10-24): **Option A approved** in response to the BUILD/WIP decision request.
Submitted tasks in WAITING_EXTERNAL_RESPONSE do not occupy the active implementation slot.
The authorized sqlparse build was later rejected after exact search found competing PRs; no
implementation is active now. Upstream publication remains subject to human review. An ACTIONABLE task is not
interrupted by the session gate. This file is the single place to see the state; keep it short.

PRE-FLIGHT questions: (1) problem still exists on current code/release; (2) no open PR solves it;
(3) no closed PR, commit or discussion shows it was already solved or rejected; (4) project policy
allows human-reviewed AI-assisted contributions; (5) an outside contributor has a real path to contribute.

## Submitted — waiting outside active implementation WIP

### pypa/distutils#433: `build_py` crashes when `sys.implementation.cache_tag is None`

- **State: SUBMITTED / WAITING_EXTERNAL_RESPONSE: https://github.com/pypa/distutils/pull/434 (opened 2026-10-18
  by the owner after the integration got HTTP 403 on PR creation; Agent 1 notice: lab issue #62; head `0d08e50` = the
  approved commit).** The only GitHub Actions run has zero jobs and conclusion `action_required`; GitHub requires a
  maintainer with write access to approve workflows from this fork, so there is no author-side action (checked
  2026-10-22). No further work without an upstream signal. Agent 2
  checked the public PR page on 2026-10-18 ~12:40Z: the title matches; the testing section gives 14 passed and
  239/4 vs 237/4 with the same 4 environment failures; the disclosure says the author reviewed the final patch,
  understands it and takes responsibility. No comments, reviews or labels yet. Review:
  `lab/observations/traces/2026-10-12-distutils-433-review.md`; builder response:
  `lab/observations/traces/2026-10-12-distutils-433-review-response.txt`.
  Revised patch: `lab/observations/traces/2026-10-12-distutils-433-reviewed.patch`. Main findings: `install` and
  `bdist_dumb` (and so wheel builds) still crashed in `install_lib`; the first test failed with `TypeError`, not the bug.
- Issue: https://github.com/pypa/distutils/issues/433, opened 2026-10-06 by zooba, open, no comments, no labels.
  `build_py.byte_compile` checks only `sys.dont_write_bytecode`; with `cache_tag is None` it calls
  `util.byte_compile`, where `importlib.util.cache_from_source` raises `NotImplementedError`.
  The issue proposes `if sys.dont_write_bytecode or sys.implementation.cache_tag is None:`.
- Proposed roles (rotated from #14775): **Agent 1 builds, Agent 2 reviews.**
- **Final review (Agent 2, 2026-10-15 ~16:30Z): APPROVED FOR SUBMISSION**, on one condition: the PR body has a testing
  section and the full AI disclosure; `lab/observations/traces/2026-10-15-distutils-433-pr-body.md` meets both.
  Checked branch `RobertMalczyk/distutils:fix/433-missing-cache-tag` @ `0d08e50` (named differently from the order's
  `fix-433-cache-tag`; open the PR from the real name). (1) Exactly the 5 expected files, +45/-3. (2) Changed lines
  identical to the reviewed patch. (3) Base is upstream main `3ed4242`; the issue is open with no comments or PR;
  the newest upstream PR is still #432. (4) `install_lib` is still needed; without it `install` and wheel builds crash.
  (5) Both new tests fail on main with `NotImplementedError: sys.implementation.cache_tag is None` and pass with the
  fix; `test_build_py.py` and `test_install_lib.py` give 14 passed; ruff check/format are clean. (6) Full suite on
  Python 3.12: 239 passed / 4 failed with the fix, 237 passed / the same 4 failed on main (environment), so the body
  must not claim an all-green suite. (7) The 2026-10-12 draft disclosure said only "reviewed by me"; the body must
  say the human reviewed, understands and takes responsibility. Not blocking: the commit uses the owner's personal
  e-mail, which becomes public with the PR.

PRE-FLIGHT answers:

1. **Still exists:** yes. Reproduced on distutils main `3ed42426` (2026-08-06) with Python 3.11.15: `build_py` with
   `compile=1` and `sys.implementation.cache_tag = None` raises `NotImplementedError: sys.implementation.cache_tag is None`;
   the same run with the real tag succeeds. setuptools main `4e612f9` vendors the same unguarded check in
   `setuptools/_distutils/command/build_py.py:390`.
2. **No open PR:** the issue shows "No branches or pull requests". The newest distutils PR heads are #430, #431, #432 (all
   opened before the issue; none touches `build_py` or `byte_compile`). Related but separate: pypa/setuptools#5344
   (same reporter, setuptools' own `install_lib._gen_exclusion_paths`) has PR pypa/setuptools#5345, which touches only
   `setuptools/command/install_lib.py`, its test and a newsfragment.
3. **Not solved or rejected elsewhere:** no comment on the issue; `git log -S cache_tag` on distutils shows only an old
   build-dir change; setuptools' vendored copy is unchanged.
4. **Policy:** no AI policy in pypa/distutils or in setuptools' developer guide. The guide asks for tests and a towncrier
   newsfragment; distutils has `newsfragments/` and `towncrier.toml`. Disclose AI help anyway.
5. **Path:** outside PRs are merged (for example pypa/distutils#379 and #397, July 2026; "credit @dchaudhari7177").
   setuptools tells contributors to fix `_distutils` upstream in pypa/distutils.

Risks: no maintainer reply on the issue yet, and one maintainer (jaraco) merges everything, so review may be slow.
Scope question for the build: `install_lib.byte_compile` (`distutils/command/install_lib.py:129`) has the same
unguarded check; the issue does not mention it.

Independent check and build (Agent 1): all five pre-flight answers still passed on upstream commit
`3ed42426ce6f41e9d07dc63f3315d85f19e25618`. The unpatched focused scenario failed 0/1 with
`NotImplementedError`; a one-condition `build_py` guard plus regression test and newsfragment changed it to 1/1.
The focused module passed 8/8. The broader suite had 229 passes, 28 skips and 12 environment-linked failures
outside `test_build_py`; it is not reported as green. Review artifact:
`lab/observations/traces/2026-10-12-distutils-433.patch`. Do not extend the patch to `install_lib` unless review
shows the issue scope requires it. No fork, PR, comment or maintainer message exists.

Discovery cost: one helper search over about 20 projects. Most bugs opened in Sep–Oct 2026 already had a PR within days.
Several projects were rejected by policy: pallets bans AI-assisted contributions from new contributors, and jsonschema
and rich restrict PRs.

Builder disposition (Agent 1): accepted the revised two-command patch after an independent same-environment A/B replay.
With both guards absent, the two new regressions failed at the intended `cache_from_source` call (0/2); the reviewed
patch passed them (2/2), passed both focused modules (14/14), and changed the full suite from 228 to 230 passes with
the same 12 environment-linked failures and 28 skips. The owner approved this scope for submission and created
`RobertMalczyk/distutils`, whose public `main` resolves to the reviewed upstream base `3ed42426`. AI assistance must be
disclosed. No PR, issue comment or maintainer contact exists yet.

## Waiting on an external reply

- **pytest #14775**: WAITING_EXTERNAL_RESPONSE. Fix already in open PR pytest-dev/pytest#14777 (by another
  contributor). Our added value, an async-fixture regression test and changelog wording, was posted there by the owner on
  2026-10-12 (https://github.com/pytest-dev/pytest/pull/14777#issuecomment-6121058763). No further work
  without a reply from the PR author or a maintainer.
  - External result: technical information given to an existing contributor; no competing PR.
  - Builder (Agent 2): reproduction, async trigger, test. Reviewer (Agent 1): independent reproduction and challenges.
  - Waste: several sessions of work before the existing PR #14777 was found. This is the baseline the
    PRE-FLIGHT step exists to avoid.

## No active implementation task

- **sqlparse #885/#886 — REJECTED after late PRE-FLIGHT correction.** Current master `60cdc649` reproduces `IndexError` for
  `format("( AS )", strip_whitespace=True)` and `ValueError` for the malformed
  `CASE` reproducer. The earlier review considered closed PRs #862–#864/#887 but
  missed two open, exact competing fixes: #918 fixes #885 from base `60cdc649`
  with the same short-parenthesis guard and a regression; #894 fixes #886 from the
  same base with direct-child guards and a regression. They were opened on
  2026-10-05 and 2026-09-13, before this task's PRE-FLIGHT. Both remain open and
  mergeable with no review. Therefore PRE-FLIGHT question 2 fails and no fifth PR
  will be prepared. PR #887 and earlier equivalent PRs
  #862–#864 were closed unmerged by their own authors with no review or maintainer
  rejection. CONTRIBUTING contains no AI ban, the PR template enables automated AI
  review, disclosed AI-assisted PR #939 remains open, and outside PRs #867/#868
  merged in July 2026. This passes questions 1–5. The owner approved Option A on 2026-10-24:
  BUILD is authorized; submitted distutils is waiting outside the active implementation limit.
  Agent 1's minimal patch on `60cdc649` changes two guards and adds two regressions:
  both direct reproducers change from exceptions to returned input, the regression
  module passes 95 tests (1 xpass), and the full suite passes 508 tests (2 xfail,
  1 xpass). Changed source files pass ruff; current ruff reports unrelated legacy
  lint/format findings, retained in the trace. Patch and raw result summary:
  `lab/observations/traces/2026-10-24-sqlparse-885-886.patch` and
  `lab/observations/traces/2026-10-24-sqlparse-885-886-build.txt`.
  **State: REVIEWED (Agent 2, 2026-10-24) — READY FOR HUMAN REVIEW after Agent 1 accepts or rebuts three
  small changes.** Review: `lab/observations/traces/2026-10-24-sqlparse-885-886-review.md`; reviewed patch:
  `...-reviewed.patch`. Both reporter inputs and the new tests fail on master and pass with the fix; full suite
  509 passed with the reviewed patch. 170,000 fuzzed malformed inputs × 4 option sets found the two crash sites on
  master and zero exceptions with the patch. Changes: third guard `> 2` (as in #864), `(::)` parametrized into the
  #885 test, one-line comments. Root cause is malformed grouping; the guards are symptom fixes, as in all four
  earlier PRs. Human must decide: provenance wording crediting closed PRs #862–#864/#887, and whether to offer a
  grouping-level fix instead.

  **Owner scope/provenance decision (2026-10-24): Option A approved** in response to
  the separate scope/authorship decision email (not the earlier BUILD/WIP decision).
  Keep the narrow filter guards. In the future PR body, credit the authors of closed,
  unmerged PRs #862, #863, #864 and #887 for the earlier guard-based fixes; explain
  that this submission adds regression coverage and independent verification, and
  disclose AI assistance. Explicitly state that malformed token grouping is the root
  cause and that a broader grouping-level change can be considered at a maintainer's
  request. Suggested attribution: "This uses the same guard-based approach as the
  earlier closed, unmerged PRs #862, #863, #864 and #887. Credit goes to their authors
  for the earlier fixes; this submission adds regression coverage and independent
  verification."
  This approval is retained as history, but it cannot override the newly verified
  competing-work blocker. No fork branch, PR, comment or maintainer contact was created.

## Rejected at PRE-FLIGHT

| Candidate | Failed question | Evidence (2026-10-12) |
|---|---|---|
| pallets/click #3362 (`write_usage` splits options at hyphens) | 2, 3, 4 | The issue remains open, but exact PR search found at least ten prior attempts, including #3782, #3810, #3812, #3814 and #3836 titled `[rejected AI]`, plus #3796/#3797/#3798/#3804 titled `AI junk`. The proposed `break_on_hyphens=False` solution is therefore already implemented repeatedly and explicitly rejected under Pallets' AI-contribution policy. No clone, code or upstream contact (checked 2026-10-25, Agent 1). |
| python-pathspec (recheck) | 2 | No new issue since #161 (fixed by merged PR #162); the newest numbers #168-#170 are pull requests and open merge refs are #69, #153, #168, #170. Nothing to take (checked 2026-10-25, Agent 2). |
| natsort #192/#193 (huge digit runs), #208 (short fastnumbers version) | 2, value | Active maintainer who merges outside PRs (#196, #201, #205, #207) and has an open contribution guide with no AI rule. But every recent bug is an edge case found by other AI-assisted contributors and already has a PR: #194 is open for #192/#193 after #197/#198 were withdrawn, and the #208 report and PR #209 were withdrawn after the maintainer asked whether it was "a real problem actually found in real code". The same AI-assisted reporter also filed pathspec #161. Small projects are now being mined for edge cases by other agents; the maintainer filters for real-world impact. Cloned only to read history and open PRs; no code work or upstream contact (checked 2026-10-25, Agent 2). |
| pytest-subtests #56 (`--last-failed` misses failed subtests) | 2 | Open issue, but maintainer bluetech says the pytest-core integration in pytest#13738 intentionally fails the parent test when a subtest fails and verified that this makes `--lf` work. A parallel plugin fix would duplicate the chosen integration path (checked 2026-10-25). |
| pytest-subtests #202 (xdist cannot serialize `StrEnum`/`Path` subtest context) | 5 | Maintainers diagnosed `_to_json` retaining non-serializable context values, but current main `1e57601` announces that the plugin was integrated into pytest 9.0, will no longer be maintained and will be archived. The old plugin has no real contribution path; no code or upstream contact (checked 2026-10-25). |
| execnet #271 (Python 3.12 creates a thread during interpreter shutdown) | assignment / 3, 5 | Open and assigned to maintainer RonnyPfannschmidt. The proposed direction uses private `threading._register_atexit`, so scope and compatibility need maintainer design rather than a small uncoordinated patch. No reproduction, code or upstream contact (checked 2026-10-25). |
| inflect #201 (`plural('Property')` returns `Propertys`) | Independent check (1: not a bug) | Reproduces on main `f51d6c4`, but it is the designed default: the `-y` rule returns `word + 's'` for a capitalized word when `classical(names=True)`, which is on by default (docstring: "By default all classical modes are off except names"), so proper names pluralize as `Sallys`/`Kennedys`; `tests/test_classical_names.py` pins `Sally` -> `Sallys`. `p.classical(names=False)` already returns `Properties`. Fixing `Property` without breaking `Sally` needs a common-noun-versus-name decision; the issue is labelled `feature` and the maintainer wrote that the expected behavior is not clearly desirable. No open PR targets it (28 open; #246 is a broad refactor). Agent 1 passed it as a bug; Agent 2 disagrees (checked 2026-10-25). |
| dinnerbell #51 (stale open calls push today's Slack Home cards past the 100-block limit) | Independent check (value, 5) | Agent 2 agrees the bug exists on main `a16245d`: `for_today()` orders by date ascending, `home_view()` slices to `MAX_VIEW_BLOCKS = 100`, so about 49 stale open calls hide today's card and its actions. No open PR touches it (only #55, parallel tests). Rejected anyway: the maintainer filed it on 2026-10-24 from their own review of #50, wrote the fix and the test in the issue, and calls it unlikely in practice because the scheduler tick marks old calls done (`Step.MARK_DONE`). All 184 commits are the maintainer's (Claude co-authored, about 10 PRs a day), with no outside contributor ever merged. An outside PR would race the author's own pipeline on a one-day-old issue for little value outside the lab (checked 2026-10-25, Agent 2 independent check of Agent 1's DEC-0049). |
| sqlparse #885/#886 (formatter crashes on malformed input) | 2 | Open PR #918 fixes #885 and open PR #894 fixes #886 from the same upstream base. Both predate our PRE-FLIGHT and contain regression tests. Our independently correct build/review is preserved, but a fifth PR would duplicate active work (checked 2026-10-24, Agent 1). |
| flit #817 (docs still mention `--setup-py`), #804 (wheels written with mode 0600) | 1 | Both already fixed on main `1418ccb`: the command-line docs no longer mention `--setup-py` (only `history.rst` does, correctly), and `flit_core/wheel.py` chmods the `mkstemp` file to normal permissions (commit `39f214f`, 2026-07-16). Issue pages still look open. Open PRs were listed from `refs/pull/*/merge` first (43 open; the newest, #827–#838, are unrelated). No code work (checked 2026-10-24, round 18, Agent 2). |
| pip #14384 (`pip debug` and five other commands ignore extra positional arguments) | 2 | Open PRs #14389 and #14391 both implement rejection for the affected commands. Maintainer pfmoore preferred the human-authored contribution after #14389 disclosed LLM use. No clone, reproduction or code work (checked 2026-10-24, round 17, Agent 1). |
| pytest #15047 (`--fixtures` exit code 0) | 2 | Issue comment by lpyu001: "submitted a PR"; another contributor offered a fix; maintainer (bluetech) wants it as a breaking change for pytest 10.0. |
| requests #7620 (PR 5410 change missing from main) | 5 | Issue page says PRs are restricted; maintainer (nateprewitt) has no strong opinion and suggests removing the change. |
| setuptools #5354 (editable install drops mapped packages with shared prefix) | 2 | Issue header links open PR pypa/setuptools#5355 (checked 2026-10-18). |
| setuptools #5338 (`best_effort_version` with `v` prefix) | 2 | Reporter's open PR pypa/setuptools#5339 (checked 2026-10-18). |
| wheel #706 (epoch-zero mtime uses build time) | 2 | Reporter plans the fix; open PR pypa/wheel#707 (checked 2026-10-18). |
| more-itertools #1332 (`set_partitions([])`) | 2 | Reporter's open PR more-itertools#1333 (checked 2026-10-18). |
| platformdirs #629 (ELOOP message on illumos) | 2 | Open PR tox-dev/platformdirs#630 "test: use host strerror for runtime warnings", committed 2026-10-18, the day the issue opened. |
| cattrs #796 (dataclass `default_factory` field required in union disambiguation) | 2 | No PR yet, but the reporter offered to open one; a parallel PR would compete with them (checked 2026-10-19). |
| cattrs #795, #797; build #1228; keyring #772 | 2 | Each has an open fix PR (cattrs #798/#803, #799; build #1231; keyring #773) (checked 2026-10-19). |
| pipx #2155, #2156, #2159; build #1220 | 3 | Already fixed and closed within a day of opening (checked 2026-10-19). |
| twine #1404 (percent-encoded URL credentials) | 3, 4 | Closed and locked by maintainer (woodruffw): credentials in URLs are unsupported, and AI-generated issues are not wanted. |
| setuptools #5296 (84.0.0 drops executable bit on `.py` package data in wheels, opened 2026-08-10) | 2 | Reproduced on main `4e612f9` (wheel mode 0644; 0755 with 83.0.0). Root cause: since 84.0.0 `file_util.copy_file` sets the exact mtime (`os.utime(..., ns=...)`); the file is first copied as a module with `preserve_mode=False`, so the later package-data copy is skipped as up to date. 83.0.0 kept the bit only because the second-resolution mtime made the copy run again. Not taken: four open PRs already fix it (#5299, #5302, #5318, #5321), found through `refs/pull/*` subjects; the issue page showed none. |
| markdown-it-py #438, #441, #445 | 2 | Each has an open fix PR (#439, #443/#444, #446); at least 10 fix PRs from different outside contributors since 2026-09-23 (checked 2026-10-19, round 4: smaller projects). |
| tomli #312 | 2 | Open fix PR #314 (checked 2026-10-19). |
| iniconfig #83 | 2 | Maintainer (RonnyPfannschmidt) opened and self-assigned it (checked 2026-10-19). |
| humanize #270 (Romanian ordinals) | 5 | Needs a design change across all strings (Django-style placeholders) that the maintainer has not chosen; not a small bug (checked 2026-10-19). |
| tomli #309; validate-pyproject #323, #326 | 3 | Maintainers chose docs only, or the fix belongs to SchemaStore/fastjsonschema (checked 2026-10-19). |
| pygments (old lexer bugs) | 5 | 341 PRs still carry a merge ref (open or not yet cleaned up), 170 of them numbered #3218–#3416; the last merge on master was 2026-07-28 and the last commit 2026-09-27. A new PR would wait in that queue (checked 2026-10-19, round 5). |
| packaging #934 (marker variable on the right-hand side) | 3 | Needs a spec decision first: maintainer (henryiii) opened a discuss.python.org thread; the reporter wants the spec narrowed instead (checked 2026-10-20, round 6). structlog and tox show no open bug-labelled issues. |
| babel (older bugs #1067, #1084, #1190, #1219) | 2, 5 | 62 PRs numbered #1336–#1397 opened since 2026-09-04, 53 of them still carrying a merge ref (open) (#1190 → #1368, #1219 → #1347); 4 outside commits merged since 2026-08-01. marshmallow shows no open bug-labelled issues; arrow's open bugs are mostly DST and timezone design questions (checked 2026-10-20, round 7). |
| nox #748 (`session.notify` with a function) | 3 | The maintainers' preferred docstring fix is already on main (`nox/sessions.py`: "Passing the decorated function object is not currently supported"); the issue is just still open. nox #833 and #1088 have open PRs (#1178, #1117); #734 is a pyenv/virtualenv problem. attrs: an AI policy allows human-owned work, but its open bugs are old typing or design questions, and one carries an "AI flypaper" label (checked 2026-10-20, round 8). |
| nox #666 (no live pip output with `--verbose`), #1021 (virtualenv backend and old Pythons) | 3 | #666 is already fixed on main: `install` defaults to `silent = not verbose` (`nox/sessions.py:792`); the issue is still open. #1021 has no agreed fix among three maintainers (checked 2026-10-20, round 9). |
| typeguard #578 (instrumented `__new__` aliases the defining class to the subclass) | 2 | The issue remains open, but two open PRs already fix it (#581 and #583); the issue discussion also compares both patches. A third competing fix, #590, has existed. Rejected before reproduction or policy analysis (checked 2026-10-21, round 10). |
| pluggy #808 (`call_historic()` retains the caller's kwargs mapping) | 3, 4, 5 | The issue is open but assigned to maintainer RonnyPfannschmidt. He explicitly told an outside contributor not to proceed because of the AI PR backlog, then closed matching disclosed-AI PR #810 as a minimal-effort assist. No reproduction or code work (checked 2026-10-22, round 11). |
| h11 #200 (Sphinx 9 documentation build) | 2 | The issue is open with no comments, but open PR #202 implements the exact `add_js_file`/`add_css_file` replacement and says `Fixes #200`. No clone, reproduction, policy analysis or code work (checked 2026-10-22, round 12). |
| python-pathspec #161 (custom Pattern rejected by default backend when re2/hyperscan installed) | 2 | Small queue (3 open PRs), but #152-#167 hold only one issue and it is already fixed: the maintainer merged the reporter's disclosed AI-assisted PR #162 on 2026-10-16 ("Thanks for finding and fixing this"). Positive policy signal: keep pathspec in mind for a future bug. No clone or code work (checked 2026-10-22, round 13, Agent 2). |
| cachetools #446 (class-access `@cachedmethod` rejects a keyword instance argument, regression in 7.2.4) | 2 | Open bug, but the reporter's open PR #447 says `Fixes #446` (opened 2026-10-20, no review yet). The neighbouring regression #443 was fixed by the maintainer within days, choosing between two outside PRs. Short queue with an active maintainer who merges outside fixes. No clone or code work (checked 2026-10-22, round 15, Agent 2). |
| yarl #1862 (IPv6 zone identifier leaks into Host header) | 2 | The issue remains open, but open PRs #1864 and #1973 both implement zone removal from `host_port_subcomponent` and declare `Fixes #1862`. No clone, reproduction, policy analysis or code work (checked 2026-10-22, round 14). |
