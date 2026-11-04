---
name: explain
description: Explains a meaning or a difficulty as one flowing account, in plain words, with each new term defined in the sentence where it first appears. Use for /explain, or when the user asks "what does this mean", "I don't understand", "explain", asks about a term, mechanism, annotation, or result, or is stuck during a lesson. To make the user able to say it back, use teach.
---

# Explain

Make one thing clear. Not a lesson plan, not a quiz. Say what the thing is, how it works, and why, in one account the user reads once, top to bottom.

## Rules

1. **Say where it sits first.** Before the mechanism, say what the thing is and where it fits in the whole (zoom from the large object to the part: heart, muscle, one cell). Name every everyday noun the account will use and say what it points at. A cell here is a heart muscle cell, not blood. Say what "inside" and "outside" refer to.
2. **Tell it as a story when it is a process.** Time order, start to end. Say what happens before naming it. One idea per paragraph.
3. **Put each term beside the thing.** Define a new word in the sentence where the thing it names first happens. Put its rule, number or reason in the same paragraph, right where it matters. No separate Definitions box, no Properties box, no list of words before the story. A table of words at the end is allowed as a recap, not as the first introduction.
4. **One new term at a time.** Never use a term the user has not seen defined in this session. If their reply shows they did not follow, the gap is in your account: go back and fill it, do not push forward.
5. **Answer their own questions first.** If their annotations or comments already ask it ("which cell?", "inside what?"), answer those in their words before adding anything new.
6. **Figures are rare.** Words first. Use at most one figure per account, and a second only if the first cannot show the structure. Never one per step. Ask `make-the-figure` for it, or write a small Mermaid block if that is enough. Do not add a figure that repeats a nearby one.
7. **Tie it to the user's project.** The device, the electrode, the signal. End with one question that asks them to say it back or predict something.
8. **Label what you know.** A claim about a paper carries its paper and page. Background knowledge from memory is `[assistant]` and general knowledge, not yet checked (**principle-sources-not-memory**).

## When the account goes in a file

If the user reads in Obsidian, write the account into the session or note file under a new heading, following the Obsidian writing playbook (placement, front matter, comment format). Answer open comment threads with `answer-comments`. The chat reply is the file path and what to read next, in three lines or fewer.

New layout or new kind of topic: write the first step or paragraph as a sample, tell the user where it is, and wait for approval before writing the rest.

## Check before you hand it over

- Every term used was defined earlier in the same account.
- No Definitions or Properties boxes. No lists where a sentence works.
- Figures: no more than one or two, and each shows something the words do not.
- A reader new to the field can follow it without opening another page.

**Reply:** the account (or the file path), then one question for the user.
