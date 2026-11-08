# Literature review (Zotero loop)

State: explore. Output: `docs/rstack/explore/03_literature-map.md` (themes, search log, gap), `docs/literature-review/references.yaml`, `docs/rstack/explore/inquiry.md` and `claims.md`, per-paper snapshots in `docs/literature-review/papers/<cite>/`, and per-paper analyses in `docs/literature-review/papers/<cite>/`. Runs after the **init** interview and repeats as the user reads more papers.

**Two loops.** Scope first, then deepen. Steps 1 to 3 are the scope loop and need no blind analysis or critic. Steps 4 onward are the deepen loop and start only when the scope check passes (the question is narrow, a gap is named, feasibility is judged). If the aims change, run `interrogate` again and scope again.

1. Read `00_interview.md`, `01_context.md`, and `02_aims-and-milestones.md`. The search serves the work packages they name. If they do not exist yet, run **Proposal intake** first.
   **Scope.** Run `interrogate` in interview mode on the proposal and write down the aims, what the user already understands, and the gaps. Then do a quick scoping search (`paper-lookup`, `openalex-database`): is the topic already reviewed, is there enough literature, which terms do papers use. Ask the supervisor about anything the papers cannot settle. Learning runs beside this playbook.
2. **Register the collection.** Record the Zotero collection (name and key) at the top of `docs/literature-review/references.yaml` (template in `references/references.template.yaml`). The user keeps all papers in one flat collection and highlights by colour: purple interpretation and context, orange methods, green results, blue mechanism, red unclear or doubtful, yellow general notes. The `zotero-cli` skill documents the command line.
3. **Scope check.** Show the narrowed question, the gap, and feasibility. The user confirms before the deepen loop starts.
4. **Read.** The user reads the key papers the narrowed question needs in Zotero and highlights by colour. Snapshot the annotations with `scripts/zotero_snapshot.py` into each paper's folder.
5. **Ask and answer** with **Inquiry**: align the user's reading with the assistant's, interrogate both, extend beyond the papers, then search. The user's questions drive what is searched, answered, and claimed.
6. **Find more.** Discovery only suggests candidates. Every candidate is resolved to a DOI and approved by the user before it enters Zotero.
   - `paper-lookup` and `openalex-database` for targeted searches.
   - `deep-research` for a landscape of a domain the user is new to. Treat its report as an unverified lead list.
   - HyperResearch only on request, run from `~/academic-space`: `/opt/miniconda3/envs/core/bin/hyperresearch scholar search "<query>" --scope papers -j` for citation-ranked results. The full pipeline is slow and heavy.
7. **Map.** Write `03_literature-map.md`: themes, conflicts between studies, search log, and the gap, with links to `docs/literature-review/cross-papers/` and the papers by cite. `sources` audits whether a claim matches its source. `citation-management` (from `claude-scientific-writer`) verifies every reference resolves.
8. Run `scripts/check_references.py docs/literature-review/references.yaml` and fix what it reports. Then continue with **Proposal synthesis**.

**Reply:** papers ingested and their verdicts, questions answered and still open, the gap, and what the user must decide.
