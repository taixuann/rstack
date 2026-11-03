---
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
kind: paper-readme
voice: assistant
paper: <cite>
zotero_key: <key>
doi: <doi>
category: article | review | dataset | standard | patent | other
parts: [<project parts this paper serves>]
---

# <cite>: <short title>

**Status:** <read | snapshotted | unread>. Critic review: <PASS | REPAIR | BLOCKED | NO_REVIEW> (<revision, date>). Discussion with the user: <not started | done on date>.

## The short version

<Relevance verdict in one paragraph: what it gives the project, what it does not, what is unresolved.>

## What to read, in this order

| Order | File | What it is | Read it when |
|---|---|---|---|
| 1 | this README | where things are, what is open | always first |
| 2 | [annotations.md](annotations.md) | the user's Zotero annotations, never edited | you want the user's own questions |
| 3 | [source-analysis.md](source-analysis.md) | the assistant's reading, every statement tagged `[assistant]` | you want what the paper says |
| 4 | [review.md](review.md) | the critic's audit trail; read only the last section | you doubt a claim in the analysis |

Add `learning-<date>.md` and `alignment.md` rows as they appear.

## What is open

- [ ] <next steps, decisions, unresolved conflicts in the paper>

## Integrity record

- `annotations.md`: snapshot date, sha256. No front matter, so the hash stays fixed.
- `source-analysis.md`: reviewed sha256 (front matter excluded) and whole-file sha256.
- `status` and `review` live only in `docs/literature-review/references.yaml`.
