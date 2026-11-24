# Phase: analysis

**Entry check.** Design exit passed: the design note and plan are frozen. Formerly named `progressing`.

**Playbooks, in order.**
1. Raw intake (data into `data/raw/` with provenance)
2. Analysis plan (`analysis/<name>/`, nothing runs)
3. Analysis run (one figure or table, with provenance)
   Experiment log runs alongside while the experiments are carried out (what was done, as run, in `method/log.md`).
4. Analysis review (called, not a stage every run passes)
5. Analysis reconcile (consolidate Check/Main/Verify into `analysis/<name>/docs/results.md` and push to `docs/reports/<question>/results/README.md`)
6. Package results (last: a folder someone else can run)

**Reads and writes.** Reads `docs/reports/<question>/` (`README.md`, `method/procedure.md` or `method/design.md`), `data/raw/`. Writes `data/raw/` (raw-intake only), `analysis/<name>/`, `analysis/<name>/docs/results/`, `.rstack/`, `docs/reports/<question>/results/README.md`, `docs/rstack/tasks.md` (through project-admin). Rows are in `layout.md`; a playbook states its own subset.

**Starting tasks.** Intake data with provenance. Run the planned analyses per question. Run sensitivity checks. Accept or reject each result. Rerun the pipeline clean. Package the results. Tailor them to the project.

**Exit gate angles.** Each is one adversary for `interrogate` (see `admin/exit-review.md`).

1. **Provenance.** Every number traces to a script and an input (path, hash). Rerun from a clean state matches.
2. **Quality control.** QC ran before analysis, and excluded data is listed with the reason.
3. **Explain the number.** Each reported value has n, spread, a limiter, and a check that it measured what was meant.
4. **Sensitivity.** At least one analysis choice was varied and the conclusion held or the change is reported.
5. **Honest labels.** Deviations from the plan are logged. Post-hoc findings are labelled. Negative results are kept.
6. **Raw untouched.** `data/raw/` is unchanged and hashes match.
7. **Challenge review.** Every result marked `cited: true` has a usable `review.md` on its current run (no open blocking finding, or a waiver the user wrote), its claim is written for that run, and `docs/review.md` covers the accepted runs. `rstack_run.py check` enforces this (**Analysis review**).

**Done when.** Planned analyses done, every result dispositioned, rerun clean, package built.

**Skills.** Bundled (in rstack): `statistical-analysis`, `uncertainty-and-units`, `analysis-report`, `figures`, `reproduce`, `hillclimb`, `swarm`, `acceptance-checks`. External (install separately; use only if installed, and `setup-research` lists what is missing): `neurokit2` (ECG and biosignals).
