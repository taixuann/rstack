# Exit review

Gate review at every phase exit. **Project admin** calls it before a phase change. It turns the phase's rules into findings, then into tasks, so the phase cannot close with known holes.

1. Read the Exit gate angles in `references/phases/<phase>.md`, the README, the phase's section in `docs/rstack/tasks.md`, and the documents with that `phase:` in `docs/rstack/`.
2. Run `interrogate` with each gate angle as one adversary. A finding survives only if it names the file and the missing or weak item, or comes from a check you ran.
3. Write `docs/rstack/reviews/<phase>.md`: date, then one row per finding with the angle, the finding, the evidence, and a severity of blocks exit, should fix, or note.
4. Through the Tasks job, add a task under a `### Goal: Gate review <date>` for every blocking and should-fix finding.
5. The exit passes only when every blocking task is ticked and every goal of the phase is done or deferred by the user and the user approves. After fixes, re-review only the angles that failed. Then continue with **Project admin** to change phase.

**Reply:** the findings by severity, the tasks added, and whether the exit can pass.
