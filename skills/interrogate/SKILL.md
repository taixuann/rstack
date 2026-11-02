---
name: interrogate
description: "Adversarial review of a design, analysis, manuscript, or code: adversaries try to break it and only findings proven by a run or a traceable check survive. Use for 'interrogate', 'adversarial review', 'challenge this', 'stress test this', 'find blind spots', or 'tear this apart'. Reports findings; does not apply fixes."
---

# Interrogate

Adversaries try to break a work product. A finding survives only when a run or a traceable check proves it. Report findings; do not fix.

## Frame
Scope is what the user names; otherwise the current work product (latest diff, draft, or analysis). Restate the intent in your own words from the user's message and the artifacts; ask when unclear.

## Delegation mechanism

Use whatever sub-agent facility the harness offers. In Claude Science that is `host.delegate(...)` in the `repl` tool (run `help(host.delegate)` first; never guess its signature). If no sub-agent facility exists, run the workers one after another yourself and say the run was sequential. Every worker brief stands alone: goal, scope, exact slice, how to verify, what to report, and its own output path.

## Fan out
Spawn several adversaries, each from a different angle (for research: statistics and assumptions, confounds and design, data provenance and leakage, citations and claims, reproducibility). Each gets the scope, the intent, and this brief:

> Break this. Prove each finding with a run against the real artifact: a failing test, a script that reproduces the wrong number, a recomputation from raw data, or a citation that does not say what is claimed. Report each finding with a title, the exact command or check, the output it produced, and the output the intent requires. Leave out anything you did not run, including style, wording, and risks that matter only after a future change. No findings is a valid result.

## Verify
Rerun each finding's command yourself. Keep a finding when the output shows the failure and the failure breaks the intent; drop the rest; merge findings with one root cause. Adversaries find different failures, so keep every verified finding rather than choosing one adversary's list.

## Output
- **Intent**: the restatement.
- **Findings**: per verified finding, the command, its output, how it breaks the intent, which adversaries found it. Say "no verified findings" when none survive.
- **Dropped**: per adversary, the count dropped and why.

---
Adapted from the pstack plugin (cursor/plugins, MIT License, (c) 2026 Lauren Tan), generalised for any domain and agent harness.
