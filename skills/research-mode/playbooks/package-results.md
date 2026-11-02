### Package results

Freeze and hand off a finished study.

1. Confirm every reported number traces to a script and an input (path, hash). Rerun the final pipeline from a clean state.
2. Assign each result a disposition: accepted, rejected, or ambiguous, with the evidence. Write them to `docs/rstack/progressing/results.md`.
3. Use the `export` skill to package inputs, code, accepted outputs, provenance, and reproduction steps into a single folder.
4. Leave `data/raw/` untouched and untracked data out of the package unless the user asks.

**Reply:** package path, dispositions, and declared gaps.
