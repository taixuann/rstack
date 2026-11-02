### Project docs

Write or refresh a project's `README.md`, `AGENTS.md`, and `CLAUDE.md` from the templates in `references/`. Used by Scaffold, and at every state change.

1. Read the existing files. Never overwrite facts the user wrote.
2. Fill only what is known: from the user, from `data/raw/` metadata, from files you read. Everything else stays `TODO: unknown`. Never invent devices, subject counts, rates, or citations.
3. README is the front page and map of content, kept short (**principle-minimize-reader-load**). It holds the state header, the task block, a Contents list of links to each stage's documents, questions grouped by work package, and the State history. No folder tree, install, licence, or changelog sections.
   - The task block is generated. Edit `docs/rstack/<state>/tasks.md`, then run `scripts/sync_readme_tasks.py <project>`.
   - Name work packages and questions in plain words and sentences. No codes like WP1 or Q1.1.
   - Each question owns its decision, its hypotheses with status (candidate, frozen, supported, rejected) and design link, and its evidence (data, accepted results, reproduce command).
   - Shared data: put the detailed inventory in `data/raw/README.md` and link it from each question.
4. AGENTS.md is the stable operating contract. It changes rarely. Do not put results or tasks in it.
   - `CLAUDE.md` is a stub from `references/CLAUDE.template.md` that imports `AGENTS.md` (`@AGENTS.md`). Claude Code reads `CLAUDE.md` and not `AGENTS.md`; Codex and other tools read `AGENTS.md`. Keep one source of truth: never copy rules into `CLAUDE.md`.
5. Tasks live in `docs/rstack/<state>/tasks.md`. Seed it from the state's defaults below, then tailor it to the project's scope (explore does this through the Proposal intake playbook). Tick them as they finish, then sync the README.
6. State change: run the **State review** playbook for the current state and clear its blocking tasks, confirm the exit check with the user, set `state` and `updated`, add the State history row, create `docs/rstack/<new-state>/` with a seeded `tasks.md`, add the new state's line to Contents, and sync the README. The old state's `tasks.md` stays as its record. Moving backwards is allowed; log the reason.
7. Read both files back and report what is still `TODO`.

**States, default tasks, and exit checks**

| State | Default tasks | Exit check |
|---|---|---|
| explore | Run the project interview. Write context, aims, and milestones. Register the Zotero collection, ingest and review papers, and run the inquiry. Map the literature and name the gap. Write questions and hypotheses per work package. Outline methods and feasibility. | Proposal chain holds (`interrogate`), `check_references.py` passes, each question has candidate hypotheses |
| design | Freeze each question's hypotheses. Choose the design. Justify sample size. Write the analysis plan. Attack the design with `interrogate`. Plan data intake and ethics. | Design note and analysis plan frozen |
| progressing | Intake data with provenance. Run the planned analyses per question. Run sensitivity checks. Accept or reject each result. Rerun the pipeline clean. | Planned analyses done, every result dispositioned, rerun clean |
| ready-for-publish | Draft the manuscript. Verify numbers and citations. Peer-review pass. Package results. Submit. | Submitted |
| closed | Record the reason (published or abandoned). Archive the package. | none |

**Skills per state.** Bundled means in rstack. External means install it separately (for example from `claude-scientific-writer` or K-Dense's `scientific-agent-skills`); use it only if installed.

| State | Bundled | External |
|---|---|---|
| explore | `literature-review`, `paper-lookup`, `research-lookup`, `openalex-database`, `liteparse`, `zotero-cli`, `brainstorming`, `hypotheses`, `scientific-critical-thinking`, `sources`, `interrogate` | `citation-management`, `scholar-evaluation`, `deep-research` |
| design | `experimental-design`, `statistical-power`, `hypotheses`, `what-if-oracle`, `arena`, `interrogate` | `lab-hardware-cad`, `analytical-method-validation`, `iso-standards-readiness` |
| progressing | `exploratory-data-analysis`, `statistical-analysis`, `uncertainty-and-units`, `analysis-report`, `figures`, `scientific-visualization`, `reproduce`, `swarm` | `neurokit2` (ECG and biosignals) |
| ready-for-publish | `scientific-slides`, `pptx-posters`, `latex-posters`, `peer-review`, `export` | `scientific-writing`, `scientific-schematics`, `citation-management`, `venue-templates`, `infographics` |
| closed | `export`, `sources` | none |

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
