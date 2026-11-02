### State review

Gate review at every state exit. **Project docs** calls it before a state change. It turns the state's rules into findings, then into tasks, so the state cannot close with known holes.

1. Read `references/state-gates/<state>.md`, the README, the state's `tasks.md`, and the state's documents in `docs/rstack/<state>/`.
2. Run `interrogate` with each gate angle as one adversary. A finding survives only if it names the file and the missing or weak item, or comes from a check you ran.
3. Write `docs/rstack/<state>/review.md`: date, then one row per finding with the angle, the finding, the evidence, and a severity of blocks exit, should fix, or note.
4. Add a task to `tasks.md` under a "Gate review <date>" heading for every blocking and should-fix finding. Run `scripts/sync_readme_tasks.py` so the README shows them.
5. The exit passes only when every blocking task is ticked and the user approves. After fixes, re-review only the angles that failed. Then continue with **Project docs** to change state.

**Reply:** the findings by severity, the tasks added, and whether the exit can pass.
