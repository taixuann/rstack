### Project admin

Phase: any. Keeps a project's documents, tasks and phase in order, and gives a bot the brief for one phase. It runs as the advisor for the project's tasks and is the only writer of `README.md`, `AGENTS.md`, `CLAUDE.md` and `docs/rstack/tasks.md`. Read `references/layout.md` first; it says where everything lives.

Pick the job, then read the one reference it names:

| Job | When | Read |
|---|---|---|
| Tasks (advisor) | Any time, asked or not: reads Todoist and the project, advises on arrangement, records decisions in `docs/rstack/`. Also when the user changes tasks | `references/admin/tasks.md` |
| Docs | Write or refresh README, AGENTS, CLAUDE; the first write is done by the **init** skill | `references/admin/docs.md` |
| Exit review | A phase is about to end | `references/admin/exit-review.md` |
| Brief | A bot is assigned a phase, or a session starts cold | `references/phases/<phase>.md` |
| Change phase | The exit review passed and the user approved | below |

**Task principles.** One task per outcome. A chain (Before, Steps, Done when, After) goes in the task's `Detail:` lines and its Todoist description, never in extra tasks or deeper levels. Dates, deadlines and reminders are the user's; a step waiting on something the user does not control gets none. Details and the check: `references/admin/tasks.md`.

**Phase brief.** `references/phases/<phase>.md` holds, for one phase: the entry check, the playbooks in order, what each reads and writes (rows of `layout.md`), the exit-gate angles, the starting tasks, and what done means. A bot given a phase reads that file, then the playbooks in order, and stops at the gate.

**Change phase.**
1. Run the exit review for the current phase and clear its blocking tasks.
2. Confirm the exit with the user. Never advance without it. Moving backwards is allowed; log the reason.
3. Set `state` and `updated` in `README.md` (old names `progressing` and `ready-for-publish` still read as `analysis` and `write`). Add the State history row.
4. Give the phase's new documents `phase: <new-phase>` in their front matter; create `docs/rstack/reviews/` for the exit review when needed.
5. Ask the Tasks job for the new `## Phase:` section, seeded from the phase file's starting tasks and tailored to the project. The old section stays as its record.
6. Add the new phase's line to the README Contents and sync (`scripts/sync_readme_tasks.py`).
7. Run `scripts/check_layout.py <project>` and tell the user about any unknown folder. Never move one.

**Keeping records.** Besides the tasks, project-admin keeps the records in step with the work: `docs/rstack/` documents and `reviews/`, `decisions.tsv` rows, the README state, task block and Contents, and each question's `docs/reports/<question>/README.md` (its status and its table of analyses, papers and talks). It records only what the user decided or what a file shows; its own judgment is shown first.

Other skills: `interrogate` (exit review adversaries), `setup-research` (reports missing external skills and tools, with install steps).

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
