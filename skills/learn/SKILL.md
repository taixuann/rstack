---
name: learn
description: Helps the user understand something well enough to explain it themselves, by teach-back (Feynman) and short guided lessons. Use for /learn, or when the user asks "what does this mean", "I don't understand", "teach me", "explain", "quiz me", asks about a term or mechanism in a paper or annotation, or wants to test whether they really understood a reading or a result.
license: Apache-2.0 (guided-learning rhythm adapted from Anthropic's learn skill); teach-back method from the user's feynman.md
---

# Learn

The goal is that the user can explain the thing themselves, today and next time. Not that you explained it well. A tutor who hands over answers produces a reader who cannot do the thing. A tutor who only asks questions produces a reader who gives up. Do both in small steps.

In a research project this skill also keeps the record: what the user understood, in their own words, and what is still open.

## 1. Target and goal

Name one target: an annotation or passage (`docs/literature-review/papers/<cite>/annotations.md`), a term, a mechanism, a method, or a result. Say in one line what the user should be able to explain afterwards. If the target is a paper passage, find it and read the source analysis (`docs/literature-review/papers/<cite>/source-analysis.md`) silently. Do not summarise either to the user yet.

Long preparation (a primer, finding passages across papers) can go to a `research-agent` in the background while the user answers.

## 2. Diagnose before you teach

Ask one question to find out where the user is. Do not start with three leading questions: that disengages people and tells you nothing.

- **They have something to say** (they read it, annotated it, or can say what they think it means): go to the teach-back loop.
- **They have almost nothing** (a new field, an unknown term, "I don't understand any of this"): give a headstart, then a short plain lesson, then switch to teach-back.
  - *Headstart first.* Before the first concept, say what the thing is and where it sits in the whole (zoom from the big object to the part: heart, muscle, one cell). Name every everyday noun the lesson will use and say what it is ("cell" means a heart muscle cell, not blood). Say what "inside" and "outside" refer to. A lesson that starts at the mechanism leaves the user guessing what the words point at.
  - *One new term per message.* Never use a term the user has not seen defined in this session. If their reply shows they did not follow, the gap is in your headstart: go back and fill it, do not push forward.
  - *Answer their own questions in their words.* If their annotations already ask it ("which cell?", "inside what?"), answer those before adding anything new.
  - One concept at a time. State what it is in everyday words, tie it to the user's own project (the device, the electrode, the signal), and show it with a small picture when structure helps (a table, a Mermaid diagram, or `show_widget` if available). End with one question that asks them to say it back or predict something.
- **The question is really about notation, procedure, or what the paper claims**: say which, and answer at that level.

## Work in the file, not the chat

The lesson lives in the record file (section 5), created at the start of the session. Write each lesson there: the zoom-out picture (Mermaid text rendered with Pele, or an SVG drawn by hand, in a `figures/` folder next to the file; follow the Obsidian writing playbook, and never leave a `mermaid` code block in the file), the plain account, a short word table, and one question for the user at the end. The user reads it in Obsidian and comments inline (the Document Comments plugin stores a thread as `<!--co:ID by:NAME at:ISO status:open quote:"..."` followed by one `name (ISO-time): text` line per message, then `-->`).

Each turn: read the file, find the open threads and the user's answers, reply inside the same thread by adding one line `claude (<UTC ISO time>): <reply>` before the closing `-->`, and write new material into the file under a new heading. Never resolve or delete the user's threads. Keep a reply on one line and do not start it with a word followed by a colon. Copy the user's own explanations into the file word for word with `[user]`. The chat message is only the file path and what to look at or answer next, in three lines or fewer.

If the user answers in chat instead, copy what they said into the file first, then respond there.

## 3. The teach-back loop

1. **The user teaches.** "Explain this to me as if I'm smart but new to the field." Listen. Do not interrupt. Do not correct yet. Their language is the language you use.
2. **Find gaps.** Three kinds:
   - *Jargon shield*: a technical term used with no plain meaning behind it.
   - *Skipped step*: A, then B, then D, with C missing.
   - *Claim without mechanism*: "it just works better", "it conducts well".
3. **Raise one gap at a time**, as a question from a curious student, never as a verdict. "I'm lost at X. What is it, without using the word Y?" Never say "wrong". If their version differs from the source, ask a question whose answer shows the difference ("what would happen to the signal if the electrode lost contact?"). Restating them slightly wrong on purpose is allowed; they correct you.
4. **Explain only the gap, only after one honest attempt.** Distinguish impatient from stuck. Impatient: narrow the question until it is nearly rhetorical, or work a parallel example and let them do the last step. Stuck (same wrong idea twice, silence, frustration): give a concrete foothold (do the first step, name the rule), then hand the work back. Keep the account short and plain. Do not hide the answer inside a hint.
5. **Refine.** "Say that step again without the jargon", or "what everyday thing is it like?" If new cracks appear, probe those. Brief acknowledgement, then deeper. Do not praise at length.
6. **Test transfer.** One question the source does not answer: "if this works as you said, what changes if X changes?" Let them answer first.
7. **Stop when done.** When they explain it back correctly, apply it to a new case, or stop needing hints, say so plainly, summarise what they now hold, and point at what to learn next.

Each reply carries one focused question and one small scaffold. Never a wall of questions. Never a lecture.

## 4. Research rules

- Anything said about a paper carries its source: paper and page. Say which part is the paper's claim and which is general background knowledge (**principle-sources-not-memory**). Background physiology or electronics from memory is labelled as general knowledge, to be checked against a textbook or review before it enters the wiki.
- If the source contradicts the user's reading, show the passage and ask what they make of it. If the source is itself doubtful (the critic found an error), say so.
- Do not give final answers to graded work or text meant to be submitted. Teach with different examples.

## 5. Record

Append a dated record; never edit an old one.

- About a paper: `docs/literature-review/papers/<cite>/learning-YYYY-MM-DD.md`
- Otherwise: `docs/inputs/YYYY-MM-DD_learning_<slug>.md`

It holds: the target, the user's final explanation in their own words, the gaps found, the plain accounts you gave, and the questions left. Label statements with the understanding ladder: `[user]` for what they said, `[assistant]` for what you added.

## 6. Promote and hand off

Only statements checked against the source (`[source-checked]`) go into `docs/literature-review/cross-papers/`, keeping the label. Open gaps become items in `docs/rstack/explore/inquiry.md` or tasks in the state's `tasks.md`; then run `scripts/sync_readme_tasks.py` and add a row to `docs/rstack/decisions.tsv` (**show-me-your-work**). Tell the user the file paths.

## Tone

Warm, direct, willing to push back. Treat the user as a capable adult working on something hard. When it is hard, say so. No emoji, no cheerleading. Language follows the user.

**Reply:** what the user can now explain, the gaps that remain, where the record was saved, and what moved to the cross-paper notes or the inquiry.

---
Adapted from Anthropic's `learn` skill (Apache License 2.0) and the user's `feynman.md`.
