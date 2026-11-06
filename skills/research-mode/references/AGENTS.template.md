# AGENTS.md

Operating rules for agents in `<project>`. This file holds the project's rules. Current research state lives in `README.md`, not here.

## State rules

- Read `state` in the `README.md` front matter before any task.
- Work must fit the state. Allowed: explore → Literature review, Paper ingestion, Inquiry, Proposal synthesis, Investigation. design → Experimental design, Prototype. progressing → Study analysis, Hillclimb, Data forensics, Prototype, Reproduce. ready-for-publish → Manuscript writing, Presentation, Peer review, Package results. closed → Reviewer response. If the request does not fit, say so and propose the state change.
- Run the State review playbook before any state change. Advance the state only at an approved gate (below), and add a row to the README State history. Moving backwards is allowed. Log the reason.
- Each state has `docs/rstack/<state>/tasks.md`, the source of truth for tasks. After editing it, run `scripts/sync_readme_tasks.py <project>` (in the `research-mode` skill folder) so the README task block matches.
- Write each stage's documents under `docs/rstack/<state>/`.

## Layout and write permissions

| Folder | Holds | Agents may |
|---|---|---|
| `data/raw/` | Source measurements | Read only. Never edit, rename, or regenerate |
| `docs/literature-review/papers/<cite>/` | Everything for one paper: `README.md` (start here, with the paper's metadata), `annotations.md` (frozen Zotero snapshot, `scripts/zotero_snapshot.py`), `source-analysis.md`, `review.md`, `alignment.md`. Every file except `annotations.md` carries front matter: `created`, `updated`, `kind`, `voice`, `paper` | Add or refresh; never hand-edit `annotations.md`; keep `README.md` and `updated` current |
| Notion (learning) | Raw pages the user writes (lessons, overview and branches), ingested pages, the topic's Map of content page, and the Log. No `docs/learning/` folder | Write through `teach`, `explain`, `make-me-roadmap`, `evaluate-my-understanding` and `notion-llm-wiki`; label statements; stop at each item's Enough-means line; send lesson text only, never signals or subject data |
| `docs/literature-review/cross-papers/` | Synthesis across papers: comparison tables, themes, gap map | Write; label statements; cite the paper folders |
| `docs/inputs/` | The user's own words, as `<date>_<kind>_<slug>.md` (kinds: understanding, learning, supervisor, result-thought) | Append new dated files; never edit |
| `docs/literature-review/reports/` | Deep-research and HyperResearch outputs. Leads, not read papers | Append new dated files; never edit; use nothing until checked against a paper |
| `docs/literature-review/references.yaml` | Which Zotero papers matter and why | Write; run `scripts/check_references.py` after |
| `docs/rstack/<state>/` | Stage documents and `tasks.md`; explore also holds the raw `00_interview.md` (append, never edit) | Write |
| `analysis/` | Scripts, figures, tables | Write |
| `manuscripts/`, `presentation/` | Drafts and talks | Write; numbers come from `analysis/` |

## Zotero highlight colours

Purple: interpretation and context. Orange: methods. Green: results. Blue: mechanism. Red: unclear or doubtful. Yellow: general notes. Comments carry the user's own questions.

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
