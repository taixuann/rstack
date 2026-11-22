### Paper critique

Phase: write, stage: critique. Output: review files in `docs/rstack/writing/<piece>/review/`, and a draft the user revised until it passes. Nothing here edits the draft except an accepted mechanical fix. Skills: `number-check`, `peer-review`, `scientific-critical-thinking`, `academic-humanizer`, `citation-management`. Agent: `critic`. Reads the draft, `docs/reports/<topic>/`, `docs/rstack/writing/<piece>/`. Writes `docs/rstack/writing/<piece>/review/` and `findings.tsv`.

1. **Number check.** Validate the bibliography with `citation-management` (`validate_citations.py`), then run `number_check.py draft <project> <piece>` and save the output to `docs/rstack/writing/<piece>/review/<date>-numbers.txt`. Any FAIL stops here: the user fixes the draft first.
2. **Reader test.** Spawn a fresh `critic` in reader mode. Give it the draft folder only. It writes `<date>-reader.md`: what the paper claims, how, and with what limits.
3. **Three reviews, each a fresh `critic`, each with its own file.** They may run at the same time.
   - Evidence mode, given the draft, `docs/reports/<topic>/` and the reader file: `<date>-evidence.md`.
   - Referee mode, given the draft and `docs/reports/<topic>/`, using `peer-review`: `<date>-referee.md`.
   - Prose mode, given the draft, `references/paragraph-quality.md` and the `academic-humanizer` skill: `<date>-prose.md`.
4. **Check the critics, then record.** Open each file. For each finding, open the line it cites and confirm it says what the finding claims. Drop a finding you cannot confirm and say that you dropped it. Add each confirmed one to the ledger: `writing.py finding <project> <piece> add --round N --mode <mode> --severity <blocks|should-fix|note> --location file:line --text "..."`. A finding the ledger already holds as rejected is not added again unless there is new evidence; say so.
5. **Decide with the user, one finding at a time,** in order: blocks, should fix, note. The user decides each: fix it, or reject it with a reason in their own words. Record it: `writing.py finding <project> <piece> set <id> rejected --reason "..."`, or `set <id> fixed` after the user's edit and a re-check of that line. The user edits the text. You apply only accepted mechanical fixes.
6. **Run again** from step 1 after the user's edits, as the next round, with new files. Give each critic the ledger (`docs/rstack/writing/<piece>/findings.tsv`) so it does not raise a rejected finding again. If the count of open findings does not fall from one round to the next, stop and tell the user: the text or the report needs a decision, not another round.
7. **Pass.** Run `writing.py gate <project> <piece> critique-passed --approved-by-user` on the user's word. It refuses while the number check fails, a reader or evidence file is missing, or a finding that blocks is open.
8. **After the critique.** The critic is one more reviewer. Tell the user the piece now goes to co-authors and the supervisor; their comments enter the same ledger with `--mode people`.

**Reply:** the number-check result, the count of findings per file by severity, what the user fixed and rejected, what no critic could check, and whether it passed.
