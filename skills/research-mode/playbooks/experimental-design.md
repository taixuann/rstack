### Experimental design

Phase: design. Output: in `docs/reports/<question>/` (opened by **Report init**), tailored to the report's Objective and type. Maintains shared `docs/reports/resources.md` (general lab inventory — never report-specific beaker numbers/run labels) and `docs/reports/samples.yaml` (`devices` + `library_studies`), plus either:
- **Experimental / sample branch:** `docs/reports/<question>/samples.yaml` (report-specific `r.[...]` `remarks` only — no `planned_runs` or invented IDs) + `docs/reports/<question>/procedure/<slug>.md` (self-contained single-file SOP from `templates/report/method/procedure.md`, one `## E<n>` block per stage), or
- **Hardware / software setup branch:** `docs/reports/<question>/method/design.md` (architecture, wiring/config, bench verification from `templates/report/method/design.md`).
And `docs/reports/<question>/log.md` for as-run records.

Reads `docs/reports/<question>/README.md` (the specific Objective and active sections) and the Inquiry note (never links the wiki directly). Nothing is made or measured here.

Skills for this playbook: `brainstorming`, `interrogate`, Inquiry (`qmd`), `hypotheses`, `experimental-design`, `statistical-power` (subject comparisons only), `uncertainty-and-units`, `what-if-oracle` (failure modes and fallbacks), `arena` (competing designs), `wiki-mode` (if filling wiki gaps). Specific principles: `principle-question-first`, `principle-exploratory-vs-confirmatory`, `principle-attack-the-premise`, `principle-model-the-domain`.

**The loop, per report / experiment**

1. **Brainstorm and interrogate first.** Read the report's `README.md` (especially its specific **Objective** and which `method/` parts were selected in **Report init**). Run `brainstorming` and `interrogate` (interview mode) to sketch candidate approaches, surface missing parameters, and challenge weak assumptions before looking anything up.
2. **Inquiry loop (`qmd`).** Run **Inquiry** (`qmd` on `-c <project>`, and `-c wiki` when the work involves method, procedure, hardware, or software). Save lab/wiki findings to `docs/inputs/<date>_inquiry_<experiment>-wiki.md` (labelled `[user]` or `[studies]`). Loop back to `brainstorming` and `interrogate` as new details arrive until the design is solid.
   - **Copy, do not link.** Copy every needed value, unit, tolerance, setting, and source mark directly into `procedure/<slug>.md` or `method/design.md` so the single file stands alone with no wiki links or cross-file dependencies for bench execution.
3. **Resources (`docs/reports/resources.md`) & Samples (`samples.yaml`).** From `templates/report/method/resources.md`, maintain the general lab inventory (3-tier Equipment & Software, Materials/Tools/Consumables, Raw Chemicals, Standing Stock Solutions & Standard Reagents — never report-specific beaker numbers or run labels). Keep shared `devices` & `library_studies` in `docs/reports/samples.yaml`, and report-specific `remarks` (`r.[...]`) only in `docs/reports/<question>/samples.yaml`. Anything short becomes a task.
4. **Build the branch output.**
   - **Branch A — Experimental / sample procedure (`procedure/<slug>.md` + `samples.yaml`):** Use `templates/report/method/procedure.md` (one single self-contained file with one `## E<n>` block per stage: objective and scope, safety/pre-checks/calibration, Materials/Solutions/Instrument Setup, Phase-structured step-by-step execution with tolerances, pass/failure criteria, what to record in `log.md`, and data/analysis handoff). Define `r.[...]` remark patterns in `docs/reports/<question>/samples.yaml` (no `planned_runs` or invented IDs).
   - **Branch B — Hardware / software setup (`method/design.md`):** Detail the architecture, wiring/pinout or software flow, instrument/interface settings, calibration, and bench acceptance checks.
5. **Interrogate the final design.** Run `interrogate` against the Exit gate angles in `references/phases/design.md` and `what-if-oracle` for major failure modes and fallbacks (skipped angles for setup-only reports stay marked `N/A`). Plan the smallest end-to-end pilot first when applicable.
6. **Freeze, record, and offer `analysis/` prep.** Freeze `method/procedure.md` / `method/design.md` and `method/samples.csv` (never edit frozen sections afterwards; deviations go to `method/log.md`). Run **Project admin** (Tasks + Keeping records) to log the decision in `docs/rstack/decisions.tsv`, update `docs/reports/<question>/README.md`, and create execution tasks in `docs/rstack/tasks.md`. Then ask the user whether to open a skeleton `analysis/<name>/` folder now (basic objective and expected inputs, even before `data/raw/` exists) and run **Analysis plan** to prepare the analysis frame ahead of measurements.

**Reply:** the method files written (`resources.md`, `procedure.md`/`design.md`, `samples.csv`), open `TODO: unknown` items, tasks/decisions logged, and whether to pre-create `analysis/<name>/` via **Analysis plan**.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start experimental-design`). Items: file (a glob with a match), decision (a new `decisions.tsv` row). Also verify `method/procedure.md` (and `method/samples.csv`) or `method/design.md` exists according to the chosen branch.

- file docs/reports/*/method/resources.md
- decision
