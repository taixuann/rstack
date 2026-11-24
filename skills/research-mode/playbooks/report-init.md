### Report init

Phase: explore, last (and in design, for a new question or setup report). Turn an unclear goal into a scoped `docs/reports/<question>/` folder tailored to what the work actually needs, then hand follow-up tasks and records to **Project admin**. This playbook writes documents only. It never touches `data/raw/` or `analysis/`.

Specific principles: `principle-question-first`, `principle-subtract-before-you-add`, `principle-ask-do-not-fill`. Skills: `interrogate`, `brainstorming`, `hypotheses`, `what-if-oracle` (for rough feasibility and risks), `learn-mode`, `scientific-critical-thinking`.

| File | Holds |
|---|---|
| `docs/reports/<question>/README.md` | Intention (`[user]`), selected report scope (`fundamental/`, `method/`, `analysis/`, `results/` or `N/A`), hypotheses, and status |
| `docs/reports/<question>/fundamental/README.md` | Created only when `fundamental/` is needed |

1. **Interview and frame.** Run `interrogate` (interview mode) and `brainstorming` with the user — offering quick-select options or freeform answers — to classify the report and decide what it actually needs:
   - What is the specific **Objective** of this report, what decision does it support, and what counts as success? (Do not leave Objective vague; downstream design and procedures anchor to it.)
   - Does it need `fundamental/` (background theory/concepts via `learn-mode`)?
   - Does it need `method/` — and if so, which parts: sample preparation, hardware setup, software setup, or experimental procedure?
   - Does it need `analysis/` and `results/` (or is it purely a hardware/software setup report)?
2. **Inquiry loop (`qmd`).** Query the project collection (`-c <project>`) via **Inquiry** to check what already exists. Only query `-c wiki` when the report includes method, procedure, hardware, or software setup (label wiki items `[user]` or `[studies]`). If scope or requirements are still unclear, loop back to step 1 until settled.
3. **Open the report folder.** Ask the user for a short slug (`<question>`, e.g. "setup-4-probe-measurement"); never overwrite an existing folder. Create `docs/reports/<question>/README.md` from `templates/report/README.md`. Fill Intention in the user's own words (`[user]`); mark unneeded sections `N/A`.
4. **Create only needed sub-areas.**
   - If `fundamental/` is needed: create `fundamental/README.md` from `templates/report/fundamental/README.md`, list required concepts, and point learning work to `learn-mode` (`docs/inputs/` → `docs/understanding/`).
   - If `method/` is needed: note the required building blocks (sample, hardware, software, procedure) and hand off to **Experimental design** when entering `design`.
   - If `hypotheses` / `experimental-design` apply (research/experiment reports): draft falsifiable hypotheses (citing `references.yaml` / `claims.md`) and rough feasibility (samples, repeats, time, consent/ethics).
5. **Hand off to Project admin.** Run **Project admin** (Tasks + Keeping records) to turn the needed work (setup, purchases, `learn-mode` topics, design, analysis) into concrete tasks in `docs/rstack/tasks.md`, update the project `README.md`, and log the decision in `docs/rstack/decisions.tsv`.
6. **Exit check (when closing explore or freezing a study report).** Assemble the chain (problem → gap → question → method → milestones), run `interrogate` on it and `scientific-critical-thinking` on the weakest claim, and offer the `explore → design` state change (**Project admin**).

**Reply:** the report folder opened, which sections are active vs `N/A`, tasks/decisions logged via **Project admin**, and what is still `TODO: unknown`.

## Done when

Checked by `scripts/verify_playbook.py` (start it with `start report-init question=<slug>`). Items: file (a glob with a match), decision (a new `decisions.tsv` row).

- file docs/reports/{question}/README.md
- decision
