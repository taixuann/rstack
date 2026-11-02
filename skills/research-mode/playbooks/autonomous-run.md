### Autonomous run

A long task driven to completion while the user is away ("run until done", "I'm going to bed").

1. Write the done predicate, a stop condition, a time or budget cap, and the actions that always pause (deleting data, overwriting `data/raw/`, sending messages, spending money).
2. Open a decision log via `show-me-your-work` and write a row per step.
3. Work in small verified units. After each, check the artifact, not the self-report.
4. On a blocker, log it and continue with independent work. Stop at the cap or predicate.

5. **Pause.** Before stopping for any reason (going offline, a long break, context nearly full), finish or cleanly abandon the current unit, save scripts, outputs, and the log, and write `docs/rstack/PAUSE.md`: state, next three steps, open questions, commands to rerun.
6. **Resume.** Read the README state, `tasks.md`, the decision log, and `PAUSE.md`. Treat their claims as unverified. Check the real state (files present, scripts rerun, outputs matching the log), then continue under the matching playbook.

**Reply:** what finished, what is open, the log path, and the first thing to check.
