### Package results

State: ready-for-publish. Builds `analysis/<name>/package/`: a folder someone else can open, install and run on their own machine. It is made from the accepted runs and their provenance, one package per analysis. Nothing is computed here, and nothing is guessed.

**The rule: never guess a result.** A claim, an objective and every number in the package come from a file the user confirmed (`docs/results/<figure>.md`, `docs/method.md`, the run's `<figure>_data/`). You never write, reword, round or interpret one. If something is missing or still TODO, say so and stop; the package waits for the user. `rstack_run.py package` enforces this: it refuses while a claim is TODO or was written for an older run, an Objective or Why is missing, the analysis has no Question, a run is not verified, `check` fails, or two figures used different versions of the lib or a preset. Its README is built from files; nothing in it is worded by hand. Principles: `principle-explain-the-number`, `principle-sources-not-memory`, `principle-raw-data-is-read-only`, `principle-prove-it-works`. Skills: `interrogate`, `acceptance-checks`, `scientific-critical-thinking` (to test the wording of a claim), `show-me-your-work`; `analysis-report` and `brainstorming` only after the build, and never inside `package/` (step 9).

```
package/
  README.md         question, how to run it, then per figure: objective, claim (quoted), run id, inputs, review
  manifest.json     every file with its sha256, the run behind each figure, the inputs excluded
  requirements.txt  the packages the scripts import, at the versions used; no virtual environment inside
  reproduce.py      standard library only: checks the files, reruns every figure, compares the figure data
  data/raw/         copies of the raw files the accepted runs used (hashed); data/derived/ the tables read from them
  lib/ scripts/ presets/ inputs/   exactly what the runs used; lib/load.py reads data/derived/ so raw-viewer is not needed
  figures/          <run id>_<figure>.png and .pdf
  provenance/       per figure: run.yaml, inputs, checks, log, environment, review, outputs
  docs/             analysis README, method, results, reviews
```

1. **Orient.** Name the analysis. List its accepted results (`docs/results/`), the run behind each, and every README task with no accepted result. State which of those will not be packaged and why; that goes in the README under Not included.
2. **Settle what is open.** Run `rstack_run.py check analysis/<name>` and fix what it names. A cited result needs its review on its current run (**Analysis review**). Re-run a figure if it used another lib or preset version than the others.
3. **Interrogate with the user.** Use `interrogate` in interview mode, one figure at a time, then the analysis as a whole. For each figure show the image, its Objective and Why, the claim, and the number it rests on, and ask whether that is what the user decided. Test each claim's wording against its evidence with `scientific-critical-thinking`: is it stronger than the data (n, spread, scope), does it say cause where the data show association, does it cover more than the inputs it used? Say so; the user decides the wording. The user answers in their own words; you may transcribe them into `docs/results/<figure>.md`, labelled `[user]`. For the whole analysis ask: does the Question get answered, is every hypothesis in the README decided as its table says, is anything left out or chosen among several runs. Anything the user has not decided stays TODO.
4. **Decide the data.** For each raw input the runs used, ask: may it leave the project? Recordings of people, ethics-restricted data and files over the size limit are not copied (`--exclude-raw id,id`, `--max-raw-mb N`); the README lists them and `reproduce.py` then cannot rerun figures that need them. Raw data is copied, never moved or edited.
5. **Build.** `rstack_run.py package analysis/<name>` (add `--replace` to rebuild; the folder is derived). A refused build leaves no folder; fix what it lists and run it again. It reads each raw file the way the run did (raw-viewer) and saves the table, so a missing profile refuses with the file's name.
6. **Prove it.** Copy `package/` to a clean folder outside the project, make a fresh virtual environment there, `pip install -r requirements.txt`, then `python reproduce.py`. It must report that every file and every figure matches. A mismatch is a finding: find out why (a package version, a missing seed) and report it. Never edit `manifest.json` or a recorded hash to make it pass. Tell the user that figure images can differ slightly between machines; the data files are what is compared.
7. **Read the README it made.** Every claim is a quote and every figure has a run id. Anything you added is labelled `[assistant]`.
8. **Hand over.** Give the path. Do not commit, send or publish it; sharing is the user's step.
9. **Optional, after the package.** A reader-facing report is written from the package files with `analysis-report`, as `docs/report.md` outside `package/`: the question clauses mapped to steps, the provenance, the method, the results, the checks, the limitations and the decision log, all copied from the files. Its interpretation section holds only the user's confirmed claims; anything else is a labelled `[assistant]` hypothesis, kept apart and confirmed by the user, and never the skill's rule to commit to a mechanism the data do not show. What to do next is a separate discussion with `brainstorming`, also outside `package/`.

**Reply:** the package path, the figures in it and the ones left out with the reason, the data not copied, the result of `reproduce.py` in a clean environment, and anything still TODO.
