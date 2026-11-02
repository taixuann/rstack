# Literature review and discussion

State: explore, after the Proposal interview. Output: `docs/rstack/explore/03_literature-map.md` (themes, search log, gap), paper snapshots in `docs/raw/papers/`, notes in `docs/wiki/` via `karpathy-llm-wiki`.

0. Read `00_interview.md`, `01_context.md`, and `02_aims-and-milestones.md`. The search serves the work packages and questions they name. If they do not exist yet, run the **Proposal** playbook first.
1. Define the question and inclusion criteria before searching.
2. `literature-review` is the main skill (find, rank, read, synthesise). `paper-lookup` for the scholarly APIs, `openalex-database` for bibliometric queries, `research-lookup` for a focused fact. For papers already in Zotero, run `scripts/zotero_snapshot.py --collection <key> --out docs/raw/papers` (the `paper-reader` agent can do one paper at a time). `swarm` fans out one worker per paper.
3. Read PDFs with `liteparse`. Resolve every DOI before listing a paper.
4. **Highlight colours** in Zotero carry meaning: purple interpretation and context, orange methods, green results, blue mechanism, red unclear or doubtful, yellow general notes. Read each paper by colour. Judge orange (methods) with `scientific-critical-thinking`. Turn blue and red items, and purple comments phrased as questions, into open questions and candidate hypotheses (`brainstorming`, `hypotheses`).
5. Wiki page per paper in `docs/wiki/`: Context, Methods, Results, Mechanism, Open questions, taken from the matching colours. List a paper as read only if you read it; mark abstract-only.
6. Synthesise by theme and by conflict between studies, then name the gap the project fills. `sources` audits whether a claim matches its source.
7. `citations` to verify every reference resolves and matches the claim. Never cite from memory.
8. Write the gap into `03_literature-map.md`, then continue the Proposal playbook (`04` and `05`, then the exit check).
