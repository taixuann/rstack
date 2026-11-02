### Project docs

Write or refresh a project's `README.md` and `AGENTS.md` from the templates in `references/`. Used by Scaffold, and at every state change.

1. Read the existing files. Never overwrite facts the user wrote.
2. Fill only what is known: from the user, from `data/raw/` metadata, from files you read. Everything else stays `TODO: unknown`. Never invent devices, subject counts, rates, or citations.
3. README is the research state: the front matter `state`, the one-sentence question, hypotheses with their status, evidence, accepted results, open questions, and a State history row per change. Keep it short and scannable. No install, licence, or changelog sections. Lead with the conclusion (**principle-minimize-reader-load**).
4. AGENTS.md is the stable operating contract. It changes rarely. Do not put results in it.
5. State change: confirm the exit check for the current state with the user, set `state` and `updated`, add the History row, and create `docs/rstack/<new-state>/`. Exit checks: scaffold → explore: folders exist and a question is drafted. explore → design: literature synthesis in `docs/wiki/`, gap named, candidate hypotheses written. design → progressing: design note and analysis plan frozen, sample size justified. progressing → ready-for-publish: planned analyses done, every result accepted or rejected, pipeline rerun clean. ready-for-publish → closed: submitted, published, or abandoned, with the reason.
6. Read both files back and report what is still `TODO`.

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
