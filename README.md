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
| `analysis/` | Derived work, each number traced to a script |
| `manuscripts/`, `presentation/` | Writing and talks |

Learning is not in the project folder. Lessons, ingested pages and the roadmap live in Notion (see `docs/statechart/LEARNING.md`).

Each project's `README.md` carries a research state: explore → design → progressing → ready-for-publish → closed.

`data/raw` is immutable. Everything about one paper lives in `docs/literature-review/papers/<cite>/`, starting at its `README.md`.

## What is inside

- **Mode:** `research-mode` with non-negotiables, a principles index, autonomy, subagent and reply rules.
- **22 playbooks** in `skills/research-mode/playbooks/`:

| playbook | group | for |
|---|---|---|
| literature-review | phase | the Zotero loop: ingest papers, run the inquiry, find more, map the gap |
| paper-ingestion | phase | one paper to a frozen Source Analysis reviewed by an independent critic |
| inquiry | phase | align the user's reading with the assistant's, interrogate both, extend, search, claim |
| proposal-synthesis | phase | questions, hypotheses, methods, feasibility, explore exit check |
| experimental-design | phase | hypothesis, design, power, protocol |
| study-analysis | phase | analysing data, figures, results |
| manuscript-writing | phase | drafting and auditing manuscripts |
| package-results | phase | freezing and handing off a study |
| state-review | phase | gate review at every state exit: rules per state, findings become tasks |
| investigation | anytime | a read-only question |
| hillclimb | anytime | sustained improvement of one metric |
| reproduce | anytime | re-running a published or prior result |
| data-forensics | anytime | diagnosing an anomaly in captured data |
| prototype | anytime | a throwaway pilot that settles a fork |
| peer-review | anytime | reviewing others' work |
| reviewer-response | anytime | answering reviewer comments |
| presentation | anytime | slides, talks, posters |
| project-docs | support | README (state, tasks, questions, hypotheses, evidence), AGENTS.md, CLAUDE.md stub, state changes |
| obsidian-writing | support | notes the user comments on in Obsidian: front matter, Mermaid diagrams, comment threads |
| notion-writing | support | lessons the user comments on in Notion: Raw pages, open and closed, Mermaid, native comments |
| authoring-a-skill | support | writing a skill or playbook, with a reuse-first sourcing ladder |
| autonomous-run | support | long unattended work, with pause and resume |

- **17 principles** as `principle-*` skills.
- **Workflow skills:** `swarm`, `arena`, `interrogate`, `figure-it-out`, `show-me-your-work`, `init` (new project: folders, README, AGENTS, CLAUDE, interview), `teach` (teach-back lessons in Notion, from the Roadmap section), `explain` (one flowing account of a meaning), `make-the-figure` (one figure, only where words cannot), `make-me-roadmap` (the learning plan, a Roadmap section on the topic's Map of content page), `evaluate-my-understanding` (mastery levels 0 to 4, in each ingested page's Understanding section), `paper-ingest` (deep read of one paper), `statechart` (model a workflow in TLA+, check it with TLC, draw it; from pstack), plus the one-line commands `bro`, `in-your-own-words`, and `unslop`.
- **Self-upgrade:** `reflect` (mine a session, then add, edit, or retire playbooks with your approval) and `correct` (make repeated mistakes impossible).
- **Agents:** `research-agent` (delegate for playbook steps) on Haiku at medium effort, plus `source-analyst` (deep read of one paper) and `paper-critic` (independent three-pass review), both on Sonnet at medium effort.
- **Zotero:** `scripts/zotero_snapshot.py` snapshots colour-coded annotations into `docs/literature-review/papers/`, `docs/literature-review/references.yaml` records why each paper matters, and `scripts/check_references.py` checks it. Needs the `zotero-cli` command (`pip install zotero-mcp-server`).
- **Setup and help:** `setup-research`, `research-help`.
- **32 bundled domain skills**: 25 copied from the former `openscience-adapter` (literature, experimental design, figures, posters, peer review, and others), five from [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) (MIT: `statistical-analysis`, `statistical-power`, `exploratory-data-analysis`, `uncertainty-and-units`, `what-if-oracle`), plus `zotero-cli` from [zotero-mcp](https://github.com/54yyyu/zotero-mcp) (MIT) and `skill-creator` from [anthropics/skills](https://github.com/anthropics/skills) (Apache-2.0). Playbooks call them by name. Anthropic's proprietary `docx`, `pdf`, `pptx` and `xlsx` skills are not bundled because their license forbids redistribution.
- **Works best with** [`claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer): the playbooks name its `scientific-writing`, `scientific-schematics`, `citation-management`, `venue-templates` and `infographics`. Without it, those steps are skipped.

## Checks and publishing

- `scripts/check_plugin.py`: playbooks name only skills that exist (bundled or declared in `skills-manifest.yaml`), and the playbook list and counts match the files.
- `scripts/publish.sh`: runs the checks, mirrors this folder into a clone of the GitHub repo, and commits. Pass `--push` to push and update the installed plugin.

## Maintainers

The canonical copy lives in the `research-space` repo under `rstack/`. Publish a snapshot here by copying `rstack/` into a clone of this repo (`rsync -a --delete --exclude .git rstack/ <clone>/`), committing, and pushing. Do not use `git subtree push`: the research-space history contains skills that cannot be redistributed.

## Credits

The workflow skills and mode structure are adapted from pstack (cursor/plugins, MIT License, (c) 2026 Lauren Tan).
