---
name: evaluate-my-understanding
description: Tests how well the user holds a concept and records it as a mastery level from 0 to 4 in a short "Understanding check" block at the end of the user's page in Notion, with the evidence. Use for /evaluate-my-understanding, at the end of a teach lesson, when the user asks "do I understand this", "test me", "how well do I know X", or before relying on a concept in the proposal or design. Does not teach; teach and explain do that.
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

A short block headed "Understanding check" at the end of the user's own page in Notion. Rows: Concept, Level, Evidence (the user's answer, in their words, with the date). Add it with `insert_content` at the end. Never touch the rest of the page. Run only when the user asks for a check.

## Procedure

1. **Pick the concepts**: the ones the lesson covered, or the ones the user names. Read the user's page and its "Understanding check" block for the current level.
2. **Ask fresh questions.** Questions the lesson did not give, so a good memory does not pass, and only as deep as the user's own page goes. Use `interrogate` in learning mode, short rounds, one to four questions, a counter-case or a number each. A level 4 question uses `scientific-critical-thinking` on the paper's assumptions. When the same agent just taught the lesson, hand the questioning to a fresh `research-agent` with the concept, the source page, and this table; it returns the user's answers and your grading evidence, not the lesson text.
3. **Keep the answers.** Copy the user's answers word for word, labelled `[user]`, into the Evidence cell or under the block. Do not help during the test: no hints before the answer. A hint ends the test for that level; note it.
4. **Grade by what they did.** Highest level whose test they passed without help. Record the `interrogate` class too (confirmed, misconception with the page, unknown, my error): the class says if this answer agrees with the source, the level says how well they hold it.
5. **Write the row**: concept, level, class, the user's answer, date. Level 2 or higher needs the answer in the Evidence cell. Read the row back to check it.
6. **Feed back.** Name the concepts that stay at 0 or 1, or fell, and ask the user whether they want a lesson on them. Log the changes in `docs/rstack/decisions.tsv` (**show-me-your-work**).

Only lesson text goes to Notion, never signals or subject data.

**Reply:** the concepts tested, the level each earned and why, any that fell, and which low ones you propose to teach. Three lines or fewer for one concept.
