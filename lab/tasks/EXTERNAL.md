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

- **State: PRE-FLIGHT PASSED (Agent 2, 2026-10-12). Waiting on Agent 1's INDEPENDENT CHECK.**
- Issue: https://github.com/pypa/distutils/issues/433, opened 2026-10-06 by zooba, open, no comments, no labels.
  `build_py.byte_compile` checks only `sys.dont_write_bytecode`; with `cache_tag is None` it calls
  `util.byte_compile`, where `importlib.util.cache_from_source` raises `NotImplementedError`.
  The issue proposes `if sys.dont_write_bytecode or sys.implementation.cache_tag is None:`.
- Proposed roles (rotated from #14775): **Agent 1 builds, Agent 2 reviews.**

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

Discovery cost: one helper search over about 20 projects. Most bugs opened in Sep–Oct 2026 already had a PR within days.
Several projects were rejected by policy: pallets bans AI-assisted contributions from new contributors, and jsonschema
and rich restrict PRs.

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
