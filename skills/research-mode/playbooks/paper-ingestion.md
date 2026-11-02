### Paper ingestion

State: explore, once per paper. Turn one paper and the user's annotations into source-grounded notes, freeze them, and have independent critics review them. The producer and the critics are always separate agents in fresh contexts. A review in the same context is `NON_QUALIFYING_SAME_CONTEXT` and cannot give a PASS.

**Route.** The user marks key papers. `FULL` for key papers and for any paper whose notes changed in a major way. `SCOPED` for a local repair to notes that already passed. `NO_REVIEW` for background papers; they are used as context only and never as the sole support for a claim.

1. **Snapshot.** Run `scripts/zotero_snapshot.py <key> --out docs/raw/papers`. Add or refresh the entry in `docs/rstack/references.yaml` with `status: snapshotted` and `review: needs_review`.
2. **Produce.** The `paper-reader` agent writes `docs/wiki/<snapshot name>.md` with these parts, using the user's colours:
   - Paper map: contribution, system and materials, preparation sequence, measurement and analysis methods with instruments and settings, results including negative and null ones, limitations, every figure and table, supplements, references.
   - Experimental records (orange): one per process step, with inputs, outputs, technique, instrument, parameters, conditions, and page.
   - Findings (green): one claim each, with value, unit, uncertainty, n, comparator, conditions, page, and the figure or table it rests on.
   - Mechanism (blue), Context (purple), and Open questions (red and question-style comments, verbatim).
   Procedure facts belong in records, not findings.
3. **Freeze.** Create `docs/rstack/explore/reviews/<cite>.md` from `references/review.template.md`. Record the Zotero item version and the sha256 of the snapshot and the wiki page.
4. **Review (FULL route).**
   - `source-critic` runs first and alone. It reads only the paper and writes its own source inventory into the review file before it opens the wiki page. Then it compares the two.
   - `evidence-critic` and `gap-critic` then run in parallel on the wiki page and the paper.
   - Critics edit nothing except their own section of the review file.
5. **Race check.** Before the verdict, re-read the Zotero version and the hashes. If either changed, the verdict is `BLOCKED` with a `stale_revision` issue. Re-freeze and review again.
6. **Verdict.** `PASS` only when all six dimensions pass (source and identity, paper coverage, record coverage, figure and table coverage, finding fidelity, traceability), no blocking issue is open, and every critic was independent. `REPAIR` when the source is enough and the producer can fix a bounded defect. `BLOCKED` when evidence is unavailable (no full text, missing figure or supplement) or independence is impossible. Missing evidence is a blocker, not a failed claim. Never turn missing evidence into "not reported".
7. **Repair and re-review.** The producer repairs after `REPAIR`. Re-review only the affected parts, or everything if the paper map, findings, or source changed.
8. **Record.** Set `review` in `references.yaml` to `pass`, `repair`, or `blocked`. Set `status: read` only for `PASS` papers and for `NO_REVIEW` papers the user read. Run `scripts/check_references.py`.

**Reply:** the verdict per paper, open issues with their locations, and what the producer must repair.
