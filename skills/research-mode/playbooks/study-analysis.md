# Study analysis

Output: scripts, figures, tables in `analysis/`; results summary in `analysis/results.md`.

1. Find the design note and its analysis plan. If none exists, write the plan first and mark later departures as deviations.
2. `exploratory-data-analysis` to inspect shape, missingness, units, distributions. Never edit raw data in place.
3. `statistical-analysis` for test selection, assumption checks, effect sizes with confidence intervals, multiplicity. `uncertainty-and-units` for propagated error.
4. One sensitivity check: vary one analysis choice and see whether the conclusion holds.
5. Figures: `figure-style` for correctness rules, `figure-composer` for multi-panel figures, `scientific-visualization` to audit truthfulness and accessibility. Save every figure and table as artifacts.
6. `scientific-critical-thinking` on the conclusion; `interrogate` for an adversarial check. Write what the data support and do not support; label post-hoc findings.
7. For many datasets or conditions, run one script over all of them (`swarm` if slices are independent). For heavy compute use the remote-compute skills. Log long runs with `show-me-your-work`.
