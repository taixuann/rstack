# Playbooks

rstack has 18 playbooks in `skills/research-mode/playbooks/`. `research-mode` picks one from the project phase (explore, design, analysis, write, closed) and the task.

| playbook | phase | for |
|---|---|---|
| literature-review | explore | the Zotero loop: ingest papers, run the inquiry, find more, map the gap |
| inquiry | any | consult the wiki, interview and brainstorm before a search or a design; in explore also align the user's reading with the assistant's, extend, search, claim |
| report-init | explore, design | interview and scope a report (`fundamental/`, `method/`, `analysis/`, `results/` or `N/A`), run `Inquiry`, open `docs/reports/<question>/`, hand tasks to `project-admin` |
| experimental-design | design | one self-contained note per experiment (materials, equipment, procedure, preparation order, characterization tiers), built after an Inquiry on the experiment; no wiki links; units in `method/samples.csv` |
| experiment-log | design | what was done as run, against the frozen design; deviations in one line each |
| raw-intake | analysis | checking and correcting raw filenames and date folders, dry run first, sealed by `.intake.log` |
| analysis-plan | analysis | README, inputs menu and provenance-ready scripts for one analysis |
| analysis-run | analysis | run through `rstack_run.py`: one provenance folder per figure, checks, replay, tick after the user sees it |
| analysis-review | analysis | changed run (compare, accept one) or challenge (independent critic on a run, then the whole analysis); `check` gates cited results |
| analysis-reconcile | analysis | reconcile accepted runs into final `docs/results/` claims, update `docs/reports/<question>/results/README.md` & hypotheses, and pass `check` |
| package-results | analysis | build a self-contained `package/` from the accepted runs; the user confirms every claim, nothing is guessed |
| paper-preparation | write | target and the evidence report (one report per topic) from the analysis outputs; gate `report-approved` |
| paper-writing | write | the user writes; you ask questions from main points to paragraphs; gate `draft-ready` |
| paper-critique | write | critic modes reader, evidence, referee, prose; findings ledger; gate `critique-passed` |
| presentation | write | slides from the same report; the user gives every line |
| peer-review | write | reviewing a manuscript, proposal or analysis |
| reviewer-response | closed | answering reviewer comments |
| project-admin | any | tasks (the only writer of `tasks.md`, mirrored to Todoist), README/AGENTS/CLAUDE, exit review, the phase brief, phase change |

Each phase has a brief in `skills/research-mode/references/phases/<phase>.md`, and the folder standard is `references/layout.md`. Notes the user comments on in Obsidian use the `obsidian-notes` skill.

## Workflow skills

`learn-mode` (project understanding in `docs/understanding/`), `wiki-mode` (cross-project lab `wiki/`), `playbook-control` (meta governance: `figure-it-out`, `correct`, `reflect`, `skill-creator`), `swarm` (parallel workers), `arena` (compare options), `interrogate` (adversarial review or interview), `show-me-your-work` (decision log), `statechart` (model a workflow in TLA+), `unslop`, `init`, `setup-research`, `research-help`.
