### Report bootstrap

Phase: explore, last (and in design, for a new question). Turn the context, aims, and literature into questions and methods, open each question's report folder, then check the whole proposal. This playbook writes documents only. It never touches `data/raw/` or `analysis/`.

| File | Holds |
|---|---|
| `04_questions-and-hypotheses.md` | Per work package: the questions as sentences and the candidate hypotheses, each with its source papers |
| `05_methods-and-feasibility.md` | Per work package: candidate methods, resources, risks, ethics, fallbacks |
| `docs/reports/<question>/README.md` and `fundamental/README.md` | One folder per question, from `templates/report/` |

1. Read `02_aims-and-milestones.md`, `03_literature-map.md`, and `references.yaml`. Every question must trace to the gap or to a paper. If `wiki/` exists, read `wiki/CLAUDE.md` and follow its router for the methods, procedures and past analyses the questions can build on; label them as the user's own experience, not as literature.
2. Write `04` with `hypotheses` (falsifiable, with the result that would refute each) and `brainstorming` for alternatives. Cite papers by their `references.yaml` cite and update their `used_in`.
3. Write `05` with `experimental-design` for method candidates and a rough feasibility estimate (devices or samples per condition, repeat measurements, time per run, and whether the milestones allow them). Include ethics and consent for human-subject work.
3a. **Open the reports.** For each question the user wants to answer with an experiment, ask the user to name it (a short slug such as setup-4-probe-measurement). Never overwrite an existing folder. Create `docs/reports/<question>/` from `templates/report/README.md` and `templates/report/fundamental/README.md` only. The `method/` and `results/` folders and the evidence files come from their own playbooks.
3b. **Intention.** Fill the `README.md` Intention with the user's own words, unedited and labelled `[user]`: the question, the decision it supports, what counts as success. Whatever the user has not said stays `TODO: unknown`. Fill the hypotheses and the plan from `04` and `05`, with links.
3c. **Fundamental.** Fill the `fundamental/README.md` table: one row per concept the method needs, the user's understanding left `TODO: unknown` for the user to write. Learning a concept is the user's own work; anything done outside the project is not tracked and not asked about. When the user brings it, put their raw words in `docs/inputs/`, then record the note in `docs/understanding/` with `doc-coauthoring`. Check its claims with **Literature review** and **Inquiry**; a statement moves up the ladder only by that review.
4. Update the README: one block per work package with its questions and candidate hypotheses (as sentences), linked to these files.
5. **Exit check.** Assemble the chain from the files: problem exists, gap follows from the literature, each question addresses the gap, the methods can answer it, the milestones are feasible, the contribution is clear. Run `interrogate` on it and `scientific-critical-thinking` on the weakest claim. Fix weak links.
6. Offer the explore → design state change (**Project admin**).

**Reply:** the chain with its weakest link, what changed since intake, and what is still unknown.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start report-bootstrap question=<slug>`). Items: file (a glob with a match), cmd (exit 0), decision (a new decisions.tsv row).

- file docs/reports/{question}/README.md
- file docs/reports/{question}/fundamental/README.md
- decision
