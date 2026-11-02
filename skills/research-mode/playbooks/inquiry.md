### Inquiry

State: explore. After the user has read papers and annotated them in Zotero. Turn the user's questions into answers, searches, and claims. The user's own words stay verbatim.

1. **Collect.** Run `scripts/inquiry_extract.py <project>`. It appends new question-like annotations (red highlights and comments with a question) to `docs/rstack/explore/inquiry.md` under Open, once each.
2. **Group and confirm.** Group the open items under plain-language theme headings (for example "How the signal reaches the electrode"). Show the grouped list and wait. The user edits or confirms before anything costs time or money.
3. **Triage** each item as one of:
   - answered by the same paper (a question raised early may be answered later in the text; cite the page),
   - answered by another paper already read,
   - needs search,
   - for the supervisor.
4. **Answer** from papers that passed review, with cite and page. Use `arena` for competing explanations of a mechanism, `scientific-critical-thinking` for the strength of the evidence, and `brainstorming` for alternatives. Say plainly when the papers do not settle it.
5. **Search.** Write the items that need search into `docs/rstack/explore/inquiry-search.md`: the questions, the context, and the papers already read. Run them only with the user's go-ahead, by `paper-lookup` or `openalex-database` for targeted searches, or by HyperResearch (run from `~/academic-space`) or `deep-research` for a broad pass. Results are leads. Resolve every DOI, let the user add chosen papers to Zotero, then run **Paper ingestion** on them.
6. **Claims.** Write `docs/rstack/explore/claims.md`. One line per claim, then branches under it: mechanism, evidence (cite and page), caveat, open question. Add a Mermaid mindmap of the claim tree (`markdown-mermaid-writing`). Claims come only from answered items and from findings that passed review.
7. **Checkpoint.** Show the claims. The user confirms or corrects them before they feed `03` to `05`.

**Reply:** items answered, items waiting for search or the supervisor, and the claims proposed.
