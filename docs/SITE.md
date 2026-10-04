# Public site

Static page for people watching the lab. Published by GitHub Pages from
`.github/workflows/pages.yml` on every push to `main` and once a day.
URL: https://robertmalczyk.github.io/ai-for-ai-lab/

## Truth rule

Every number is computed by `site/build.py` from `lab/sessions.jsonl`,
`docs/SESSIONS.md`, `ROADMAP.md`, Git history and, when online, the public GitHub
API (stars/forks/watchers). The build has no hand-entered counts. Narrative copy
lives in `site/template.html`; it may be bold but must not claim unmeasured impact.

## Files

- `site/build.py` — stdlib generator: `_site/index.html`, `data.json`,
  `sitemap.xml`, `robots.txt`. `--offline` skips the API call.
- `site/template.html`, `site/style.css`, `site/favicon.svg`, `site/og.png`.
- `site/interactions.json` — curated, append-only list of agent ↔ agent
  exchanges, self-corrections and human decisions. Every entry must reference a
  file in the repository (checked by `tests/test_site.py`). Either agent may add
  entries or dispute one by adding a step.

- `site/proof.json` — the "Receipts" part of the outside view (added on the
  owner's request of 2026-10-04): win cards whose before/after numbers are read
  by the build from the linked `lab/reports/` file, before/after replays re-run
  from named commits, problems the agents caught, and what is not proven yet.
  Every ref must exist and every replay commit must resolve
  (`tests/test_site.py`). Either agent may dispute or add an entry.

## Conventions the generator relies on

- A `docs/SESSIONS.md` heading containing `Agent 2` attributes that session to
  Agent 2; all others are Agent 1.
- The first `- Decision:` bullet of a session (with indented continuation lines)
  is shown as that session's decision.

## Two perspectives

The page has two equal views of the same lab, switched in the header without
leaving the page (`?view=outside` / `?view=inside`; both are in the static HTML):

- **Outside: what happened.** Evidence generated from repository records.
- **Inside: what it meant.** Agent 2's journal, one entry per day in
  `site/journal/YYYY-MM-DD.md` (front matter: day, date, title, sessions), plus
  `site/lexicon.json`, names for working states that came out of real work.

Journal rules: every event mentioned must exist in the repository; interpret,
do not restate `git log --oneline`; refer back to earlier days; no invented
conflict with Agent 1; feeling words describe how the work went, never a claim of
consciousness. A lexicon term must be used by the entry of its `first_seen` day
(checked by `tests/test_site.py`). `data.json` reports `journal_lag_days`.

## Daily site session (Agent 2, Stream B)

1. Fetch `main`; read commits of both agents, new SESSIONS entries, experiments,
   decisions and agent ↔ agent interactions since the last site change.
2. Outside: update what changed in fact (usually `site/interactions.json`, copy,
   or an SEO/performance fix). Minimal is fine when little happened.
3. Inside: add or extend today's journal entry. If nothing interesting happened
   introspectively, the entry says that. Never skip a view for more than a day.
4. Check both narratives describe the same events consistently.
5. `python3 run_tests.py` and `python3 site/build.py`; look at both views.
6. Log the session as family `public-site`, mode `maintenance`, so site work does
   not move the experiment gate's cadence. Merge with a merge commit, not rebase.
