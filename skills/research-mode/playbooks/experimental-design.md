### Experimental design

Phase: design. Output: in `docs/reports/<question>/` (the folder **Report bootstrap** opened): `method/design.md` (one `## E<n>` block per experiment, the contract that **Analysis plan** and the bench work use), `method/resources.md` (what the lab has) and `method/samples.csv` (one row per unit). The folder's `README.md` is the index; update its status and contents. Reads `README.md` of the question and the Inquiry note (never the wiki directly). Writes `method/design.md`, `method/resources.md`, `method/samples.csv`. Nothing is made or measured here.

Templates are in `templates/report/`. Copy them; never invent the fields. The `experimental-design` skill is the statistics engine (design type, randomisation, replication, DOE matrices). This playbook adds the bench reality it does not cover: materials, preparation, equipment and what gets measured.

Skills for this playbook: Inquiry, `hypotheses` (falsifiable hypotheses, each with the result that refutes it), `brainstorming` (choosing between directions), `experimental-design` (the design and its seeded scripts), `statistical-power` (subject comparisons only), `uncertainty-and-units` (measurement uncertainty), `interrogate`, `arena` (two or more plausible designs), `doc-coauthoring` (filling wiki gaps, through **Protocol wiki**). Principles: **principle-question-first**, **principle-exploratory-vs-confirmatory**, **principle-attack-the-premise**.

**The loop, per experiment**

1. **Inquire first.** Run **Inquiry** for this experiment: read the question's `README.md` (objective, intention, hypotheses, plan) and `method/resources.md`; consult the wiki through `wiki/CLAUDE.md` (its router, the project's playbook, procedures, `wiki/equipment/`, and its measurement-tier table, which is the "claim answered" column of design section 6: rstack's cheap, mid, expensive is about cost, the wiki's validation, core, advanced about purpose); then interview, `brainstorming` and `interrogate` to find what is not known yet. Inquiry writes `docs/rstack/d-inquiry/inquiry-<experiment>-wiki.md`. **No wiki page or gaps:** run **Protocol wiki** with the user to fill it first, or write the note in full and offer **Protocol wiki** after the freeze.
   **Copy, do not link.** The design note holds the materials, equipment, procedure, settings and source marks in full, copied from that inquiry note. It has no wiki path, no wiki link and no `[[link]]`; someone reading only the note can run the experiment. If `method/resources.md` has `TODO: unknown` rows the experiment needs, ask for them now. If the experiment repeats an earlier one, say why.
   **Question sweep.** Before step 10, go through sections 3 to 6 step by step. Every step and every quantity has a value, a unit, a source, a tolerance, what to record and a failure criterion. Anything missing is a `TODO: unknown` the user answers. Do not freeze with one left, unless the user accepts it as a task.
2. **Purpose.** Fill section 1: question, the decision it serves, the type (baseline or repeat, sweep, confirmation, pilot), a falsifiable hypothesis with what refutes it, one primary endpoint. A sweep changes one number of a known recipe; a repeat changes nothing and tests repeatability. Say which.
3. **Design.** Fill section 2 with the `experimental-design` skill: the unit and the level of a true replicate, factors, controls that differ in one thing, replicates, blocking of nuisance factors, a seeded run order. For device and materials work plan replicates and repeat measurements, not a power calculation. Argue the strongest alternative design before settling. Write the unit rows to `method/samples.csv` with status planned.
4. **Materials.** Fill section 3 from `method/resources.md`: amount per unit, overage, total, and every stock solution with concentration, volume and the step that uses it. Anything short or expired becomes a task.
5. **Preparation plan.** Fill section 4. List every step with what it depends on, its hands-on time and its waiting time. Mark what runs in parallel (wash and dry glassware while weighing) and start the longest dependent chain first. Write the run sheet in start order. Check each equipment booking against `method/resources.md`.
6. **Protocol.** Fill section 5 so someone else could run it: settings, what to record, failure criteria, naming of units and files.
7. **Characterization tiers.** Fill section 6 from the menu in `method/resources.md`: cheap for every unit, mid and expensive for a subset, chosen by a rule written now. Name the claim each technique supports. A mechanism claim with no technique that measures the mechanism stays an interpretation.
8. **Analyses to build.** Fill section 7 with the user: which analyses will answer the hypotheses (`analysis/<name>/`), the question each answers, its inputs from section 6, and the figures or tables expected. Check both ways: each hypothesis has an analysis, each technique feeds one. Add one row per analysis to the report README's "Analyses, papers and talks" table (status planned). Do not plan the method here; **Analysis plan** does that from the row.
9. **Interrogate.** Run `interrogate` on the note with the angles of `the Exit gate angles in `references/phases/design.md``. Fix what survives. A pilot is the smallest end-to-end run; plan it first as its own experiment (type pilot) and write what it must show.
10. **Freeze.** The note is now a snapshot: do not edit sections 1 to 8 afterwards. Through **Project admin** (Tasks job), add a goal for the experiment under the design phase and the work under analysis: prepare stocks, run each batch, characterize each tier, record the as-run section. Set the hypotheses to `frozen` in the README. Offer the design → analysis change (**Project admin**) only when the exit review (**Project admin**) passes.

After the work, `method/log.md` records every deviation (**Experiment log**); section 9 only points to it. Do not edit sections 1 to 8 afterwards; that is how a post-hoc change gets labelled.

Discussion mode: argue the strongest alternative design before settling; push back on weak controls, a replicate at the wrong level, and characterization chosen after the numbers.

**Reply:** the design path, the units added to `method/samples.csv`, what is short or unknown, the tasks added, and the open decisions.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start experimental-design`). Items: file (a glob with a match), cmd (exit 0), decision (a new decisions.tsv row).

- file docs/reports/*/method/design.md
- file docs/reports/*/method/resources.md
- file docs/reports/*/method/samples.csv
- decision
