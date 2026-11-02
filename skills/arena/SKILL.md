---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, and graft the strongest parts of the losers into it. Use for /arena, 'arena this', or when one attempt at a non-trivial artifact (an experimental design, analysis plan, figure, draft, or code) would lock in the wrong shape."
---

# Arena

Todo list: Frame, Fan out, Cross-judge, Pick, Graft, Verify.

## Frame
Every candidate gets the same prompt, so the prompt is the contract.
1. State the artifact each candidate produces.
2. Derive a rubric of 3-6 concrete, gradeable criteria for this task. The rubric is for the picker; candidates see only the task.
3. Choose the number of runners (at least two). Use different models or settings when the work is judgment-sensitive; the same one N times when it is generation-bound.
4. Give each candidate its own output location.

## Delegation mechanism

Use whatever sub-agent facility the harness offers. In Claude Science that is `host.delegate(...)` in the `repl` tool (run `help(host.delegate)` first; never guess its signature). If no sub-agent facility exists, run the workers one after another yourself and say the run was sequential. Every worker brief stands alone: goal, scope, exact slice, how to verify, what to report, and its own output path.

## Fan out
Spawn all candidates in one step. Each produces the artifact plus a short rationale naming the alternatives it considered and rejected. A candidate with no output is a dropout; proceed with N-1.

## Cross-judge
After all candidates finish, spawn one read-only judge, preferably from a different model than the one that did the work. It sees the rubric and candidates by label, scores each criterion, and recommends a base. If no independent judge is possible, skip it and say so.

## Pick a base
Read every candidate end to end. Score against the rubric criterion by criterion, not on feel, and compare with the judge. Disagreement means someone is biased or the rubric was ambiguous; read both rationales. Pick the base easiest to extend without breaking invariants; if tied, prefer the simpler one.

## Graft
Walk each loser once more for what is worth porting, usually one or two things each. Fold them in by hand so the result keeps one coherent logic. If candidates converge, note the agreement and ship the consensus. If they diverge wildly, the frame was under-specified: reframe and rerun rather than averaging.

## Verify
Check the synthesised artifact against the real thing (run the analysis, open the file, test the claim). If it exposes a problem, either the frame was wrong or a graft was missed.

## Output
One artifact plus a synthesis note: the base and why, the judge's verdict (or that none ran), each graft and its source, what was rejected, convergence or dropouts, and the verification result.

---
Adapted from the pstack plugin (cursor/plugins, MIT License, (c) 2026 Lauren Tan), generalised for any domain and agent harness.
