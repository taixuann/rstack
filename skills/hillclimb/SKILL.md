---
name: hillclimb
description: "Sustained, iterative improvement of one measurable metric (model accuracy, detection sensitivity, fit residual) against a target, changing one thing per measurement with a frozen evaluation harness and decision log. Use when tuning a model, filter, or algorithm in analysis."
---

# Hillclimb

**You own the metric and the experiment's integrity.** Sustained, iterative improvement of one measurable thing (model accuracy, detection sensitivity, a fit residual) against a target. A one-off fix belongs in **Analysis run** / **Analysis review**.

1. Fix one metric, the direction that counts as better, and a checkable stop predicate with a floor on iterations. Capture the baseline before any change.
2. Freeze the evaluation harness (fixed split, seeds, metric code) and prove it can tell good from bad on a known case. Keep the test set untouched until the end.
3. Open a decision log via `show-me-your-work`: id, hypothesis, change, before, after, delta, verdict, note.
4. Loop one hypothesis per iteration. Make the smallest change, measure on the validation split, keep it only if it moves past noise and the gates hold. Log the row either way. Run long sweeps in the background and log each run.
5. On a plateau, pivot category or re-read the data before concluding. Prefer simplicity: keep a simplification that holds the number.
6. Evaluate once on the held-out set. Report that number, not the best validation number.

**Reply:** metric and target, baseline to final, iterations (kept vs reverted), the decision log path, and the held-out result.
