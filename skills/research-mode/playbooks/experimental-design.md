# Experimental design

State: design. Output: design note at `docs/rstack/design/<yyyy-mm-dd>_<name>.md`, and the frozen analysis plan beside it.

Load these skills only as needed:
- `hypotheses` to turn the question into falsifiable hypotheses with predictions and the result that would refute each. `brainstorming` to choose between directions.
- `experimental-design` for the design itself: groups, randomisation, blinding, controls, confounders.
- Plan replicates and repeatability instead of a power calculation when the work is device or materials measurement: how many devices or samples per condition, how many repeat measurements, what spread is acceptable, and how measurement uncertainty is reported (`uncertainty-and-units` if installed). Use a formal power calculation only for subject-based comparisons.
- State before data is examined which comparisons you will make and how results are shown (for example means with error bars and the individual points overlaid).
- `interrogate` to attack the finished design; `arena` when two or more designs are plausible.

The note contains: one primary question and a falsifiable hypothesis, with what would refute it; variables and primary endpoint; the design with a short tradeoffs table against the best alternative; sample size with effect-size source, alpha, power, dropout; protocol and the data to record (and where it lives in `data/raw/`); the pre-stated analysis plan that Analysis plan will consume; risks and fallbacks.

At the end, set the README hypotheses to `frozen` and offer the design → progressing state change (**Project docs**).

Discussion mode: argue the strongest alternative design before settling; push back on weak controls or underpowered plans.
