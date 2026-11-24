---
name: learn-mode
description: "Build and organise project-level understanding notes in docs/understanding/ and fundamental/: capture the user's raw words in docs/inputs/, shape notes with doc-coauthoring and obsidian-notes, keep Understanding Ladder labels, and refresh qmd so inquiry can retrieve them. Use for /learn-mode, 'build understanding', or recording what the user is learning in a project."
---

# Learn mode

Project-level knowledge building for `projects/res_<name>/`. Unlike `research-mode` (which drives phase gates and experiments) and `wiki-mode` (which stores cross-project lab knowledge in `wiki/`), `learn-mode` turns what you understand into clean, searchable project notes.

## Flow

1. **Check the index.** Read `docs/understanding/README.md` (or `docs/reports/<question>/fundamental/README.md` when learning background for a single question). If `qmd` is available, query `-c <project>` first to avoid duplicating an existing note.
2. **Capture raw words first.** Put the user's spoken or written understanding into `docs/inputs/<date>_understanding_<slug>.md` with standard input front matter (`created`, `kind: understanding`, `voice: user`, `source`, `topic`, `report`, `confirmed`). Never edit the body of `docs/inputs/` files.
3. **Co-author the structure.** Use `doc-coauthoring` (context gathering → clarifying questions → section-by-section refinement → fresh-reader check) to shape one note per topic in `docs/understanding/`.
4. **Format for Obsidian and the ladder.** Follow `obsidian-notes`:
   - Front matter: `created`, `updated`, `kind`, `voice`.
   - Define each term in the sentence where it first appears (no separate Definitions boxes).
   - Quote the user's raw words verbatim marked `[user]`; label assistant explanations `[assistant]`. Claims only move to `[source-checked]` or `[verified: cite]` via `inquiry` / `literature-review`.
   - At most one `mermaid` block or hand-drawn SVG in `figures/`, embedded as `![[figures/<name>.svg]]`.
   - Never alter existing Obsidian Document Comments (`<!--c:ID-->`, `<!--co:ID-->`).
5. **Verify and index.** Update the table in `docs/understanding/README.md`, run `../research-mode/scripts/check_references.py docs/literature-review/references.yaml` (when present), and refresh the project's `qmd` collection (`qmd update && qmd embed`) so `inquiry` can retrieve the new note as project memory.

**Reply:** the input file saved, the note created or updated in `docs/understanding/`, the open unknowns left as `TODO: unknown`, and whether `check_references.py` passed.
