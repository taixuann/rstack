### Protocol wiki

Write or fill pages of the lab's `wiki/` (reusable protocol knowledge: workflows, resources, equipment) with `doc-coauthoring`. Read `wiki/SCHEMA.md` first. Its rules (no invented parameters, source marks, front matter, structure) outrank this playbook. `doc-coauthoring` is an Anthropic skill the user installs; without it, run the same steps by hand.

Two directions, same steps:
- **Wiki first.** The user feeds protocols and experience. The pages are built and filled, and **Experimental design** later copies them into an experiment note.
- **Design first.** A frozen or run experiment note exists. Ingest it into the wiki as a workflow and its resources.

Skills for this playbook: `doc-coauthoring`, `interrogate` (interview mode), `brainstorming`. Principles: **principle-sources-not-memory**, **principle-raw-data-is-read-only**.

1. **Intake.** Save what arrives to `wiki/raw/<domain>/` as received, with source and date. Never edit it. Read `wiki/SCHEMA.md`, `wiki/index.md` and the target page.
2. **Question sweep.** Walk the target page step by step. For every step and every quantity ask: the value and unit, where it comes from, what it depends on (temperature, lot, instrument, order), the tolerance, what to record, the failure criterion, and what comes before, after or alongside it. Put every gap down as `TODO: unknown` with who can answer. Show the whole list grouped by step. Guess nothing.
3. **Fill, one section at a time, with `doc-coauthoring`.** Ask for the missing context, brainstorm, curate, then draft only what the user said. Mark each source as `wiki/SCHEMA.md` says. A number you derived is marked for the user to check against the bottle label or the instrument.
4. **Reader test.** A fresh agent reads only the page and its resources and answers the questions a bench user would ask. Fix every answer it got wrong or could not find.
5. **Consistency.** Quantities agree across pages (a recipe and its concentration). Every chemical and instrument a workflow uses is in the project's resources or in `wiki/equipment/`. Update `index.md` and `log.md`.
6. **Status.** A page is a stub or a draft. Only the user sets it to reviewed.

**Design first, in addition:** take sections 2 to 6 of the note. Split them into a workflow and its resources. Ask the user to confirm each quantity before it is written. Take values from the note's sources, never from run data.

Commit in the wiki repo only. Nothing leaves the machine.

**Reply:** the pages changed, the unknowns still open, the reader-test result, and what you need from the user.
