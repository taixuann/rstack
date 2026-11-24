### Analysis reconcile

Phase: analysis (after **Analysis review**, before **Package results** or **Paper preparation**). Reconciles all accepted runs inside `analysis/<name>/` into one consolidated `analysis/<name>/docs/results.md` (covering **Check**, **Main**, and **Verify** numbers and cross-checks) and promotes them to the parent question's report (`docs/reports/<question>/results/README.md` and `docs/reports/<question>/README.md`).

Skills: `analysis-report`, `scientific-critical-thinking`, `interrogate`, `show-me-your-work`. Specific principles: `principle-explain-the-number`, `principle-sources-not-memory`, `principle-exploratory-vs-confirmatory`, `principle-prove-it-works`.

1. **Check consistency across runs.** Read `analysis/<name>/README.md`, `docs/method.md` (Deviations, Exclusions), `docs/review.md`, and every `docs/results/<figure>.md`. Verify `claim_for` matches the accepted `run_id` and no `Check`/`Main`/`Verify` findings contradict each other.
2. **Finalize per-figure result pages (`analysis/<name>/docs/results/<figure>.md`).** Ensure each accepted figure's claim states exact numbers, units, `n`, spread, and limits (no `TODO`), and set `cited: true` for results that will feed a manuscript or report.
3. **Write `analysis/<name>/docs/results.md`.** Consolidate the whole analysis into one file with:
   - Cross-check summary against `docs/method.md` (exclusions, deviations, hypothesis verdicts).
   - **Check**, **Main**, and **Verify** sections reporting every accepted number, unit, `n`, spread, and `run_id` (linking each figure's `docs/results/<figure>.md`).
4. **Update the parent report (`docs/reports/<question>/`).**
   - Create or update `docs/reports/<question>/results/README.md` with one row per accepted result: claim summary, key number + unit, and relative links to `analysis/<name>/docs/results.md` and `analysis/<name>/docs/results/<figure>.md`.
   - Update the Hypotheses table (`supported` / `rejected`) and status in `docs/reports/<question>/README.md`.
5. **Verify gate.** Run `python3 {scripts}/rstack_run.py check analysis/<name>` to confirm no cited result has a stale claim or missing review.
6. **Record.** Run **Project admin** (Keeping records) to log the reconciliation in `docs/rstack/decisions.tsv`, update the Aspect Checklist and report `state:` in `docs/rstack/README.md`, and update `docs/rstack/tasks.md` if ready for **Package results** or `write`.

**Reply:** `analysis/<name>/docs/results.md` summary (Check/Main/Verify), `docs/reports/<question>/results/README.md` updated, hypothesis statuses changed, and `rstack_run.py check` output.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start analysis-reconcile analysis=analysis/<name>`). Items: file (a glob with a match), cmd (exit 0), decision (a new `decisions.tsv` row).

- file {analysis}/docs/results.md
- cmd python3 {scripts}/rstack_run.py check {analysis}
- decision
