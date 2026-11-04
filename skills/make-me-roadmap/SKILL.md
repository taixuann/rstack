---
name: make-me-roadmap
description: Builds the learning roadmap for a research project, which is the ordered list of what the user needs to understand and what "can explain it" means for each item. Use for /make-me-roadmap, at the start of learning in a project, or when the user's goals or questions change what they need to learn. Writes docs/learning/roadmap.md. teach follows it.
---

# Make me a roadmap

A plan for understanding, not for reading. The roadmap says what the user must be able to explain, in what order, and why each item matters for the project.

## Procedure

1. **Gather.** Read the project README and aims (`docs/rstack/explore/01_context.md`, `02_aims-and-milestones.md`), the user's annotations and questions, `docs/inputs/`, and any existing roadmap and sessions. Do not summarise them to the user.
2. **Find the gaps.** Ask with `interrogate` in interview mode, short rounds: what do you already explain well, what do you not, what must you understand for the next milestone? Skip what the files already answer. Anything they cannot answer yet stays `TODO: unknown`.
3. **Write the list.** One row per item, in dependency order (a term before the mechanism that uses it, a mechanism before the device that depends on it). Each row: the item, the line "you can explain: ...", why it matters to the project, which paper or annotation prompted it, status (`open`, `in progress`, `explained`), and the session that covered it.
4. **Keep it short.** A roadmap the user will not read is not a plan. Merge rows that one lesson covers. Mark the next one.
5. **Check with the user.** Show the order and ask what is missing or wrong. Their reorder wins.

## File

`docs/learning/roadmap.md`, with front matter `created`, `updated`, `kind: learning`, `voice`. Use the template at `../research-mode/references/roadmap.template.md`. Follow the Obsidian writing playbook.

## Ownership

This skill writes the structure of the roadmap. `teach` only changes an item's status and its session link. If a lesson shows the plan must change, stop and run this skill again.

Log the change in `docs/rstack/decisions.tsv` (**show-me-your-work**).

**Reply:** the path, the next item, and the one open point the user should settle.
