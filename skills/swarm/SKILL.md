---
name: swarm
description: "Fan out N parallel workers on independent slices or competing arms, drain them, and return one consolidated report. Use for /swarm, 'swarm this', or any task with parallel coverage, races, gauntlets, or exploration, such as one worker per paper, dataset, file, or sub-question."
---

# Swarm

Open a todo list with: Frame, Fan out, Aggregate, Report.

## Frame
1. State the done predicate and the artifact or report the swarm returns.
2. Choose the shape: partition into slices, race N workers on identical briefs, or both. For a race declare the selection rule up front: `first pass`, `rank all`, or `best-of`.
3. Give each worker its own writable output location. When workers verify or measure something, the brief names the exact inputs (file versions, commit, dataset hash) and the method (sample count, what one sample is, order), and the worker records both.

## Delegation mechanism

Use whatever sub-agent facility the harness offers. In Claude Science that is `host.delegate(...)` in the `repl` tool (run `help(host.delegate)` first; never guess its signature). If no sub-agent facility exists, run the workers one after another yourself and say the run was sequential. Every worker brief stands alone: goal, scope, exact slice, how to verify, what to report, and its own output path.

## Fan out
Spawn all workers in one step, in the background. Reports use `PASS`, `ISSUES`, or `BLOCKED`, each with evidence. A worker that can prove a defect lists every defect it can prove, not only the first. If a worker drops out, proceed with N-1 and note it.

## Aggregate
Read the terminal results. Drop a result that omits the inputs and method its brief names and respawn that worker once; after a second miss record a gap. A gap is not a pass. For coverage, every required slice needs a result. For a race, apply the declared rule. Do not paste raw worker output.

## Report
One consolidated report: result table, one-line issues, gaps or dropouts, and the race rule when used.

---
Adapted from the pstack plugin (cursor/plugins, MIT License, (c) 2026 Lauren Tan), generalised for any domain and agent harness.
