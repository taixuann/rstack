---
name: citation-management
description: "Turn DOIs into BibTeX, clean and deduplicate a .bib file, and validate it (missing fields, duplicate keys, DOIs that do not resolve). Use in Paper preparation when building docs/writing/<piece>/references.bib, and before a critique. Finding papers is not this skill's job."
license: MIT
compatibility: "Python 3.9+ with requests. doi_to_bibtex.py and validate_citations.py --check-dois need network access to api.crossref.org and doi.org."
metadata:
  adapted-from: "K-Dense-AI/claude-scientific-writer, skill citation-management 2.1 (MIT, (c) K-Dense Inc.)"
  changes: "search scripts (Google Scholar, PubMed, OpenAlex) and their references removed; SKILL.md rewritten for rstack"
---

# Citation management

One job: a correct `references.bib`. Searching the literature is done elsewhere (hyperresearch, Zotero). A reference enters the bibliography only from a resolved DOI or a Zotero export, never from memory.

## Commands

Run from this skill's folder.

```bash
python scripts/doi_to_bibtex.py 10.1002/adma.200400767                 # one DOI to a BibTeX entry
python scripts/doi_to_bibtex.py -i dois.txt -o new.bib                  # a file of DOIs
python scripts/format_bibtex.py refs.bib --deduplicate --sort key -o clean.bib
python scripts/validate_citations.py refs.bib                           # offline: fields, duplicates, format
python scripts/validate_citations.py refs.bib --check-dois --report report.json
```

## Rules

1. Every entry has a DOI where one exists. An entry with no DOI says what it is (book, thesis, standard, dataset) and has enough fields to find it.
2. The key in `references.bib` is the key in `citations.yaml` and in the text. Renaming a key means changing all three; `format_bibtex.py --rekey` changes only the first, so use it before any text exists.
3. Metadata comes from Crossref or the publisher, not from a search-result snippet. Check the title, the year and the first author against the paper itself for every reference the argument leans on.
4. Preprint and published version: cite the published one when it exists.
5. A DOI that does not resolve is a finding. Report it; do not guess the right one.
6. `validate_citations.py` prints warnings about how long a reference list "should" be for some venues. Those are rules of thumb from other fields. Ignore them; the limit is the one in `target.md`.
7. Existence is not support. That a reference is real says nothing about whether it supports the sentence; `citations.yaml` records what each work is cited for, with the page, and the critic checks the sentence against it.

`references/bibtex_formatting.md` covers entry types and fields; `references/citation_validation.md` covers what the validator checks. `assets/citation_checklist.md` is a last pass before submission.
