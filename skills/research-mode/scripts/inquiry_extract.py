#!/usr/bin/env python3
"""Write the user's new question-like Zotero annotations to a new docs/inputs/<today>_inquiry_questions.md.

Usage: inquiry_extract.py PROJECT_DIR   |   inquiry_extract.py --selftest
Reads papers from PROJECT_DIR/docs/literature-review/references.yaml and their annotations through `zotero-cli`.
An annotation counts as a question when it is red or its comment contains a question mark.
Each is written once, keyed by its Zotero annotation key, skipping keys already in any docs/inputs/*_inquiry_*.md. Existing files are never edited.
"""
import datetime, json, subprocess, sys
from pathlib import Path
import yaml

HEAD = "---\ncreated: {d}\nkind: inquiry\nvoice: user\nsource: chat\ntopic: questions from reading, from Zotero annotations\nreport: none\nconfirmed: no\n---\n# Inquiry questions {d}\n\nThe user's questions from reading, verbatim. Group by theme, then triage each as answered by this paper, answered by another paper, needs search, or for the supervisor.\n\n"


def is_question(a):
    return a.get("color_category") == "Red" or "?" in (a.get("comment") or "")


def entries(cite, anns, known):
    out = []
    for a in anns:
        if not is_question(a) or a["annotation_key"] in known:
            continue
        asked = " ".join((a.get("comment") or a.get("text") or "").split())
        quote = " ".join((a.get("text") or "").split())
        line = f"- [ ] {asked} ({cite}, p.{a.get('page','?')}, {a.get('color_category','')}) key {a['annotation_key']}"
        if quote and a.get("comment"):
            line += f"\n  - Passage: \"{quote[:200]}\""
        out.append(line)
    return out


def run(project):
    project = Path(project)
    refs = yaml.safe_load((project / "docs/literature-review/references.yaml").read_text())
    inputs = project / "docs/inputs"
    text = "".join(f.read_text() for f in inputs.glob("*_inquiry_*.md"))
    new = []
    for p in refs.get("papers") or []:
        anns = json.loads(subprocess.run(["zotero-cli", "ann", "list", "--item-key", p["key"], "--format", "json"],
                                         capture_output=True, text=True, check=True).stdout)
        known = {a["annotation_key"] for a in anns if f"key {a['annotation_key']}" in text}
        new += entries(p["cite"], anns, known)
    if not new:
        print("no new questions")
        return
    today = datetime.date.today().isoformat()
    f = inputs / f"{today}_inquiry_questions.md"
    if f.exists():
        sys.exit(f"{f} exists; a dated input is never edited. Move or rename it, then rerun.")
    f.write_text(HEAD.format(d=today) + "\n".join(new) + "\n")
    print(f"wrote {len(new)} questions to {f}")


def selftest():
    anns = [{"annotation_key": "A", "color_category": "Purple", "comment": "Why a gel?", "text": "gel", "page": "1"},
            {"annotation_key": "B", "color_category": "Red", "comment": "", "text": "unclear bit", "page": "2"},
            {"annotation_key": "C", "color_category": "Green", "comment": "result", "text": "x", "page": "3"},
            {"annotation_key": "D", "color_category": "Purple", "comment": "Seen? yes", "text": "y", "page": "4"}]
    got = entries("X 2020", anns, {"D"})
    assert len(got) == 2 and "key A" in got[0] and "key B" in got[1] and "Passage" in got[0], got
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        sys.exit(__doc__)
