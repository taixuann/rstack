### Analysis plan

State: progressing (design if the analysis is already planned). Output: `analysis/<name>/` with `README.md`, `inputs.yaml`, `scripts/`. Nothing runs here. The README is the contract that **Analysis run** and **Analysis review** are held to. It stays short, one screen; the reasoning lives in `docs/`.

```
analysis/<name>/
  README.md     this analysis only: question, hypotheses, tasks, runs, links (one screen)
  inputs.yaml   the menu: every file it may use, the only place inputs are listed
  docs/
    method.md       how it answers: written once at plan time
    plan-review.md  interrogate findings and what the user decided
  scripts/      one <figure>.py and <figure>.checks.py per figure or table
  docs/results/ one file per accepted figure, written when it is ticked
  figures/<figure-name>/   written by runs
  tables/                  written by runs, only if needed
```

Skills for this playbook: `interrogate` (interview mode, then adversarial), `hypotheses`, `brainstorming` (only if the direction is open), `statistical-analysis`, `uncertainty-and-units`, `acceptance-checks`, `scientific-critical-thinking` (to test the plan), and from `analysis-report` its rules for restating the question and for provenance of inputs. `experimental-design` is for planning new data collection in the design state, not here.

Start the folder with `rstack_run.py new <project> <name> --figure check:<fig> --figure main:<fig>`. It creates the README, `inputs.yaml`, `docs/method.md`, `docs/plan-review.md`, the shared lib, and for each figure a script, a checks file and a task, all from `templates/analysis/` in the research-mode skill, with `TODO` where you must write. Nothing existing is overwritten. Steps 5 to 8 fill those files in.

1. **Find what exists.** Read the design note, the project's questions and hypotheses, and earlier analyses. If this analysis repeats one, say why. If no question exists yet, stop and write it first (step 3). Drop whatever does not serve the question (**principle-subtract-before-you-add**).
2. **Interview the user.** Use `interrogate` in interview mode, in short rounds of one to four questions, each built on the last answer: what the analysis decides; what the user expects and what would surprise them; what they would do for each outcome; which files and conditions matter and why; what could go wrong with the data. Write answers down in the user's words. Anything unknown is `TODO: unknown` with an owner; never fill it in.
2a. **Restate the question with its binding clauses** (`analysis-report`, rule 1): population, time window, inclusion and exclusion rules, the exact metric and its unit, the direction that counts as better, thresholds, and what would count as no effect. Quote any ambiguous wording and write down the reading adopted. Then write the checklist the results must satisfy: every clause, every group or comparison it names or implies, every output it asks for. It goes in `docs/method.md`; the plan-review and the critic check the results against it. A specification in the request is run as written; a better method you prefer is a sensitivity analysis beside it, never instead.
3. **Hypotheses.** Use `hypotheses`: each one a falsifiable sentence with its prediction, the result that would refute it, and a label, exploratory or confirmatory (**principle-exploratory-vs-confirmatory**). If the direction itself is still open ("which analysis is worth doing?"), use `brainstorming` first, then come back. If answering needs data that does not exist yet, stop: that is a study to design in the `design` state with `experimental-design`, not an analysis.
4. **Method.** Use `statistical-analysis` to choose the test or fit and check its assumptions, the effect size to report, and the correction for many comparisons. Use `uncertainty-and-units` for units, dimensions and how error propagates. Name the sampling and the subject, session or batch structure (**principle-model-the-domain**), so no replicate is counted as independent when it is not. State the n each comparison will have.
5. **Write the three documents.** Plain words. Each file in `docs/` opens with `Part of [README](../README.md).`
   - **`README.md`**, this order:
     - **Question**: one sentence, and the decision it supports.
     - **Hypotheses**: a table of hypothesis (from step 3, with its label), supports if, refutes if. Written before any run.
     - **Tasks**: this analysis's own checklist in three groups under `### Check`, `### Main`, `### Verify` (see step 5a). One task per figure or table, and the task text names it, such as ``- [ ] `iv-per-device` per-device curves``. The plan writes it, **Analysis run** ticks it.
     - **Runs**: a table of run id, inputs, note, status, which **Analysis run** appends to.
     - **Links**: `docs/method.md`, `docs/plan-review.md`, `inputs.yaml`.
   - **`docs/method.md`**: the **Checks** (step 5a); what is computed and why this method; assumptions, n, effect size, correction, units; the groups the inputs form; a `### <figure>` block per figure and table with Objective (what it shows or decides), Why (the hypothesis or check it serves), what is compared with quantity and unit per axis, and the frame; the runner refuses a run of a figure whose Objective or Why is missing or TODO; limits and confounds; **Deviations**, empty, filled if the analysis later departs from the plan.
   - **`docs/plan-review.md`**: written by step 9.
5a. **Plan the checks before the figures.** Real analyses do not go straight to the final figure. Split the tasks into three groups, each task one run:
   - **Check**: before the real figures. Per unit (device, sample, subject, session): is the data usable? Are the units close enough to combine or average? Does the instrument or pipeline behave on something known? Small diagnostic figures and tables live here.
   - **Main**: the figures and tables the claim rests on.
   - **Verify**: after the main result. Does it survive dropping one unit, another window or method choice? Does it match something known? Small supporting figures.
   A first Check task for every analysis (`analysis-report`, rule 2): before the first filter, list the distinct values and counts of every column you filter or group on, read from the file and not assumed from its name, name the unit of analysis, and show the row-count flow (how many records left at each step and why).
   In `docs/method.md` under **Checks**, write for every check the pass and fail criterion and what happens on failure (exclude the unit, change the method, stop), before any data is looked at. Exclusions are recorded there with the unit, the criterion and the run that showed it; raw data is never edited. A check that finds something the plan did not foresee goes in **Deviations** with the reason. Diagnostic figures obey the same figure rules as the final ones.
6. **`inputs.yaml` is the user's.** One entry per file: `id`, `path` (relative to the project root), `label`, `legend`. The user writes it, with an optional `use:` field per file for why it is included. The README does not list inputs. Check only that each path exists and each `id` is unique. Raw data stays where it is (**principle-raw-data-is-read-only**); tables sent from raw-viewer land in `analysis/`.
7. **Install the shared lib, then write the scripts.** `new` runs `rstack_run.py lib <project>`, which copies `load.py` (reads inputs, raw files through raw-viewer), `style.py` (preset, tick count, rules check, figrecipe save) and `figrules.py` from rstack's `templates/lib/` into `<project>/analysis/lib/`, never overwriting, and lists files that differ from the template. The project owns its copy; every run snapshots it. Fix a bug in the template and the project copy, not only one. One script pair per figure or table: `scripts/<figure>.py` makes it; `scripts/<figure>.checks.py` is its oracle, written from the plan's criteria with `acceptance-checks` (exit 0 passes; it reads the run's outputs from `RSTACK_OUTPUTS`). A script reads the selected inputs from the file named by the `RSTACK_INPUTS` environment variable, never from a hard-coded path or from `inputs.yaml` directly. It runs from the analysis folder, imports `load` and `style` from `analysis/lib/`, and writes only `figures/<figure>/` (`style.save_figure` saves it with figrecipe) and `tables/<figure>*`. figrecipe's data files have no header row. No absolute paths, no network, no random numbers without a fixed seed written to the log. Every number a figure shows comes from the inputs (**principle-explain-the-number**). `save_figure` checks the rules in **Analysis run**.
8. **Choose the frame for each figure.** By `principle-frame-follows-the-data`: a closed box (`nature-single`) for data that crosses zero, loops, spectra, matrices and twin axes; an open L-frame (`nature-open`, or a journal preset from `tools/figrecipe/presets/`) for distributions, kinetics, dose-response. Write the choice and the reason in `docs/method.md` under the figure, and pass the preset name to `new_figure` in the script. Choose colours by `principle-color-means-one-thing`: one colour per condition across the project, readable in greyscale, taken from the project's colour file.
9. **Interrogate the plan.** Run `interrogate` on the README and the script outline, with `scientific-critical-thinking` for the lenses (its bias, statistical-pitfall and experimental-design references: selection, confounding, measurement, multiplicity, pseudoreplication, effect size), angles: assumptions and test choice, confounds and pseudoreplication, units and scale, whether the expected evidence could actually separate the hypotheses, whether the inputs can answer the question. Findings go to the user, who decides which change the plan. Record each finding and the decision in `docs/plan-review.md`, and apply accepted ones to the README or `docs/method.md`. Do not fix silently.
10. **Ready check.** Every item true, or the plan is not ready:
    - the question names a decision
    - every hypothesis has a falsifier
    - the method follows from the question, and n is stated
    - expected evidence was written before any run
    - every input exists and has an id
    - every figure has an Objective, a Why, quantities and units
    - the README Tasks list has one task per figure and table, each naming its figure, and every check has a written criterion and a `<figure>.checks.py`
    - the interrogate findings are resolved or deliberately deferred
11. **Approval.** Show the user the README, `docs/method.md` and the script outline. Do not run until they approve. Then add one task, "Analysis `<name>`", under the right goal of `docs/rstack/tasks.md` through **Task tracking**; it is ticked when this README's Tasks are all done.

**Reply:** the README summary, where `docs/method.md` and `docs/plan-review.md` are, the interrogate findings and what was decided, what is still `TODO: unknown`, and whether the ready check passes.
