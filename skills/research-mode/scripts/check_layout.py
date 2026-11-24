#!/usr/bin/env python3
"""Flag project folders that references/layout.md does not list.

Usage: check_layout.py PROJECT_DIR      Exit 1 when an unknown folder is found.
"""
import re
import sys
from pathlib import Path

LAYOUT = Path(__file__).resolve().parents[1] / "references/layout.md"
PHASES = ("explore", "design", "analysis", "write", "closed")
OLD_NAMES = {"brainstorm": "docs/inputs/ (dated <date>_brainstorm_<slug>.md)", "d-brainstorm": "docs/inputs/ (dated <date>_brainstorm_<slug>.md)", "inquiry": "docs/rstack/d-inquiry/", **{x: "docs/rstack/ itself (flat; put phase: in the front matter)" for x in PHASES}, **{"p-" + x: "docs/rstack/ itself (flat; put phase: in the front matter)" for x in PHASES}}  # names before the flat layout and the short-lived p- folders
OK_DIRS = ("d-inquiry", "reviews", "writing")
ROOT_OK = {"data", "docs", "analysis", ".rstack", ".git", ".gitignore", "README.md", "AGENTS.md", "CLAUDE.md", ".claude", ".obsidian", ".DS_Store"}


def known_docs():
    """Second-level folders under docs/ named in the layout table."""
    return set(re.findall(r"`docs/([a-z-]+)/", LAYOUT.read_text())) | set(re.findall(r"`docs/([a-z-]+)\.", LAYOUT.read_text()))


def check(project):
    p, out = Path(project), []
    for d in sorted(p.iterdir()):
        if d.name not in ROOT_OK:
            out.append(f"UNKNOWN {d.name}: not in references/layout.md (move it, or add a row there first)")
    docs = p / "docs"
    if docs.is_dir():
        ok = known_docs()
        out += [f"UNKNOWN docs/{d.name}: not in references/layout.md" for d in sorted(docs.iterdir()) if d.is_dir() and d.name not in ok]
    st = p / "docs/rstack"
    if st.is_dir():
        for d in sorted(x for x in st.iterdir() if x.is_dir()):
            n = d.name
            if n in OLD_NAMES:
                out.append(f"RENAME docs/rstack/{n}: use {OLD_NAMES[n]}")
            elif n not in OK_DIRS:
                out.append(f"UNKNOWN docs/rstack/{n}: allowed folders are {', '.join(OK_DIRS)}; project documents sit flat in docs/rstack/")
        for f in sorted(st.glob("*.md")):
            home = "docs/inputs/ as <date>_brainstorm_<slug>.md" if f.name.startswith("brainstorm") else "docs/inputs/ as <date>_inquiry_<slug>.md" if f.name.startswith("inquiry") else "docs/literature-review/" if f.name.startswith("claims") else None
            if home:
                out.append(f"STRAY docs/rstack/{f.name}: move it to {home}")
    return out


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        for d in ("data/raw", "docs/rstack", "docs/reports", "docs/writing", "manuscripts", "docs/notes"):
            (p / d).mkdir(parents=True)
        r = check(p)
        assert any("manuscripts" in l for l in r) and any("docs/notes" in l for l in r) and len(r) == 2, r
        for n in ("brainstorm-x.md", "inquiry.md", "claims.md", "01_context.md"):
            (p / "docs/rstack" / n).write_text("x")
        s = [l for l in check(p) if l.startswith("STRAY")]
        assert len(s) == 3 and "<date>_brainstorm_" in s[0] and "docs/literature-review/" in s[1] and "<date>_inquiry_" in s[2], s
        (p / "docs/rstack/p-explore").mkdir()
        (p / "docs/rstack/brainstorm").mkdir()
        (p / "docs/rstack/notes").mkdir()
        (p / "docs/rstack/reviews").mkdir()
        r = check(p)
        assert any(l.startswith("RENAME docs/rstack/p-explore") and "flat" in l for l in r), r
        assert any(l.startswith("RENAME docs/rstack/brainstorm") and "<date>_brainstorm_" in l for l in r), r
        assert any(l.startswith("UNKNOWN docs/rstack/notes") for l in r), r
        assert not any(l.startswith(("UNKNOWN docs/rstack/reviews", "RENAME docs/rstack/reviews")) for l in r), r
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        r = check(sys.argv[1])
        print("\n".join(r) or "layout ok")
        sys.exit(1 if r else 0)
    else:
        sys.exit(__doc__)
