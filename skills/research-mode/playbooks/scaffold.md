# Scaffold (blueprint-folder bootstrap)

Standard research-project layout. Create the missing folders, never rename or overwrite existing ones.

```
data/raw/        immutable source measurements; never edit, never regenerate
docs/raw/        source papers, PDFs, web captures (input to the wiki)
docs/wiki/       synthesized knowledge, maintained with `karpathy-llm-wiki`
analysis/        scripts, figures, tables, design notes, decisions.tsv
manuscripts/     drafts and submission files
presentation/    slides, posters, talk notes
```

1. Confirm the target folder (default: the project folder the user names under research-space/projects/).
2. Create the folders above with `.gitkeep`; skip existing ones. Map legacy folders instead of moving them (`docs/manuscripts` → `manuscripts`, `docs/presentation` → `presentation`, `docs/experiments` → `analysis/design`) and ask before moving anything.
3. If asked, add a root README: question, status, folder map.
4. Read the tree back from disk and report it.

`data/raw` holds measurements and `docs/raw` holds literature; keep them separate. Derived data goes in `analysis/`, never back into `data/raw`.
