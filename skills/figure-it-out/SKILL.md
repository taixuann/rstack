---
name: figure-it-out
description: "Design an auditable playbook when no narrower one fits: a large multi-part study, a big data migration, an ambitious analysis, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'."
---

# Figure it out

When the task matches no existing playbook, design one. The deliverable before any execution is the workflow itself: phases that scale rigor to the task, apply the scientific method, and leave a decision trail a human can audit later.

## Start
Todo list: first item is to read the Principles section of the `research-mode` skill, then the phases below.

## Phase A: Frame
Ground first, then commit. Do not start until you can state:
- Definition of done as a falsifiable predicate, checkable on the real artifact.
- Scope, quantified: rough units and effort, plus blockers found while grounding.
- Rigor level, biased high. One-way doors and high blast radius get more; reversible low-stakes steps get less. Rigor means gates and artifacts, not trying harder.
Present framing and tradeoffs before a long run. Reversible work proceeds; a multi-hour run earns one checkpoint with the user.

## Phase B: Design the workflow
Decompose into atomic, independently checkable units, riskiest unknown first. Build the verification harness before the work, with a baseline captured from the pre-change state, so each check reads old value vs new value. For one-way-door decisions use `arena`. Parallelise only across seams (`swarm`), each worker with its own output location. Write the phase list down; the human reviews that list.

## Phase C: Run the loop
Each unit is an experiment: state the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert if not. Verify each unit before starting the next. Inspect artifacts, never trust a self-report; when something passes too easily, suspect the measurement first. Verdicts are VERIFIED, NOT VERIFIED, or INCONCLUSIVE; inconclusive is not a pass, and negatives stay visible.

## Phase D: Audit trail
Log through `show-me-your-work`, a row as each step lands.

## Phase E: Verify and hand back
Check the whole against the Phase A predicate on the real product, not only the harness. Turn any recurring correction into a check or script.

**Reply:** the playbook you designed, the rigor level and why, the trail path, what is verified against the predicate, and what is still open.

---
Adapted from the pstack plugin (cursor/plugins, MIT License, (c) 2026 Lauren Tan), generalised for any domain and agent harness.
