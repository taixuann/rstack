# Project layout

Every folder a project may have, who writes it, and whether it is read-only. A playbook opens by naming the rows it reads and writes. `scripts/check_layout.py <project>` flags any folder not listed here (for example a stray `manuscripts/`). To add a folder, add its row here first.

| Path | Holds | Written by | Read-only? |
|---|---|---|---|
| `README.md`, `AGENTS.md`, `CLAUDE.md` | Front page and state, operating contract, import stub | project-admin | no |
| `data/raw/` | Measurements as received, one dated folder per intake | raw-intake | yes, after the intake log seals it |
| `docs/inputs/` | The user's own words, dated: `<date>_<kind>_<slug>.md` | the user, or inquiry on their behalf | yes |
| `docs/literature-review/papers/<cite>/` | README, annotations, alignment for one paper | literature-review, inquiry | `annotations.md` yes |
| `docs/literature-review/cross-papers/` | Comparisons, themes, gap map | literature-review | no |
| `docs/literature-review/<date>_<slug>.md` | Symlinks to HyperResearch final reports (leads, not read papers). The vault holds the real file; the only link folder | literature-review | yes |
| `docs/literature-review/reports/` | Older deep-research outputs, kept as they are | none | yes |
| `docs/literature-review/references.yaml` | Which Zotero papers matter and why | literature-review | no |
| `docs/rstack/tasks.md`, `todoist-map.tsv` | The task list and its Todoist map | project-admin only | no |
| `docs/rstack/requests.tsv` | Handoffs between role bots: date, from, to, kind, text, status (see `docs/bots/README.md`) | any bot appends; the recipient sets `status` | append only |
| `docs/rstack/decisions.tsv` | Decision trail of long or unattended work | show-me-your-work | append only |
| `docs/rstack/<phase>/` | Documents of one phase: the proposal documents, review.md, results.md. Never brainstorm or inquiry files | the phase's playbooks | no |
| `docs/rstack/brainstorm/` | One note per brainstorm, `<slug>.md`, from the `brainstorming` skill | brainstorming, any playbook that brainstorms | no |
| `docs/rstack/inquiry/` | The Inquiry playbook's files: `inquiry.md`, `inquiry-search.md`, `inquiry-<topic>-wiki.md`, `claims.md` | inquiry, literature-review (reads) | no |
| `docs/rstack/writing/<piece>/` | One piece's control files: `target.md`, `todo.md`, `decisions.tsv`, `findings.tsv`, `scaffold/`, `review/` | paper-preparation, paper-writing, paper-critique (through `writing.py`) | the gates only through the script |
| `docs/reports/<question>/` | One folder per question, three folders and the evidence files: `fundamental/`, `method/`, `results/`. `README.md` is the index (intention, hypotheses, plan, status, links). `fundamental/` holds the background: the user's understanding, then checked facts. `method/` holds the how-to building blocks (instrument setup, sample fabrication, measurement procedure) that **Experimental design** turns into procedures, and `method/design.md`, `method/resources.md`, `method/samples.csv`; `method/log.md`; optional `results/README.md` (an index of results that answer the question); the paper evidence files `claims.yaml`, `methods.yaml`, `figures.yaml`, `citations.yaml`, `limitations.md`. Every number links to its source file | `README.md` and `fundamental/`: report-bootstrap; design files: experimental-design; `method/log.md`: experiment-log; `results.md`: analysis-review, only when needed; evidence files: paper-preparation | `method/design.md` after the design gate; the evidence files after `report-approved`; the rest stays open |
| `docs/writing/<piece>/` | `main.tex`, `references.bib`, `figures/`, `sections/` | the user; the assistant never writes prose | no |
| `docs/presentation/<piece>/` | Slides | the user | no |
| `analysis/<name>/docs/results/<figure>.md` | One page per accepted figure, beside the run that made it | analysis-run (`rstack_run.py tick`) | no |
| `analysis/<name>/` | Scripts, figures, tables, `package/`, `export/` | analysis-plan, analysis-run, package-results | outputs of an accepted run: yes |
| `.rstack/` | Provenance, `active-playbook.json` | rstack_run.py, verify_playbook.py | yes |

## Workspace level (outside projects)

| Path | Holds | Written by |
|---|---|---|
| `wiki/` | Reusable protocols: workflows, procedures, equipment. Its own git repo; `wiki/CLAUDE.md` is its router | protocol-wiki only |
| `tools/` | Local tools. `tools/README.md` lists each tool, its entry command, and which playbook uses it | the user |

A report folder is per question. Several analyses, papers and talks may serve one question (`report:` in a piece's `target.md` names the folder). `results/README.md` links to result pages and never copies a number.
