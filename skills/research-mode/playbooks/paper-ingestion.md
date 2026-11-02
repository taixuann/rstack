### Paper ingestion

State: explore, once per paper. Produce the assistant's independent reading of one paper, freeze it, and have a critic review it. The analyst and the critic are always separate agents in fresh contexts. A review in the same context is `NON_QUALIFYING_SAME_CONTEXT` and cannot give a PASS. This is the assistant's side of the understanding ladder. The user's side is their annotations, and **Inquiry** brings the two together.

Per-paper folders: `docs/raw/papers/<cite>/annotations.md` (the user's Zotero snapshot, raw; `learning-<date>.md` records from the **Learning** playbook sit beside it) and `docs/wiki/papers/<cite>/` with `source-analysis.md`, `review.md`, and later `alignment.md`.

**Route.** The user marks key papers. `FULL` for key papers and for any paper whose analysis changed in a major way. `SCOPED` for a local repair to an analysis that already passed. `NO_REVIEW` for background papers; they are context only and never the sole support for a claim.

1. **Analyze.** The `source-analyst` agent reads the paper end to end and writes `source-analysis.md` from `references/source-analysis.template.md`: thesis, methods, experimental records, findings with value, unit, uncertainty, n, comparator and page, citations, caveats, figures and tables, relevance verdict against the project aims. It does this blind to the user's annotations. Procedure facts belong in records, not findings. Every statement is labelled `[assistant]`.
2. **Snapshot.** The analyst then runs `scripts/zotero_snapshot.py <key> --out docs/raw/papers` and adds the entry to `docs/rstack/references.yaml` with `status: snapshotted` and `review: needs_review`.
3. **Freeze.** Create `review.md` from `references/review.template.md`. Record the Zotero item version and the sha256 of the snapshot and the analysis.
4. **Review (FULL route).** The `paper-critic` agent runs alone in a fresh context, in three passes: source fidelity with a blind inventory first, then evidence strength, then gaps. One critic is enough; the independence that matters is from the analyst, not between critics.
5. **Race check.** Before the verdict, re-read the Zotero version and the hashes. If either changed, the verdict is `BLOCKED` with a `stale_revision` issue. Re-freeze and review again.
6. **Verdict.** `PASS` only when all six dimensions pass (source and identity, paper coverage, record coverage, figure and table coverage, finding fidelity, traceability), no blocking issue is open, and the critic was independent. `REPAIR` when the source is enough and the analyst can fix a bounded defect. `BLOCKED` when evidence is unavailable (no full text, missing figure or supplement) or independence is impossible. Missing evidence is a blocker, not a failed claim. Never turn it into "not reported".
7. **Promote.** Statements in `source-analysis.md` that the critic confirmed against the paper become `[source-checked]`. Set `review` in `references.yaml` to `pass`, `repair`, or `blocked`. Set `status: read` only for `PASS` papers and for `NO_REVIEW` papers the user read. Run `scripts/check_references.py`.
8. **Repair and re-review.** The analyst repairs after `REPAIR`. Re-review only the affected parts, or everything if the findings or the source changed.

**Reply:** the verdict per paper, open issues with their locations, and what the analyst must repair.
