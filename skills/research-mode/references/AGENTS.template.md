# AGENTS.md

Operating rules for agents in `<project>`. This file holds the project's rules. Current research state lives in `README.md`, not here.

## State rules

- Read `state` in the `README.md` front matter before any task.
- Work must fit the state. Allowed: explore → Literature review, Inquiry, Proposal synthesis, Investigation. design → Experimental design, Prototype. progressing → Raw intake, Analysis plan, Analysis run, Analysis review, Hillclimb, Prototype, Reproduce. ready-for-publish → Peer review, Package results (writing and slides are the wstack plugin's). closed → Reviewer response. If the request does not fit, say so and propose the state change.
- Run the State review playbook before any state change. Advance the state only at an approved gate (below), and add a row to the README State history. Moving backwards is allowed. Log the reason.
- `docs/rstack/tasks.md` (Phase > Goal > Task) is the source of truth for tasks. Edit it through the Task tracking playbook, then run `scripts/sync_readme_tasks.py <project>` (in the `research-mode` skill folder) so the README task block matches.
- Write each stage's documents under `docs/rstack/<state>/`.

## Layout and write permissions

| Folder | Holds | Agents may |
|---|---|---|
| `data/raw/` | Source measurements | Read only. Never edit, rename, or regenerate |
| `docs/literature-review/papers/<cite>/` | Everything for one paper: `README.md` (start here, with the paper's metadata), `annotations.md` (frozen Zotero snapshot, `scripts/zotero_snapshot.py`), `alignment.md`. Every file except `annotations.md` carries front matter: `created`, `updated`, `kind`, `voice`, `paper` | Add or refresh; never hand-edit `annotations.md`; keep `README.md` and `updated` current |
| `docs/literature-review/cross-papers/` | Synthesis across papers: comparison tables, themes, gap map | Write; label statements; cite the paper folders |
| `docs/inputs/` | The user's own words, as `<date>_<kind>_<slug>.md` (kinds: understanding, learning, supervisor, result-thought) | Append new dated files; never edit |
| `docs/literature-review/reports/` | Deep-research and HyperResearch outputs. Leads, not read papers | Append new dated files; never edit; use nothing until checked against a paper |
| `docs/literature-review/references.yaml` | Which Zotero papers matter and why | Write; run `scripts/check_references.py` after |
| `docs/rstack/<state>/` | Stage documents; `docs/rstack/tasks.md` holds the tasks; explore also holds the raw `00_interview.md` (append, never edit) | Write |
| `analysis/` | Scripts, figures, tables | Write |
| `docs/wstack/`, `docs/reports/`, `docs/writing/`, `docs/presentation/` | Written by the wstack plugin: control files, reports, manuscripts, slides | Read only for rstack; numbers in them come from `analysis/` |

## Zotero highlight colours

Purple: interpretation and context. Orange: methods. Green: results. Blue: mechanism. Red: unclear or doubtful. Yellow: general notes. Comments carry the user's own questions.

## Data protection

- <Data-specific rule, for example human-subject data stays local and identifiers stay out of filenames and logs.>
- Do not invent measurements, metadata, or thresholds. Missing facts stay `TODO: unknown`.

## Commands

TODO: unknown. Environment setup, the one command that reruns the pipeline from `data/raw/`, and the validation command.

## Analysis rules and what enforces them

| Rule | Enforced by |
|---|---|
| Check tasks finish before main, main before verify | `rstack_run.py run` refuses (gate on README Tasks) |
| A run serves a task that names its figure | `rstack_run.py run` refuses with no such task |
| One run makes one figure; it writes only `figures/<figure>/` and `tables/<figure>*` | Runner marks the run `rejected` |
| Figures are saved with figrecipe (`<figure>.yaml`, `<figure>_data/`) through `analysis/lib/style.py` | Runner marks the run `rejected` |
| A result has an executable check | No `<figure>.checks.py` leaves the run `completed`; `tick` refuses |
| A task is ticked only after the user saw the figure | `rstack_run.py tick` needs `--approved-by-user` (a declaration, not a proof) |
| A result can be reproduced | `rstack_run.py replay` compares `<figure>_data/` and tables, with the run's snapshot of `analysis/lib/` |
| A figure's preset is chosen per figure and snapshotted; a style override is recorded | `style.new_figure(preset)` copies the preset into the run; `save_figure` writes `style_overrides.json`; the runner warns |
| Small derived inputs are kept with the run | Runner copies derived inputs up to 5 MB into `inputs/`; raw files are hashed |
| Provenance is tracked in git | Runner warns when `.rstack/` is git-ignored |
| An accepted figure has a result file; a re-run supersedes it | `tick` writes `docs/results/<figure>.md` and lists superseded runs |
| A figure sent to a paper or slide names its run | `rstack_run.py export` copies it as `<run id>_<figure>.png` after a hash check |
| A failed or rejected run leaves no files in `figures/` or `tables/` | Runner restores them; the run's files stay in its own `outputs/` |
| Every figure in `figures/` has a verified run, and says which | `check` fails with no `run.txt` or a different run id inside the png |
| A figure has an objective and a reason before it runs | `rstack_run.py run` refuses while Objective or Why in `docs/method.md` is missing or TODO |
| A claim is re-checked after the result changes | `claim_for` in the results file; `show` flags it, `check` fails it for cited results |
| A package never contains a guessed result | `rstack_run.py package` refuses a TODO or stale claim, a missing Question, Objective or Why, a failing `check`, and mixed lib versions; its README is built from files |
| A package reproduces on its own | `reproduce.py` checks every file hash and the figure data; prove it in a clean environment |
| A review is a real review | `check` refuses TODO in it and a `blocking:` count that the findings table contradicts |
| A cited result was reviewed on its current run by someone who did not make it | `cited: true`; `check` needs a usable `review.md` in the run and `docs/review.md` covering it |
| Figure style: no title, 3 to 5 ticks, decimal labels, SI units | `style.save_figure` raises on a violation; the runner does not re-check style |

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

- Every number in `README.md` and `docs/writing/` traces to a script and an input.
- Rerun the pipeline from a clean state before reporting. Label post-hoc findings.
- Log decisions in `docs/rstack/decisions.tsv` (`show-me-your-work`).
