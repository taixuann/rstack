---
name: teach
description: Runs a lesson so the user can explain something themselves, by teach-back (Feynman). Takes the next item on the learning roadmap, writes the lesson from what the user already understands, and records what they now hold. Use for /teach, or when the user says "teach me", "quiz me", "test whether I understood", "next lesson", or wants to be able to say a reading or a result back in their own words. For a plain "what does this mean", use explain.
license: Apache-2.0 (guided-learning rhythm adapted from Anthropic's learn skill); teach-back method from the user's feynman.md
---

# Teach

The goal is that the user can explain the thing themselves, today and next time. Not that you explained it well. A tutor who hands over answers produces a reader who cannot do the thing. A tutor who only asks questions produces a reader who gives up. Do both in small steps.

This skill runs the lesson. Other skills do the parts:

| Part | Skill |
|---|---|
| The plan: what to learn, in what order | `make-me-roadmap` |
| A flowing account of a meaning or a difficulty | `explain` |
| A figure, when words cannot carry it | `make-the-figure` |
| Replies inside the user's comment threads | `answer-comments` |
| Questions to the user, and capturing their answers | `interrogate` (interview mode) |

Writing rules for notes the user reads in Obsidian (placement, front matter, comment format, checks) live in the Obsidian writing playbook. Follow it; do not restate it here.

## 1. Pick the target

Read `docs/learning/roadmap.md`. If it does not exist, or the user's question is not on it, run `make-me-roadmap` first. Take the next open item, or the one the user names. Say in one line what they should be able to explain afterwards. If the target is a paper passage, find it and read the source analysis (`docs/literature-review/papers/<cite>/source-analysis.md`) silently. Do not summarise it to the user yet.

Long preparation (a primer, finding passages across papers) can go to a `research-agent` in the background while the user answers.

## 2. Find where the user is

Read what they have already said: their annotations, `docs/inputs/`, earlier sessions, open comment threads. Then ask one question with `interrogate`. Do not start with three leading questions: that disengages people and tells you nothing.

- **They have something to say**: go to the teach-back loop.
- **They have almost nothing** (a new field, an unknown term): call `explain` for a headstart and a short account, then switch to teach-back.
- **The question is really about notation, procedure, or what the paper claims**: say which, and answer at that level.

## 3. Write the lesson from their understanding

The lesson is a section in the session file, built from their words, not a lecture prepared in advance. Use their wording for terms they already own. Start from the gap you found, not from page one. Keep the file short enough that they will read all of it.

New kind of lesson (first session on a topic, or a new layout): write one step as a sample, tell the user where it is, and wait for approval before writing the rest.

At the start of each turn, run `answer-comments` on the session file. Copy any answer the user gave in chat into the file first, word for word, labelled `[user]`.

## 4. The teach-back loop

1. **The user teaches.** "Explain this to me as if I'm smart but new to the field." Listen. Do not interrupt. Do not correct yet. Their language is the language you use.
2. **Find gaps.** Three kinds:
   - *Jargon shield*: a technical term used with no plain meaning behind it.
   - *Skipped step*: A, then B, then D, with C missing.
   - *Claim without mechanism*: "it just works better", "it conducts well".
3. **Raise one gap at a time**, as a question from a curious student, never as a verdict. "I'm lost at X. What is it, without using the word Y?" Never say "wrong". If their version differs from the source, ask a question whose answer shows the difference ("what would happen to the signal if the electrode lost contact?"). Restating them slightly wrong on purpose is allowed; they correct you.
4. **Explain only the gap, only after one honest attempt**, by calling `explain`. Distinguish impatient from stuck. Impatient: narrow the question until it is nearly rhetorical, or work a parallel example and let them do the last step. Stuck (same wrong idea twice, silence, frustration): give a concrete foothold (do the first step, name the rule), then hand the work back. Do not hide the answer inside a hint.
5. **Refine.** "Say that step again without the jargon", or "what everyday thing is it like?" If new cracks appear, probe those. Brief acknowledgement, then deeper. Do not praise at length.
6. **Test transfer.** One question the source does not answer: "if this works as you said, what changes if X changes?" Let them answer first.
7. **Stop when done.** When they explain it back correctly, apply it to a new case, or stop needing hints, say so plainly, summarise what they now hold, and point at what to learn next.

Each reply carries one focused question and one small scaffold. Never a wall of questions. Never a lecture.

## 5. Research rules

- Anything said about a paper carries its source: paper and page. Say which part is the paper's claim and which is general background knowledge (**principle-sources-not-memory**). Background physiology or electronics from memory is labelled as general knowledge, to be checked against a textbook or review before it enters the wiki.
- If the source contradicts the user's reading, show the passage and ask what they make of it. If the source is itself doubtful (the critic found an error), say so.
- Do not give final answers to graded work or text meant to be submitted. Teach with different examples.

## 6. Record

Append a dated record; never edit an old one.

- The session: `docs/learning/sessions/YYYY-MM-DD_<slug>.md`, with `papers: [<cite>]` in its front matter when a paper prompted it. Sessions belong to the topic, not to one paper.
- Each idea the user now holds: one short note in `docs/learning/concepts/<concept>.md` (a definition, then its properties; front matter `status: unchecked` until checked against a textbook or review), created or updated, linking back to the session. Link concept notes from the session with `[[concept]]`.
- The roadmap: tick the item's status. Do not re-plan it; if the plan must change, run `make-me-roadmap`. If the user's question belongs to a paper, add it to that paper's README with a link to the session.

A session file holds: the target, the user's final explanation in their own words, the gaps found, the accounts you gave, and the questions left. Label statements with the understanding ladder: `[user]` for what they said, `[assistant]` for what you added.

## 7. Promote and hand off

Only statements checked against the source (`[source-checked]`) go into `docs/literature-review/cross-papers/`, keeping the label. Open gaps become items in `docs/rstack/explore/inquiry.md` or tasks in the state's `tasks.md`; then run `scripts/sync_readme_tasks.py` and add a row to `docs/rstack/decisions.tsv` (**show-me-your-work**).

## Tone

Warm, direct, willing to push back. Treat the user as a capable adult working on something hard. When it is hard, say so. No emoji, no cheerleading. Language follows the user.

**Reply:** the file path and the one thing to read or answer next, in three lines or fewer. When the lesson ends: what the user can now explain, the gaps that remain, where the record was saved, and what moved to the cross-paper notes or the inquiry.

---
Adapted from Anthropic's `learn` skill (Apache License 2.0) and the user's `feynman.md`.
