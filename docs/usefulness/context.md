# Usefulness test: context-saving tool and practices

Tester: independent subagent, 2026-10-06. The lab checkout was read-only. The
subagent could not write a file, so Agent 2 transcribed its returned results here.
Repos: psf/requests (HISTORY.md), pallets/flask (CHANGES.rst, upgrade 3.1.3 -> main).

| Item | Verdict | Evidence |
| --- | --- | --- |
| `review` (scoped claim review) | NICHE | Flask upgrade, 5 claims over 6 files: flagged 3, only 1 really changed (redirect default now 303). 2 false alarms (a removed `# type: ignore`; unchanged signature). Full reread 126972 B, scoped 98784 B (-22.2%) plus 2930 B of JSON. `git diff --stat` gives the same changed-file list in 303 B; one `grep` per claim answers all 5 correctly in 586 B. |
| Latest-section read | EQUAL | The lab's heading-based read prints whole real changelogs (64563/64563 and 73648/73648 B, 0% saved): they have no `## ` headings and put the newest release on top. The lab's `tail -n 170` baseline returns 2011-era releases. A plain `awk '/^Version /{n++} n==2'` gives the latest released section in 206 B (requests equivalent 257 B). On the lab's own diary the 81% saving reproduces (2314 vs 12196 B), but `grep -n '^## ' \| tail -1` plus `sed` gives the same 2314 B. |
| Continuity window | NICHE | Hard-codes "Agent 2"/"administrator"; returns the whole file on real logs. The normal tool is `git log <my-last-sha>^..HEAD --oneline` (1817 B for 28 commits in requests). |
| Unique-line edit anchor | EQUAL | Claude Code's Edit tool already refuses a repeated anchor ("Found 53 matches" for `**Bugfixes**`). Raw `patch` does misplace silently (exit 0, wrong release), so the advice matters only for agents using raw patch. |
| Targeted tool discovery | EQUAL | Names first and definitions on demand is how the harness already works (ToolSearch). The lab's own caveat puts the saving against a careful targeted query at about 2 entries (4-5 KB). |

Who benefits: essentially nobody outside the lab. The percentages measure the lab's
own earlier inefficiency (an oversized `tail`, broad tool lists), not a gain over what
a competent agent already does.
