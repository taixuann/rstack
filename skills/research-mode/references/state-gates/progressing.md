# Gate angles: progressing

1. **Provenance.** Every number traces to a script and an input (path, hash). Rerun from a clean state matches.
2. **Quality control.** QC ran before analysis, and excluded data is listed with the reason.
3. **Explain the number.** Each reported value has n, spread, a limiter, and a check that it measured what was meant.
4. **Sensitivity.** At least one analysis choice was varied and the conclusion held or the change is reported.
5. **Honest labels.** Deviations from the plan are logged. Post-hoc findings are labelled. Negative results are kept.
6. **Raw untouched.** `data/raw/` is unchanged and hashes match.
7. **Challenge review.** Every result marked `cited: true` has a usable `review.md` on its current run (no open blocking finding, or a waiver the user wrote), its claim is written for that run, and `docs/review.md` covers the accepted runs. `rstack_run.py check` enforces this (**Analysis review**).
