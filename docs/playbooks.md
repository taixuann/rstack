# Playbooks

rstack has 21 playbooks in `skills/research-mode/playbooks/`. `research-mode` picks one from the project phase (explore, design, analysis, write, closed) and the task.

| playbook | phase | for |
|---|---|---|
| literature-review | explore | the Zotero loop: ingest papers, run the inquiry, find more, map the gap |
| inquiry | any | consult the wiki, interview and brainstorm before a search or a design; in explore also align the user's reading with the assistant's, extend, search, claim |
| report-bootstrap | explore, design | questions, hypotheses, methods, feasibility; opens each question's report folder (intention, `fundamental/`); explore exit check |
| experimental-design | design | one self-contained note per experiment (materials, equipment, procedure, preparation order, characterization tiers), built after an Inquiry on the experiment; no wiki links; units in `method/samples.csv` |
| experiment-log | design | what was done as run, against the frozen design; deviations in one line each |
| raw-intake | analysis | checking and correcting raw filenames and date folders, dry run first, sealed by `.intake.log` |
| analysis-plan | analysis | README, inputs menu and provenance-ready scripts for one analysis |
| analysis-run | analysis | run through `rstack_run.py`: one provenance folder per figure, checks, replay, tick after the user sees it |
| analysis-review | analysis | changed run (compare, accept one) or challenge (independent critic on a run, then the whole analysis); `check` gates cited results |
| hillclimb | analysis | sustained improvement of one metric |
| reproduce | analysis | re-running a published or prior result |
| package-results | analysis | build a self-contained `package/` from the accepted runs; the user confirms every claim, nothing is guessed |
| paper-preparation | write | target and the evidence report (one report per topic) from the analysis outputs; gate `report-approved` |
| paper-writing | write | the user writes; you ask questions from main points to paragraphs; gate `draft-ready` |
| paper-critique | write | critic modes reader, evidence, referee, prose; findings ledger; gate `critique-passed` |
| presentation | write | slides from the same report; the user gives every line |
| peer-review | write | reviewing a manuscript, proposal or analysis |
| reviewer-response | closed | answering reviewer comments |
| project-admin | any | tasks (the only writer of `tasks.md`, mirrored to Todoist), README/AGENTS/CLAUDE, exit review, the phase brief, phase change |
| protocol-wiki | any | navigate the lab `wiki/` through its own router; `brainstorming`, `interrogate`, `doc-coauthoring` |
| authoring-a-skill | any | writing a skill or playbook, with a reuse-first sourcing ladder |

Each phase has a brief in `skills/research-mode/references/phases/<phase>.md`, and the folder standard is `references/layout.md`. Notes the user comments on in Obsidian use the `obsidian-notes` skill.

## Workflow skills

`swarm` (parallel workers), `arena` (compare options), `interrogate` (adversarial review or interview), `figure-it-out` (design a playbook when none fits), `show-me-your-work` (decision log), `statechart` (model a workflow in TLA+), `unslop`, `reflect` and `correct` (improve the method), `init`, `setup-research`, `research-help`.
