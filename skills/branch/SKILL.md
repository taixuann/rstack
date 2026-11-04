---
name: branch
description: Writes one short note for a word or question the user wants opened up, from a comment or a command, and links it from the note it came from. Use for /branch <word or question>, or when an open comment says to branch, expand, define, or "what is X" about a term inside a learning note. answer-comments hands such comments here. Stops at the project's "Enough means" line and at depth 3.
---

# Branch

A core learning note stays short because everything the user wants to dig into goes into its own small note. This skill writes that note. It does not teach a lesson (`teach`) and does not answer ordinary comments (`answer-comments`).

## Where branches live

`docs/learning/branches/<slug>.md`, flat. The slug is kebab-case and carries no date. Nesting is said in front matter, never in subfolders:

```
created, updated, kind: learning, voice: assistant,
parent: <name of a core note or another branch, no .md>,
depth: <parent depth + 1; a core note is depth 0>,
status: unchecked
```

`status: unchecked` stays until the branch is checked against a textbook, review, or paper (`sources`). Then set `checked` and say against what.

## Triggers

- `/branch <word or question>`: the parent is the note the user is reading, or the one they name.
- An open comment thread that asks to branch, expand, define, or "what is X" about a term. `answer-comments` hands it here; the parent is the note the comment is in.

## Procedure

1. **Read the parent note and its limit.** Read the parent and its "Enough means" line (the first line of a core note, and its row in `docs/learning/roadmap.md` with the "Stop here" column). The depth is the parent's plus one.
2. **Apply the two limits.**
   - Depth above 3 (default): do not create the note. Add one line to the roadmap's Parked list (the word, the parent, why it matters), and tell the user.
   - The word is below the "Stop here" line: say so, add it to the Parked list, and ask. Create it only if the user says to branch anyway.
3. **Check it does not exist.** If `branches/<slug>.md` exists, link to it instead of writing a new one.
4. **Write the note** with the `explain` rules: say what the thing is and where it sits first, one flowing account, each term defined beside the thing, one idea per paragraph, no Definitions or Properties boxes, at most one figure (`make-the-figure`), `[assistant]` labels on statements from general knowledge, sources with page for paper claims. Tie it to the project in the last paragraph. Keep it short: stop at what the parent needs.
5. **Link it from the parent, with the least possible edit.** The Document Comments plugin refuses a new comment when the file changes after the user selected text. So: read the parent again, then make one batched edit that does only two things: add `- [[slug]]: <one line>` under a `## Branches` list at the end of the parent (create the heading the first time), and add the one-line reply in the thread (`claude (<UTC time>): Branched: [[slug]]`). Never rewrite the note, never reword or move a thread, never resolve it. Put the explanation in the branch file, not in the parent.
6. **Check** with `scripts/check_references.py` (the parent exists, links to the branch with `[[slug]]`, and the depth is right).

`teach` lists the branches made in each lesson on its log line; this skill does not write the log.

**Reply:** the branch path and depth, or why it was parked. Two lines or fewer.
