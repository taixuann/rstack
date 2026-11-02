# Recipes and pitfalls

**Recipes**
- New project: `/research-mode scaffold projects/res_<name> and write a one-page README with the question.`
- Design: `/research-mode design the study for <question>. Argue the best alternative design first.`
- Analysis: `/research-mode analyse data/raw/<file> per the plan in docs/rstack/design/<note>. Label post-hoc findings.`
- Literature: `/research-mode review the literature on <topic>; sources to docs/raw, notes to docs/wiki.`
- Manuscript: `/research-mode draft the Methods section; every number copied from analysis/.`
- Review: `/research-mode peer-review manuscripts/<draft>.md and separate blocking issues.`

**Pitfalls**
- Asking for a result before the plan is written. Write the analysis plan first.
- Pointing the agent at `data/raw` with write access. Raw is read-only.
- Citing from memory. Every reference must resolve.
- Reporting the best validation score. Report the held-out one.
