---
name: scientific-slides
description: "Structure and design rules for a research talk: how to order the slides for a group meeting, conference talk, seminar or defence, how many slides fit the time, how to show data on a slide, and Beamer templates. Use with the Presentation playbook. It does not write the slide text and does not generate slide images."
license: MIT
metadata:
  adapted-from: "K-Dense-AI/claude-scientific-writer, skill scientific-slides (MIT, (c) K-Dense Inc.)"
  changes: "AI image generation, PowerPoint tooling and the defence template removed; SKILL.md rewritten for rstack"
---

# Scientific slides

Reference material for the **Presentation** playbook. The playbook owns the steps; this skill answers the design questions that come up in them. Every title and line of text on a slide is the user's.

## Which file answers what

| Question | Read |
|---|---|
| What order do the slides go in, for this kind of talk? | `references/talk_types_guide.md`, `references/presentation_structure.md` |
| How many slides fit the minutes, and how long per part? | `assets/timing_guidelines.md` |
| How should a figure from the paper change for a slide? | `references/data_visualization_slides.md` |
| Layout, type size, colour, how much on one slide | `references/slide_design_principles.md` |
| What goes wrong most often | `references/common_pitfalls.md` |
| Beamer | `references/beamer_guide.md`, `assets/beamer_template_conference.tex`, `assets/beamer_template_seminar.tex` |

## Rules that hold in rstack

1. One message per slide, and the slide's title is that message as a full statement. The user gives it.
2. One main figure per slide. It comes from `figures.yaml`; a figure made for a paper usually needs larger labels and fewer panels on a slide, and that is a new export from the analysis, not an edit of the image.
3. Every number on a slide is in the report and passes `number-check`.
4. A slide that needs a sentence of explanation to be read is two slides, or the explanation belongs in the talk notes.
5. A limit that belongs to a claim is said on the slide that makes the claim.
6. The templates carry sample text. Strip it; never leave or adapt it as content.

The timing and layout numbers in the references are rules of thumb from their authors, not requirements. The event's own instructions win.
