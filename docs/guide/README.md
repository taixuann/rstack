# The rstack guide

Start with a clear **intention**. Not sure which mode or playbook fits? Run `/rstack:using-rstack` — it interviews your intention, checks the active project's state, and routes you to the right mode:

- `/rstack:learn-mode` — turn your raw reading into project understanding (`docs/inputs/` → `docs/understanding/`).
- `/rstack:wiki-mode` — record reusable cross-project lab procedures in `wiki/`.
- `/rstack:research-mode` — execute phase playbooks (`explore → design → analysis → write → closed`).
- `/rstack:playbook-control` — design bespoke workflows (`figure-it-out`), fix recurring mistakes (`correct`), upgrade playbooks (`reflect`), model-check states (`statechart`), or author skills.

## Walkthroughs

1. [Set up rstack](./01-setup.md). Install, profile, models, external CLI tools (`qmd`, `zotero-cli`, `raw-viewer`, `hyperresearch`).
2. [Route work through `/research-mode`](./02-research-mode.md). Give it a goal and watch it pick a playbook.
3. [Scaffold and design](./03-scaffold-and-design.md). Folder blueprint, hypotheses, `report-init`, `experimental-design`.
4. [Analyse and verify](./04-analyse-and-verify.md) and [the analysis runner](./analysis-runner.md). Data, figures, numbers you can trace.
5. [Literature and writing](./05-literature-and-writing.md). Literature review, citations, manuscripts, reviews.
6. [Steer with principle names](./06-principles.md). Principles in `skills/research-mode/principles/`.
7. [Make it yours](./07-make-it-yours.md). Your own workflows and governance via `/playbook-control`.

## Commands and scripts by phase

Run scripts inside `skills/research-mode/scripts/` from your project or workspace root:

| Phase / Mode | Key script or command | Purpose |
|---|---|---|
| Setup & memory | `qmd collection add`, `qmd update && qmd embed` | Index `<project>` (excluding `**/data/**`) and `wiki/` for `Inquiry` |
| Project init & layout | `init_project.py`, `check_layout.py <project>`, `sync_readme_tasks.py <project>` | Scaffold project, verify standard folders, sync `README.md` tasks |
| Explore & Zotero | `zotero_snapshot.py`, `inquiry_extract.py <project>`, `check_references.py <refs.yaml>` | Snapshot Zotero highlights, extract questions, verify links & front matter |
| Design & Freeze | `verify_playbook.py start <playbook> --project <dir>` | Track `Done when` gates for `experimental-design` and `report-init` |
| Analysis | `raw_intake.py`, `rstack_run.py` (`new`, `run`, `tick`, `replay`, `package`) | Standardize raw filenames, run provenance-tracked analyses ([details](./analysis-runner.md)) |
| Write | `writing.py gate` | Advance `paper-preparation` / `paper-writing` / `paper-critique` gates |
| Plugin maintenance | `python3 rstack/scripts/check_plugin.py`, `claude plugin validate rstack` | Verify rstack consistency after any `/playbook-control` edit |

Stuck? Type `/rstack:using-rstack` (interactive routing) or `/rstack:research-help` (Q&A).
