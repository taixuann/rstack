# Phase: design

**Entry check.** Explore exit passed: questions and candidate hypotheses exist.

**Playbooks, in order.**
1. Inquiry on each experiment (reads the wiki, interview, brainstorm, interrogate)
2. Experimental design (the self-contained note, resources, preparation, protocol)
3. Experiment log (continues in the analysis phase while the experiments run) (as the experiments run: what was done, as run, against the design; the report later cites it)

**Reads and writes.** Reads `docs/rstack/`; the wiki is read only by Inquiry (via `wiki/CLAUDE.md`), and the design note copies what it needs. Writes `docs/reports/<question>/` (`method/design.md`, `method/resources.md`, `method/samples.csv`, `method/log.md`), `docs/rstack/d-inquiry/inquiry-<experiment>-wiki.md` (Inquiry's notes), `docs/rstack/tasks.md` (through project-admin). Rows are in `layout.md`; a playbook states its own subset.

**Starting tasks.** Freeze each question's hypotheses. Choose the design. Justify sample size. Write the analysis plan. Attack the design with `interrogate`. Plan data intake and ethics. Tailor them to the project.

**Exit gate angles.** Each is one adversary for `interrogate` (see `admin/exit-review.md`).

1. **Falsifiable.** Each hypothesis is a testable statement with the result that would refute it, frozen before any outcome data is examined.
2. **Controls and confounders.** What else could produce the effect (for a device: skin preparation, motion, contact pressure, temperature, operator)? Which are controlled, randomized, or recorded?
3. **Repeatability.** Replicates per condition, repeat measurements, calibration of the reference instrument, and how measurement uncertainty is reported.
4. **Pilot first.** The smallest end-to-end run is planned as its own experiment (type pilot) before the full run, with what it must show.
5. **Pre-stated analysis.** Comparisons, exclusions, and how results are shown are written before data. Exploratory and confirmatory work are separated.
6. **Ethics and data.** Consent and the approved plan exist. Raw data is immutable, identifiers are kept out, and storage is decided.
7. **Fallbacks.** Each major risk has a fallback and a trigger for using it.
8. **Materials and access.** Every item an experiment needs is in `method/resources.md` and in enough amount, not expired. Every stock has a recipe and a step that uses it. Each equipment booking fits its limit.
9. **Preparation.** The preparation plan names what depends on what, what waits, and what runs in parallel. A step with no owner or no time is a finding.
10. **Characterization chosen in advance.** The tiers and the rule that picks the units are written before any result, and each technique names the claim it supports.
11. **Self-contained.** A reader with only the note can run the experiment: materials, equipment and procedure are written out with every quantity's value, unit and source, there is no wiki path or link, and no `TODO: unknown` remains that the experiment needs.

**Done when.** The design note and analysis plan are frozen (`verify_playbook.py` for experimental-design passes).

**Skills.** Bundled (in rstack): `experimental-design`, `statistical-power`, `hypotheses`, `what-if-oracle`, `arena`, `interrogate`. External (install separately; use only if installed, and `setup-research` lists what is missing): `lab-hardware-cad`, `analytical-method-validation`, `iso-standards-readiness`.
