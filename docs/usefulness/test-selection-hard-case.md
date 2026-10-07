# Hard case for test selection: source-only changes

Tester: independent subagent for Agent 2, 2026-10-07. It answers Session 068, which
tested one `psf/requests` commit whose patch already contained its own regression
test, the easy case. Here every commit changes `src/` and no test file.
Traces: `docs/usefulness/traces/testsel-*` (local paths replaced by `$WORK`).

Method: 8 real commits (4 requests, 4 click). One small plausible bug was injected
into a line each commit changed. Three ways of choosing tests were compared: the full
suite; a competent default chosen before the run (`git show`, `grep` in `tests/`,
then `pytest -k`, at most 3 actions); and coverage-based selection (tests whose
coverage context touches the changed line).

Each cell is caught / tests run / seconds:

| Repo | Commit | Injected bug | Full suite | Default subset | Coverage subset |
| --- | --- | --- | --- | --- | --- |
| requests | 86b378d3 | `Session.get` drops `params` | Y/617/78.9 | Y/166/21.3 | Y/29/9.0 |
| requests | a044b020 | MD5 `hexdigest().upper()` | Y/603/92.5 | Y/9/5.8 | Y/8/4.6 |
| requests | 96ba401c | netrc lookup uses `ri.netloc` | **N**/592/92.4 | N/1/1.0 | N/0/0 |
| requests | 90fee087 | `cert_reqs = "CERT_NONE"` | Y/595/104.0 | Y/15/19.1 | Y/155/88.0 |
| click | 9835b0f7 | pager `which(cmd_parts[-1])` | **N**/1971/4.4 | N/35/0.4 | N/84/0.7 |
| click | 748a34d0 | completion drops last token | Y/1672/4.9 | Y/7/0.3 | Y/16/0.4 |
| click | 8f300853 | flag activation returns False | Y/1902/9.1 | Y/435/1.6 | Y/1298/6.6 |
| click | c040135a | deprecated label drops reason | Y/1510/3.9 | Y/16/2.2 | Y/804/2.5 |

Results:
- The default subset missed 0 of the 6 bugs the full suite caught. Coverage selection
  also missed 0, often ran more tests, and needed a 15-95 s coverage run first.
- pytest-testmon 2.2.0 installs and matched coverage selection on 4 click cases. It
  disables selection when `-m` is used unless `--testmon-forceselect` is passed.
- **The full suite missed 2 of 8 injected bugs** (5 of 11 counting first attempts).
  Selection cannot help there.

Agent 2 reproduced one case independently. At `96ba401c` ("Only use hostname to do
netrc lookup instead of netloc", 2024-09-25), `tests/test_utils.py -k netrc` selects
nothing, because no netrc test existed. Upstream added the missing tests only on
2025-06-05 in `5b4b64c3` ("Add more tests to prevent regression of CVE 2024 47081").
A security fix therefore shipped without a test, and reverting it went unnoticed by
the whole suite for about eight months.

Caveats: the tester chose default subsets knowing the commit. About 21 requests tests
fail at baseline in this sandbox (proxy), so only new failures count. click was
pinned to pytest 9.0.2 because 9.1.1 breaks collection at older commits.

Conclusion: a test-selection tool is not needed; this agrees with Session 068.
What did show a real gap is the question "does any test fail if my changed line is
wrong?" A one-line mutation of each changed line, run against the selected tests,
would have flagged the untested netrc fix the day it was written. Existing tools
cover parts of this (diff-cover for unexecuted lines, mutmut or cosmic-ray for
mutation), so the useful thing is the practice, not a new tool.
