# Project layout

Every folder a project may have, who writes it, and whether it is read-only. A playbook opens by naming the rows it reads and writes. `scripts/check_layout.py <project>` flags any folder not listed here (for example a stray `manuscripts/`). To add a folder, add its row here first.

| Path | Holds | Written by | Read-only? |
|---|---|---|---|
| `README.md`, `AGENTS.md`, `CLAUDE.md` | Front page and state, operating contract, import stub | project-admin | no |
| `data/raw/` | Measurements as received, one dated folder per intake | raw-intake | yes, after the intake log seals it |
| `docs/inputs/` | The user's own words, dated: `<date>_<kind>_<slug>.md`, kind one of understanding, learning, supervisor, result-thought, interview, inquiry, brainstorm (the last two are assistant-written working notes: `voice: assistant`, `source: assistant`, `confirmed: no`). Front matter: `created`, `kind`, `voice`, `source`, `topic`, `report`, `confirmed` | the user, or inquiry on their behalf | the body yes; the front matter may grow |
| `docs/figures/` | Figures that illustrate project documents (understanding notes, the docs index), as `.svg` with a `.png` export. A figure for one report goes in that report's `figures/` | the user, with the assistant | no |
| `docs/understanding/` | The user's understanding notes, kept beside the work: `README.md` is the index, one note per topic, labelled `[user]` or `[assistant]`. Basic, Core and Advanced levels of the Deepen understanding tasks | the user, with `doc-coauthoring` | no |
| `docs/literature-review/papers/<cite>/` | README, annotations, alignment for one paper | literature-review, inquiry | `annotations.md` yes |
| `docs/literature-review/hyperresearch-reports/` | HyperResearch and deep-research reports as `<date>_<tool>_<slug>.md`: leads, not read papers. Move the final report here from the vault; its `[[...]]` links still point at the vault | none | yes |
| `docs/literature-review/claims.md` | One line per claim from the papers and from the reports, each with its source type (paper or report), cite and page, label and status. A report claim stays a lead until a paper the user read confirms it | inquiry | no |
| `docs/literature-review/references.yaml` | Which Zotero papers matter and why | literature-review | no |
| `docs/rstack/tasks.md`, `todoist-map.tsv` | The task list and its Todoist map | project-admin only | no |
| `docs/rstack/requests.tsv` | Handoffs between role bots: date, from, to, kind, text, status (see `docs/bots/README.md`) | any bot appends; the recipient sets `status` | append only |
| `docs/rstack/decisions.tsv` | Decision trail of long or unattended work | show-me-your-work | append only |
| `docs/rstack/<NN>_<name>.md` | The project's own documents, flat, each with `phase:` in its front matter (01_context, 02_aims-and-milestones, 03 to 05 and, in analysis, `results.md`). Never brainstorm or inquiry files | the phase's playbooks | no |
| `docs/rstack/reviews/<phase>.md` | One exit review per phase | project-admin (exit review) | no |
| `docs/rstack/d-inquiry/` | One brief per deep-research search as `<date>_<about>.md` (questions and context only), only. The question log and wiki lookups are dated `inquiry` files in `docs/inputs/` | inquiry, literature-review (reads) | no |
| `docs/rstack/writing/<piece>/` | One piece's control files: `target.md`, `todo.md`, `decisions.tsv`, `findings.tsv`, `scaffold/`, `review/` | paper-preparation, paper-writing, paper-critique (through `writing.py`) | the gates only through the script |
| `docs/reports/<question>/` | One folder per question, plus shared `docs/reports/resources.md` (general lab inventory: 3-tier Equipment & Software, Materials/Tools/Consumables, Raw Chemicals, Standing Stocks & Standard Reagents — never report-specific beaker labels) and `docs/reports/samples.yaml` (shared `devices` & `library_studies`). Inside each report: `README.md` (index, intention, hypotheses, plan, status, links), `fundamental/` (user understanding then checked facts), `procedure/<slug>.md` (self-contained single-file SOP per procedure, one `## E<n>` block per stage, no wiki links), `samples.yaml` (report-specific `r.[...]` `remarks` only — no `planned_runs` or invented IDs), `log.md` (as-run bench log), `results/README.md`, and paper evidence files (`claims.yaml`, `methods.yaml`, `figures.yaml`, `citations.yaml`, `limitations.md`). (Legacy `method/` + `samples.csv` still readable.) | `README.md`, `fundamental/`: report-init; `procedure/<slug>.md`, `resources.md`, `samples.yaml`: experimental-design; `log.md`: experiment-log; `results/README.md`: analysis-reconcile; evidence files: paper-preparation | `procedure/<slug>.md` after the design gate; the evidence files after `report-approved`; the rest stays open |
| `docs/writing/<piece>/` | `main.tex`, `references.bib`, `figures/`, `sections/` | the user; the assistant never writes prose | no |
| `docs/presentation/<piece>/` | Slides | the user | no |
| `analysis/lib/` | Shared project-wide analysis library (`load.py`, `style.py`, `figrules.py`) and shared config home (`analysis/lib/plot-config.yaml`, `analysis/lib/color-code.yaml`) | analysis-plan (`rstack_run.py lib`) | no |
| `analysis/<name>/docs/results.md` | Consolidated Check/Main/Verify results and cross-checks for one analysis | analysis-reconcile | no |
| `analysis/<name>/docs/results/<figure>.md` | One page per accepted figure, beside the run that made it | analysis-run (`rstack_run.py tick`) | no |
| `analysis/<name>/` | Scripts, figures, tables, `package/`, `export/` | analysis-plan, analysis-run, package-results | outputs of an accepted run: yes |
| `.rstack/` | Provenance, `active-playbook.json` | rstack_run.py, verify_playbook.py | yes |

## Workspace level (outside projects)

| Path | Holds | Written by |
|---|---|---|
| `wiki/` | Reusable protocols: workflows, procedures, equipment. Its own git repo; `wiki/CLAUDE.md` is its router | wiki-mode only |
| `tools/` | Local tools. `tools/README.md` lists each tool, its entry command, and which playbook uses it | the user |

A report folder is per question. Several analyses, papers and talks may serve one question (`report:` in a piece's `target.md` names the folder). `results/README.md` links to result pages and never copies a number. `resources.md` (whether per-report `method/resources.md` or shared `docs/reports/resources.md`) is a general lab inventory and must NEVER contain report-specific beaker numbers or run labels.

## Front matter by folder

Every Markdown file starts with front matter. The fields depend on the folder. A body that came in (the user's words, an annotation snapshot) is never edited; its front matter may grow.

| Folder | Fields | Checked by |
|---|---|---|
| `docs/inputs/` | `created`, `kind`, `voice: user`, `source` (chat, interview, supervisor-message), `topic`, `report` (a folder in `docs/reports/`, or `none`), `confirmed` (`user`, or `supervisor` once he confirms it) | `check_references.py` |
| `docs/literature-review/papers/<cite>/` | `created`, `updated`, `kind`, `voice`, `paper` | `check_references.py` |
| `docs/understanding/` | `created`, `updated`, `voice`, `level` (basic, core, advanced), `status` (unchecked, source-checked) | convention, not yet checked |
| `docs/reports/<question>/README.md` | `created`, `updated`, `status`, `question` | convention, not yet checked |
