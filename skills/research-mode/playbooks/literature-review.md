# Literature review (HyperResearch)

Phase: explore. Runs the full search-and-triage loop: consult internal memory (`Inquiry`), generate and stress-test questions (`brainstorming` + `interrogate`), write the inquiry brief, run `/hyperresearch` on the user's go-ahead, file the report with metadata and backlinks, and feed chosen papers into Zotero. Needs the external tool `hyperresearch` (see `setup-research`).

A report from HyperResearch is a lead. Nothing in it is used as a claim until a paper the user read confirms it (the understanding ladder, **Inquiry**).

Specific principles: `principle-sources-not-memory`, `principle-guard-the-context-window`. Tools/skills: `brainstorming`, `interrogate`, `liteparse` (for non-Zotero PDFs/docs), `sources` (to audit claims against passages), `zotero-cli`.

1. **Check internal memory first.** Run **Inquiry** (`qmd` on `-c <project>` and `-c wiki`) to see what the project and lab already know so the external search does not repeat it.
2. **Frame the inquiry brief.** Use `brainstorming` (named moves) and `interrogate` (interview mode) with the user to expand and sharpen the gaps, then write one brief at `docs/rstack/d-inquiry/<date>_<inquiry-problems>.md` (the questions, why they matter, what is already read from `references.yaml`, and what a good answer must contain).
3. **Wait for user approval.** Show `docs/rstack/d-inquiry/<date>_<inquiry-problems>.md` and the proposed `/hyperresearch` prompt. Wait for the user's explicit yes before anything runs; the run costs time and money.
4. **Tier and run.** Light first, to check scope and terms (about 30 minutes); full only for gaps that remain; dissertation only when asked (`hyperresearch profile list -j`). Run `/hyperresearch <prompt>` from `~/academic-space`, where its vault is. Read the final report path with `/opt/miniconda3/envs/core/bin/hyperresearch run status -j` and verify `run verify <vault_tag> -j` passes. A blocked fetch (login, captcha) goes to the user.
5. **File with metadata and backlinks.** Move `research/notes/final_report_<vault_tag>.md` to `docs/literature-review/hyperresearch-reports/<YYYY-MM-DD>_hyperresearch_<slug>.md`. Add front matter (`created`, `kind: report`, `tool: hyperresearch`, `source`, `status: lead`, `inquiry: <date>_<inquiry-problems>.md`) and a backlink to `docs/rstack/d-inquiry/<date>_<inquiry-problems>.md`; also link the filed report back inside that brief. Never edit the report body after filing.
6. **Candidates and Zotero.** List candidate papers from the report with resolved DOIs. The user decides which go into Zotero; nothing enters Zotero unapproved.
7. **Align, log, and verify.** The user reads chosen papers in Zotero and highlights by colour (`zotero-cli`, `scripts/zotero_snapshot.py`), then **Inquiry** aligns the reading and updates questions/claims. Run **Project admin** (Keeping records) to record the inquiry/search decision and chosen papers in `docs/rstack/decisions.tsv` (and update `docs/rstack/tasks.md` if follow-up tasks changed). Run `scripts/check_references.py docs/literature-review/references.yaml` and fix what it reports before moving to **Report init**.

**Reply:** the brief path, the run (tag, tier), the filed report path, candidate papers waiting for your decision, and what is still open.
