### Learning

State: any. Use when the user wants to understand something: an annotation they made, a mechanism, a method, a result. The user teaches first and the assistant plays a curious student who finds the gaps. The goal is the user's understanding, not a finished document. Sessions are short and one gap at a time.

Where it sits: during Paper ingestion or Inquiry, when a red annotation or a misconception shows up; before Investigation, when a term is unclear; and in later states, when a result needs reasoning. Inquiry hands every "misconception" and "unknown" item here.

1. **Pick the target and the goal.** One thing: an annotation or passage (`docs/raw/papers/<cite>/annotations.md`), a concept, or a result. Say in one line what the user should be able to explain afterwards. Find the source passages (paper snapshot, `docs/wiki/papers/<cite>/source-analysis.md`) and read them silently. Do not summarise them to the user.
2. **The user teaches.** Ask: "Teach me this as if I am smart but new to the field." Listen. Do not interrupt. Do not explain. Language follows the user.
3. **Find the gaps.** Look for jargon shields (a term used without a plain meaning), skipped steps (A to B to D with C missing), and claims with no mechanism ("it just works better"). Raise the single most important gap as a question. Never say "wrong". If the user's version differs from the source, ask a question that lets them notice it (`interrogate` interview mode). Restating them slightly wrong on purpose is allowed.
4. **Explain only the gap, only after they tried.** When the user is stuck after one honest attempt, give a short plain account of that gap alone, with the source passage cited (paper, page). Say what is the paper's claim and what is general knowledge. Do not give a lecture. Use `bro` when a reply came out too dense. Write every reply through `unslop`.
5. **Refine.** Ask the user to explain that step again without the jargon, or with an analogy. If new cracks appear, probe them. Repeat steps 3 to 5 until the explanation holds without jargon shields, skipped steps, or hand-waving.
6. **Test transfer.** One question the source does not answer: "If this works as you described, what happens if X changes?" or "Where else would this apply?" Let the user answer first. Use `in-your-own-words` to restate the user's goal and your reading of it when the direction is unclear.
7. **Record.** Append a dated record; never edit an old one. About a paper: `docs/raw/papers/<cite>/learning-YYYY-MM-DD.md`. Otherwise: `docs/raw/inputs/YYYY-MM-DD_learning_<slug>.md`. It holds the user's final explanation in their own words, the gaps found, and the questions left. Label statements with the understanding ladder: `[user]` for what they said, `[assistant]` for what you added.
8. **Promote and hand off.** Only statements checked against the source (`[source-checked]`) go into `docs/wiki/` with `karpathy-llm-wiki`, keeping the label. Open gaps become items in `docs/rstack/explore/inquiry.md` or tasks in the state's `tasks.md`, then run `scripts/sync_readme_tasks.py`.

**Reply:** what the user can now explain, the gaps that remain, where the record was saved, and what moved to the wiki or the inquiry.

Adapted from the user's `feynman.md` (teach-back method) and pstack's teach skill (plain explanation after the person has tried), MIT License, (c) 2026 Lauren Tan.
