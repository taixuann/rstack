---
name: make-the-figure
description: Makes one figure for a note the user reads in Obsidian, only where words cannot carry the idea. Use for /make-the-figure, or when the user asks for a picture, diagram or figure of a mechanism, structure or process, or when explain finds a structure words cannot show. Not for plots of data; use figures for those.
---

# Make the figure

A figure earns its place only when words cannot carry the idea: a structure in space, a set of parts and arrows, a before and after. A figure that repeats the text, or a near copy of the one above it, costs the reader attention and adds nothing.

## Budget

- Default: one figure per lesson or note. A second only if the first cannot show the structure.
- Never one figure per step of a mechanism. If steps differ only by a value or a label, show them in one figure with the changing quantity marked, or in a small table.
- The user asking for a figure overrides the budget for that request.

## Choose the form

1. **Mermaid** in a `mermaid` code block when it is boxes, arrows, a sequence, a timeline, states. Obsidian draws it in the user's theme. Keep labels short. Preview with `scripts/render_diagram.mjs` under the research-mode skill, as the Obsidian writing playbook describes.
2. **Hand-drawn SVG** in the `figures/` folder of that area, embedded as `![[figures/<name>.svg]]`, when Mermaid cannot draw it (a cell with ions, a circuit, a labelled part). Draw the thing itself with labelled parts, arrows for what moves, and a readout of the quantity that changes. Render to PNG (`rsvg-convert -w 1000 x.svg -o x.png`) and look at it before the user does.
3. **A plot of data** is not this skill. Use `figures` (with `scientific-visualization`).

## Rules

- Say in one line what the figure shows and what it leaves out.
- Label every part; a term in the figure was defined in the text.
- Do not put numbers in a figure that the note does not source or label as general knowledge.
- Check with `scripts/check_references.py` (embeds resolve, Mermaid parses).

**Reply:** the figure's path and the one thing it shows.
