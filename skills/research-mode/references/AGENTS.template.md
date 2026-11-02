# AGENTS.md

Operating rules for agents in `<project>`. The workspace `AGENTS.md` at the research-space root applies first. This file adds project rules and never relaxes them. Current research state lives in `README.md`, not here.

## State rules

- Read `state` in the `README.md` front matter before any task.
- Work must fit the state. Allowed: explore → Literature review, Investigation. design → Experimental design, Prototype. progressing → Study analysis, Hillclimb, Data forensics, Prototype, Reproduce. ready-for-publish → Manuscript writing, Presentation, Peer review, Package results. closed → Reviewer response. If the request does not fit, say so and propose the state change.
- Advance the state only at an approved gate (below), and add a row to the README State history. Moving backwards is allowed. Log the reason.
- Keep the README Current tasks list to the current state's tasks. On a state change, move the finished list to `docs/rstack/<state>/tasks.md`.
- Write each stage's documents under `docs/rstack/<state>/`.

## Layout and write permissions

| Folder | Holds | Agents may |
|---|---|---|
| `data/raw/` | Source measurements | Read only. Never edit, rename, or regenerate |
| `docs/raw/` | Papers and datasheets | Add after the source is resolved |
| `docs/wiki/` | Synthesized notes (`karpathy-llm-wiki`) | Write |
| `docs/rstack/<state>/` | Stage documents, `decisions.tsv` | Write |
| `analysis/` | Scripts, figures, tables | Write |
| `manuscripts/`, `presentation/` | Drafts and talks | Write; numbers come from `analysis/` |

## Data protection

- <Data-specific rule, for example human-subject data stays local and identifiers stay out of filenames and logs.>
- Do not invent measurements, metadata, or thresholds. Missing facts stay `TODO: unknown`.

## Commands

TODO: unknown. Environment setup, the one command that reruns the pipeline from `data/raw/`, and the validation command.

## Analysis conventions

TODO: unknown. Sampling rate, units, filters, statistics defaults, figure style.

## Gates that need the human

- Every state change.
- Adding any file to `data/raw/`.
- Scientific acceptance of a result.
- Changing a hypothesis or analysis plan after outcome data has been examined.
- Deleting or overwriting an output that a report cites.
- Anything that sends data or text off this machine.

## Verification

- Every number in `README.md` and `manuscripts/` traces to a script and an input.
- Rerun the pipeline from a clean state before reporting. Label post-hoc findings.
- Log decisions in `docs/rstack/decisions.tsv` (`show-me-your-work`).
