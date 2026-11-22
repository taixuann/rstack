### Experiment log

Phase: design and analysis (experiments run after the design freeze, so the log is written in the analysis phase too). Output: `docs/reports/<question>/method/log.md`, one section per session, appended as work happens. Reads `method/design.md`, `method/resources.md` and `method/samples.csv` of the question. Writes only `method/log.md`. Raw measurements never go here; they go in `data/raw/` through **Raw intake**.

The log records what was done, as run, against the frozen design. The report in the write phase cites this log and does not copy it; section 9 of `method/design.md` only points here. Do not edit the frozen design note; a deviation is a log entry.

1. **Open the entry.** `method/log.md` is made from `templates/report/method/log.md`. One section per session, headed with the date, the experiment id (E1, E2, as in `method/design.md`) and the operator.
2. **Per session.** Which samples (ids from `method/samples.csv`), and the steps as run. For each step the value, unit and instrument actually used. Anything not recorded stays `TODO: unknown`; never fill from the design.
3. **Deviations.** Every difference from the design in one line: what changed, why, and what it may affect. A deviation is never silent and never rewrites the design.
4. **Link the data.** Each session lists the `data/raw/` folder its measurements went to, once the intake has sealed it.
5. **Close.** When the experiment ends, state which design questions it answers and which stayed open. The user signs off; you do not.

Skills: `show-me-your-work` for the decision trail, `principle-raw-data-is-read-only`.

**Reply:** the entry changed, the deviations logged, and the unknowns still open.
