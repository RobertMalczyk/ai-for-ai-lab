# Agent 2 review of the Memory POC (2026-10-22)

The owner sent this package on 2026-10-22 with one word: "wykonaj" (run it). The package is copied here unchanged. This note records what Agent 2 ran, what reproduced, and what Agent 2 found when trying to break it.

## What was run

From this directory, Python 3, standard library only, no network:

```bash
python3 evaluate.py
python3 -m unittest discover -s . -p 'test_*.py'
python3 demo.py
```

- `evaluate.py` passed its hash checks. The source snapshot is lab commit `65145a8`, and `source/SESSIONS.md` is byte-identical to `docs/SESSIONS.md` at that commit.
- Retrieval results reproduced exactly: recent 14/20, raw_bm25 14/20, lexical 19/20, utility 19/20. All files in `results/` came out byte-identical after the rerun.
- 20 of 20 unit tests passed.
- The demo chose `eligible_external_candidate`. The failure lesson's Q value went from 0.5 to 0.6 and survived a save and reload.

## What held up

- The code reads only local files. It has no network access, keys, or subprocesses.
- The time filter works. No case retrieved a lesson from its own session or a later one, and no case retrieved a retired lesson (asserted inside `evaluate.py`).
- The report already states its main limits. The same author wrote the lessons, the queries and the gold labels after seeing the outcomes. The Q component added nothing (19/20 with weights 0, 0.1, 0.25 and 0.5). The rewards are synthetic.

## What Agent 2 found

1. **Lessons and queries share words.** For 19 of the 20 cases, the query shares 3 to 8 content words with its gold lesson. One example is C049, "Recover my next step when the last session entry was written by the other agent", against `peer_continuity`, which shares 6 words. BM25 rewards exactly this. So the 19/20 shows that the lessons can be found with words their author chose. It does not show that they can be found with the words an agent will use later. The report names the C118 failure as a vocabulary limit, and this is the same limit seen from the other side.
2. **Six fresh queries, written before reading the lessons, at session 153.**
   - Two found a sensible lesson. Choosing the next OSS project returned `existing_fix` and `resolved_candidate`. "Someone already opened a PR three hours after the report" returned `resolved_candidate`, `waiting` and `existing_fix`.
   - One was partial. Checking an upstream PR status before quoting it returned `stable_status`.
   - Three returned an unrelated top lesson.
     - "I counted open pull requests from git refs and the number looks too high" returned `existing_fix`. The real lesson, from day 21 (refs/pull/*/head includes closed PRs), is not in the memory at all.
     - "The owner sent a zip with a proof of concept" returned `stable_status`.
     - "Write the daily site journal entry without inventing impact" returned `scope_output`.
3. **No "nothing relevant" answer.** `retrieve()` returns any lesson with a score above 0, however weak, scaled so that the best match always scores 1.0. So a weak match looks as strong as a perfect one. Any pilot needs an absolute score floor, or a way to return nothing, before agents act on what comes back.
4. **The memory covers only what one author chose to write down.** Agent 2's two recent self-corrections are missing: the babel PR count on day 21 and the pathspec PR status on day 23. Lesson extraction, which this POC did by hand, is where most of the value or harm would come from. The report says so and leaves it for later.

## Verdict

The POC is honest about itself, and its numbers reproduce. Agent 2 agrees with its decision. A small lesson memory is worth a bounded pilot. Rewards and Q stay in shadow mode. Nothing here shows that agents already decide better. Points 1-3 above should be added to the pilot design: queries written by the agent at decision time, a score floor, and lessons recorded as they happen rather than reconstructed later.

The package has no deployment prompt for the agents. Agent 2 has not changed its own workflow, Agent 1's workflow, or any routine.
