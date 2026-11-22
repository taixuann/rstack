# Literature review (HyperResearch)

Phase: explore. Runs `/hyperresearch` on the questions **Inquiry** wrote down, and links the report into the project. It does not search, rank or read papers itself. Reads `docs/rstack/inquiry/inquiry.md` and `inquiry-search.md`. Writes `docs/literature-review/<date>_<slug>.md` (a symlink) and `docs/literature-review/references.yaml`. HyperResearch writes everything else in its own vault. Needs the external tool `hyperresearch` (see `setup-research`).

A report from HyperResearch is a lead. Nothing in it is used as a claim until a paper the user read confirms it (the understanding ladder, **Inquiry**).

1. **Prompt.** From the needs-search items in `inquiry-search.md`, write one prompt in the user's words: the questions, why they matter, what is already read (cites from `references.yaml`), and what a good answer must contain. Show it and wait for the user's yes before anything runs; the run costs time and money.
2. **Tier.** Light first, to check scope and terms (about 30 minutes). Full only for the gaps that remain after the light report. Dissertation only when the user asks. `hyperresearch profile list -j` shows the installed scale gear.
3. **Run.** Run `/hyperresearch <prompt>` from `~/academic-space`, where its vault is. Follow its own skill files; do not reimplement them. Read the final report path with `/opt/miniconda3/envs/core/bin/hyperresearch run status -j`, and check `run verify <vault_tag> -j` passes. A blocked fetch (login, captcha) goes to the user.
4. **Link.** Symlink the final report into the project, in this folder only: `docs/literature-review/<YYYY-MM-DD>_<slug>.md` pointing at `research/notes/final_report_<vault_tag>.md` (absolute path). Never copy it into the project and never edit it. Put a row in `docs/literature-review/references.yaml` or at the top of the next `inquiry.md` section: vault tag, tier, date, prompt file.
5. **Candidates.** List the papers the report names that matter for the questions. Resolve each to a DOI. The user decides which go into Zotero. Nothing enters Zotero unapproved.
6. **Back to inquiry.** The user reads the chosen papers in Zotero and highlights by colour (`zotero-cli` skill, `scripts/zotero_snapshot.py`). Then **Inquiry** aligns the reading and updates the questions. Repeat from step 1 only if a new gap needs a new search.
7. **Map.** When the gaps are answered, write `docs/rstack/explore/03_literature-map.md`: themes, conflicts between studies, the search log (each run: tag, tier, date), and the gap, with links to `docs/literature-review/cross-papers/` and the papers by cite. `sources` audits whether a claim matches its source. `citation-management` verifies every reference resolves.
8. Run `scripts/check_references.py docs/literature-review/references.yaml` and fix what it reports. Then continue with **Report bootstrap**.

**Reply:** the run (tag, tier), the report link, candidate papers waiting for your decision, and what is still open.
