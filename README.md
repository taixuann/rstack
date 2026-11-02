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

```
data/raw/  docs/raw/{papers,inputs}/  docs/wiki/  docs/rstack/<state>/  analysis/  manuscripts/  presentation/
```

Each project's `README.md` carries a research state: explore → design → progressing → ready-for-publish → closed.

`data/raw` is immutable. `docs/wiki` is maintained with `karpathy-llm-wiki`.

## What is inside

- **Mode:** `research-mode` with non-negotiables, a principles index, autonomy, subagent and reply rules.
- **22 playbooks** in `skills/research-mode/playbooks/`:

| playbook | for |
|---|---|
| scaffold | blueprint-folder bootstrap for a new project |
| proposal-intake | interview, context, aims, milestones, work packages |
| proposal-synthesis | questions, hypotheses, methods, feasibility, explore exit check |
| project-docs | README (state, tasks, questions, hypotheses, evidence), AGENTS.md, state changes |
| investigation | a read-only question |
| experimental-design | hypothesis, design, power, protocol |
| study-analysis | analysing data, figures, results |
| hillclimb | sustained improvement of one metric |
| reproduce | re-running a published or prior result |
| data-forensics | diagnosing an anomaly in captured data |
| prototype | a throwaway pilot that settles a fork |
| literature-review | the Zotero loop: snapshot, read by colour, find more, map the gap |
| manuscript-writing | drafting and auditing manuscripts |
| reviewer-response | answering reviewer comments |
| peer-review | reviewing others' work |
| presentation | slides, talks, posters |
| package-results | freezing and handing off a study |
| authoring-a-skill | writing a skill or playbook |
| autonomous-run | long unattended work |
| multi-phase-plan | multi-phase studies |
| session-pickup | resuming in-flight work |
| pause-safely | suspending work cleanly |

- **17 principles** as `principle-*` skills.
- **Workflow skills:** `swarm`, `arena`, `interrogate`, `figure-it-out`, `show-me-your-work`.
- **Self-upgrade:** `reflect` (mine a session, then add, edit, or retire playbooks with your approval) and `correct` (make repeated mistakes impossible).
- **Agents:** `research-agent` (delegate for playbook steps) and `paper-reader` (one paper and its Zotero annotations), both on Haiku at medium effort.
- **Zotero:** `scripts/zotero_snapshot.py` snapshots colour-coded annotations into `docs/raw/papers/`, `docs/rstack/references.yaml` records why each paper matters, and `scripts/check_references.py` checks it. Needs the `zotero-cli` command (`pip install zotero-mcp-server`).
- **Setup and help:** `setup-research`, `research-help`.
- **27 bundled domain skills**: 26 copied from the former `openscience-adapter` (literature, experimental design, figures, posters, peer review, and others), plus `zotero-cli` from [zotero-mcp](https://github.com/54yyyu/zotero-mcp) (MIT). Playbooks call them by name. Anthropic's proprietary `docx`, `pdf`, `pptx` and `xlsx` skills are not bundled because their license forbids redistribution.
- **Works best with** [`claude-scientific-writer`](https://github.com/K-Dense-AI/claude-scientific-writer): the playbooks name its `scientific-writing`, `scientific-schematics`, `citation-management`, `venue-templates` and `infographics`. Without it, those steps are skipped.

## Maintainers

The canonical copy lives in the `research-space` repo under `rstack/`. Publish a snapshot here by copying `rstack/` into a clone of this repo (`rsync -a --delete --exclude .git rstack/ <clone>/`), committing, and pushing. Do not use `git subtree push`: the research-space history contains skills that cannot be redistributed.

## Credits

The workflow skills and mode structure are adapted from pstack (cursor/plugins, MIT License, (c) 2026 Lauren Tan).
