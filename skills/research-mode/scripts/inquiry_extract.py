#!/usr/bin/env python3
"""Append the user's question-like Zotero annotations to docs/rstack/explore/inquiry.md.

Usage: inquiry_extract.py PROJECT_DIR   |   inquiry_extract.py --selftest
Reads papers from PROJECT_DIR/docs/rstack/references.yaml and their annotations through `zotero-cli`.
An annotation counts as a question when it is red or its comment contains a question mark.
Each is added once, under "## Open (new)", keyed by its Zotero annotation key. Existing entries are kept.
"""
import json, subprocess, sys
from pathlib import Path
import yaml

HEAD = "# Inquiry\n\nThe user's questions from reading, verbatim. Group by theme, then triage each as answered by this paper, answered by another paper, needs search, or for the supervisor.\n\n## Open (new)\n"


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
    refs = yaml.safe_load((project / "docs/rstack/references.yaml").read_text())
    f = project / "docs/rstack/explore/inquiry.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    text = f.read_text() if f.exists() else HEAD
    new = []
    for p in refs.get("papers") or []:
        anns = json.loads(subprocess.run(["zotero-cli", "ann", "list", "--item-key", p["key"], "--format", "json"],
                                         capture_output=True, text=True, check=True).stdout)
        known = {a["annotation_key"] for a in anns if f"key {a['annotation_key']}" in text}
        new += entries(p["cite"], anns, known)
    if new:
        if "## Open (new)" not in text:
            text += "\n## Open (new)\n"
        head, tail = text.split("## Open (new)\n", 1)
        text = head + "## Open (new)\n" + "\n".join(new) + "\n" + tail
    f.write_text(text)
    print(f"added {len(new)} questions to {f}")


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
