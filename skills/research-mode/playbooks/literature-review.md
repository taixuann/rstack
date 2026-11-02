# Literature review (Zotero loop)

State: explore. Output: `docs/rstack/explore/03_literature-map.md` (themes, search log, gap), `docs/rstack/references.yaml`, `docs/rstack/explore/inquiry.md` and `claims.md`, paper snapshots in `docs/raw/papers/`, and notes in `docs/wiki/` via `karpathy-llm-wiki`. Runs after **Proposal intake** and repeats as the user reads more papers.

1. Read `00_interview.md`, `01_context.md`, and `02_aims-and-milestones.md`. The search serves the work packages they name. If they do not exist yet, run **Proposal intake** first.
2. **Register the collection.** Record the Zotero collection (name and key) at the top of `docs/rstack/references.yaml` (template in `references/references.template.yaml`). The user keeps all papers in one flat collection and highlights by colour: purple interpretation and context, orange methods, green results, blue mechanism, red unclear or doubtful, yellow general notes. The `zotero-cli` skill documents the command line.
3. **Ingest** each paper the user has read with **Paper ingestion**. `swarm` can run one reader per paper.
4. **Ask and answer** with **Inquiry**: the user's questions drive what to search next, what to answer, and what becomes a claim.
5. **Find more.** Discovery only suggests candidates. Every candidate is resolved to a DOI and approved by the user before it enters Zotero.
   - `paper-lookup` and `openalex-database` for targeted searches.
   - `deep-research` for a landscape of a domain the user is new to. Treat its report as an unverified lead list.
   - HyperResearch only on request, run from `~/academic-space`: `/opt/miniconda3/envs/core/bin/hyperresearch scholar search "<query>" --scope papers -j` for citation-ranked results. The full pipeline is slow and heavy.
6. **Map.** Write `03_literature-map.md`: themes, conflicts between studies, search log, and the gap, with links to `docs/wiki/` and the papers by cite. `sources` audits whether a claim matches its source. `citation-management` (from `claude-scientific-writer`) verifies every reference resolves.
7. Run `scripts/check_references.py docs/rstack/references.yaml` and fix what it reports. Then continue with **Proposal synthesis**.

**Reply:** papers ingested and their verdicts, questions answered and still open, the gap, and what the user must decide.
