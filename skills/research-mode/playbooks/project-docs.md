### Project docs

Write or refresh a project's `README.md` and `AGENTS.md` from the templates in `references/`. Used by Scaffold, and at every state change.

1. Read the existing files. Never overwrite facts the user wrote.
2. Fill only what is known: from the user, from `data/raw/` metadata, from files you read. Everything else stays `TODO: unknown`. Never invent devices, subject counts, rates, or citations.
3. README is the front page, kept short (**principle-minimize-reader-load**). It holds the state header, the current state's tasks, one block per research question, and the State history. No folder map, install, licence, or changelog sections.
   - Each question owns its decision, its hypotheses with status (candidate, frozen, supported, rejected) and design link, and its evidence (data, accepted results, reproduce command).
   - Shared data: put the detailed inventory in `data/raw/README.md` and link it from each question.
4. AGENTS.md is the stable operating contract. It changes rarely. Do not put results or tasks in it.
5. Tasks: seed the list from the state's defaults below, then tailor it to the project's scope (explore does this through the scope interview). Tick them as they finish.
6. State change: confirm the exit check with the user, set `state` and `updated`, add the State history row, move the finished task list to `docs/rstack/<old-state>/tasks.md`, seed the new state's tasks, and create `docs/rstack/<new-state>/`. Moving backwards is allowed; log the reason.
7. Read both files back and report what is still `TODO`.

**States, default tasks, and exit checks**

| State | Default tasks | Exit check |
|---|---|---|
| explore | Define scope and search terms. Search and screen. Read and synthesize into `docs/wiki/`. Name the gap. Write questions and candidate hypotheses. | Synthesis exists, gap named, each question has candidate hypotheses |
| design | Freeze each question's hypotheses. Choose the design. Justify sample size. Write the analysis plan. Attack the design with `interrogate`. Plan data intake and ethics. | Design note and analysis plan frozen |
| progressing | Intake data with provenance. Run the planned analyses per question. Run sensitivity checks. Accept or reject each result. Rerun the pipeline clean. | Planned analyses done, every result dispositioned, rerun clean |
| ready-for-publish | Draft the manuscript. Verify numbers and citations. Peer-review pass. Package results. Submit. | Submitted |
| closed | Record the reason (published or abandoned). Archive the package. | none |

**Skills per state.** Bundled means in rstack. External means install it separately (for example from K-Dense's `scientific-agent-skills`); use it only if installed.

| State | Bundled | External |
|---|---|---|
| explore | `literature-review`, `paper-lookup`, `research-lookup`, `openalex-database`, `pyzotero`, `zotero-local`, `liteparse`, `brainstorming`, `hypotheses`, `scientific-critical-thinking`, `sources`, `citations`, `interrogate` | `scientific-brainstorming`, `scholar-evaluation` |
| design | `experimental-design`, `statistical-power`, `statistical-conventions`, `hypotheses`, `arena`, `interrogate` | `lab-hardware-cad`, `analytical-method-validation`, `iso-standards-readiness`, `what-if-oracle` |
| progressing | `analysis-report`, `figures`, `scientific-visualization`, `reproduce`, `execution-hygiene`, `compute`, `swarm` | `exploratory-data-analysis`, `statistical-analysis`, `uncertainty-and-units`, `neurokit2` (ECG and biosignals) |
| ready-for-publish | `paper-writing`, `ml-paper-writing`, `schematics`, `scientific-slides`, `pptx-posters`, `latex-posters`, `peer-review`, `citations`, `export` | `venue-templates`, `scientific-writing` |
| closed | `export`, `sources` | none |

**Reply:** what changed, what remains unknown, and the questions you need answered to fill it.
