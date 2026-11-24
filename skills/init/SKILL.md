---
name: init
description: Starts a research project, or adds rstack to an existing one. Creates the standard folders and README.md, AGENTS.md and CLAUDE.md, then interviews the user to write the context, aims and milestones. Use for /init in a research project (instead of the built-in /init), or when the user wants to start, bootstrap, scaffold, or set up a new research project.
---

# Init

One command from an empty folder to a project with its front docs and a first interview. It replaces the old Scaffold and Proposal intake playbooks. In a research project use this, not the built-in `/init`: the built-in one writes a generic software `CLAUDE.md`.

State after init: `explore`. Init is a trigger, not a state.

## 1. Orient

Confirm the project folder (default: a new folder under `research-space/projects/`, named `res_<name>`) and whether it is new or existing. For an existing folder, list what is already there. Never rename, move, or overwrite. Map legacy folders instead of moving them (`manuscripts/` to `docs/writing/<piece>/`, `presentation/` to `docs/presentation/<piece>/`, `docs/experiments` to `docs/reports/<question>/`; `scripts/check_layout.py` lists what does not fit) and ask before moving anything.

## 2. Create the structure

Run `../research-mode/scripts/init_project.py <project> [--title "<title>"]`. It creates the folders below with `.gitkeep`, then `README.md` (state `explore`), `AGENTS.md`, `CLAUDE.md` (a stub that imports `AGENTS.md`), `docs/rstack/README.md`, and `docs/rstack/tasks.md` (Phase > Goal > Task), and syncs the task block. It skips anything that exists and says so. If it reports the task block was not synced (an old `docs/rstack/README.md` without the markers), add the markers per `../research-mode/templates/project/rstack-README.md` and run `sync_readme_tasks.py`.

```
data/raw/                              immutable source measurements; never edit, never regenerate
docs/rstack/                           phase state & exit gate control (README.md), tasks.md, decisions.tsv, d-inquiry/
docs/reports/                          one folder per question (README.md, fundamental/, method/, results/)
docs/literature-review/papers/<cite>/  one folder per paper: README, annotations, alignment
docs/literature-review/hyperresearch-reports/ HyperResearch and deep-research reports (leads)
docs/literature-review/references.yaml which papers matter and why
docs/writing/                          manuscript drafts and talk notes
docs/figures/                          shared diagrams and figures
docs/inputs/                           the user's own words, dated, never edited
docs/understanding/                    project learning notes (`learn-mode`)
analysis/                              scripts, figures, tables
```

`data/raw` holds measurements and `docs/literature-review` holds literature. Keep them separate. Derived data goes in `analysis/`, never back into `data/raw`.

## 3. Interview

Read `../research-mode/references/explore-questions.md`. Run the interview with `interrogate` in interview mode: short rounds of one to four related questions, a recommended option first, skipping what is already known. Save the answers verbatim in `docs/inputs/<date>_interview_<slug>.md` (a new dated file per session, never edited, with the input front matter). If the user is unsure what the work packages are, use `brainstorming` to propose candidates and mark them as proposals.

Do not invent devices, subject counts, rates, dates, or citations. Anything unanswered stays `TODO: unknown` with an owner (the user or the supervisor).

## 4. Write the front docs

From the answers write directly into the root `README.md` (Context, Aim & Milestones, work packages) and `docs/rstack/README.md` (phase state & explore exit-gate checklist):

| Where | Holds |
|---|---|
| `README.md` | Project overview: `state:`, Context (background, stakeholders, stack, constraints), Aim & Milestones (3–5 objectives, work packages, milestones with dates), Tasks, Contents (`docs/`), State history |
| `docs/rstack/README.md` | Current phase state, exit-gate checklist for advancing to `design`, and index of `tasks.md`, `decisions.tsv`, `d-inquiry/` |

Name each work package in plain words ("Electrode fabrication", "Embedded acquisition"). No codes like WP1 or Q1.1. `research-grants` has useful section structure for aims and timelines.

Then fill the project facts in `AGENTS.md` that the interview answered (data protection and ethics rules when people are recorded; environment and the rerun command stay `TODO: unknown` until known). Replace the generic goals and tasks in `tasks.md` with ones for this project (the **Project admin** (Tasks job) playbook owns the file from here on), and run `../research-mode/scripts/sync_readme_tasks.py <project>`. Link the new files in the README Contents.

## 5. Challenge the scope

Run `interrogate` on the scope: is it too big for the time, are the work packages separable, is anything the supervisor expects missing? List the points only the supervisor can answer as a task.

## 6. Log and hand off

Append rows to `docs/rstack/decisions.tsv` (**show-me-your-work**) for the folder creation, the interview, and each document written. Read the tree back from disk. Offer the **Literature review** playbook next, and expect to revise `02` once the literature changes the plan.

**Reply:** the files written (as clickable paths), what is still `TODO: unknown`, the weakest scope risk, and the next step.
