---
name: make-me-roadmap
description: Reads the user's own overview page in Notion and says in chat what is still open and in what order to take it. The user's page is the plan; this skill writes no Roadmap section, table or task lines. Use for /make-me-roadmap, at the start of learning in a project, or when the user's questions change what they need to learn.
---

# Make me a roadmap (light version)

The user writes the plan. This skill only reads it back and helps order it.

## Procedure

1. **Read the user's overview page** (a Raw page, for example `2026-11-06_overview`). Take the points in the user's own words and order. Read nothing else unless the user asks.
2. **List what is open.** One line each, in the user's wording. Mark what a lesson has already covered (the pages `teach` and `explain` wrote, and any understanding check).
3. **Say the next one.** Suggest an order only where one point needs another first (a term before the mechanism that uses it). Say why in one sentence. The user's order wins.
4. **Stop.** Do not write a table, a Roadmap section, "Enough means" rows or `Learn:` lines in `tasks.md`. Do not edit the user's page. If the user wants a point added, they write it, or you add it after they say so.

**Reply:** the open points in the user's words, the suggested next one, and one open question if there is one. Five lines or fewer.
