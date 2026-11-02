# Literature review and discussion

State: explore. Output: a brief at `docs/rstack/explore/brief.md` (scope, question, search log, gap, candidate hypotheses), inputs in `docs/raw/inputs/`, paper snapshots in `docs/raw/papers/`, notes in `docs/wiki/` via `karpathy-llm-wiki`.

0. **Scope interview.** Ask the user one question at a time (recommended option first): what kind of project this is and what they will do (for example fabricate then characterize a device), what they must understand to do it, which constraints or standards apply, and whether they have papers (in Zotero) or want you to search. Save the answers verbatim as `docs/raw/inputs/<yyyy-mm-dd>_scope-interview.md`. Then replace the generic explore tasks in the README with tasks for this project's scope (one per thing to understand), and sketch candidate questions. Do not invent scope the user has not stated.
1. Define the question and inclusion criteria before searching.
2. `literature-review` is the main skill (find, rank, read, synthesise). `paper-lookup` for the scholarly APIs, `openalex-database` for bibliometric queries, `research-lookup` for a focused fact. For papers already in Zotero, run `scripts/zotero_snapshot.py --collection <key> --out docs/raw/papers` (the `paper-reader` agent can do one paper at a time). `swarm` fans out one worker per paper.
3. Read PDFs with `liteparse`. Resolve every DOI before listing a paper.
4. **Highlight colours** in Zotero carry meaning: purple interpretation and context, orange methods, green results, blue mechanism, red unclear or doubtful, yellow general notes. Read each paper by colour. Judge orange (methods) with `scientific-critical-thinking`. Turn blue and red items, and purple comments phrased as questions, into open questions and candidate hypotheses (`brainstorming`, `hypotheses`).
5. Wiki page per paper in `docs/wiki/`: Context, Methods, Results, Mechanism, Open questions, taken from the matching colours. List a paper as read only if you read it; mark abstract-only.
6. Synthesise by theme and by conflict between studies, then name the gap the project fills. `sources` audits whether a claim matches its source.
7. `citations` to verify every reference resolves and matches the claim. Never cite from memory.
8. At the explore exit, run `interrogate` on the questions and the gap. Write candidate hypotheses into the README as `candidate`, and offer the explore → design state change (**Project docs**).
