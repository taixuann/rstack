---
name: using-rstack
description: "Interactive intent router for rstack: interviews and interrogates what the user actually wants to achieve, checks the active project's state, and dispatches to the right mode (learn-mode, wiki-mode, research-mode, or playbook-control) and playbook. Use for /using-rstack or when the user is unsure which mode or playbook to run."
---

# Using rstack

Start from **intention**, not command names. Run `interrogate` (interview mode) in 1–3 short questions (offering quick-select options or freeform answers) to clarify what the user wants to accomplish, which project (if any) it targets, and what concrete output counts as done.

## 1. Clarify the intention (`interrogate` interview mode)

Ask only what is missing:
1. **Goal:** What outcome do you want right now?
2. **Scope:** Is it for a specific project (`projects/res_<name>/`), for the shared lab `wiki/`, or for `rstack` workflows themselves?
3. **Project state (when targeting a project):** Read `state` in `<project>/README.md` (`explore`, `design`, `analysis`, `write`, `closed`).

## 2. Route to the right mode

| Intention | Route to | Why / Next step |
|---|---|---|
| Learn a concept, capture your reading/notes into `docs/inputs/` and `docs/understanding/` | `learn-mode` | Shapes project understanding with `doc-coauthoring` + `obsidian-notes`, refreshes `qmd` |
| Record reusable lab procedures, equipment setup, or protocols across projects | `wiki-mode` | Writes in `wiki/` (`protocol-wiki` + `doc-coauthoring`), refreshes `qmd -c wiki` |
| Execute research work on a project (literature search, report init, design, log, analysis, writing) | `research-mode` | Picks the matching playbook for the project's `state` (or proposes a state change via `Project admin`) |
| Design a bespoke workflow, fix a recurring mistake, upgrade/author skills, or model-check a state machine | `playbook-control` | Routes to `figure-it-out`, `correct`, `reflect`, `statechart`, or `skill-creator` |

## 3. Hand off

State the clarified intention, the chosen mode (and playbook, if `research-mode`), and proceed directly with that mode's workflow (or hand the user the exact prompt if they asked only for routing).
