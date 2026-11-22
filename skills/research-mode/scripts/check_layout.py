#!/usr/bin/env python3
"""Flag project folders that references/layout.md does not list.

Usage: check_layout.py PROJECT_DIR      Exit 1 when an unknown folder is found.
"""
import re
import sys
from pathlib import Path

LAYOUT = Path(__file__).resolve().parents[1] / "references/layout.md"
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
        for d in sorted(x for x in st.iterdir() if x.is_dir() and x.name not in ("brainstorm", "inquiry", "writing")):
            for f in sorted(d.glob("*.md")):
                home = "brainstorm" if f.name.startswith("brainstorm") else "inquiry" if f.name.startswith(("inquiry", "claims")) else None
                if home:
                    out.append(f"STRAY docs/rstack/{d.name}/{f.name}: move it to docs/rstack/{home}/")
    return out


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        for d in ("data/raw", "docs/rstack", "docs/reports", "docs/writing", "manuscripts", "docs/notes"):
            (p / d).mkdir(parents=True)
        r = check(p)
        assert any("manuscripts" in l for l in r) and any("docs/notes" in l for l in r) and len(r) == 2, r
        (p / "docs/rstack/explore").mkdir()
        for n in ("brainstorm-x.md", "inquiry.md", "claims.md", "01_context.md"):
            (p / "docs/rstack/explore" / n).write_text("x")
        s = [l for l in check(p) if l.startswith("STRAY")]
        assert len(s) == 3 and "brainstorm/" in s[0], s
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
