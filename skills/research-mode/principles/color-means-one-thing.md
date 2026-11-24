---
name: principle-color-means-one-thing
description: "Apply when choosing colours, markers or a colormap for a figure. A condition keeps one colour in every figure, and the figure still reads in greyscale and for colour-blind readers."
disable-model-invocation: true
---

# Color Means One Thing

A colour is a label. If a reader learns that blue is the low-resistance state in one figure, it must be that in every figure of the project.

- Give each condition, device, or state one colour and keep the list in the project's colour file. Take colours from the file or the preset palette, never from memory.
- Make the figure readable without colour: add a marker or a line style to each series, so greyscale prints and colour-blind readers can still tell them apart.
- Use at most about five colours. More series than that need small multiples, not more colours.
- For a continuous quantity use one perceptually uniform ramp (such as viridis). Use a diverging ramp only when the data has a meaningful zero. Never `jet`, `rainbow` or `hsv`.
- Say what each colour means in the legend or the caption.
