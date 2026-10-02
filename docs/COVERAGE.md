# Declaration coverage audit

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab coverage --root .
```

The equivalent direct-module form emits the same JSON and exit code:

```bash
PYTHONPATH=src python3 -m ai_for_ai_lab.coverage --root .
```

A fresh checkpoint cannot notice new files it never captured. This read-only
audit compares the current claim declarations against Git's inventory under
`src/` and `tests/`. It includes tracked paths and nonignored untracked files,
so staging is not required to detect a new module. Ignored untracked files and
paths outside those two directories are explicitly outside scope. Tracked paths
remain inventoried even when a matching ignore pattern exists or the working
file was deleted. There is no recursive submodule inventory.

The JSON report has version=1, scope, coverage_complete, tracked_files,
untracked_files, covered_files, and uncovered (path/git_state pairs). Paths are
sorted; NUL-delimited Git output preserves spaces and newlines in filenames.
Exit 0 means all inventoried paths occur somewhere in the declarations; exit 1
means gaps; exit 2 means invalid input or inability to inventory. `git_error`
means Git failed or timed out; `invalid_repository` means root is not the worktree
root; missing Git is `io_error`. Git is needed only for this command.

`coverage_complete=true` is not evidence freshness, dependency completeness,
semantic correctness, or proof that files exist. Empty inventories can be fully
covered; inspect the reported counts. A wrong claim can mention a path and satisfy
this audit. Use checkpoint inspection separately to detect edits/deletions of
captured evidence. Missing paths outside the inventory cannot be discovered here.
The original omitted-dependency benchmark is retained, not relabeled as solved.

When a gap is reported, inspect the file, decide which claims really depend on it,
then update handoff/claims.json, run tests, and refresh the checkpoint deliberately.
Do not auto-assign every file to every claim merely to get a green result.

The audit never modifies the index, claims or checkpoint. Inventory assumes a
quiescent worktree; concurrent staging/edits are not an atomic snapshot. This
first version reports separately from the checkpoint; session instructions require
both checks, but neither command silently changes the behavior of the other.
