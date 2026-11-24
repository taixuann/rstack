# Phase: explore

**Entry check.** A new project starts here. The **init** skill has run; `README.md` says `state: explore`.

**Playbooks, in order.**
1. Inquiry (before any search: wiki, interview, brainstorm; then the standard inquiry)
2. Literature review (runs `/hyperresearch` on the inquiry, light then full; symlinks the report)
3. Inquiry again on the papers the user chose and read
4. Report bootstrap (last: context, aims and literature into questions and methods)

**Reads and writes.** Reads `docs/inputs/`, `docs/literature-review/`. Writes `docs/literature-review/` (symlinks to HyperResearch reports; the rest is yours), `docs/rstack/`, `docs/rstack/tasks.md` (through project-admin). Rows are in `layout.md`; a playbook states its own subset.

**Starting tasks.** Run the project interview. Write context, aims and milestones. Register the Zotero collection, ingest and review papers, and run the inquiry. Map the literature and name the gap. Write questions and hypotheses per work package. Outline methods and feasibility. Tailor them to the project.

**Exit gate angles.** Each is one adversary for `interrogate` (see `admin/exit-review.md`).

A finding survives only if it names the file and the missing or weak item.

1. **Chain.** Does the problem exist (evidence cited)? Does the gap follow from papers marked `read`? Does each question address the gap? Can the candidate methods answer it? Would the outcomes fill the gap?
2. **Scope against time.** Work packages times duration against the months available. What is the smallest version that still meets the first milestone? Which parts depend on each other?
3. **Unknowns have owners.** Every `TODO: unknown` has an owner (the user or the supervisor) and a due point, or is dropped.
4. **Evidence quality.** Every claim in `01` to `05` traces to a `references.yaml` entry. HyperResearch reports are leads, not read papers.
5. **Gates outside the work.** If people are recorded, are consent and an approved plan done or scheduled? Is equipment or access confirmed or a listed risk?
6. **Learning gap.** Terms and mechanisms the user flagged as unclear each have a note in `docs/literature-review/cross-papers/` or a task.
7. **Key papers reviewed.** Each paper the proposal leans on has a `PASS` review, or is marked `NO_REVIEW` and is not the sole support for any claim.
8. **Questions resolved.** Every item in `docs/rstack/d-inquiry/inquiry.md` is answered with a cite, assigned to the supervisor, or queued for search. No claim in `claims.md` rests on an unanswered item.
9. **Scope.** Was the question narrowed, with a gap and a feasibility judgement, before papers were analysed? If the aims changed, was the scope redone?
10. **Learning in sync.** The user's overview page has no open point without an owner. Lessons ingested since the last review are carried into `docs/rstack/`.
11. **Wiki is not literature.** Anything taken from `wiki/` is labelled as the user's own experience and is never the sole support of a claim about the literature.
12. **Searches recorded.** Each HyperResearch run is linked in `docs/literature-review/` (a working symlink) and logged in `03_literature-map.md` with its tag, tier and date.
13. **Reports opened** (**Report bootstrap**). Every question has `docs/reports/<question>/README.md` with its intention, hypotheses, what would refute each, and the plan, and `fundamental/README.md` listing the background and its checks.

**Done when.** The proposal chain holds (`interrogate`), `scripts/check_references.py` passes, each question has candidate hypotheses and an opened `docs/reports/<question>/README.md`.

**Skills.** Bundled (in rstack): `liteparse`, `zotero-cli`, `brainstorming`, `hypotheses`, `scientific-critical-thinking`, `sources`, `interrogate`, `obsidian-notes`. External (install separately; use only if installed, and `setup-research` lists what is missing): `/hyperresearch` (CLI and skills, installed in `~/academic-space`), `scholar-evaluation`.
