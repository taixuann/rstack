### Experiment log

Phase: design and analysis (experiments and setup runs happen after design freeze, so logging spans both). Output: `docs/reports/<question>/method/log.md`, one dated section per session, appended as work happens. Reads `method/procedure.md` or `method/design.md`, `method/resources.md`, and `method/samples.csv` (when present). Writes only `method/log.md` unless the user approves updating the report `README.md` or running `Raw intake`. Raw measurements never go here; they go in `data/raw/` through **Raw intake**.

The log records what was done, as run, against the frozen design or procedure. Never edit the frozen design/procedure; every deviation is a log entry.

1. **Clarify and route (`Inquiry` + `interrogate` + `brainstorming`).** When the user reports what they did on a date, run **Inquiry** (`qmd -c <project>`), `interrogate` (interview mode), and `brainstorming` (when troubleshooting) to identify which report(s) (`docs/reports/<question>/`) the session belongs to, which units from `method/samples.csv` were used, and which steps of `method/procedure.md` or `method/design.md` were run. If one session covered multiple reports, split entries into each report's own `method/log.md`.
2. **Record the session (`method/log.md`).** Create `method/log.md` from `templates/report/method/log.md` if missing. Add one dated section with operator, experiment/run ID, samples used, and actual values, units, and instruments. Anything not recorded stays `TODO: unknown`; never copy numbers from the design as if they were measured.
3. **Log deviations.** Record every difference from the frozen `procedure.md` or `design.md` in one line: what changed, why, and what it may affect.
4. **Check data files for that date.** If raw data files exist for that session/date, ask the user for explicit approval to link them in `method/log.md` and `docs/reports/<question>/README.md`, and ask whether to run **Raw intake** now to check and standardize filenames/date folders.
5. **Record and close.** Run **Project admin** (Keeping records) when a deviation, new finding, or completed run updates `docs/rstack/decisions.tsv` or `docs/rstack/tasks.md`. When an experiment ends, state which questions it answers and which remain open; the user signs off.

Skills: `interrogate`, `brainstorming`, `show-me-your-work`. Specific principles: `principle-raw-data-is-read-only`, `principle-sources-not-memory`.

**Reply:** the report log(s) updated, deviations recorded, data files waiting for approval or **Raw intake**, and unknowns still open.
