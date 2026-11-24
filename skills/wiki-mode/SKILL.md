---
name: wiki-mode
description: "Store and maintain cross-project lab knowledge in research-space/wiki/ (equipment, procedures, reusable protocols, past lab experience) using protocol-wiki, doc-coauthoring, and qmd. Use for /wiki-mode, 'add to wiki', or recording reusable lab protocols outside a single project."
---

# Wiki mode

Cross-project lab memory in `research-space/wiki/`. Use this when knowledge belongs to the whole lab (procedures, equipment setup, fabrication tricks, reusable characterization workflows) rather than a single project's `docs/understanding/`.

## Flow

1. **Search existing wiki first.** If `qmd` is installed, query `-c wiki` (`qmd query -c wiki ...` or `qmd search ... -c wiki`) to see what already exists before creating a new page. Read `wiki/CLAUDE.md` for wiki-specific rules and schema; those rules outrank this skill.
2. **Draft or update the page.** Follow `references/protocol-wiki.md`: use `brainstorming` to explore alternatives, `interrogate` (interview mode) to surface missing parameters, and `doc-coauthoring` to structure the page section by section.
3. **Preserve provenance and marks.** Keep the wiki's source marks (`[user]` or `[studies]`), never invent measurements (`TODO: unknown` with who can answer), and never ingest raw data (`**/data/**`).
4. **Commit and refresh memory.** Commit changes inside the `wiki/` repository only (if it is its own git repo), then run `qmd update` and `qmd embed` so future `inquiry` and `experimental-design` runs retrieve the updated wiki pages.

**Reply:** pages created or updated in `wiki/`, open `TODO: unknown` items, and `qmd` index status.
