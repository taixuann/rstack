# Analysis workflow statechart

How one analysis moves from plan to claim. TLC checked `AnalysisStates.tla`: 9 states, 14 steps, all rules hold, no deadlock. Removing the check guard from the main step made `NoMainBeforeCheck` fail with a 4-step path, so the rules do catch a skipped stage.

**Rules the model checks**
- No task runs before the plan is approved.
- No main task before the check tasks are done.
- No verify task before the main tasks are done.
- The challenge review needs the verify tasks done.
- A result is cited only after the challenge review.

**What the model leaves out.** One task per group (the real README has many). The re-run case: an input or the code changing sends every result back to "Check tasks to run" and withdraws the claim. A failed check, which the plan handles as an exclusion or a recorded deviation. The "nothing more happens" step after a claim.

**Make it again:** from this folder, `../../skills/statechart/scripts/statechart AnalysisStates.tla --config AnalysisStates.cfg --view analysis.view.mjs --out <new folder>`.

```mermaid
---
title: "One analysis, from plan to claim"
---
stateDiagram-v2
  state "Legend" as legend {
    lg0: ready
    lg1: working
    lg2: end
  }
  class lg0 teal
  class lg1 blue
  class lg2 tan
  s0: No plan yet
  s1: Plan written
  s2: Plan interrogated, awaiting approval
  s3: Check tasks to run
  s4: Main tasks to run
  s5: Verify tasks to run
  s6: Verified, ready for challenge
  s7: Challenge review passed
  s8: Claim made
  [*] --> s0
  s0 --> s1: you and the assistant write the README and method
  s1 --> s2: the plan is interrogated
  s2 --> s3: you approve the plan
  s3 --> s4: the check tasks pass
  s4 --> s3: an input or the code changes, so results are stale
  s4 --> s5: the main figures and tables are made
  s5 --> s3: an input or the code changes, so results are stale
  s5 --> s6: the verify tasks pass
  s6 --> s3: an input or the code changes, so results are stale
  s6 --> s7: the challenge review finds nothing open
  s7 --> s3: an input or the code changes, so results are stale
  s7 --> s8: the result is cited
  s8 --> s3: an input or the code changes, so results are stale
  class s0 teal
  class s1 teal
  class s2 teal
  class s3 blue
  class s4 blue
  class s5 blue
  class s6 blue
  class s7 blue
  class s8 tan
```
