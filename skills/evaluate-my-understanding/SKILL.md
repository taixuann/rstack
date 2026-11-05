---
name: evaluate-my-understanding
description: Tests how well the user holds a concept and records it as a mastery level from 0 to 4 in the ## Understanding section of the concept's ingested page in Notion, with the evidence. Use for /evaluate-my-understanding, at the end of a teach lesson, when the user asks "do I understand this", "test me", "how well do I know X", or before relying on a concept in the proposal or design. Does not teach; teach and explain do that.
---

# Evaluate my understanding

Measure, do not teach. The record says what the user can do today, and the evidence for it. A level the user did not earn by doing something is a wrong record.

## Mastery levels

Not the ladder labels (`[user]`, `[source-checked]`): those say who said a statement. These say how well the user holds a concept.

| Level | The user can |
|---|---|
| 0 | Has not met it |
| 1 | Recognise it when shown, and say what it points at |
| 2 | Explain it in their own words, without the source |
| 3 | Predict or apply it in a case the lesson did not give |
| 4 | Critique a claim about it: find what a paper assumes, or where it would fail |

A level rises only with something the user did, linked as evidence: their answer on a Raw page. It never rises because the assistant said it went well. It can fall: re-test after a gap and record what you saw.

## Where the record lives

The `## Understanding` heading at the end of the concept's **ingested page** in Notion. Its rows are: Concept, Level, Class, Evidence, Date. Evidence is a link to the Raw page that holds the user's answer. The Roadmap section on the topic's Map of content page reads these rows for each item's status (explained means level 2 or higher on every row of that item's page). Never copy the level into the Roadmap.

This skill edits only the `## Understanding` section of an ingested page, with `insert_content` or `update_content` on its own rows. Never touch the rest of the page, and never replace the whole page. Ingest keeps this section when it rewrites a page (see `notion-llm-wiki`).

## Procedure

1. **Pick the concepts**: the ones the lesson covered, or the ones the user names, or the Roadmap's next items. Find each concept's ingested page and read its `## Understanding` rows for the current level. If the concept has no ingested page yet, say so: ingest the Raw page first.
2. **Ask fresh questions.** Questions the lesson did not give, so a good memory does not pass, and only up to the item's "Enough means" line; do not test below it. Use `interrogate` in learning mode, short rounds, one to four questions, a counter-case or a number each. A level 4 question uses `scientific-critical-thinking` on the paper's assumptions. When the same agent just taught the lesson, hand the questioning to a fresh `research-agent` with the concept, the source page, and this table; it returns the user's answers and your grading evidence, not the lesson text.
3. **Put the answers on a new Raw page.** Open a Raw page for the test (Notion writing playbook, with a `Continues:` link to the lesson page) and copy the user's answers word for word, labelled `[user]`. This page is the evidence. Do not help during the test: no hints before the answer. A hint ends the test for that level; note it.
4. **Grade by what they did.** Highest level whose test they passed without help. Record the `interrogate` class too (confirmed, misconception with the page, unknown, my error): the class says if this answer agrees with the source, the level says how well they hold it.
5. **Write the row** once the test page is ingested: concept, level, class, a link to the test Raw page, date. Level 2 or higher needs an evidence link that opens; read the row back to check it. The level changes only when a test page is ingested.
6. **Feed back.** Concepts that stay at 0 or 1, or fell, are candidates for the Roadmap. Name them and ask: the user approves before `make-me-roadmap` adds any. Tick the item's `Learn:` line in `tasks.md` only when its Understanding rows reach the level its Enough-means line asks for. Log the changes in `docs/rstack/decisions.tsv` (**show-me-your-work**).

Only lesson text goes to Notion, never signals or subject data.

**Reply:** the concepts tested, the level each earned and why, any that fell, and which low ones you propose for the Roadmap. Three lines or fewer for one concept.
