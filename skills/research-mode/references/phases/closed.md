# Phase: closed

**Entry check.** The write phase ended in submission, or the project is abandoned.

**Playbooks, in order.**
1. Reviewer response (after submission: answer reviewers, edit the manuscript, quote the new text with its location)

**Reads and writes.** Reads everything. Writes `docs/writing/<piece>/` (the user), `docs/rstack/closed/`, `docs/rstack/tasks.md` (through project-admin). Rows are in `layout.md`; a playbook states its own subset.

**Starting tasks.** Record the reason (published or abandoned). Archive the package. Answer reviewers if a decision arrives. Tailor them to the project.

**Exit gate angles.** Each is one adversary for `interrogate` (see `admin/exit-review.md`).

1. **Handover.** A new person can rerun the pipeline from `README.md`, `AGENTS.md`, `CLAUDE.md`, and `docs/rstack/` alone.
2. **Package.** Inputs, code, accepted outputs, and provenance are packaged with reproduction steps (`export`).
3. **Data and licences.** Where the data lives, who may use it, and under what licence or consent are written down.
4. **Reason.** The closing reason (published, submitted, abandoned) is recorded with the date.
5. **Open issues.** Unfinished work and known problems are listed for whoever continues.

**Done when.** Reason recorded; handover rerun passes.

**Skills.** Bundled (in rstack): `sources`. External (install separately; use only if installed, and `setup-research` lists what is missing): none.
