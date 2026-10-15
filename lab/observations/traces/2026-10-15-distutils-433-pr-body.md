Title: Skip bytecode compilation when sys.implementation.cache_tag is None

Fixes #433.

When `sys.implementation.cache_tag` is `None` (bytecode caching disabled), `build_py` and `install_lib` call `importlib.util.cache_from_source`, which raises `NotImplementedError`. So `build`, `install` and `bdist_*` crash instead of skipping compilation. This change treats a `None` cache tag like `sys.dont_write_bytecode` in both commands' `byte_compile`, and leaves bytecode files out of `get_outputs()`, so `install --record` works too.

`install_lib` is included because the issue only names `build_py`, but `install` (and wheel builds that go through it) still crashes with only the `build_py` change.

Testing:
- New tests `test_build_py.py::TestBuildPy::test_byte_compile_without_cache_tag` and `test_install_lib.py::TestInstallLib::test_without_cache_tag` fail on `main` with the reported `NotImplementedError` and pass with this change.
- `test_build_py.py` and `test_install_lib.py`: 14 passed.
- Full suite on Python 3.12 (Linux): 239 passed, 27 skipped, 4 failed. The same 4 tests (`test_bdist_dumb::test_simple_built`, `test_install::test_record`, `test_record_extensions`, `test_debug_mode`) also fail on `main` in this environment (237 passed there), so they come from the local setup, not from this change.
- `ruff check` and `ruff format --check` pass on the changed files.

This change was prepared with the help of AI agents. I reviewed it, understand it, and take responsibility for it.
