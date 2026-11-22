### Presentation

Phase: write, kind: slides. Output: `docs/presentation/<piece>/slides.md` and talk notes. The user gives every title and line of text; you build the order and place the figures. Principles: `principle-the-user-writes-the-prose`, `principle-report-before-prose`. Skills: `interrogate` (interview mode), `scientific-slides`, `number-check`. Agent: `critic`.

1. **Target.** `docs/rstack/writing/<piece>/target.md` with `kind: slides`: the event, the minutes, the audience, the key message in one sentence, and the claims the talk makes. Ask what is missing and label the answers `[user]`.
2. **Report.** A talk needs an approved report. Use this piece's own, built with **Paper preparation** steps 3 to 10, or a paper's: write `report: <piece>` in the target. Run `number_check.py report <project> <piece>`. No approved report means stop here.
3. **Outline interview.** Use `interrogate` in interview mode. Ask for the one thing the audience should remember, then one line per slide: what that slide says, as a full statement. Ask how many slides fit the minutes; `scientific-slides` has the order for each kind of talk and timing rules of thumb. Write the user's lines verbatim to `docs/rstack/writing/<piece>/scaffold/outline.md`, labelled `[user]`. Ask until each chosen claim has a slide, each result slide names its figure and report entries, and the order reads as one argument: what is the question, what was done, what was found, what it means, what limits it.
4. **Build the structure.** Write `docs/presentation/<piece>/slides.md`, one `##` heading per slide. The heading is the user's line, unchanged. Under it place the figure from `figures.yaml` by its path, one main figure per slide, and a comment listing the report entries the slide rests on. Add no other text. A slide whose line has no figure or entry behind it is flagged to the user, not filled.
5. **The user writes** any further text on the slides and the talk notes in `docs/presentation/<piece>/notes.md`.
6. **Develop by questions.** For each slide ask: can the audience read the figure in the time it is shown, which one number should they take away, what do you say that the slide does not show. Do not write the slide text or the notes.
7. **Check the numbers.** Run `number_check.py draft <project> <piece> docs/presentation/<piece>`. Show every FAIL with its line.
8. **Critique.** Spawn a fresh `critic` in reader mode on the slides only: what does the talk claim, slide by slide. Then a fresh `critic` in evidence mode with the slides, the report and the reader file. Files go to `docs/rstack/writing/<piece>/review/`. Check each finding against the line it cites, then walk them with the user.
9. **Mechanical fixes.** List them one per line; apply only the accepted ones.
10. **Pass.** The gates are the same three as for a paper, each run with `writing.py gate <project> <piece> <gate> --approved-by-user` on the user's word: `report-approved` after step 2 (for a report shared with a paper, this freezes it for the talk too), `draft-ready` before step 8, `critique-passed` at the end. Findings go in the ledger as in **Paper critique**.

For Beamer, `scientific-slides` has two templates and a guide; strip the sample text. PowerPoint is the user's own step.

**Reply:** the slide list with the figure on each, the open questions, the number-check result, the findings by severity, and whether it passed.
