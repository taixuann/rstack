---
name: number-check
description: "Check a manuscript or slides against the report in docs/reports/<topic>/ with a script: every number, unit, uncertainty and citation key in the draft must be in the report, and the report must be complete for its target. Fails with file and line. Use for /rstack:number-check, before a critique, after the user edits a section, or when asked whether the draft's numbers match the results."
---

# Number check

`scripts/number_check.py` needs Python 3 and PyYAML. Run it; do not check numbers by eye.

```bash
python scripts/number_check.py report <project> <piece>          # is docs/reports/<topic>/ complete, and is each value in its source file?
python scripts/number_check.py draft <project> <piece>           # main.tex and sections/ of docs/writing/<piece>/ against the report
python scripts/number_check.py draft <project> <piece> <path>    # one file or folder, for example docs/presentation/<piece>/
python scripts/number_check.py --selftest                        # runs on tests/fixture
```

- `FAIL file:line: message` and exit 1 means stop. Show the user every FAIL line as printed.
- `WARN` and `UNCHECKED` do not fail. Show their count, and the lines when asked.
- Never make a FAIL pass by editing `docs/reports/<topic>/`, by adding a `rstack: not-a-result` marker yourself, or by changing a number in the draft. The user changes the draft. A number missing from the report is added by the analysis, then Paper preparation runs again.
- The rules and the known limits are in `../research-mode/references/report-schema.md`.
