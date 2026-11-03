#!/usr/bin/env python3
"""Check docs/literature-review/references.yaml against the files on disk.

Usage: check_references.py REFERENCES_YAML   |   check_references.py --selftest
Paths are relative to the project root (two levels above docs/rstack/).
Exit 1 and print each problem when a check fails.
"""
import re, sys, tempfile
from pathlib import Path
import yaml

STATUS = {"unread", "snapshotted", "read"}
REVIEW = {"needs_review", "pass", "repair", "blocked", "no_review"}
KINDS = {"understanding", "learning", "supervisor", "result-thought"}
DATED = r"\d{4}-\d{2}-\d{2}"
USED_IN = {"01_context", "02_aims-and-milestones", "03_literature-map",
           "04_questions-and-hypotheses", "05_methods-and-feasibility"}


def check_raw(root):
    """Raw inputs and reports are dated; inputs carry a known kind. Files starting with . or README are skipped."""
    errs = []
    for f in sorted((root / "docs/inputs").glob("*")):
        if f.name.startswith(".") or f.name.startswith("README"):
            continue
        m = re.fullmatch(DATED + r"_([a-z-]+)_[a-z0-9-]+\.md", f.name)
        if not m or m.group(1) not in KINDS:
            errs.append(f"inputs/{f.name}: name must be <date>_<kind>_<slug>.md, kind in {sorted(KINDS)}")
    for f in sorted((root / "docs/literature-review/reports").glob("*")):
        if not f.name.startswith(".") and not re.fullmatch(DATED + r"_[a-z0-9-]+_[a-z0-9-]+\.md", f.name):
            errs.append(f"reports/{f.name}: name must be <date>_<tool>_<slug>.md")
    for f in sorted((root / "docs/literature-review/papers").glob("*/learning-*")):
        if not re.fullmatch(r"learning-" + DATED + r"\.md", f.name):
            errs.append(f"papers/{f.parent.name}/{f.name}: name must be learning-<date>.md")
    return errs


def check_readmes(root):
    """Every paper folder has a README.md, and the project README links it."""
    errs = []
    top = root / "README.md"
    top_text = top.read_text() if top.exists() else None
    for d in sorted((root / "docs/literature-review/papers").glob("*")):
        if not d.is_dir():
            continue
        rel = f"docs/literature-review/papers/{d.name}/README.md"
        if not (d / "README.md").exists():
            errs.append(f"papers/{d.name}: README.md missing; write it from references/paper-readme.template.md")
        elif top_text is not None and rel not in top_text:
            errs.append(f"README.md: Contents does not link {rel}")
    return errs


def check_notes(root):
    """Notes the user reads in Obsidian: front matter, no mermaid block, embeds resolve, diagrams fresh, comments balanced."""
    errs = []
    base = root / "docs"
    files = [f for d in ("literature-review", "inputs") for f in sorted((base / d).rglob("*.md"))]
    for f in files:
        if f.name == "annotations.md":
            continue
        rel = f.relative_to(root)
        text = f.read_text()
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        keys = set(re.findall(r"^(\w+):", m.group(1), re.M)) if m else set()
        need = {"created", "updated", "kind", "voice"}
        if "papers" in f.parts:
            need.add("paper")
        if need - keys:
            errs.append(f"{rel}: front matter missing {sorted(need - keys)}")
        if "```mermaid" in text:
            errs.append(f"{rel}: mermaid block; write figures/<name>.mmd, run scripts/render_diagram.mjs, embed the SVG")
        for e in re.findall(r"!\[\[([^\]|]+)", text):
            if not (f.parent / e).exists():
                errs.append(f"{rel}: embed not found: {e}")
        ids = lambda pat: set(re.findall(pat, text))
        opened, closed, threads = ids(r"<!--c:(\w+)-->"), ids(r"<!--/c:(\w+)-->"), ids(r"<!--co:(\w+)")
        if not (opened == closed == threads):
            errs.append(f"{rel}: unbalanced comment markers {sorted(opened ^ closed | opened ^ threads)}; restore them, never delete half a comment")
    for mmd in sorted(base.rglob("*.mmd")):
        svg = mmd.with_suffix(".svg")
        if not svg.exists() or svg.stat().st_mtime < mmd.stat().st_mtime:
            errs.append(f"{mmd.relative_to(root)}: SVG missing or older; run scripts/render_diagram.mjs on it")
    return errs


def check(ref_file):
    ref_file = Path(ref_file)
    root = ref_file.resolve().parents[2]
    data = yaml.safe_load(ref_file.read_text()) or {}
    errs, seen = [], set()
    if not (data.get("zotero") or {}).get("collection_key"):
        errs.append("zotero.collection_key missing")
    for p in data.get("papers") or []:
        k = p.get("key", "?")
        if k in seen:
            errs.append(f"{k}: duplicate key")
        seen.add(k)
        for f in ("key", "cite", "status"):
            if not p.get(f):
                errs.append(f"{k}: {f} missing")
        if p.get("status") not in STATUS:
            errs.append(f"{k}: status must be one of {sorted(STATUS)}")
        for f in ("snapshot", "analysis"):
            if p.get(f) and not (root / p[f]).exists():
                errs.append(f"{k}: {f} path not found: {p[f]}")
        if p.get("review") and p["review"] not in REVIEW:
            errs.append(f"{k}: review must be one of {sorted(REVIEW)}")
        if p.get("status") == "read" and p.get("review") in ("needs_review", "repair", "blocked"):
            errs.append(f"{k}: status read but review is {p['review']}")
        if p.get("status") in ("snapshotted", "read") and not p.get("snapshot"):
            errs.append(f"{k}: status {p['status']} needs a snapshot")
        if p.get("status") == "read" and not p.get("analysis"):
            errs.append(f"{k}: status read needs an analysis path")
        for u in p.get("used_in") or []:
            if u not in USED_IN:
                errs.append(f"{k}: unknown used_in {u}")
    return errs + check_raw(root) + check_readmes(root) + check_notes(root)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/rstack").mkdir(parents=True)
        (root / "docs/literature-review/papers").mkdir(parents=True)
        (root / "docs/literature-review/papers/a.md").write_text("x")
        good = {"zotero": {"collection_key": "C"}, "papers": [
            {"key": "A", "cite": "X 2020", "status": "snapshotted", "snapshot": "docs/literature-review/papers/a.md", "used_in": ["01_context"], "review": "needs_review"}]}
        f = root / "docs/literature-review/references.yaml"
        f.write_text(yaml.safe_dump(good))
        assert check(f) == [], check(f)
        good["papers"][0].update(status="read", snapshot="docs/literature-review/papers/missing.md", used_in=["nope"])
        f.write_text(yaml.safe_dump(good))
        e = " ".join(check(f))
        assert "not found" in e and "unknown used_in" in e and "needs an analysis" in e and "review is needs_review" in e, e
        (root / "docs/inputs").mkdir()
        (root / "docs/inputs/2026-11-02_learning_ecg.md").write_text("x")
        (root / "docs/inputs/notes.md").write_text("x")
        e = " ".join(check(f))
        assert "inputs/notes.md" in e and "2026-11-02_learning" not in e, e
        (root / "docs/literature-review/papers/b").mkdir()
        (root / "README.md").write_text("no links")
        e = " ".join(check(f))
        assert "papers/b: README.md missing" in e, e
        (root / "docs/literature-review/papers/b/README.md").write_text("x")
        e = " ".join(check(f))
        assert "Contents does not link docs/literature-review/papers/b/README.md" in e, e
        (root / "README.md").write_text("docs/literature-review/papers/b/README.md")
        e = " ".join(check(f))
        assert "papers/b/README.md: front matter missing" in e, e
        b = root / "docs/literature-review/papers/b"
        fm = "---\ncreated: x\nupdated: x\nkind: k\nvoice: v\npaper: b\n---\n"
        (b / "README.md").write_text(fm + "```mermaid\nx\n```\n![[figures/f.svg]]\n<!--c:q1-->t<!--/c:q1-->\n")
        e = " ".join(check(f))
        assert "mermaid block" in e and "embed not found: figures/f.svg" in e and "unbalanced comment markers ['q1']" in e, e
        (b / "figures").mkdir()
        (b / "figures/f.mmd").write_text("flowchart LR\n A-->B")
        e = " ".join(check(f))
        assert "f.mmd: SVG missing or older" in e, e
        (b / "figures/f.svg").write_text("<svg/>")
        (root / "docs/literature-review/papers/a.md").write_text(fm)
        (b / "README.md").write_text(fm + "![[figures/f.svg]]\n<!--c:q1-->t<!--/c:q1-->\n<!--co:q1 by:me status:open\nme (x): hi\n-->\n")
        assert check(f) == [], check(f)
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/literature-review/reports").mkdir(parents=True)
        (root / "docs/literature-review/reports/summary.md").write_text("x")
        (root / "docs/literature-review/papers/a").mkdir(parents=True)
        (root / "docs/literature-review/papers/a/learning-notes.md").write_text("x")
        e = " ".join(check_raw(root))
        assert "reports/summary.md" in e and "learning-notes.md" in e, e
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        problems = check(sys.argv[1])
        print("\n".join(problems) or "references ok")
        sys.exit(1 if problems else 0)
    else:
        sys.exit(__doc__)
