# External tasks (WIP = 1)

Work mode set by the owner on 2026-10-12 (see `site/interactions.json`, human_decisions):
DISCOVER → PRE-FLIGHT → INDEPENDENT CHECK (other agent) → BUILD → ADVERSARIAL REVIEW → READY FOR HUMAN REVIEW,
or REJECTED / BLOCKED WITH EVIDENCE. Only one task is active at a time. An ACTIONABLE task is not
interrupted by the session gate. This file is the single place to see the state; keep it short.

PRE-FLIGHT questions: (1) problem still exists on current code/release; (2) no open PR solves it;
(3) no closed PR, commit or discussion shows it was already solved or rejected; (4) project policy
allows human-reviewed AI-assisted contributions; (5) an outside contributor has a real path to contribute.

## Active

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

## Rejected at PRE-FLIGHT

| Candidate | Failed question | Evidence (2026-10-12) |
|---|---|---|
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
| sqlparse #885, #886 (malformed `( AS )` and `CASE` input crash the formatter with `IndexError` / `ValueError`) | 2 | The only two issues among numbers #850–#939; every other number is a pull request. PR #887 says it closes both. The queue is crowded with outside fixes for old issues, some labelled as AI-assisted and agent-reviewed (e.g. #939, opened 2026-10-22). No clone, reproduction or policy analysis (checked 2026-10-23, round 16, Agent 2). |
