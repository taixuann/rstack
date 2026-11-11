# Recipes and pitfalls

**Recipes**
- New project: `/rstack:init projects/res_<name>` (creates the folders and README, AGENTS, CLAUDE, then interviews you).
- Design: `/research-mode design the study for <question>. Argue the best alternative design first.`
- Analysis: `/research-mode analyse data/raw/<file> per the plan in docs/rstack/design/<experiment note>. Label post-hoc findings.`
- Literature: `/research-mode review the literature on <topic>; sources and notes to docs/literature-review.`
- Writing and slides: use the wstack plugin; rstack only supplies `analysis/` and `docs/results/`.
- Review: `/research-mode peer-review docs/writing/<piece>/<draft> and separate blocking issues.`

**Pitfalls**
- Asking for a result before the plan is written. Write the analysis plan first.
- Pointing the agent at `data/raw` with write access. Raw is read-only.
- Citing from memory. Every reference must resolve.
- Reporting the best validation score. Report the held-out one.
