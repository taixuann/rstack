---
name: evaluate-my-understanding
description: Tests how well the user holds a concept and records it as a mastery level from 0 to 4 in docs/learning/understanding.md, with the evidence. Use for /evaluate-my-understanding, at the end of a teach lesson, when the user asks "do I understand this", "test me", "how well do I know X", or before relying on a concept in the proposal or design. Does not teach; teach and explain do that.
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

A level rises only with something the user did, linked as evidence: their answer in a session or `docs/inputs/` file. It never rises because the assistant said it went well. It can fall: re-test after a gap and record what you saw.

## Procedure

1. **Pick the concepts**: the ones the lesson covered, or the ones the user names, or the roadmap's next items. Read `docs/learning/understanding.md` (create it from `../research-mode/references/understanding.template.md` if missing) for their current level.
2. **Ask fresh questions.** Questions the lesson did not give, so a good memory does not pass. Use `interrogate` in interview mode, short rounds, one to four questions, a counter-case or a number each. A level 4 question uses `scientific-critical-thinking` on the paper's assumptions. When the same agent just taught the lesson, hand the questioning to a fresh `research-agent` with the concept, the source page, and this table; it returns the user's answers and your grading evidence, not the lesson text.
3. **Do not help during the test.** No hints before the answer. A hint ends the test for that level; note it.
4. **Grade by what they did.** Highest level whose test they passed without help. Record the `interrogate` class too (confirmed, misconception with the page, unknown, my error): the class says if this answer agrees with the source, the level says how well they hold it.
5. **Write the row.** Concept, level, class, evidence (a relative link to the answer, for example `sessions/2026-11-04_heart-to-signal.md`), date. Level 2 or higher needs an evidence link that exists; `scripts/check_references.py` fails otherwise. Copy their answers word for word, labelled `[user]`, into the session or an input file the link points to.
6. **Feed back.** Concepts that stay at 0 or 1, or fell, are candidates for the roadmap. Name them and ask: the user approves before `make-me-roadmap` adds any. Log the changes in `docs/rstack/decisions.tsv` (**show-me-your-work**).

**Reply:** the concepts tested, the level each earned and why, any that fell, and which low ones you propose for the roadmap. Three lines or fewer for one concept.
