---
name: make-the-figure
description: Makes one figure for a lesson the user reads in Notion, only where words cannot carry the idea. Use for /make-the-figure, or when the user asks for a picture, diagram or figure of a mechanism, structure or process, or when explain finds a structure words cannot show. Not for plots of data; use figures for those.
---

# Make the figure

A figure earns its place only when words cannot carry the idea: a structure in space, a set of parts and arrows, a before and after. A figure that repeats the text, or a near copy of the one above it, costs the reader attention and adds nothing.

## Budget

- Default: one figure per lesson or note. A second only if the first cannot show the structure.
- Never one figure per step of a mechanism. If steps differ only by a value or a label, show them in one figure with the changing quantity marked, or in a small table.
- The user asking for a figure overrides the budget for that request.

## Choose the form

1. **Mermaid** in a `mermaid` code block when it is boxes, arrows, a sequence, a timeline, states. Notion draws it. Keep labels short. Preview it with `scripts/render_diagram.mjs` under the research-mode skill before writing it into the page.
2. **Hand-drawn SVG** when Mermaid cannot draw it. Uploading an image to a Notion page is untested, so say so and ask the user before trying; until then describe the part in words or a table (a cell with ions, a circuit, a labelled part). Draw the thing itself with labelled parts, arrows for what moves, and a readout of the quantity that changes. Render to PNG (`rsvg-convert -w 1000 x.svg -o x.png`) and look at it before the user does.
3. **A plot of data** is not this skill. Use `figures` (with `scientific-visualization`).

## Rules

- Say in one line what the figure shows and what it leaves out.
- Label every part; a term in the figure was defined in the text.
- Do not put numbers in a figure that the note does not source or label as general knowledge.
- Check that the Mermaid parses, by rendering it, before the page is written.

**Reply:** the figure's path and the one thing it shows.
