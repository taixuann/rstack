### Proposal

State: explore (runs first). Turn the user's project into a proposal-shaped set of documents, so the literature review has something to serve. Follows the standard proposal chain: problem → gap → question → methodology → expected outcomes, with objectives, milestones, and feasibility.

Files, flat in `docs/rstack/explore/`:

| File | Holds |
|---|---|
| `tasks.md` | The explore task list. Source of truth for the README's task block |
| `00_interview.md` | The user's answers, verbatim and never edited |
| `01_context.md` | Background and problem statement, stakeholders, stack, constraints |
| `02_aims-and-milestones.md` | Aim, 3 to 5 objectives, work packages, milestones with dates, deliverables |
| `03_literature-map.md` | Themes, search log, links to `docs/wiki/`, the gap |
| `04_questions-and-hypotheses.md` | Questions and candidate hypotheses per work package |
| `05_methods-and-feasibility.md` | Candidate methods per work package, resources, risks, ethics, fallbacks |

Add `06_*` files only when needed. Keep each file short and link, don't copy.

1. Read `references/explore-questions.md`. Run the interview one question at a time, skipping what is already known. Save the answers verbatim in `00_interview.md`.
2. Write `01_context.md` and `02_aims-and-milestones.md` from the answers. Mark anything unanswered `TODO: unknown`. Group work by work package, one per separable domain.
3. Replace the generic explore tasks in `tasks.md` with ones for this project: one per thing to understand or decide, grouped by work package. Run `scripts/sync_readme_tasks.py` so the README shows them.
4. Hand off to the Literature review playbook for `03_literature-map.md`, then write `04` and `05` (`hypotheses`, `brainstorming`, `experimental-design` for method candidates).
5. At the exit, assemble the proposal chain from the files and run `interrogate` on it: does the problem exist, does the gap follow from the literature, does the question address the gap, can the methods answer it, are the milestones feasible? Fix weak links, then offer the explore → design state change (**Project docs**).

**Reply:** the files written, what is still `TODO: unknown`, and the weakest link in the chain.
