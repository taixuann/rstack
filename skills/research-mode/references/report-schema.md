# The report: schema and number-check rules

`docs/reports/<question>/` is the folder of one question. Its `README.md` indexes it; `method/design.md`, `method/resources.md`, `method/samples.csv` and `method/log.md` hold the design and what was done; the five files below hold what a piece may say. rstack builds the five in preparation from its outputs and the user's answers. `results/README.md` is an optional index of results that answer the question, written only when needed (Analysis review); it links to result pages and copies no number. The text is checked against it by `number-check` (`skills/number-check/scripts/number_check.py`).

## Files

| File | Holds | Comes from |
|---|---|---|
| `docs/rstack/writing/<piece>/target.md` | venue, rules, key message, chosen claims, `report:` (the question folder), stage, hashes | the user's answers |
| `claims.yaml` | each claim with its numbers | `analysis/<name>/docs/results/<figure>.md` and the figure data of the accepted runs; each entry confirmed by the user |
| `methods.yaml` | facts of the method, with value and unit where there is one | the analysis method notes and the experiment records |
| `figures.yaml` | figure id, path, what it shows, the run behind it | the accepted runs |
| `citations.yaml` | key, DOI, what the work is cited for, page, label | the literature notes |
| `limitations.md` | one line per limit, with an id (`L1`) | the user's words |
| `docs/writing/<piece>/references.bib` | the bibliography | exported from Zotero or made with `citation-management` |
| `docs/rstack/writing/<piece>/todo.md` | what is still unknown, with an owner | the assistant |

Every number links to its file: `source` is a path from the project root, and the report check opens it and fails when the value is not written there, digit for digit. Nothing is typed from memory.

After approval the five evidence files are frozen (not the rest of the folder). `target.md` records their sha256 in `report_hashes`, and the draft check fails if one changed. A slide deck may use a paper's report: its `target.md` says `report: <question>`.

```yaml
# claims.yaml
- id: C1
  statement: "..."             # the user's confirmed wording
  figure: F2
  numbers:
    - id: C1.n1
      quantity: peak current
      value: '3.24'            # quoted, so trailing zeros are kept
      unit: mA                 # '' for a pure number
      uncertainty: '0.05'      # or none, for a count
      uncertainty_kind: SD     # SD, SEM, CI95, range, none
      n: 5
      source: analysis/cv/figures/peak/peak_data/summary.csv   # must exist

# methods.yaml
- {id: M1, fact: scan rate, value: '50', unit: mV/s, source: analysis/cv/docs/method.md}

# figures.yaml
- {id: F2, path: analysis/cv/figures/peak/peak.png, shows: "...", run: "...", claims: [C1]}

# citations.yaml
- {key: smith2021, doi: 10.x/y, supports: "...", page: 4, label: source-checked}
```

## What the report check does

`number_check.py report <project> <piece>` fails when: a file is missing; a value or uncertainty is not written in its source file; `target.md` front matter lacks kind, venue, audience, key message, claims or stage (and article type for a paper); any line of `target.md` still says TODO; a chosen claim lacks a statement, a figure in `figures.yaml`, or a number with quantity, value, unit, uncertainty, kind, n and an existing source file; a methods fact lacks its source; a figure path does not exist; a citation key is not in `references.bib` or has no `supports`. It prints one `HASH` line per evidence file.

## What the draft check does

`number_check.py draft <project> <piece> [file or folder]` reads `.tex` and `.md`. With no path it reads `main.tex` and `sections/` of `docs/writing/<piece>/`.

1. **Skipped text.** Code blocks, inline code, comments, links, citation keys, labels, dates, list numbers, heading numbers, and the numbers of figures, tables, sections and equations.
2. **Checked numbers.** A number with a unit the report uses, with `±`, with `%`, with a decimal point, or after `n =`.
3. **Match.** The number equals a report value after SI-prefix scaling (3.24 mA is 0.00324 A) and is a correct rounding of it, by decimal places in the unit written. More digits than the report has is a failure.
4. **Unit.** The unit is the report's unit up to an SI prefix. A number written with no unit, or with another unit, where the report has one, fails.
5. **Uncertainty.** A `±` in the draft must match the report's. A report number with an uncertainty, written without it, is a warning.
6. **Derived numbers fail.** A percent change or a ratio worked out in the prose is not in the report. The analysis adds it, then it passes.
7. **Citations.** Every `[@key]` or `\cite{key}` must be in `citations.yaml`.
8. **Bare integers** with no unit are listed as UNCHECKED and never fail.
9. **Coverage.** A number of a chosen claim that never appears in the draft is a warning.
10. **Exemption.** A line that contains `rstack: not-a-result` in a comment is skipped and counted in the last line of the output, so a reviewer sees how many there are.

Output is `FAIL file:line: message`, with the nearest report entry. Exit 1 on any FAIL.

Known limits: only a leading SI prefix is converted, so mA/cm² against A/m² fails; write the report's unit. `siunitx` macros and numbers written as words are not read. Rounding is judged by decimal places, so 3200 µA does not match 3.24 mA.
