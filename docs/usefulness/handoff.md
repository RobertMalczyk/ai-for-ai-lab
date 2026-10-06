# Usefulness test: handoff/freshness tools (`capture`/`check`, `checkpoint`)

Tester: independent subagent, 2026-10-06. Lab checkout used read-only at
`/home/claude/ai-for-ai-lab` (nothing modified). Workdir:
`$WORK/handoff/`.
Raw transcripts (every command, exit code, byte count, full output):
`log_requests.txt`, `log_click.txt`, `log_checkpoint.txt`, `log_setup.txt` in the same dir.
Harness: `run.sh` (`r` prints `$ cmd`, `[exit=N bytes=N]`, output; `lab` = `PYTHONPATH=<lab>/src python3 -m ai_for_ai_lab`).

## Bottom line

* `capture`/`check` = `sha256sum files > note.sha256` / `sha256sum -c note.sha256`
  wrapped in JSON plus two text fields. On every committed-history scenario it reported
  exactly what `git diff --stat <old>..HEAD -- <files>` reported, with *less*
  information (no line counts, no commit messages). It **missed** both "trap"
  scenarios (relevant change in an unlisted file; change-then-revert) — so does
  path-filtered `git diff`, but unfiltered `git diff --stat`/`git log` caught both
  in 76-142 bytes. Its only real win is a note captured on a **dirty** working
  tree, which `sha256sum -c` or `git stash create` handle equally well.
* `checkpoint` adds a claim -> files grouping. That is the only output git does not
  hand you directly. It is hardwired to `handoff/claims.json` + `handoff/checkpoint.json`
  inside the target repo, writes lab-specific goal text, and has no docs in `--help`.

Verdicts: **capture/check: EQUAL** (NICHE at best: dirty-tree note in a non-git or
git-averse setup). **checkpoint: NICHE** (a team that maintains a hand-written
claim->file map and wants a per-claim "needs_review" list; nobody outside the lab does this today).

## Repos and setup

```
git clone -q --filter=blob:none https://github.com/psf/requests   # 6495 commits
git clone -q --filter=blob:none https://github.com/pallets/click
```
Capsules stored outside the repos in `caps/`.

## Scenarios and raw results

### R1 — requests: relevant change in a listed file
Note at `3816cfa1`: goal "Make no_proxy parsing robust to whitespace/empty entries",
next step "Edit should_bypass_proxies/proxy_bypass in src/requests/utils.py, add cases to tests/test_utils.py".
Resume at `a4f9a599` ("Port bpo-39057 to Requests" = someone already did this work).
```
$ lab check --root . caps/R1.json
[exit=1 bytes=142]
{"evidence":[{"path":"src/requests/utils.py","status":"changed"},{"path":"tests/test_utils.py","status":"changed"}],"fresh":false,"version":1}

$ git diff --stat 3816cfa1..HEAD -- src/requests/utils.py tests/test_utils.py
[exit=0 bytes=137]
 src/requests/utils.py |  6 ++++--
 tests/test_utils.py   | 23 +++++++++++++++++++++++
 2 files changed, 27 insertions(+), 2 deletions(-)

$ git log --oneline 3816cfa1..HEAD -- src/requests/utils.py tests/test_utils.py
[exit=0 bytes=43]
a4f9a599 Port bpo-39057 to Requests (#7427)
```
Capsule tells "changed". git tells "changed, +27/-2, by commit 'Port bpo-39057'" — i.e. *the task is already done*. Capsule cannot say that.

### R2 — requests: only unrelated files changed
Note at `fd628095` on adapters.py + tests/test_adapters.py; resume at `cd90742e` (11 other files changed).
```
$ lab check --root . caps/R2.json
[exit=0 bytes=151]
{"evidence":[{"path":"src/requests/adapters.py","status":"unchanged"},{"path":"tests/test_adapters.py","status":"unchanged"}],"fresh":true,"version":1}

$ git diff --stat fd628095..HEAD -- src/requests/adapters.py tests/test_adapters.py
[exit=0 bytes=0]
```
Both correct, no false alarm. git: 0 bytes; capsule: 151 bytes.

### R3 — requests: relevant change in a file the note did NOT list
Note at `b684dcb9`: next step "Annotate Session.request headers/params using SupportsItems in src/requests/sessions.py", evidence = sessions.py only.
Resume at `3816cfa1` "Parameterize SupportsItems to handle Mapping key invariance" (changes `_types.py`, which defines SupportsItems).
```
$ lab check --root . caps/R3.json
[exit=0 bytes=96]
{"evidence":[{"path":"src/requests/sessions.py","status":"unchanged"}],"fresh":true,"version":1}

$ git diff --stat b684dcb9..HEAD -- src/requests/sessions.py
[exit=0 bytes=0]

$ git diff --stat b684dcb9..HEAD
[exit=0 bytes=125]
 src/requests/_types.py | 10 ++++++----
 src/requests/utils.py  |  6 +++---
 2 files changed, 9 insertions(+), 7 deletions(-)

$ git log --oneline b684dcb9..HEAD
[exit=0 bytes=76]
3816cfa1 Parameterize SupportsItems to handle Mapping key invariance (#7426)
```
Capsule says `fresh:true` with exit 0 = **false reassurance**. The commit subject literally names the thing the next step depends on.

### C1 — click: change then revert (A->B->A)
Note at `f67c2bb`: "Deprecate parameter names that are not Python identifiers", evidence core.py + tests/test_deprecations.py.
Resume at `d036881` after `e2bddbc` implemented exactly that and `d036881` reverted it.
```
$ lab check --root . caps/C1.json
[exit=0 bytes=148]
{"evidence":[{"path":"src/click/core.py","status":"unchanged"},{"path":"tests/test_deprecations.py","status":"unchanged"}],"fresh":true,"version":1}

$ git diff --stat f67c2bb..HEAD -- src/click/core.py tests/test_deprecations.py
[exit=0 bytes=0]

$ git log --oneline f67c2bb..HEAD -- src/click/core.py tests/test_deprecations.py
[exit=0 bytes=142]
d036881 Revert "Deprecate a parameter name that is not a Python identifier"
e2bddbc Deprecate a parameter name that is not a Python identifier
```
Capsule: "fresh". Reality: the planned change was made and deliberately reverted by maintainers — the single most important fact for the next step. Only `git log` shows it.

### C2 — click: uncommitted edit after a clean-tree note
Capture at `a59f7c6`, then append a WIP line to core.py.
```
$ lab check --root . caps/C2.json
[exit=1 bytes=142]
{"evidence":[{"path":"src/click/core.py","status":"changed"},{"path":"tests/test_options.py","status":"unchanged"}],"fresh":false,"version":1}

$ git status --short
[exit=0 bytes=20]
 M src/click/core.py
```
Equal detection; git 20 bytes vs 142.

### C3 — click: note captured on a DIRTY tree, then further edited (the capsule's one real case)
```
$ git status --short          # at capture time
 M src/click/core.py
# ... another edit appended ...
$ lab check --root . caps/C3.json
[exit=1 bytes=142]
{"evidence":[{"path":"src/click/core.py","status":"changed"},{"path":"tests/test_options.py","status":"unchanged"}],"fresh":false,"version":1}
$ git status --short          # identical to capture time -> git status alone cannot tell
[exit=0 bytes=20]
 M src/click/core.py
```
C3b: edit undone back to note-time bytes -> capsule `fresh:true` (exit 0, 143 bytes) while `git status` still shows ` M`. Correct and git-status-alone can't do this.

But the same is achievable with tools every agent has (C3d):
```
$ sha256sum src/click/core.py tests/test_options.py > caps/C3.sha256
$ sha256sum -c caps/C3.sha256
[exit=1 bytes=105]
src/click/core.py: FAILED
tests/test_options.py: OK
sha256sum: WARNING: 1 computed checksum did NOT match

$ git stash create            # at note time, record this hash in the note
4f48a6bd0cdbad14701ab6923bd71565524ba511
$ git diff --stat 4f48a6bd0cdbad14701ab6923bd71565524ba511 -- src/click/core.py tests/test_options.py
[exit=0 bytes=56]
 src/click/core.py | 1 +
 1 file changed, 1 insertion(+)
```
`git stash create` beats the capsule here: same detection AND it can show the actual diff (`git diff <hash>`), which a SHA-256 cannot.

### K1 — `checkpoint` on click
Hand-wrote `handoff/claims.json` at `6d5bac5` (3 claims, 6 files), `checkpoint --refresh`, resumed at `2247b35`.
```
$ lab checkpoint --root . --refresh
[exit=0 bytes=58]
{"claims":3,"saved":"handoff/checkpoint.json","version":1}

$ lab checkpoint --root .        # at 2247b35
[exit=1 bytes=508]
{"claims":[{"changed_evidence":["src/click/core.py"],"id":"help-param","status":"needs_review"},{"changed_evidence":["src/click/utils.py","tests/test_utils/test_make_default_short_help.py"],"id":"short-help","status":"needs_review"},{"changed_evidence":[],"id":"types-path","status":"evidence_unchanged"}],"fresh":false,"missing_paths":[],"reread_paths":["handoff/claims.json","src/click/core.py","src/click/utils.py","tests/test_info_dict.py","tests/test_utils/test_make_default_short_help.py"],"version":1}

$ git diff --stat 6d5bac5..HEAD -- <same 5 files>
[exit=0 bytes=254]
 src/click/core.py                                | 253 ++++++++++++++++++++---
 src/click/utils.py                               |  52 ++---
 tests/test_utils/test_make_default_short_help.py |  28 ++-
 3 files changed, 274 insertions(+), 59 deletions(-)

$ git log --oneline --no-merges 6d5bac5..HEAD -- <same 5 files>
[exit=0 bytes=301]
9f0bcdf Add `Parameter.spec` and deprecate `human_readable_name`
b90faad Deprecate a parameter name that Click 9.0 will refuse or lower case
f67c2bb Fix short help abbreviation
05f6fd0 Always return a help record for an `Argument`
f25f697 List every argument in the `Positional arguments` help section
```
Claim "short-help: truncation bug is open" -> checkpoint says `needs_review`; git log says
"Fix short help abbreviation" — i.e. the claim is now false. Claim "help-param: Argument help
rendering still pending" -> git log shows "Always return a help record for an `Argument`".
The per-claim grouping is the only thing git doesn't hand over; git log answers the actual question.

Side effects: `checkpoint` writes `handoff/checkpoint.json` into the user's repo (`git status`: `?? handoff/`);
the embedded capsule goal/next_step are hardcoded lab text ("Resume AI FOR AI LAB from declared
project evidence", checkpoint.py `refresh`). Without the files:
```
$ lab checkpoint --root .
[exit=2 bytes=192]
{"code":"io_error","error":"[Errno 2] No such file or directory: '.../click/handoff/checkpoint.json'"}
```

## Comparison table

| Scenario | (a) blind trust | (b) plain git | (c) capsule / checkpoint | Capsule info git lacked? |
|---|---|---|---|---|
| R1 listed file changed | miss (redoes done work) | detect; 1 cmd, 137 B (+43 B log gives "why") | detect; 2 cmds (capture+check), 142 B | none |
| R2 unrelated change | ok | ok, 0 B, no false alarm | ok, 151 B, no false alarm | none |
| R3 relevant change in unlisted file | miss | path-filtered: miss (0 B); unfiltered diff/log: **detect** (125 B / 76 B) | **miss, fresh:true** | none (worse) |
| C1 change+revert | miss | diff: miss; `git log -- files`: **detect** (142 B) | **miss, fresh:true** | none (worse) |
| C2 dirty after clean note | miss | detect, `git status` 20 B | detect, 142 B | none |
| C3 dirty-at-note, edited further | miss | `git status`: can't tell; `sha256sum -c` 105 B or `git stash create`+`git diff` 56 B: detect | detect, 142 B | only vs bare `git status` |
| K1 checkpoint, 3 claims | miss | detect, 254 B diff / 301 B log w/ reasons | detect, 508 B, per-claim grouping | claim->file grouping only |

False alarms: none from any method in these scenarios (all ran on tracked files; byte-identical revert not flagged by either).
Command count: capsule always needs 2 commands (capture at note time + check); git needs 0 at note time
(the commit hash is usually already in the note / `git log`) and 1-2 at resume.

## Setup friction for an outsider
* No `pyproject.toml`/`setup.py`; not on PyPI (`pip download ai-for-ai-lab` -> "No matching distribution found").
  Usage requires cloning the lab and `PYTHONPATH=<lab>/src`.
* `python3 -m ai_for_ai_lab --help` lists 8 subcommands with no per-command description;
  `check --help` shows only `--root ROOT capsule`. The claims.json format, exit-code meaning and
  checkpoint file locations are only in `docs/CAPSULE.md`, `docs/REVIEW.md`, `docs/CHECKPOINT.md`.
* Upside: zero dependencies, Python stdlib only, ran first time, clean JSON, consistent exit codes.

## Verdicts
* **capture/check: EQUAL** to `sha256sum`/`sha256sum -c` and weaker than `git diff`/`git log`
  (no magnitude, no commit reasons, path-only scope gives false `fresh:true` in R3 and C1).
  Niche where it is not worse: snapshotting a dirty or non-git directory — already covered by coreutils.
* **checkpoint: NICHE** — a project that maintains a hand-written claim->evidence map and wants
  a "which claims to re-verify" list. It's the lab's own workflow; on click it needed a hand-authored
  JSON file in a fixed path in the repo and told me less than `git log` about whether claims still hold.

Who benefits concretely: the lab itself (self-use), and possibly agents working in non-git
directories with no shell coreutils — a very rare setup. A normal coding agent on a git repo
gets more from `git log --oneline <note-commit>..HEAD` (+ `git status`), at fewer bytes, with
no setup. Biggest real risk: `fresh:true` / exit 0 reads as "safe to proceed" when it isn't (R3, C1).
