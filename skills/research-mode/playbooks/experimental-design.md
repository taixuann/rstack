### Experimental design

State: design. Output: `docs/rstack/design/` with a `README.md` (the map), `resources.md` (what the lab has), one note per experiment (`e01_<slug>.md`), and `docs/rstack/samples.csv` (one row per unit). Each experiment note is the contract that **Analysis plan** and the bench work use. Nothing is made or measured here.

Templates are in `templates/design/`. Copy them; never invent the fields. The `experimental-design` skill is the statistics engine (design type, randomisation, replication, DOE matrices). This playbook adds the bench reality it does not cover: materials, preparation, equipment and what gets measured.

Skills for this playbook: `hypotheses` (falsifiable hypotheses, each with the result that refutes it), `brainstorming` (choosing between directions), `experimental-design` (the design and its seeded scripts), `statistical-power` (subject comparisons only), `uncertainty-and-units` (measurement uncertainty), `interrogate`, `arena` (two or more plausible designs), `doc-coauthoring` (filling wiki gaps, through **Protocol wiki**). Principles: **principle-question-first**, **principle-exploratory-vs-confirmatory**, **principle-attack-the-premise**.

**The loop, per experiment**

1. **Find what exists.** Read the README questions and hypotheses, earlier design notes and `resources.md`. If the research-space has a `wiki/` folder (above `projects/`), read it next: `wiki/index.md`, the project's `playbooks/<project>/README.md`, the workflow for this experiment, its `resources/` and the shared `wiki/equipment/`. Copy what the note needs into the note itself, in full, with the wiki's source marks, and write at its top `Wiki source: <path> @ <commit>`. The note must be self-contained: someone reading only the note can run the experiment. If `resources.md` has `TODO: unknown` rows the experiment needs, ask for them now. If the experiment repeats an earlier one, say why.
   **No wiki page, or gaps in it.** Run the **Protocol wiki** playbook with the user to fill the page first, then copy it. Or, if the user wants the design first, write the note in full and offer **Protocol wiki** (design first) after the freeze.
   **Question sweep.** Before step 9, go through sections 3 to 6 step by step. Every step and every quantity has a value, a unit, a source, a tolerance, what to record and a failure criterion. Anything missing is a `TODO: unknown` the user answers. Do not freeze with one left, unless the user accepts it as a task.
2. **Purpose.** Fill section 1: question, the decision it serves, the type (baseline or repeat, sweep, confirmation, pilot), a falsifiable hypothesis with what refutes it, one primary endpoint. A sweep changes one number of a known recipe; a repeat changes nothing and tests repeatability. Say which. Add a row to `design/README.md`.
3. **Design.** Fill section 2 with the `experimental-design` skill: the unit and the level of a true replicate, factors, controls that differ in one thing, replicates, blocking of nuisance factors, a seeded run order. For device and materials work plan replicates and repeat measurements, not a power calculation. Argue the strongest alternative design before settling. Write the unit rows to `samples.csv` with status planned.
4. **Materials.** Fill section 3 from `resources.md`: amount per unit, overage, total, and every stock solution with concentration, volume and the step that uses it. Anything short or expired becomes a task.
5. **Preparation plan.** Fill section 4. List every step with what it depends on, its hands-on time and its waiting time. Mark what runs in parallel (wash and dry glassware while weighing) and start the longest dependent chain first. Write the run sheet in start order. Check each equipment booking against `resources.md`.
6. **Protocol.** Fill section 5 so someone else could run it: settings, what to record, failure criteria, naming of units and files.
7. **Characterization tiers.** Fill section 6 from the menu in `resources.md`: cheap for every unit, mid and expensive for a subset, chosen by a rule written now. Name the claim each technique supports. A mechanism claim with no technique that measures the mechanism stays an interpretation.
8. **Interrogate.** Run `interrogate` on the note with the angles of `references/state-gates/design.md`. Fix what survives. A pilot is the smallest end-to-end run; plan it first with the **Prototype** playbook and write what it must show.
9. **Freeze.** The note is now a snapshot: do not edit sections 1 to 7 afterwards. Through **Task tracking**, add a goal for the experiment under the design phase and the work under progressing: prepare stocks, run each batch, characterize each tier, record the as-run section. Set the hypotheses to `frozen` in the README and `design/README.md` status to `frozen`. Offer the design → progressing change (**Project docs**) only when **State review** passes.

After the work, section 8 (as run) records every deviation. Do not edit sections 1 to 7 afterwards; that is how a post-hoc change gets labelled.

Discussion mode: argue the strongest alternative design before settling; push back on weak controls, a replicate at the wrong level, and characterization chosen after the numbers.

**Reply:** the note path, the units added to `samples.csv`, what is short or unknown, the tasks added, and the open decisions.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start experimental-design`). Items: file (a glob with a match), cmd (exit 0), decision (a new decisions.tsv row).

- file docs/rstack/design/README.md
- file docs/rstack/design/e[0-9]*.md
- file docs/rstack/samples.csv
- decision
