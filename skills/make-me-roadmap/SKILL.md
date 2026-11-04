---
name: make-me-roadmap
description: Builds the learning roadmap for a research project, which is the ordered list of what the user needs to understand and what "can explain it" means for each item. Use for /make-me-roadmap, at the start of learning in a project, or when the user's goals or questions change what they need to learn. Writes docs/learning/roadmap.md. teach follows it.
---

# Make me a roadmap

A plan for understanding, not for reading. The roadmap says what the user must be able to explain, in what order, and why each item matters for the project.

## Procedure

1. **Gather.** Read, for every paper in `docs/literature-review/references.yaml`: `annotations.md`, `alignment.md`, and the Inquiry output `docs/rstack/explore/inquiry.md` (its misconceptions and unknowns are the first candidates). Also read the project aims (`docs/rstack/explore/01_context.md`, `02_aims-and-milestones.md`), `docs/inputs/`, `docs/learning/understanding.md`, and any existing roadmap and sessions. Do not summarise them to the user.
2. **Find the gaps.** Start from those files; they already hold most of the answer. A concept already at level 2 or higher in `understanding.md` is not a gap. Ask with `interrogate` in interview mode only for what they leave out: what must you understand for the next milestone that no paper raised? Anything they cannot answer yet stays `TODO: unknown`. State each item's question first (**principle-question-first**).
3. **Write the list.** One row per item, merged across papers (one row for an idea two papers need, with several entries under prompted by), in dependency order (a term before the mechanism that uses it, a mechanism before the device that depends on it). Each row: the item, **Enough means** (one line: what the user can say once done, and no more, for example "can say why the electrode sees a wave, not how one cell works"), **Stop here** (what is deliberately out), why it matters to the project, which paper or annotation prompted it, status (`open`, `in progress`, `explained`, read from `docs/learning/understanding.md`: explained means level 2 or higher), and the core note that covers it. Ask what the project needs, not what the field contains: the user is building a device, not studying the subject. Deeper things go to a **Parked** list under the table, one line each.
4. **Keep it short.** A roadmap the user will not read is not a plan. Merge rows that one lesson covers. Mark the next one.
5. **Check with the user.** Show the order and ask what is missing or wrong. Their reorder wins.

## File

`docs/learning/roadmap.md`, with front matter `created`, `updated`, `kind: learning`, `voice`. Use the template at `../research-mode/references/roadmap.template.md`. Follow the Obsidian writing playbook.

## Re-running

Run it again when new papers are ingested, when `inquiry.md` changes, or when `evaluate-my-understanding` proposes low-level concepts and the user approves them. Update the file in place: keep rows and their session links, add new rows, never drop one the user did not approve dropping. Rows can also gain Parked entries from `branch`.

## Ownership

This skill writes the structure of the roadmap. `teach` only sets an item's core note, and an item's status is read from `understanding.md`, which only `evaluate-my-understanding` changes. If a lesson shows the plan must change, stop and run this skill again.

Log the change in `docs/rstack/decisions.tsv` (**show-me-your-work**).

**Reply:** the path, the next item, and the one open point the user should settle.
