# Docs job

Write or refresh a project's `README.md`, `docs/rstack/README.md`, `AGENTS.md`, and `CLAUDE.md` from `templates/project/`. Used at every phase change and to refresh. The first write is done by the **init** skill.

1. Read the existing files. Never overwrite facts the user wrote.
2. Fill only what is known: from the user, from `data/raw/` metadata, from files you read. Everything else stays `TODO: unknown`. Never invent devices, subject counts, rates, or citations.
3. `README.md` (at the project root) is the project's scientific front page: it holds the `state:` header, **Goal & Context**, **Aim & Milestones**, **Understanding** summary table, questions grouped by work package (with decision, hypotheses, status, evidence), and State history. `docs/rstack/README.md` holds the phase-state & exit-gate control board, the synced task block (`<!-- tasks:start -->`...`<!-- tasks:end -->`), and the `docs/` Contents index for `project-admin`.
   - The task block is generated from `docs/rstack/tasks.md`. Change tasks only through the Tasks job (`references/admin/tasks.md`).
   - Name work packages and questions in plain words and sentences. No codes like WP1 or Q1.1.
   - Each question owns its decision, its hypotheses with status (candidate, frozen, supported, rejected) and design link, and its evidence (data, accepted results, reproduce command).
   - Shared data: put the detailed inventory in `data/raw/README.md` and link it from each question.
4. `AGENTS.md` is the stable project-specific operating contract (data protection/ethics, run commands, analysis conventions, human gates). Do not duplicate `rstack`'s global playbook table or task/result lists inside `AGENTS.md`.
   - `CLAUDE.md` is a stub from `templates/project/CLAUDE.md` that imports `AGENTS.md` (`@AGENTS.md`) and points to `/using-rstack`, `/research-mode`, and `qmd -c <project>`. Keep one source of truth: never copy rules into `CLAUDE.md`.
5. Tasks live in `docs/rstack/tasks.md`, written only by the Tasks job. Seed a new phase from its starting tasks in `references/phases/<phase>.md`, then tailor it to the project's scope (explore does this through the **init** skill).
6. Phase change is in **Project admin**.
7. Read both files back and report what is still `TODO`.

Default tasks, exit checks and skills per phase are in `references/phases/<phase>.md`.

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
