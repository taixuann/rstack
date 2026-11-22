# Phase: write

**Entry check.** Analysis exit passed: every result has a disposition and the package exists. Formerly `ready-for-publish`. The user writes every paragraph; the assistant never writes manuscript prose.

**Playbooks, in order.**
1. Paper preparation (target and evidence report, one report per topic; gate `report-approved`)
2. Paper writing (guided by questions, main points to paragraphs; gate `draft-ready`)
3. Paper critique (independent critic modes, findings ledger; gate `critique-passed`)
4. Presentation (slides from the same report)
5. Peer review (a referee pass on the finished draft)

**Reads and writes.** Reads `analysis/`, `docs/reports/<question>/`. Writes `docs/rstack/writing/<piece>/` and `docs/reports/<question>/` (the evidence files), `docs/writing/<piece>/` and `docs/presentation/<piece>/` (the user), `docs/rstack/tasks.md` (through project-admin). Gates move only through `scripts/writing.py gate`. Rows are in `layout.md`; a playbook states its own subset.

**Starting tasks.** Pick the piece and venue. Build and approve the report. Write the draft. Pass the number check. Run the critique modes and clear blocking findings. Peer-review pass. Submit. Tailor them to the project.

**Exit gate angles.** Each is one adversary for `interrogate` (see `admin/exit-review.md`).

1. **Claim to evidence.** Every claim in the manuscript (`docs/writing/<piece>/`) points to a result in `analysis/` or a verified reference.
2. **Numbers match.** Sample sizes, endpoints, and statistics are identical in abstract, results, tables, and figures.
3. **Citations resolve.** Every reference exists and supports its sentence. None come from memory.
4. **Truthful figures.** Individual points and uncertainty are shown, axes are honest, and captions state n.
5. **Limitations.** Stated beside the claims they limit.
6. **Statements.** Ethics, data availability, and author contributions are present and true.
7. **Referee view.** A `peer-review` pass found no blocking issue left.

**Done when.** Submitted, with the critique passed.

**Skills.** Bundled (in rstack): `number-check`, `academic-humanizer`, `venue-templates`, `scientific-slides`, `citation-management`, `peer-review`, `scientific-critical-thinking`, `principle-the-user-writes-the-prose`, `principle-report-before-prose`, `principle-fixes-need-a-yes`, `principle-ask-do-not-fill`. External (install separately; use only if installed, and `setup-research` lists what is missing): `doc-coauthoring` (Anthropic), a LaTeX toolchain for `main.tex`.
