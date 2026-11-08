# Analyse and verify

Four playbooks cover an analysis. Review is called only when it is needed, and packaging comes last.

1. **Analysis plan.** `rstack_run.py new <project> <name> --figure check:<fig> --figure main:<fig>` makes the folder from templates: a one-screen README (question, hypotheses, tasks, runs), `inputs.yaml`, `docs/method.md` (method and checks), `docs/plan-review.md`, and one script, one checks file and one task per figure. You and the assistant fill them in with `interrogate`, `hypotheses` and `statistical-analysis`, the plan is interrogated, and you approve it.
2. **Analysis run.** Tasks run in the order Check, Main, Verify. `rstack_run.py run` refuses out-of-order runs, runs the figure with real figrecipe through the project's `analysis/lib/` helpers, runs the figure's checks, and keeps one provenance folder per run under `.rstack/provenance/<analysis>_<figure>/`. You see the figure, then `tick` marks the task and writes `docs/results/<figure>.md`. A re-run of a ticked figure is recorded there as superseding the old run.
3. **Analysis review.** After a changed parameter or input, `rstack_run.py diff` compares two runs and you accept one. Before a result is cited, the `critic` agent reviews its run (and then the whole analysis in `docs/review.md`); `rstack_run.py check` enforces it. `rstack_run.py show` writes a page to browse every figure with its provenance.

4. **Package results.** Once results are accepted, `rstack_run.py package analysis/<name>` builds `analysis/<name>/package/`: figures named by run id, the code, inputs and presets the runs used, `requirements.txt`, a standalone `reproduce.py`, each run's provenance, and a README made from your confirmed claims. It refuses anything unsettled. You confirm each claim in an interview first; nothing is guessed. Prove it by running `reproduce.py` in a clean environment.

Before a number is reported, **explain-the-number** asks what limits it and what else it could be measuring. Post-hoc findings are labelled. Use Reproduce to re-run a published result, and Hillclimb for sustained metric improvement.

To browse every figure with its objective, claim, review state and provenance, run `rstack_run.py show analysis/<name>` and open `provenance.html`. To send a figure to a paper, `rstack_run.py export` names the file after its run.
