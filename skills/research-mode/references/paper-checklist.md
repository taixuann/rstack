# What a paper needs

The list for a research article. Paper preparation walks it and writes, for each item, where it comes from. Each item ends as a report entry id, a `[user]` answer, or `TODO: unknown`. A short format (letter, communication) drops the items the venue's rules drop; say which.

| Group | Item | Lives in |
|---|---|---|
| Target | venue, article type, submission stage | `target.md` |
| Target | official instructions: URL and date checked | `target.md` |
| Target | limits: length, abstract, figures and tables, references | `target.md` |
| Target | required sections and statements, anonymity | `target.md` |
| Target | audience: who reads it and what they already know | `target.md` |
| Target | key message, one sentence | `target.md` |
| Target | the claims this paper makes, by id | `target.md` |
| Front matter | authors in order, affiliations, corresponding author | `target.md` |
| Front matter | contributions, funding, acknowledgements, competing interests | `target.md` |
| Introduction | the gap: what is missing and why it matters | `target.md`, the user's words |
| Introduction | the question or hypothesis | `target.md` |
| Introduction | each prior work to cite, with what it is cited for | `citations.yaml` |
| Methods | materials with supplier and grade | `methods.yaml` |
| Methods | samples: n and the replicate structure | `methods.yaml` |
| Methods | instruments and settings | `methods.yaml` |
| Methods | procedure, in order | `methods.yaml` |
| Methods | analysis method, statistics, correction for many comparisons | `methods.yaml` |
| Methods | software and versions | `methods.yaml` |
| Methods | exclusions with their criterion, deviations from the plan | `methods.yaml` |
| Methods | ethics approval, if people or animals are involved | `methods.yaml` |
| Results | per claim: the statement in the user's words | `claims.yaml` |
| Results | per number: value, unit, uncertainty and its kind, n, source file | `claims.yaml` |
| Results | per figure: id, path, what it shows, the run behind it | `figures.yaml` |
| Results | negative and null results that belong to the question | `claims.yaml` |
| Discussion | limitations | `limitations.md` |
| Discussion | alternative explanations still open | `limitations.md` |
| Discussion | comparisons with the literature | `citations.yaml` |
| Discussion | scope: what the claims do not cover | `limitations.md` |
| Back matter | data and code availability | `target.md` |
| Back matter | supplementary items | `figures.yaml` |
| Back matter | AI-use disclosure, if the venue asks | `target.md` |
| Open items | every item still unknown, with an owner | `docs/rstack/writing/<piece>/todo.md` |

The list follows the manuscript parts in `claude-scientific-writer`'s `scientific-writing` skill (MIT, K-Dense Inc.), rewritten for a materials and devices project.
