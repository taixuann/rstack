"""Two-layer checks for __FIGURE__. Exit 0 passes. Write them from docs/method.md before the first run.

Layer 1 (Synthetic & independent): prove the math/units work on a known synthetic input (never reuse the script's own helper as the oracle).
Layer 2 (Output & plausibility): verify real run outputs in RSTACK_OUTPUTS against physical bounds and method.md criteria.
"""
import os
import pathlib

# --- Layer 1: Synthetic known-answer & unit/formula check ---
# Example: feed synthetic data with an analytical answer and assert the core calculation recovers it within tolerance.
# Prove the check can fail at least once on a deliberate scratch break (wrong unit or factor).

# --- Layer 2: Real output & physical plausibility checks ---
out = pathlib.Path(os.environ["RSTACK_OUTPUTS"]) / "figures/__FIGURE__"
assert (out / "__FIGURE___data").is_dir(), "figure data missing"
# figrecipe writes the plotted points to __FIGURE___data/<id>_x.csv and _y.csv, with no header row.
raise SystemExit("TODO: add Layer 1 (synthetic known-answer) and Layer 2 (output/bounds) checks from docs/method.md, then delete this line")
