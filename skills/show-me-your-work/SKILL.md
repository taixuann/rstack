---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: an append-only TSV log with one row per decision (what, why, evidence, result). Use for /show-me-your-work, autonomous or multi-phase runs, or any work a human reviews after stepping away."
---

# Show me your work

One canonical log: a TSV, one row per decision, single-line cells, evidence as a pointer, not prose.

Columns: `ts` (ISO8601), `phase`, `decision` (what was chosen or done), `why` (plain words), `evidence` (path, commit, artifact id, `file:line`; never a paragraph), `result` (outcome or predicate state: `tests green`, `reverted`, `INCONCLUSIVE`, `open`).

Start a log with `scripts/log.py <logfile> <phase> <decision> <why> <evidence> <result>`. It stamps `ts`, writes the header on first use, strips tabs and newlines, and prefixes cells starting with `=`, `+`, `-`, `@` with a quote (spreadsheet-injection guard).

## Logging
Write each row as you would tell a teammate what you did: concrete actions, plain words. Log decision points and checkpoints, not every action: a fork chosen, a unit finished with its verification result, a pivot or revert with its trigger, a blocker, a fixed gate. For loops, one row per iteration.

A run is one agent conversation. When a run adds to a log that already has rows, its first row has phase `start`, naming the `ts` range of rows it did not write; use `start` for nothing else.

## Where it lives
Default `decisions.tsv` in the work folder (for research projects `docs/rstack/decisions.tsv`), or `.audit/<task-slug>.tsv` when several efforts run at once. Commit it when a reviewer needs the trail to trust the result.

## Rules
- Append-only. A wrong call gets a new row that supersedes it; never edit or delete history.
- Prefer evidence produced by saved scripts over one-off manual steps.

## Audit before handing back
Walk this run's rows against what actually happened: every row maps to a real action; each evidence pointer resolves and shows what the row claims; an unlogged fork or abandoned approach that shaped the work is a gap, so add it. Fix the log with superseding rows, never by rewriting.

## Independent review
Before handing back, have a different model (or at minimum a fresh sub-agent) read the trail and flag: decisions with weak evidence, verification claimed without proof, choices risky in hindsight, gaps a skim would miss. End the reply with an "Attention" section: `reviewed by <model>`, then each flag pointing to specific rows. "No flags" is valid.

---
Adapted from the pstack plugin (cursor/plugins, MIT License, (c) 2026 Lauren Tan), generalised for any domain and agent harness.
