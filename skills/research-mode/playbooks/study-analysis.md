# Study analysis

State: progressing. Output: scripts, figures, tables in `analysis/`; results summary in `docs/rstack/progressing/results.md`.

1. Find the design note and its analysis plan. If none exists, write the plan first and mark later departures as deviations.
2. Inspect shape, missingness, units, and distributions before modelling (`exploratory-data-analysis` if installed). Never edit raw data in place.
3. Report n, the spread (SD or confidence interval), and effect sizes, not only p-values. Overlay individual measurements on means and error bars (`figures`). Propagate measurement error and units explicitly (`uncertainty-and-units` if installed). Correct for multiple comparisons when you test many.
4. One sensitivity check: vary one analysis choice and see whether the conclusion holds.
5. Figures: `figures` for correctness rules, `scientific-visualization` to audit truthfulness and accessibility. Save every figure and table as artifacts.
6. `interrogate` for an adversarial check of the conclusion. Write what the data support and do not support; label post-hoc findings.
7. For many datasets or conditions, run one script over all of them (`swarm` if slices are independent). Run heavy jobs detached and log them. Log long runs with `show-me-your-work`.
8. Write the analysis report with `analysis-report`.
