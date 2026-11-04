---
name: branch
description: Opens up a word or question the user wants expanded, from a comment or a command: a short inline expansion in the text, or, only when it is big, its own note linked at the term. Use for /branch <word or question>, or when an open comment says to branch, expand, define, or "what is X" about a term inside a learning note. answer-comments hands such comments here. Stops at the project's "Enough means" line and at depth 3.
---

# Branch

A core learning note stays short because deeper things are opened up beside the term, not in a separate section. A branch is first an **inline expansion**. Only a **big** one becomes its own note. This skill does not teach a lesson (`teach`) and does not answer ordinary comments (`answer-comments`).

## Triggers

- `/branch <word or question>`: the parent is the note the user is reading, or the one they name.
- An open comment thread that asks to branch, expand, define, or "what is X" about a term. `answer-comments` hands it here; the parent is the note the comment is in.

## Procedure

1. **Read the parent note and its limit.** Read the parent and its "Enough means" line (the first line of a core note, and its row in `docs/learning/roadmap.md` with the "Stop here" column). The depth is the parent's plus one.
2. **Apply the two limits.**
   - Depth above 3 (default): do not expand it. Add one line to the roadmap's Parked list (the word, the parent, why it matters), and tell the user.
   - The word is below the "Stop here" line: say so, add it to the Parked list, and ask. Expand it only if the user says to branch anyway.
3. **Choose the size.** Write it inline unless it is big: more than two or three short paragraphs, or it needs a figure, or other notes will reuse it. When unsure, write it inline.
4. **Inline expansion (the default).** Put a short sentence or one short paragraph right where the term sits, following the `explain` rules: say what the thing is first, define the term beside the thing, no Definitions or Properties boxes, `[assistant]` on general knowledge, a source with page for paper claims. Insert it after the paragraph that holds the term. Never insert inside a comment-anchored span (`<!--c:ID-->...<!--/c:ID-->`). Do not create a file.
5. **Big branch.** Write `docs/learning/branches/<slug>.md`, flat, kebab-case, no date, with the `explain` rules, at most one figure (`make-the-figure`), tied to the project in the last paragraph. Front matter:
   ```
   created, updated, kind: learning, voice: assistant,
   parent: <name of a core note or another branch, no .md>,
   depth: <parent depth + 1; a core note is depth 0>,
   status: unchecked
   ```
   Nesting is said by `parent`, never by subfolders. `status: unchecked` stays until the note is checked against a textbook, review or paper (`sources`); then set `checked` and say against what. If `branches/<slug>.md` already exists, link to it instead. In the parent, link it inline at the term, in the sentence: `[[slug|term]]`. Never a separate list of branches at the end.
6. **Edit the parent with the least possible change.** The Document Comments plugin refuses a new comment when the file changes after the user selected text. Read the parent again, then make one batched edit: the inline expansion (or the inline link), and the one-line thread reply `claude (<UTC time>): <where it went>`. Never rewrite the note, never reword, move or resolve a thread, never touch comment-anchored text.
7. **Check** with `scripts/check_references.py` (a big branch's parent exists, links `[[slug...]]`, and the depth is right).

`teach` lists the big branches made in each lesson on its log line; this skill does not write the log.

**Reply:** where the expansion went (the path and the place), or why it was parked. Two lines or fewer.
