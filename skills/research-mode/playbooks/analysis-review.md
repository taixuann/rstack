### Analysis review

State: progressing. Review is called, not a stage every analysis passes through. Start from why you are here:

| Case | When | Weight |
|---|---|---|
| Self-check | After every run | Built into **Analysis run**: checks, figure rules, replay. No `review.md`. |
| Changed run | A parameter, an input selection, a script, the shared lib or the environment changed. Same figure, different provenance. | Compare the two runs, then accept one. |
| Challenge | A result will carry a claim, is surprising, a supervisor asks, or the progressing gate needs it | An independent reviewer attacks one run, or the whole analysis. |

The figure name is the question; each run is the evidence for it. One figure can have many runs, each with its own provenance, and any verified run can be accepted. If the changed run answers a different question, make a new figure task instead.

Where reviews live:
- A review of one run is `.rstack/provenance/<analysis>_<figure>/<run>/review.md` (template `templates/analysis/run-review.md`). It judges that run, never the live `figures/` folder.
- The review of the whole analysis is `docs/review.md` (template `templates/analysis/analysis-review.md`), with `runs:` listing the run reviewed for each figure.
- Nothing is copied by hand into a results file. `rstack_run.py show` and the page read the reviews: a figure shows review current, carried from an earlier run, stale or none.

A review counts for the run it sits in, and for a later run whose inputs, scripts, lib and figure data are identical (a replay, for example). Any other change makes it stale: the new run has not been reviewed. `docs/review.md` is stale as soon as an accepted result is a different run.

Skills for this playbook: `interrogate`, `swarm`, `arena`, `scientific-critical-thinking`, `acceptance-checks`, `hypotheses` and `brainstorming` (for a surprising result), the question checklist and decision log from `analysis-report`, and **Peer review** for anything the user will publish. The reviewer is the `critic` agent in analysis-run mode.

**Changed run**

1. Name what changed and why. `rstack_run.py diff <old run> <new run>` lists the changed inputs, scripts, lib files, environment lines and outputs.
2. Run the figure again with the change, or `replay` the old run if only the environment may have changed. The new run must be verified.
3. Read the differences in `<figure>_data/` and the tables. Say which numbers moved, by how much, and whether the claim still holds. A change you cannot explain is a finding, not noise.
4. Choose, with the user: accept the new run (`tick`), or keep the old one (`tick --run <old run id>` puts its files back). Both runs stay on disk. Record a deviation in `docs/method.md` if the plan changed.
5. After accepting a different run, re-read the claim in `docs/results/<figure>.md`. `show` flags it as stale until you set `claim_for` to the accepted run id, which says you re-checked it.

**Challenge**

1. **Independent reviewer.** The agent that made or ran the figure does not review it. Start the `critic` agent in analysis-run mode with the run folder and the analysis folder, and let it write `review.md`. Be honest about the limit: the critic is a fresh context but the same kind of model as the author, so it shares blind spots. For a result that will carry a claim, the user reads the figure and the review too; for a hard choice between methods use `arena`, and for many items `swarm`.
2. **Pick the method by the question.**
   - One result to attack: the `critic`, or `interrogate`.
   - Many independent items (each figure, each dataset, each fit): **swarm**, one worker per item, each writing its own file.
   - Two analyses or fits compete and one must be chosen: **arena**.
   - Anything the user will publish: add the **Peer review** playbook on the whole.
3. **The reviewer reads the run, not the folder**, runs `rstack_run.py check` first (a mismatch blocks), recomputes at least the headline number from the saved inputs, and answers the questions in the critic's brief: figure rules, traceability of each number, code against `docs/method.md`, the hypothesis table's "supports if / refutes if", claim against n and spread, excluded units, reproducibility.
3a. **Grade the claim and answer the checklist.** Using `scientific-critical-thinking` (its evidence hierarchy and statistical pitfalls), grade the headline claim strong, moderate, weak or unsupported with one line of reason, and separate what the data show from what the claim asserts. Check that the result answers every clause of the question checklist from `docs/method.md` (`analysis-report`), and read the decision log (Deviations, Exclusions) first: every fork where the analysis could have gone the other way. The review follows the skill's critique shape: summary, strengths, concerns by severity, recommendations, overall assessment.
3b. **A surprising result, or one that contradicts a hypothesis.** Use `brainstorming` moves (failure analysis, inversion, a changed constraint) to list alternative explanations, then `hypotheses` to turn each into a test. They are labelled `[assistant]` hypotheses, never conclusions; the test is a new run (Changed run), and the result decides.
4. **Severity and the blocker rule.** Each finding is blocks acceptance, should fix, or note, with its evidence; findings without evidence are dropped. `blocking:` in the front matter counts the blocking findings still open. `check` also refuses a review that still has TODO in it, or whose `blocking:` differs from the number of rows with severity `blocks acceptance` in its findings table, so the count cannot hide a blocker and the template cannot pass as a review. A blocker is closed in exactly two ways: a new verified run that fixes it (which then needs its own review), or a `waiver:` line the user wrote in the front matter with the reason. The agent never writes a waiver.
5. **Whole-analysis pass.** Before a manuscript cites results, one review over every accepted result into `docs/review.md`: do the claims agree with each other, is every hypothesis in the README decided as its table says, is anything cherry-picked (a run chosen among several), does a check-stage finding contradict a main-stage claim.
6. **Disposition.** The user accepts, rejects, or asks for a new run. Work that follows becomes tasks through **Task tracking**; the fix is a new run.

**Gate.** Set `cited: true` in `docs/results/<figure>.md` for each result the manuscript will cite. `rstack_run.py check` then fails unless each cited result has a usable review on its current run (no open blocking finding or a waiver), its claim is written for that run and no longer TODO, and `docs/review.md` exists, covers the current accepted runs and has no open blocker. The progressing gate needs `check` to pass.

**Reply:** the case, findings or differences by severity, the method used, what the reviewer did not check, and whether the run can be accepted.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start analysis-review analysis=analysis/<name>`). Items: file (a glob with a match), cmd (exit 0), decision (a new decisions.tsv row).

- cmd python3 {scripts}/rstack_run.py check {analysis}
- decision
