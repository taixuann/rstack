---
phase: explore
updated: YYYY-MM-DD
---

# State & Admin Control (`docs/rstack/`)

This folder tracks the project's **phase state, exit gates, tasks, folder index, and decisions** (`project-admin` and `show-me-your-work`). Project goals, context, milestones, understanding, and research results live in the root [README.md](../../README.md).

## Project Readiness (Aspect Checklist)

Each report carries its own `state:` in `docs/reports/<question>/README.md` (`explore → design → analysis → write → closed`), so one report can advance without locking the rest of the project. This board tracks project-wide readiness across aspects:

| Aspect | Where | Current status |
|---|---|---|
| Understanding | `docs/understanding/README.md` | `TODO: unknown` |
| Literature & Claims | `docs/literature-review/references.yaml` | `TODO: unknown` |
| Reports | `docs/reports/` | `TODO: unknown` |
| Supervisor & Ethics gates | `README.md` | `TODO: unknown` |

## Current Phase & Exit Gate

- **Project-level state:** `explore` (`explore → design → analysis → write → closed`)
- **Exit review target:** reviews/explore.md (when closing `explore`)
- **Gate checklist (to advance to `design`):**
  - [ ] Core questions and falsifiable hypotheses scoped in `docs/reports/<question>/README.md`
  - [ ] Key literature read and verified (`references.yaml` / `claims.md`)
  - [ ] Scope, milestones, and supervisor open points settled
  - [ ] Exit review (`interrogate` + `Project admin`) passed and approved by the user

## Tasks

<!-- tasks:start -->
<!-- tasks:end -->

## Contents (`docs/`)

Standard 7 folders: `docs/{rstack, reports, literature-review, writing, figures, inputs, understanding}`.

- `rstack/` (this folder): [tasks.md](tasks.md), [decisions.tsv](decisions.tsv), `d-inquiry/`, `reviews/`
- [reports/](../reports/): one folder per question (`README.md`, `fundamental/`, `method/`, `results/`)
- [literature-review/](../literature-review/): `references.yaml`, `papers/`, `hyperresearch-reports/`
- [understanding/](../understanding/): project learning notes (`learn-mode`)
- [inputs/](../inputs/): dated raw user/supervisor inputs (immutable)
- [figures/](../figures/) & [writing/](../writing/): shared diagrams and manuscript drafts
