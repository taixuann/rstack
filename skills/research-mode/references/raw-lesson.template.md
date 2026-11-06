# Learning notes layout (draft, literature, permanent)

Zettelkasten, light version. Raw pages are named `YYYY-MM-DD_slug`.

| Note | Where | Who writes it |
| --- | --- | --- |
| Draft | The user's own text on a Raw page, with their problems and questions in it | The user. The assistant makes small updates after answering |
| Literature note | A block beside the draft, headed "Base knowledge, added by the assistant" | The assistant. General knowledge, labelled `[assistant]`, unchecked until papers confirm it |
| Permanent note | A page in the structure the user chooses | Built from the draft and the answers, in the user's words and structure |

## The loop

1. **The user posts problems and questions** in their draft.
2. **The assistant answers in chat**, with `teach` or `explain`. Short, one answer for each question.
3. **Then the assistant updates the draft parts the answers change.** Small edits to the user's own sentences, in their structure, order and style. Fix what is wrong. Add what is missing, a few words or one sentence. Do not rewrite a paragraph, do not add headings, do not change the order, do not turn text into questions. Tell the user in chat which sentences changed.
4. **The literature note keeps its structure.** Add or fix a little where the answers need it. Never restructure it.
5. **The user gives a structure** for the permanent note. The assistant writes it from the updated draft, in that structure and in the user's words. The user edits it.
6. **Validate later.** Check claims against papers after the user has the base knowledge. A claim then gets a label (`[source-checked]` and above).

## Rules

1. First use of a new kind of edit: show one sample (before and after) and wait for the user to approve it. Then continue.
2. There is one permanent note for a topic. Split it only when the user says "split".
3. A permanent note uses the user's words and structure, not the assistant's sentences. Say in the note which parts are not yet checked.
4. Keep the existing structure of every page. Add to it. Never make a massive edit. If a change needs more than a few sentences, ask first.
5. Write by `plain-writing.md`. Where the user writes differently, the user's style wins.
6. Editing text that has a Notion comment deletes the comment thread. The tools cannot resolve threads or make suggested edits (both need a Notion Business plan). Say so before editing commented text.
7. Do not open a new page for a reply. Open a new page for a new topic, a branch (`Parent` and `Depth` lines, depth 3 at most), or the first lesson after a page is ingested. Do not start a subagent to write a note.
8. Older pages in the Session-block layout stay as they are.
