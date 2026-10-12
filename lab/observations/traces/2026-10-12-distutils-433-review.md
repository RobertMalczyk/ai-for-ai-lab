# Adversarial review of the distutils #433 patch (Agent 2, 2026-10-12)

Reviewed: `2026-10-12-distutils-433.patch` (Agent 1, commit 4ba186e) on pypa/distutils main `3ed42426`.
Environment: Python 3.12 venv without setuptools, `pip install -e '.[test]'` (Python 3.11 imports the stdlib or the
setuptools copy of distutils instead of the checkout, so it cannot test this patch).

Verdict: **changes requested.** The diagnosis is right, but the patch fixes only `build`. A user's install still
crashes.

## Findings

1. **`install` and `bdist_dumb` still crash with the patch** (blocking). End-to-end runs with
   `sys.implementation.cache_tag = None` on the patched checkout:

   | command | Agent 1 patch | revised patch |
   |---|---|---|
   | `build` | OK | OK |
   | `install --root=r1` | `NotImplementedError` in `install_lib.byte_compile` (`install_lib.py:142` → `util.py:380`) | OK |
   | `install --root=r2 --record=rec.txt` | same | OK; record lists no `.pyc` |
   | `bdist_dumb` | same | OK |

   With only the `install_lib.byte_compile` guard added, `install --record` still crashes in
   `install_lib._bytecode_filenames` (`install_lib.py:183`). `build_py.get_outputs()` has the same unguarded
   `cache_from_source` call (`build_py.py:321`). Building a wheel goes through `install_lib`: setuptools main `4e612f9`
   `bdist_wheel` runs `install` (`setuptools/command/bdist_wheel.py:420`), and setuptools' `install_lib` inherits
   `byte_compile` from distutils. So the build_py-only fix does not reach a wheel build. The issue's own text also asks to handle the
   `cache_from_source` failure safely.

2. **The regression test fails for the wrong reason without the fix** (blocking). With the fix removed, the new
   test fails with `TypeError: 'NoneType' object is not subscriptable`: `build_lib` is unset, so
   `prefix[-1]` fails before `cache_from_source` is reached. It would also pass for any early return. The revised
   test runs `build_py.run()` on a real module and fails with the reported `NotImplementedError` when the fix is
   removed.

3. **Message check is order-dependent** (minor). `caplog.records[0]` assumes the warning is the first log record.
   The revised build_py test checks any message, because `run()` logs other lines first.

## Revised patch

`2026-10-12-distutils-433-reviewed.patch` (4 files, +44/−3, plus the newsfragment):
- `build_py.byte_compile` and `install_lib.byte_compile`: skip when `cache_tag is None` (same warning as
  `dont_write_bytecode`).
- `build_py.get_outputs` and `install_lib._bytecode_filenames`: list no bytecode files when `cache_tag is None`.
- Tests: `test_build_py.py::test_byte_compile_without_cache_tag` (rewritten, end to end) and
  `test_install_lib.py::test_without_cache_tag` (byte_compile and get_outputs).
- Newsfragment `433.bugfix.rst` reworded to cover both commands.

Checks:
- Both new tests fail on main source with `NotImplementedError: sys.implementation.cache_tag is None` and pass with
  the patch.
- `test_build_py.py` + `test_install_lib.py`: 14 passed.
- Full suite: 239 passed, 27 skipped, 4 failed. main gives 237 passed, 27 skipped and the same 4 failures
  (`test_bdist_dumb::test_simple_built`, `test_install::test_record`, `test_record_extensions` and
  `test_debug_mode`). They come from local egg-info naming (`UNKNOWN-0.0.0.egg-info` vs
  `UNKNOWN-0.0.0-py3.12.egg-info`), not from this change.
- `ruff check` and `ruff format --check` on the 4 changed files: clean. `git diff --check`: clean.

Not changed and left to the builder: whether `util.byte_compile` itself should also guard. It is a public helper,
and setuptools calls it directly. Guarding it would change its error contract, so I kept the fix at the command
level, where `dont_write_bytecode` is already handled.

## Draft contribution text (for the builder to adopt or edit)

Title: `Skip bytecode compilation when sys.implementation.cache_tag is None`

Body:
> Fixes #433.
>
> When `sys.implementation.cache_tag` is `None` (bytecode caching disabled), `build_py` and `install_lib` called
> `importlib.util.cache_from_source`, which raises `NotImplementedError`. So `build`, `install` and `bdist_*`
> crashed instead of skipping compilation. This treats a `None` cache tag like `sys.dont_write_bytecode` in both
> commands' `byte_compile`, and leaves bytecode files out of `get_outputs()` (so `install --record` works too).
> Tests cover both commands; both fail on main with the reported `NotImplementedError`.
>
> This change was prepared with the help of AI agents and reviewed by me before submission.

What the human must decide before publishing: whether to send it as a PR (the maintainer has not replied on the
issue yet); whether to keep the `install_lib` part in the same PR; and the disclosure wording.
