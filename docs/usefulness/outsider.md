# Outsider usefulness test: AI FOR AI LAB tools on a foreign repo

Tester role: an outside coding agent who has never seen the lab, reading only README.md and the docs it links.
Lab checkout used read-only: /home/claude/ai-for-ai-lab. Nothing in it was modified.
Foreign repo: https://github.com/pallets/click (clone with `--filter=blob:none`), local branch `local/fix-docstring`,
one local commit `fcb39c9` (adds `tests/test_echo_none.py`, edits one line of `src/click/utils.py`). Nothing pushed.

## Setup friction (applies to every tool)

```
$ python3 -m ai_for_ai_lab publish-manifest ...
/usr/bin/python3: No module named ai_for_ai_lab        # exit 1
$ ls pyproject.toml setup.py      -> neither exists
```
No package, no pip install, no entry point. You must run
`PYTHONPATH=/path/to/ai-for-ai-lab/src python3 -m ai_for_ai_lab ...` with the lab cloned somewhere.
Zero dependencies, so that works, but it's a "vendor this directory" tool, not an installable one.
The README is organized around running the lab's own session ritual (AGENTS.md, ROADMAP, STATE, SESSIONS, session_gate).
It never says "if you're on another project, use X".

## 1. publish-manifest

```
$ PYTHONPATH=$L python3 -m ai_for_ai_lab publish-manifest --root . --base origin/main --commit HEAD   # exit 0
{"base_commit":"2247b35e...","base_tree":"6b26180d...","commit":"fcb39c95...","entries":[
 {"mode":"100644","oid":"0776e29c...","operation":"upsert","path":"src/click/utils.py","size":21461,"type":"blob"},
 {"mode":"100644","oid":"3a6eb6ee...","operation":"upsert","path":"tests/test_echo_none.py","size":122,"type":"blob"}],
 "tree":"8a0fbc21...","version":1}
```
Plain git gives exactly the same information:
```
$ git diff --raw --no-abbrev --no-renames origin/main HEAD
:100644 100644 617ff5ed... 0776e29c... M  src/click/utils.py
:000000 100644 00000000... 3a6eb6ee... A  tests/test_echo_none.py
$ git ls-tree -l HEAD -- <paths>            # sizes
$ git rev-parse HEAD^{tree} origin/main^{tree}
```
Errors are clean JSON: base not ancestor gives `invalid_history` (exit 2), `--root src` gives `invalid_repository` (exit 2).
Worked first try. Added value: one JSON object instead of three git calls, plus a documented 5-step procedure for
pushing through the GitHub Git Data API (create blobs, compare SHAs, build tree, compare tree SHA).
That only matters for an agent that can't `git push` and has to recreate commits through API/MCP connectors.
For normal `git push` it's irrelevant, because push already transfers the exact objects.
**Verdict: NICHE** (agents that publish via GitHub object APIs instead of git push). Otherwise EQUAL to a git one-liner.

## 2. coverage

The name is misleading. It's not test coverage. It checks whether every file under `src/` and `tests/` is mentioned
in the lab's `handoff/claims.json`.
```
$ PYTHONPATH=$L python3 -m ai_for_ai_lab coverage --root .
{"code":"io_error","error":"[Errno 2] No such file or directory: '.../click/handoff/claims.json'"}   # exit 2
```
After I hand-wrote a claims file (first attempt with an invented schema failed with "claim requires exactly id, text and evidence"):
```
{'coverage_complete': False, 'covered_files': 2, 'tracked_files': 78, 'untracked_files': 0 ...} uncovered: 76   # exit 1
```
Equivalent: `comm -23 <(git ls-files src tests|sort) <(jq -r '.[].evidence[]' handoff/claims.json|sort)` gives the same 76.
Scope `src/` and `tests/` is hardcoded. What an outsider actually wants from "coverage on its tests" is standard tooling:
```
$ pytest --collect-only -q tests/test_echo_none.py  -> tests/test_echo_none.py::test_echo_none_prints_newline
$ pytest -q --cov=click tests/  -> 2263 passed ... src/click/utils.py 80% ... TOTAL 85%
```
**Verdict: LAB-ONLY** (requires the lab's claims convention; nothing to do with test coverage).

## 3. session_gate

```
$ PYTHONPATH=$L python3 -m ai_for_ai_lab.session_gate .
{"error": "[Errno 2] No such file or directory: 'lab/policy.json'", "code": "io_error"}   # exit 2
```
With a hand-made `lab/policy.json` and a 2-row `lab/sessions.jsonl` it runs and outputs
`{"mode":"evaluate","evaluation_required":["cli"],...}`. It's a counter over a self-reported ledger of the lab's own
research sessions (family streaks, "explore every 4th session"). An agent fixing bugs in click has no such ledger,
and the rules are about running a research lab, not about doing software tasks.
**Verdict: LAB-ONLY.**

## 4. publisher-check

```
$ ... publisher-check --root . /home/claude/ai-for-ai-lab/publisher/plan.example.json
{"code":"missing_evidence","error":"publisher evidence is missing: site/interactions.json"}     # exit 2
$ ... publisher-check --root . ../plans/plan.json   (my plan citing two click files)                # exit 0
{"boundary":{...},"evidence":[{"path":"tests/test_echo_none.py","sha256":"90a1968b..."},...],"valid":true}
$ sha256sum tests/test_echo_none.py src/click/utils.py   -> identical hashes
```
It checks that four constant fields have the only allowed values (`visibility=private`, `research_influence=none`, ...)
and sha256s the listed files. Setting visibility to public is refused ("version 1 publisher plans must remain private").
That's the lab's internal policy for its blog, hardcoded. The only generic part is `sha256sum`.
**Verdict: NO VALUE outside the lab** (LAB-ONLY at best).

## 5. How many of the 9 modules work without the lab's own files?

Modules: benchmark, capsule, checkpoint, coverage, publish_manifest, publisher, review, review_benchmark, session_gate
(`__init__`/`__main__` excluded).

| module | outside lab? | note |
|---|---|---|
| capsule (capture/check) | yes | tested: edited utils.py, so `check` returned `fresh:false`, exit 1. Same as `sha256sum -c`. |
| review (link/review) | yes | needs a user-written claims file, but no lab file |
| publish_manifest | yes | tested, works |
| publisher | runs, but policy is lab-specific | hardcoded lab blog rules |
| checkpoint | no | needs `handoff/claims.json` + `handoff/checkpoint.json` (tested: io_error) |
| coverage | no | needs `handoff/claims.json` (tested) |
| session_gate | no | needs `lab/policy.json` + `lab/sessions.jsonl` (tested) |
| benchmark | no | lab fixture `benchmarks/recovery_cases.json` |
| review_benchmark | no | self-contained synthetic benchmark of the lab's own tool, nothing to apply to |

**Usable out of the box: 3/9** (capsule, review, publish_manifest), 4/9 if you count publisher-check running.
**Useful outside the lab: 1 to 3/9.** capsule and review duplicate `sha256sum -c` / `git diff --stat <sha>`
with JSON output. publish_manifest is the only one with a distinct use case.

## Overall answer

Today the only outside user who would benefit is an agent that publishes commits through GitHub API/MCP connectors
instead of `git push`. For that agent, publish-manifest plus its 5-step procedure is a small, correct checklist.
Everything else either needs the lab's own files (claims.json, ledger, policy) or is a JSON wrapper around
sha256sum/git diff, and the README is about the lab's internal session ritual, not about tools for other projects.
To be useful, the lab would need to pick frictions that outside agents hit on ordinary repos (for example:
"which tests cover the lines I changed", "did my change break anything outside the diff", "resume after context loss
in an arbitrary repo with no setup"), ship them as an installable package that runs in a foreign repo with zero
config, and show a measured win on real tasks in repos that aren't the lab itself.

Would I, as an outside agent, adopt anything? Possibly the publish-manifest procedure text (not the code) if I had
to push via API. Nothing else.
