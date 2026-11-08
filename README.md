# rstack

The research counterpart to [pstack](https://github.com/cursor/plugins/tree/main/pstack). pstack helps you write less, higher quality code. rstack helps you run research projects the same way: state the question, pick a playbook, delegate deliberately, and verify every number against a file.

## Install

```bash
claude plugin marketplace add taixuann/rstack
claude plugin install rstack@rstack
```

Claude Code leaves auto-update off for third-party marketplaces. To turn it on, run `/plugin`, open the Marketplaces tab, select `rstack`, and choose enable auto-update. To update once by hand: `claude plugin update rstack@rstack`.

In Claude Code, commands take an `rstack:` prefix, such as `/rstack:research-mode`. rstack is written for Claude Code, so there is no name adapter.

## Get started

1. Run `/rstack:setup-research`. It writes your research profile and, optionally, per-role models.
2. Use `/rstack:research-mode` whenever you do research that needs rigor.

New here? The [guide](./docs/guide/README.md) walks through a first task. Stuck? Ask `/rstack:research-help`.

## Standard project layout

| Folder | Holds |
|---|---|
| `data/raw/` | Raw data. Immutable |
| `docs/inputs/` | What came in: proposals, supervisor notes. Never edited |
| `docs/literature-review/` | `papers/<cite>/` (one folder per paper), `cross-papers/`, `reports/` (search reports, leads only) |
| `docs/rstack/<state>/` | The state's tasks, documents, review and decisions |
| `analysis/` | Derived work, each number traced to a script. `analysis/<name>/` holds one analysis; `analysis/lib/` the shared helpers; `analysis/<name>/package/` its self-contained results package |
| `.rstack/provenance/` | One folder per figure run: inputs with hashes, scripts, lib, environment, log, checks, outputs, review. Tracked in git |
| `manuscripts/`, `presentation/` | Writing and talks |


Each project's `README.md` carries a research state: explore → design → progressing → ready-for-publish → closed.

`data/raw` is immutable. Everything about one paper lives in `docs/literature-review/papers/<cite>/`, starting at its `README.md`.

## What is inside

- **Mode:** `research-mode` with non-negotiables, a principles index, autonomy, subagent and reply rules.
- **22 playbooks** in `skills/research-mode/playbooks/`:

| playbook | group | for |
|---|---|---|
| literature-review | phase | the Zotero loop: ingest papers, run the inquiry, find more, map the gap |
| inquiry | phase | align the user's reading with the assistant's, interrogate both, extend, search, claim |
| proposal-synthesis | phase | questions, hypotheses, methods, feasibility, explore exit check |
| experimental-design | phase | hypothesis, design, power, protocol |
| raw-intake | phase | checking and correcting raw filenames and date folders, dry run first, sealed by `.intake.log` |
| analysis-plan | phase | README, inputs menu and provenance-ready scripts for one analysis |
| analysis-run | phase | run through `rstack_run.py`: one provenance folder per figure, checks, replay, tick after the user sees it |
| analysis-review | phase | changed run (compare, accept one) or challenge (independent critic on a run, then the whole analysis); `check` gates cited results |
| manuscript-writing | phase | drafting and auditing manuscripts |
| package-results | phase | build a self-contained `package/` from the accepted runs; the user confirms every claim, nothing is guessed |
| state-review | phase | gate review at every state exit: rules per state, findings become tasks |
| investigation | anytime | a read-only question |
| hillclimb | anytime | sustained improvement of one metric |
| reproduce | anytime | re-running a published or prior result |
| prototype | anytime | a throwaway pilot that settles a fork |
| peer-review | anytime | reviewing others' work |
| reviewer-response | anytime | answering reviewer comments |
| presentation | anytime | slides, talks, posters |
| task-tracking | support | the only writer of `docs/rstack/tasks.md` (Phase > Goal > Task), kept in step with Notion |
| project-docs | support | README (state, tasks, questions, hypotheses, evidence), AGENTS.md, CLAUDE.md stub, state changes |
| obsidian-writing | support | notes the user comments on in Obsidian: front matter, Mermaid diagrams, comment threads |
| authoring-a-skill | support | writing a skill or playbook, with a reuse-first sourcing ladder |

- **20 principles** as `principle-*` skills.
- **Workflow skills:** `swarm`, `arena`, `interrogate`, `figure-it-out`, `show-me-your-work`, `init` (new project: folders, README, AGENTS, CLAUDE, interview), `statechart` (model a workflow in TLA+, check it with TLC, draw it; from pstack), plus the one-line command `unslop`.
- **Self-upgrade:** `reflect` (mine a session, then add, edit, or retire playbooks with your approval) and `correct` (make repeated mistakes impossible).
- **Agents:** `research-agent` (delegate for playbook steps) on Haiku at medium effort; `critic` (independent reviewer of a paper's Source Analysis or of an analysis run) on Sonnet at high effort.
- **Zotero:** `scripts/zotero_snapshot.py` snapshots colour-coded annotations into `docs/literature-review/papers/`, `docs/literature-review/references.yaml` records why each paper matters, and `scripts/check_references.py` checks it. Needs the `zotero-cli` command (`pip install zotero-mcp-server`).
- **Setup and help:** `setup-research`, `research-help`.
- **21 bundled domain skills**: 15 copied from the former `openscience-adapter` (literature, experimental design, figures, peer review, and others), four from [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (MIT: `statistical-analysis`, `statistical-power`, `uncertainty-and-units`, `what-if-oracle`), plus `zotero-cli` from [zotero-mcp](https://github.com/54yyyu/zotero-mcp) (MIT) and `skill-creator` from [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0). Playbooks call them by name. Anthropic's proprietary `docx`, `pdf`, `pptx` and `xlsx` skills are not bundled because their license forbids redistribution.
- **Works best with** [`claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer): the playbooks name its `scientific-writing`, `scientific-schematics`, `citation-management`, `venue-templates` and `infographics`. Without it, those steps are skipped.

## The analysis runner

`skills/research-mode/scripts/rstack_run.py` carries the analysis playbooks. Figures are always made through it, never by hand.

| Command | What it does |
|---|---|
| `new <project> <name> --figure stage:fig` | scaffold an analysis: README, `inputs.yaml`, `docs/`, scripts, the shared `analysis/lib/` |
| `run <analysis> --stage check\|main\|verify --figure F` | refuse out of order or without an Objective and Why; run with figrecipe; snapshot everything; run the checks; status verified, check-failed, rejected, failed or completed (a bad run leaves `figures/` as it was) |
| `tick <analysis> --figure F --approved-by-user [--run ID]` | after you have seen the figure: tick the task, write `docs/results/F.md`; `--run` accepts an earlier verified run |
| `check <analysis>` | figures match their runs, no figure without a verified run, cited results have a real review and a fresh claim |
| `diff`, `replay` | compare two runs; rerun a run and compare its figure data |
| `show <analysis>` | write `provenance.html`: one scroll of figures with objective, claim, review state and tabs for code, inputs, checks, log, environment |
| `export <analysis> --figure F` | copy the accepted figure out as `<run id>_<figure>.png` |
| `package <analysis>` | build `package/`: figures, code, inputs, standalone `reproduce.py`, README from your confirmed claims. Refuses anything unsettled |

The `critic` agent reviews a run or the whole analysis independently; `check` makes a cited result need that review.

## Checks and publishing

- `scripts/check_plugin.py`: playbooks name only skills that exist (bundled or declared in `skills-manifest.yaml`), and the playbook list and counts match the files.
- `scripts/publish.sh`: runs the checks, mirrors this folder into a clone of the GitHub repo, and commits. Pass `--push` to push and update the installed plugin.

## Maintainers

The canonical copy lives in the `research-space` repo under `rstack/`. Publish a snapshot here by copying `rstack/` into a clone of this repo (`rsync -a --delete --exclude .git rstack/ <clone>/`), committing, and pushing. Do not use `git subtree push`: the research-space history contains skills that cannot be redistributed.

## Credits

The workflow skills and mode structure are adapted from pstack (cursor/plugins, MIT License, (c) 2026 Lauren Tan).
