---
name: figures
description: Makes publication-quality plots from measured data with figrecipe (millimetre layout, journal presets, a recipe saved with every figure), obeying the lab rules: no title, 3 to 5 ticks, decimal labels, SI-prefixed units. Use whenever results are plotted, charted or visualized for a paper, report or answer, or an existing plot looks unpolished. Not for conceptual diagrams or schematics (use schematics) and never for drawing numbers that did not come from a run.
summary: "Publication plots from real data: sized for the page, vector, uncertainty shown."
category: core
role: workflow
allowed-tools: [Read, Write, Edit, Bash, python, experiments]
license: MIT
version: 1.0.0
author: Synthetic Sciences
metadata:
  skill-author: Synthetic Sciences
  adapted-from: alphaXiv OpenResearch orx-figures (MIT)
---

# Figures

A figure is an argument, not a screenshot of an array. It makes one claim, and a reader who skips the prose should still get it right.

## Rules (checked by `scripts/figrules.py` in the research-mode skill)

1. **No title.** The caption carries the claim. Panel letters name parts of a multi-panel figure.
2. **3 to 5 major ticks per axis.**
3. **Decimal tick labels.** Never `1e-6` style. Rescale the data and the unit together with `figrules.si_scale` so the unit reads µA, nA, mV, kΩ.
4. **Every axis has a quantity and a unit.**
5. **Every number comes from a run** (inputs listed in the run's `inputs.yaml`). Never plot a remembered or plausible number.
6. **Show individual measurements** over means and error bars; state n and what the spread is. One sample is an anecdote.
7. **Colour-blind and greyscale safe.** Use the project's colour file for conditions if it has one. Never `jet`, `rainbow` or `hsv`.
8. **Build at the printed size.** Use the preset's millimetre width; never rescale in the document.

## How

Figures are made inside an analysis run (**Analysis run** playbook), never by hand outside it. The project's `analysis/lib/` (copied from rstack by `rstack_run.py lib <project>`) holds `style.py`, `load.py` and `figrules.py`. A figure script is short:

```python
from load import load
from style import new_figure, save_figure, si_scale

df, tokens = load("dev1")                       # an id from inputs.yaml; raw files go through raw-viewer
fig, ax = new_figure("nature-single", axes_width_mm=60, axes_height_mm=50)   # closed box; "nature-open" for an L-frame; copies the preset into the run
y, unit = si_scale(df["I"].to_numpy(), "A")     # rescale data and unit together: µA, nA, mV, kΩ
ax.plot(df["V"], y, id="iv"); ax.set_xlabel("Voltage (V)"); ax.set_ylabel(f"Current ({unit})")
save_figure(fig, "iv")                          # sets about 4 ticks, checks the rules, saves with figrecipe
```

`save_figure` raises `ValueError` naming every rule that is broken (a title, a wrong tick count, scientific notation). Pick the frame, colours and caption by `principle-frame-follows-the-data`, `principle-color-means-one-thing` and `principle-caption-states-the-conclusion`. A line width or marker size that differs from the preset is allowed and is recorded in the run. It writes `figures/iv/iv.png`, `iv.pdf`, `iv.yaml` (the recipe) and `iv_data/*.csv` (the plotted points, no header). Restyle a saved figure without recomputing: `fr.reproduce(...)`.

Run figrecipe with `tools/figrecipe/.venv/bin/python`. The venv's console scripts (`figrecipe ...`) have a stale shebang and fail; use `python -m figrecipe`. Give `ax.plot(..., id="name")` an id so the data file has a stable name. Pass `constrained_layout=False` to `fr.subplots` when sizing in mm (`new_figure` does).

## Before you hand it over

- `check(fig)` passes; open the pdf at printed size and read it.
- The figure folder holds a `run.txt` from the runner; `rstack_run.py check` passes.
- The caption states the finding, n, and what any band or bar means.
