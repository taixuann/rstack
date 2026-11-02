# Literature review (Zotero loop)

State: explore. Output: `docs/rstack/explore/03_literature-map.md` (themes, search log, gap), `docs/rstack/references.yaml`, paper snapshots in `docs/raw/papers/`, notes in `docs/wiki/` via `karpathy-llm-wiki`. Runs after **Proposal intake** and repeats as the user reads more papers.

1. Read `00_interview.md`, `01_context.md`, and `02_aims-and-milestones.md`. The search serves the work packages they name. If they do not exist yet, run **Proposal intake** first.
2. **Register the collection.** Record the Zotero collection (name and key) at the top of `docs/rstack/references.yaml` (template in `references/references.template.yaml`). The user keeps all papers in one flat collection.
3. **Snapshot.** The `zotero-cli` skill documents the Zotero command line. For each new item run `scripts/zotero_snapshot.py <key> --out docs/raw/papers`, or the whole collection with `--collection <key>`. Add each paper to `references.yaml` with `status: snapshotted`. `swarm` fans out one `paper-reader` agent per paper.
4. **Read by colour.** Zotero highlight colours carry meaning: purple interpretation and context, orange methods, green results, blue mechanism, red unclear or doubtful, yellow general notes. The `paper-reader` agent writes the wiki page (Context, Methods, Results, Mechanism, Open questions) and drafts `used_in`, `parts`, and `why` for the user to confirm. Set `status: read` only for papers actually read. Mark abstract-only.
5. **Judge.** `scientific-critical-thinking` on orange (methods) and on any strong claim. Turn blue and red items and purple comments phrased as questions into open questions (`brainstorming`).
6. **Find more.** Discovery only suggests candidates. Every candidate is resolved to a DOI and approved by the user before it enters Zotero.
   - `paper-lookup` and `openalex-database` for targeted searches.
   - `deep-research` for a landscape of a domain the user is new to. Treat its report as an unverified lead list.
   - HyperResearch only on request: `/opt/miniconda3/envs/core/bin/hyperresearch scholar search "<query>" --scope papers -j` for citation-ranked results. The full pipeline is slow and heavy.
7. **Map.** Write `03_literature-map.md`: themes, conflicts between studies, search log, and the gap, with links to `docs/wiki/` and the papers by cite. `sources` audits whether a claim matches its source. `citation-management` (from `claude-scientific-writer`) verifies every reference resolves.
8. Run `scripts/check_references.py docs/rstack/references.yaml` and fix what it reports. Then continue with **Proposal synthesis**.

**Reply:** papers added and read, the gap, and open questions the user must decide.
