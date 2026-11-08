# Research lifecycle statechart

How a project moves through rstack's five states. TLC checked the model: 12 states, 26 steps, all rules hold.

![Research lifecycle](chart.svg)

**Rules the model checks**
- No analysis starts before the design is frozen (the design review sets `frozen`).
- No write-up starts before every result has a disposition (the progressing review sets `accepted`).
- A project is only published with its results accepted.
- A closed project has a reason (published or abandoned), and only a closed one does.

**What the chart leaves out.** Four steps that stay inside one chart state (for example a second review in a state whose review has already passed). Moving back clears what the later state froze or accepted, and you re-clear that gate on the way forward.

**Analysis workflow.** `ANALYSIS.md` charts the run gate and tick (check before main before verify). It was drawn before the review, accept-a-run and package steps were added, so it does not show them yet.

**Make it again**

```bash
rstack/skills/statechart/scripts/statechart \
  ResearchStates.tla --config ResearchStates.cfg --view view.mjs --out out
```

The first run installs Java and TLC through `mise`. Render the SVG with `pele@1.9.0` as in the statechart skill's `references/render.md`.

```mermaid
---
title: "A research project, from first idea to closed"
---
stateDiagram-v2
  state "Legend" as legend {
    lg0: working
    lg1: ready
    lg2: end
  }
  class lg0 blue
  class lg1 teal
  class lg2 tan
  state "Explore" as s0 {
    s1: Review pending
    s2: Review passed
  }
  state "Closed" as s3 {
    s4: Abandoned
    s5: Published
  }
  state "Design" as s6 {
    s7: Review pending
    s8: Review passed
  }
  state "Progressing" as s9 {
    s10: Review pending
    s11: Review passed
  }
  state "Ready for publish" as s12 {
    s13: Review pending
    s14: Review passed
  }
  [*] --> s1
  s1 --> s2: the state review passes
  s2 --> s7: you move to the next state
  s7 --> s8: the state review passes
  s8 --> s10: you move to the next state
  s10 --> s11: the state review passes
  s11 --> s13: you move to the next state
  s13 --> s14: the state review passes
  s14 --> s5: the paper is submitted
  s0 --> s4: you abandon the project
  s6 --> s1: you go back, and log why
  s6 --> s4: you abandon the project
  s9 --> s7: you go back, and log why
  s9 --> s4: you abandon the project
  s12 --> s10: you go back, and log why
  s12 --> s4: you abandon the project
  class s1 blue
  class s2 teal
  class s4 tan
  class s5 tan
  class s7 blue
  class s8 teal
  class s10 blue
  class s11 teal
  class s13 blue
  class s14 teal
```
