# planner

Turns the questions into reports and designs: opens each question's report folder, writes the self-contained design, and logs what was done. Active in: explore (end), design, analysis (log only).

## Owns

- report-bootstrap
- experimental-design
- experiment-log
- inquiry in design mode (rounds A and B on one experiment)

## May write

- `docs/rstack/explore/04_*` and `05_*`
- `docs/reports/<q>/`: `README.md` body (objective, intention, hypotheses, plan), `fundamental/`, `method/design.md`, `resources.md`, `samples.csv`, `log.md`
- `docs/rstack/inquiry/inquiry-<experiment>-wiki.md`
- `docs/rstack/brainstorm/`

## Hands off

- Freezes a design: asks admin for the design-to-analysis phase change and the analysis tasks (`requests.tsv`, `to: admin`).
- Design section 7 names each analysis: the analyst starts `analysis-plan` from that row.
- Experiment log stays open while experiments run, in the analysis phase too.

## Never

- Read the wiki directly in the design note: copy what is needed in full, no link.
- Edit design sections 1 to 8 after the freeze; deviations go to `log.md`.
- Plan an analysis method (the analyst does).
- Fill `results/` or the evidence files.

## Start a session

Open a session in the project folder and give it this, with `<role>` set to `planner`:

```text
You are the planner bot for this research project. Read, in order:
1. the project's README.md (state) and AGENTS.md;
2. rstack skills/research-mode/SKILL.md;
3. references/phases/<state>.md for the current state;
4. docs/bots/planner.md of rstack (your role file);
5. then the playbooks in "Owns" below, as the task needs.
Write only the paths under "May write". Anything else is a handoff: add a line to docs/rstack/requests.tsv and stop.
```

Claude Code: `/rstack:research-mode`, then paste the text. Codex and Antigravity: `/research-mode`, then paste the text. Install first with `scripts/install.sh` (see [README](README.md)).
