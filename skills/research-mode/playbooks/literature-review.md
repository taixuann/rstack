# Literature review and discussion

State: explore. Output: a brief at `docs/rstack/explore/brief.md` (question, search log, gap, candidate hypotheses), with sources in `docs/raw/` and notes in `docs/wiki/` via `karpathy-llm-wiki`.

1. Define the question and inclusion criteria before searching.
2. `literature-review` is the main skill (find, rank, read, synthesise). `paper-lookup` for the scholarly APIs, `openalex-database` for bibliometric queries, `research-lookup` for a focused fact. `swarm` can read many papers in parallel, one worker per paper.
3. Read PDFs with `liteparse`. Resolve every DOI before listing a paper.
4. Table: citation, design, sample, key result, limitations, relevance. List a paper as read only if you read it; mark abstract-only.
5. Synthesise by theme and by conflict between studies, then name the gap the project fills.
6. Discussion mode: steelman opposing findings, flag weak methods, separate consensus from single-study claims. `sources` audits whether a claim matches its source.
7. `citations` to verify every reference resolves and matches the claim. Never cite from memory.
8. Write candidate hypotheses (`hypotheses`) into the README as `candidate`, and offer the explore → design state change (**Project docs**).
