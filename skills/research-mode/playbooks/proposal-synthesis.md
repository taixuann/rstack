### Proposal synthesis

State: explore, last. Turn the context, aims, and literature into questions and methods, then check the whole proposal.

| File | Holds |
|---|---|
| `04_questions-and-hypotheses.md` | Per work package: the questions as sentences and the candidate hypotheses, each with its source papers |
| `05_methods-and-feasibility.md` | Per work package: candidate methods, resources, risks, ethics, fallbacks |

1. Read `02_aims-and-milestones.md`, `03_literature-map.md`, and `references.yaml`. Every question must trace to the gap or to a paper.
2. Write `04` with `hypotheses` (falsifiable, with the result that would refute each) and `brainstorming` for alternatives. Cite papers by their `references.yaml` cite and update their `used_in`.
3. Write `05` with `experimental-design` for method candidates and a rough feasibility estimate (devices or samples per condition, repeat measurements, time per run, and whether the milestones allow them). Include ethics and consent for human-subject work.
4. Update the README: one block per work package with its questions and candidate hypotheses (as sentences), linked to these files.
5. **Exit check.** Assemble the chain from the files: problem exists, gap follows from the literature, each question addresses the gap, the methods can answer it, the milestones are feasible, the contribution is clear. Run `interrogate` on it and `scientific-critical-thinking` on the weakest claim. Fix weak links.
6. Offer the explore → design state change (**Project docs**).

**Reply:** the chain with its weakest link, what changed since intake, and what is still unknown.
