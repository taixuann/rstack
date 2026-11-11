# Playbooks

rstack has 21 playbooks in `skills/research-mode/playbooks/`. `research-mode` picks one from the project state and the task.

| playbook | group | for |
|---|---|---|
| literature-review | phase | the Zotero loop: ingest papers, run the inquiry, find more, map the gap |
| inquiry | phase | align the user's reading with the assistant's, interrogate both, extend, search, claim |
| proposal-synthesis | phase | questions, hypotheses, methods, feasibility, explore exit check |
| experimental-design | phase | one note per experiment: purpose, design, materials and stocks, preparation order, protocol, characterization tiers; units in `samples.csv` |
| raw-intake | phase | checking and correcting raw filenames and date folders, dry run first, sealed by `.intake.log` |
| analysis-plan | phase | README, inputs menu and provenance-ready scripts for one analysis |
| analysis-run | phase | run through `rstack_run.py`: one provenance folder per figure, checks, replay, tick after the user sees it |
| analysis-review | phase | changed run (compare, accept one) or challenge (independent critic on a run, then the whole analysis); `check` gates cited results |
| package-results | phase | build a self-contained `package/` from the accepted runs; the user confirms every claim, nothing is guessed |
| state-review | phase | gate review at every state exit: rules per state, findings become tasks |
| investigation | anytime | a read-only question |
| hillclimb | anytime | sustained improvement of one metric |
| reproduce | anytime | re-running a published or prior result |
| prototype | anytime | a throwaway pilot that settles a fork |
| peer-review | anytime | reviewing others' work |
| reviewer-response | anytime | answering reviewer comments |
| task-tracking | support | the only writer of `docs/rstack/tasks.md` (Phase > Goal > Task), kept in step with Notion |
| project-docs | support | README (state, tasks, questions, hypotheses, evidence), AGENTS.md, CLAUDE.md stub, state changes |
| obsidian-writing | support | notes the user comments on in Obsidian: front matter, Mermaid diagrams, comment threads |
| protocol-wiki | support | fill the lab `wiki/` of reusable protocols with `doc-coauthoring`: question sweep, section by section, reader test; wiki first or design first |
| authoring-a-skill | support | writing a skill or playbook, with a reuse-first sourcing ladder |

## Workflow skills

`swarm` (parallel workers), `arena` (compare options), `interrogate` (adversarial review or interview), `figure-it-out` (design a playbook when none fits), `show-me-your-work` (decision log), `statechart` (model a workflow in TLA+), `unslop`, `reflect` and `correct` (improve the method), `init`, `setup-research`, `research-help`.
