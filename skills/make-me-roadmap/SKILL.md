---
name: make-me-roadmap
description: Builds the learning roadmap for a research project, which is the ordered list of what the user needs to understand and what "can explain it" means for each item. Use for /make-me-roadmap, at the start of learning in a project, or when the user's goals or questions change what they need to learn. Writes the ## Roadmap section on the topic's Map of content page in Notion. teach follows it.
---

# Make me a roadmap

A plan for understanding, not for reading. The roadmap says what the user must be able to explain, in what order, and why each item matters for the project.

## Procedure

1. **Gather.** Read, for every paper in `docs/literature-review/references.yaml`: `annotations.md`, `alignment.md`, and the Inquiry output `docs/rstack/explore/inquiry.md` (its misconceptions and unknowns are the first candidates). Also read the project aims (`docs/rstack/explore/01_context.md`, `02_aims-and-milestones.md`), `docs/inputs/`, the topic's ingested pages with their `## Understanding` rows, and any existing Roadmap section. Do not summarise them to the user.
2. **Find the gaps.** Start from those files; they already hold most of the answer. A concept already at level 2 or higher in an `## Understanding` section is not a gap. Ask with `interrogate` in interview mode only for what they leave out: what must you understand for the next milestone that no paper raised? Anything they cannot answer yet stays `TODO: unknown`. State each item's question first (**principle-question-first**).
3. **Write the list.** One row per item, merged across papers (one row for an idea two papers need, with several entries under prompted by), in dependency order (a term before the mechanism that uses it, a mechanism before the device that depends on it). Each row: the item, **Enough means** (one line: what the user can say once done, and no more, for example "can say why the electrode sees a wave, not how one cell works"), **Stop here** (what is deliberately out), why it matters to the project, which paper or annotation prompted it, status (`open`, `in progress`, `explained`), and the ingested page that covers it. Status is read from that page's `## Understanding` rows; explained means level 2 or higher on every row. Ask what the project needs, not what the field contains: the user is building a device, not studying the subject. Deeper things go to a **Parked** list under the table, one line each.
4. **Keep it short.** A roadmap the user will not read is not a plan. Merge rows that one lesson covers. Mark the next one.
5. **Check with the user.** Show the order and ask what is missing or wrong. Their reorder wins.

## Where it goes

A `## Roadmap` heading on the topic's Map of content page, below the index table. No child page. The index table is never touched by this skill. Use the columns of `../research-mode/references/roadmap.template.md`; follow the Notion writing playbook. Edit the section with `update_content` or `insert_content`, never a replace of the whole page.

## Re-running

Also add one `Learn: <item> (Roadmap)` line per item the current state needs to the `Learning` heading of `docs/rstack/<state>/tasks.md`, then run `scripts/sync_readme_tasks.py`. Run it at the start of each state. Run it again when new papers are ingested, when `inquiry.md` changes, or when `evaluate-my-understanding` proposes low-level concepts and the user approves them. Update the section in place: keep rows and their page links, add new rows, never drop one the user did not approve dropping. Branches (a Raw page with a `Parent:` line) that pass depth 3 go to the Parked list.

## Ownership

This skill writes the structure of the Roadmap section. `teach` only sets an item's Raw or ingested page link, and an item's status is read from the `## Understanding` rows, which only `evaluate-my-understanding` changes. If a lesson shows the plan must change, stop and run this skill again.

Log the change in `docs/rstack/decisions.tsv` (**show-me-your-work**). Only plan text goes to Notion, never signals or subject data.

**Reply:** the page title, the next item, and the one open point the user should settle.
