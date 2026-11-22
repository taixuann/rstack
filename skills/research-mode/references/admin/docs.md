# Docs job

Write or refresh a project's `README.md`, `AGENTS.md`, and `CLAUDE.md` from the templates in `references/`. Used at every phase change and to refresh. The first write is done by the **init** skill.

1. Read the existing files. Never overwrite facts the user wrote.
2. Fill only what is known: from the user, from `data/raw/` metadata, from files you read. Everything else stays `TODO: unknown`. Never invent devices, subject counts, rates, or citations.
3. README is the front page and map of content, kept short (**principle-minimize-reader-load**). It holds the state header, the task block, a Contents list of links to each stage's documents, questions grouped by work package, and the State history. No folder tree, install, licence, or changelog sections.
   - The task block is generated from `docs/rstack/tasks.md`. Change tasks only through the Tasks job (`references/admin/tasks.md`).
   - Name work packages and questions in plain words and sentences. No codes like WP1 or Q1.1.
   - Each question owns its decision, its hypotheses with status (candidate, frozen, supported, rejected) and design link, and its evidence (data, accepted results, reproduce command).
   - Shared data: put the detailed inventory in `data/raw/README.md` and link it from each question.
4. AGENTS.md is the stable operating contract. It changes rarely. Do not put results or tasks in it.
   - `CLAUDE.md` is a stub from `references/CLAUDE.template.md` that imports `AGENTS.md` (`@AGENTS.md`). Claude Code reads `CLAUDE.md` and not `AGENTS.md`; Codex and other tools read `AGENTS.md`. Keep one source of truth: never copy rules into `CLAUDE.md`.
5. Tasks live in `docs/rstack/tasks.md`, written only by the Tasks job. Seed a new phase from its starting tasks in `references/phases/<phase>.md`, then tailor it to the project's scope (explore does this through the **init** skill).
6. Phase change is in **Project admin**.
7. Read both files back and report what is still `TODO`.

Default tasks, exit checks and skills per phase are in `references/phases/<phase>.md`.

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
