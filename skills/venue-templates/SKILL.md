---
name: venue-templates
description: "Find and record a journal's current rules for a materials or devices manuscript (length, abstract, figures, references, required sections and statements) from its official author instructions, and pick a LaTeX template. Use in Paper preparation, when choosing a venue, or when checking a draft or PDF against venue rules."
license: MIT
compatibility: "validate_format.py needs Python 3.11+ and the Poppler tools (pdfinfo, pdffonts) to inspect a PDF."
metadata:
  adapted-from: "K-Dense-AI/claude-scientific-writer, skill venue-templates 1.3 (MIT, (c) K-Dense Inc.)"
  changes: "cut to journals; life-science, machine-learning, grant and poster material removed; workflow rewritten for rstack"
---

# Venue templates

Venue rules change. Nothing in this skill is the rule; the journal's own page is. This skill is the way to find the rule, record it, and check against it.

## The currency rule

Before writing any limit, style-file name, required section or statement into `target.md`:

1. Fix the exact journal, the article type (article, communication, letter, review) and the stage (initial submission, revision, accepted).
2. Open the journal's official author instructions. Not a publisher-wide page when the journal has its own.
3. Record the URL and the date checked in `target.md`.
4. A rule you did not find on that page is `TODO: unknown`. Never fill it from memory, from another journal of the same publisher, or from an older year.

## What to record

Length (words or pages, and what counts), abstract length and form, title limit, number of figures and tables, reference style and limit, required sections and their order, required statements (data availability, author contributions, competing interests, funding, AI-use disclosure), supporting-information rules, graphical abstract or table-of-contents entry if asked, file formats, and whether the first submission is format-free.

## Where materials and devices work is published

The usual homes are the journals of ACS, Wiley, the Royal Society of Chemistry, Elsevier, Springer Nature, IOP Publishing, AIP Publishing, APS, IEEE and MDPI. Each journal has its own author guidelines and most publishers give a LaTeX class and a Word template. Find the journal's page; do not assume one journal's rules from its publisher's flagship.

`references/journals_formatting.md` has the official starting pages for Nature Portfolio, Science, Elsevier and others, with the date they were reviewed. `references/nature_science_style.md` describes how Nature and Science papers are structured; use it for the checklist and the scaffold questions, never to write text for the user.

## Templates

Use the journal's official template when it gives one. Bundled, for drafting only:

| File | What it is |
|---|---|
| `assets/journals/elsarticle-template-num.tex`, `-num-names.tex`, `-harv.tex` | Elsevier `elsarticle` examples, with their `.bst` files (LPPL, unmodified) |
| `assets/journals/nature_article.tex` | a generic scaffold in the Nature layout; not an official Nature class |

Copy a template to `docs/writing/<piece>/main.tex` only when that folder has no `main.tex`, and strip its sample text. The file you leave holds the preamble and one `\input` per section, no prose.

## Check a PDF

```bash
python scripts/validate_format.py --file main.pdf --max-pages 8
```

It reports the page count and the embedded fonts. Its built-in venue presets are for conferences and grants and do not apply here; pass the limit from `target.md`. It cannot prove margins or font sizes.
