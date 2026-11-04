---
name: answer-comments
description: Reads the open comment threads the user left in an Obsidian note (Document Comments plugin) and replies inside each thread. Use for /answer-comments, or when the user says they commented, asks you to answer their comments, or at the start of a teach turn. Works on any note: a learning session, a paper README, an alignment.
---

# Answer comments

The user comments on text in Obsidian. The comment is the question. Answer it where it was asked.

The thread format and the rules for leaving it intact are in the Obsidian writing playbook (rule 4). Follow that; this skill is the procedure.

## Procedure

1. **Read the file again** just before you edit. The user edits while you work, and the Document Comments plugin refuses a new comment if the file changed after they selected text. So edit as little as possible: one batched write per turn.
2. **Find the open threads**: `<!--co:ID ... status:open` blocks. A thread is open if its status is `open` and the last message is the user's, or if the user replied after your last line.
3. **Answer each one**, in order of the file. Read the quoted text (`<!--c:ID-->...<!--/c:ID-->`) so you know what they are pointing at. Answer the question they asked, in the same plain words they used. If the answer needs more than a few lines, or the comment asks to branch, expand, or define a term, hand it to `branch`: a short inline expansion beside the term, or, if big, a note in `docs/learning/branches/` linked inline at the term. Reply with a one-line pointer to where it went. An account that belongs in the core note itself follows the `explain` skill, added at the end.
4. **Reply in the thread**: add one line `claude (<UTC ISO time>): <reply>` before the closing `-->`. One line. Do not start it with a word followed by a colon.
5. **Never** resolve, delete, move, or reword a thread or a comment marker. Change only the exact lines you mean to, in one write; never rewrite a whole note from memory.
6. **Anything you cannot answer** (it needs a source you do not have, or a judgment only the user can make): say so in the reply and name what is needed.
7. **Check** with `scripts/check_references.py` (comment markers must stay balanced).

**Reply:** how many threads you answered, which ones remain open and why, and the file path. Three lines or fewer.
