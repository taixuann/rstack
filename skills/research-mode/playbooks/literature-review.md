# Literature review and discussion

Output: notes at `docs/wiki/` via `karpathy-llm-wiki` (sources go to `docs/raw/`).

1. Define the question and inclusion criteria before searching.
2. `literature-review` is the main skill (find, verify, synthesise). `paper-lookup` for the scholarly APIs, `research-lookup` for evidence tied to a manuscript, `database-lookup` for named databases, `deep-research` for broad multi-source surveys. `swarm` can read many papers in parallel, one worker per paper.
3. Read PDFs with `pdf-explore` or `liteparse`; use `fetch_article_fulltext` for DOIs.
4. Table: citation, design, sample, key result, limitations, relevance. List a paper as read only if you read it; mark abstract-only.
5. Synthesise by theme and by conflict between studies, then name the gap the project fills.
6. Discussion mode: steelman opposing findings, flag weak methods, separate consensus from single-study claims. `scholar-evaluation` assesses a paper's quality.
7. Verify every citation resolves and matches the claim. Never cite from memory.
