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

## Conventions the generator relies on

- A `docs/SESSIONS.md` heading containing `Agent 2` attributes that session to
  Agent 2; all others are Agent 1.
- The first `- Decision:` bullet of a session (with indented continuation lines)
  is shown as that session's decision.

## Daily site session (Agent 2, Stream B)

1. Fetch `main`; read SESSIONS entries and commits since the last site change.
2. Ask: what one thing happened that is worth showing? Add it (usually an
   `interactions.json` entry or a copy change), not a rewrite.
3. `python3 run_tests.py` and `python3 site/build.py`; look at `_site/index.html`.
4. Log the session as family `public-site`, mode `maintenance`, so site work does
   not move the experiment gate's cadence.
