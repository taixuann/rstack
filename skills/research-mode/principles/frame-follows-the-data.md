---
name: principle-frame-follows-the-data
description: "Apply when setting up a figure: choose a closed box or an open L-frame from the data, take line widths, marker sizes and fonts from the preset, and keep to 3 to 5 major ticks. Override the preset only for a stated reason."
disable-model-invocation: true
---

# Frame Follows the Data

The data decides the frame, not habit. Choose it per figure and write the reason in the analysis's `docs/method.md`.

- **Closed box** (`*-single` presets): data that crosses zero, loops and hysteresis (I–V, CV, M–H), spectra, matrices and heatmaps, and twin axes, where the right spine is a real axis.
- **Open L-frame** (`*-open` presets): distributions, boxplots and violins, kinetics and decay, dose-response, anything with a natural floor and no ceiling. A top line would imply a ceiling that does not exist.
- **Sizes come from the preset**: line width, marker size, error-bar width, font sizes, tick length. Override one only for a stated reason; the runner records every override for the reviewer.
- **Axes**: no title, no gridlines, ticks pointing out, 3 to 5 major ticks on linear axes (a log axis ticks by decade, a categorical axis shows each category), decimal labels, and "Quantity (unit)" on every axis with the unit rescaled to read µA, mV, kΩ.
- **Build at the printed size** in millimetres; never rescale in the document.
