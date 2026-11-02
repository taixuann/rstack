# Scaffold (blueprint-folder bootstrap)

Standard research-project layout. Create the missing folders, never rename or overwrite existing ones.

```
data/raw/        immutable source measurements; never edit, never regenerate
docs/raw/        source papers, PDFs, web captures (input to the wiki)
docs/wiki/       synthesized knowledge, maintained with `karpathy-llm-wiki`
docs/rstack/     written documents of each stage, in <state>/ subfolders
analysis/        scripts, figures, tables
manuscripts/     drafts and submission files
presentation/    slides, posters, talk notes
```

1. Confirm the target folder (default: the project folder the user names under research-space/projects/).
2. Create the folders above with `.gitkeep`; skip existing ones. `docs/rstack/<state>/` folders are created when a project enters that state. Map legacy folders instead of moving them (`docs/manuscripts` → `manuscripts`, `docs/presentation` → `presentation`, `docs/experiments` → `docs/rstack/design`) and ask before moving anything.
3. Run **Project docs** to write `README.md` and `AGENTS.md` with `state: scaffold`.
4. Read the tree back from disk and report it.

`data/raw` holds measurements and `docs/raw` holds literature. Keep them separate. Derived data goes in `analysis/`, never back into `data/raw`.
