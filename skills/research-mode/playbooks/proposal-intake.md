### Proposal intake

State: explore (runs first). Prepare the information the rest of explore needs: what the project is, what it aims to do, and when. Files are flat in `docs/rstack/explore/`.

| File | Holds |
|---|---|
| `tasks.md` | The explore task list. Source of truth for the README task block |
| `00_interview.md` | The user's answers, verbatim and never edited |
| `01_context.md` | Background and problem statement, stakeholders, stack, constraints |
| `02_aims-and-milestones.md` | Aim, 3 to 5 objectives, work packages, milestones with dates, deliverables |

Name each work package in plain words (for example "Electrode fabrication", "Embedded acquisition", "ML signal quality"). Do not use codes like WP1 or Q1.1. Where a stable reference is needed, use a slug of the name.

1. Read `references/explore-questions.md`. Run the interview in short rounds of one to four related questions, with a recommended option first, skipping what is already known. Save the answers verbatim in `00_interview.md`.
2. Use `brainstorming` to propose candidate work packages and directions when the user is unsure, and mark them as proposals.
3. Write `01_context.md` and `02_aims-and-milestones.md` from the answers. For aims, objectives, and the timeline, `research-grants` has useful section structure. Mark anything unanswered `TODO: unknown`.
4. Replace the generic explore tasks in `tasks.md` with ones for this project, grouped by work package. Run `scripts/sync_readme_tasks.py` so the README shows them.
5. Run `interrogate` on the scope: is it too big for the time, are the work packages separable, is anything the supervisor expects missing?
6. Hand off to **Literature review**. Expect to come back and revise `02` once the literature has changed the plan.

**Reply:** the files written, what is still `TODO: unknown`, and the weakest scope risk.
