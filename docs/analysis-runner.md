# The analysis runner

`skills/research-mode/scripts/rstack_run.py` carries the analysis playbooks. Figures are always made through it, never by hand.

| Command | What it does |
|---|---|
| `new <project> <name> --figure stage:fig` | scaffold an analysis: README, `inputs.yaml`, `docs/`, scripts, the shared `analysis/lib/` |
| `run <analysis> --stage check\|main\|verify --figure F` | refuse out of order or without an Objective and Why; run with figrecipe; snapshot everything; run the checks; status verified, check-failed, rejected, failed or completed (a bad run leaves `figures/` as it was) |
| `tick <analysis> --figure F --approved-by-user [--run ID]` | after you have seen the figure: tick the task, write `docs/results/F.md`; `--run` accepts an earlier verified run |
| `check <analysis>` | figures match their runs, no figure without a verified run, cited results have a real review and a fresh claim |
| `diff`, `replay` | compare two runs; rerun a run and compare its figure data |
| `show <analysis>` | write `provenance.html`: one scroll of figures with objective, claim, review state and tabs for code, inputs, checks, log, environment |
| `export <analysis> --figure F` | copy the accepted figure out as `<run id>_<figure>.png` |
| `package <analysis>` | build `package/`: figures, code, inputs, standalone `reproduce.py`, README from your confirmed claims. Refuses anything unsettled |

The `critic` agent reviews a run or the whole analysis independently; `check` makes a cited result need that review.
