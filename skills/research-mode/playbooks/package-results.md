### Package results

Phase: analysis (last). Builds `analysis/<name>/package/`: a folder someone else can open, install and run on their own machine. It is made from the accepted runs and their provenance, one package per analysis. Nothing is computed here, and nothing is guessed.

**The rule: never guess a result.** A claim, an objective and every number in the package come from provenance and the confirmed files (`docs/results/<figure>.md`, `docs/results.md`, `docs/method.md`). You never write, reword, round or interpret one here. If something is missing or still TODO, say so and stop. `rstack_run.py package` enforces this: it refuses while a claim is TODO or was written for an older run, an Objective or Why is missing, the analysis has no Question, a run is not verified, `check` fails, or two selected figures used different versions of the lib or a preset. Its README is built from files; nothing in it is worded by hand. Principles: `principle-explain-the-number`, `principle-sources-not-memory`, `principle-raw-data-is-read-only`, `principle-prove-it-works`. Skills: `acceptance-checks`, `show-me-your-work`; `analysis-report` only if the user also asks for a separate report outside `package/`.

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

1. **Ask which figures to package.** List the accepted figures in `docs/results/` (with their run id and claim) and ask the user whether to package all of them or only a specific subset (`--figures fig1,fig2`). Also check if any raw input is sensitive or too large to copy (`--exclude-raw id,id`, `--max-raw-mb N`). Raw data is copied, never moved or edited.
2. **Check what is open.** Run `rstack_run.py check analysis/<name>` and fix anything it names before building.
3. **Build.** Run `rstack_run.py package analysis/<name>` (with `--figures ...` if a subset was chosen, and `--replace` to rebuild; `analysis/<name>/package/` is derived). A refused build leaves no folder behind; fix what it reports and re-run.
4. **Prove it.** Copy `package/` to a clean folder (or fresh venv, `pip install -r requirements.txt`) and run `python reproduce.py` to confirm hashes, scripts, and figure data match. Read the generated `README.md` to confirm every claim and run id is intact.
5. **Hand over.** Give the `analysis/<name>/package/` path. Do not commit, send or publish it. (Optional: if the user also wants a reader-facing `docs/report.md` outside `package/`, write it from the package files with `analysis-report`.)

**Reply:** the `analysis/<name>/package/` path, which figures were packaged (and any excluded), any raw data excluded, and the `reproduce.py` check result.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start package-results analysis=analysis/<name>`). Items: file (a glob with a match), cmd (exit 0), decision (a new decisions.tsv row).

- file {analysis}/package/manifest.json
- file {analysis}/package/README.md
- file {analysis}/package/reproduce.py
- cmd python3 {scripts}/rstack_run.py check {analysis}
- decision
