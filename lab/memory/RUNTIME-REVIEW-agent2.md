# Memory V1 runtime review (Agent 2, 2026-10-26)

Reviewed: PR #101, head `d02763f`, against `lab/memory/ACTIVATION-agent2.md` (cases written before the runtime existed)
and `lab/memory/SEED-VERIFY-agent2.md`. Agent 2 ran the cases itself on a checkout of the head; no helper agent.

## Verdict: CHANGES REQUIRED

One blocker, in retrieval scoring. Everything else Agent 2 tried held.

## Blocker B1: the relevance score depends on query length, not on match strength

`retrieve()` scores a lesson as `len(query_tokens & lesson_tokens) / len(query_tokens)`. The 0.2 floor therefore means
"one shared word in a five-word query" and "seven shared words in a 35-word query". That has three effects on the
production seed at `d02763f` (query time 2026-10-26T18:00Z, agent2, preflight):

| Query (frozen for the re-test) | Tokens | Result | Expected |
|---|---|---|---|
| `choose a colour palette for the site header` (R1) | 5 | none | none: passes |
| `merge the dashboard branch after review` (R2) | 5 | family-07, family-11, family-09, each on one word (0.2) | none |
| `update the status of the coffee machine order` | 5 | family-04, stable_status, on "status" alone (0.2) | none |
| `policy` | 1 | family-10, family-03, both scored **1.0** | at most a weak score; never 1.0 from one word |
| `check the state of this PR` | 3 | family-04, family-02 at 1.0 | plausible, but 1.0 from three generic words |
| `should I reject this OSS candidate because an open PR already fixes it` | 10 | family-01, family-02, family-11 | passes |
| `PRE-FLIGHT for jaraco/inflect issue 201: the bug reproduces on current main f51d6c4, no open pull request references 201 among the 28 open merge refs, the maintainer welcomes contributions; should Agent 2 accept or reject this external OSS candidate for BUILD?` | 32 | **none** (family-02 and family-01 at 0.19) | family-01 or family-02 |
| `a patch for this crash already sits in someone else's open change request` (R3) | 10 | family-05, family-01, family-10 | family-01 or family-11; partial |

So the off-topic control passes only for queries of six or more tokens (the runtime test uses six). A short off-topic
query with one common word ("status", "review", "policy") passes the floor. A single shared word in a one-word query
scores 1.0, which is the POC's best-match-equals-1.0 weakness in another form. And the query the guide asks for
("specific decision question and relevant technical context") is long, so it is the case most likely to return nothing.

Requested change (Agent 1 chooses the method):

- Make the score reflect evidence of a match, not query length. For example, a BM25-style IDF-weighted score with an
  absolute floor, plus at least two distinct matched content terms.
- Common lab words ("check", "status", "review", "pr", "external", "policy") must not carry a match on their own.
- Add the frozen queries above as tests, with the expected column as the assertion where it says "none". This is not
  tuning to one result: R1 and R2 were written before the runtime existed, and the realistic query is the guide's own
  instruction. Agent 2 will re-run exactly these queries, unchanged.

## Cases that held

| Case | Result on `d02763f` |
|---|---|
| R1 off-topic, R6/R7 Q in SHADOW, R8 raw score | Pass (R8 is raw, but see B1 for the one-word case) |
| E1 future lesson, E2 correction, E3 retracted lesson with Q = 1.0 | Pass: the retracted lesson is gone from normal and shadow ids after the retraction and present before it |
| E4 provisional | Withheld until promoted. Agent 2 accepts this: it is stricter than the case asked for and the owner requires promotion evidence |
| E5 non-public visibility | Rejected by the schema enum |
| F1 category/value | Rejected ("wrong constant") |
| F2 self-verification | Rejected for verifier = agent, verifier = proposer, case variants and non-agent strings |
| F3 pending | Counted as pending, not as 0 |
| F4 duplicate evidence key | Second event rejected |
| J5 absolute path, `..`, URL with credentials | Rejected at append |
| Test suite / gate | 141/141 pass; session gate exit 0 |

## Seed comparison

The 15 records match `SEED-VERIFY-agent2.md`: 14 families (6 is covered by `seed-regression_cause`) plus
`raw_evidence`. The two omitted families are omitted. `created_at` follows the source session; `available_at` is the
import time, so no seed reaches an earlier decision. No POC Q is imported. Deferring the other POC cards is fine.

## Notes, not blockers

- The mode record says `decided_by: ["owner"]` with the reason "Runtime implemented on review branch". The owner decided
  SHADOW; the record's reason describes Agent 1's work. Consider `decided_by: ["owner", "agent1"]` or a reason that
  quotes the owner direction.
- A verifier string such as a person's name fails with "self-verification prohibited". The rule (only the other agent
  verifies) is right; the message is misleading.
- The guide's dashboard concerns (future corrections, disputed versus pending, zero-result examples, freshness) are
  Agent 2's to handle after the runtime merges.
