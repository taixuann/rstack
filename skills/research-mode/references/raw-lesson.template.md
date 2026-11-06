# Raw lesson page layout (light version)

The user writes the page. The assistant helps them understand and write it better. Raw pages are named `YYYY-MM-DD_slug`.

## The loop

1. **The user writes** in their own page, in their own words. The assistant never changes those words first.
2. **The user asks.** The user points at a passage or a question. The assistant answers in chat with `teach` or `explain`, whichever fits: `explain` for a plain meaning, `teach` when the user wants to say it back. This is back and forth. No page edit yet.
3. **Base knowledge when it helps.** The assistant can add a block under the user's text, headed "Base knowledge, added by the assistant". It holds general knowledge, labelled `[assistant]` and unchecked. It has no quiz. The user can delete it.
4. **The user says they are satisfied.** Only then does the assistant edit the passage directly. It rewrites it in the user's way: the user's words, order and tone, with the corrected or added idea. It keeps the user's claims, not its own phrasing.
5. **Validate later.** Checking against papers comes after the user has the base knowledge. Claims then get a label (`[source-checked]` and above).

## Rules

1. Never edit the user's text before step 4.
2. Write by `plain-writing.md`. Match the user's own style where the user writes differently. The user's style wins.
3. Copy the user's words from chat into the page only when the user asks. Mark them `[user]`.
4. Editing text that has a Notion comment deletes the comment thread. The tool cannot resolve threads or make suggested edits (both need a Notion Business plan). Say so before editing commented text.
5. Do not open a new page for a reply. Open a new page only for a new topic, a branch (`Parent` and `Depth` lines, depth 3 at most), or the first lesson after a page is ingested.
6. Do not start a subagent to write a page. Write it in the current chat.
7. The old Session block layout (About block, My words, Account, Your turn, "What changed") is retired. Pages that use it stay as they are.
8. Page history in Notion shows what changed. Do not keep old versions on the page.
