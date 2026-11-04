#!/usr/bin/env python3
"""Check docs/literature-review/references.yaml against the files on disk.

Usage: check_references.py REFERENCES_YAML   |   check_references.py --selftest
Paths are relative to the project root (two levels above docs/rstack/).
Exit 1 and print each problem when a check fails.
"""
import re
import shutil
import subprocess, sys, tempfile
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
    return errs


def front(text):
    """Front matter keys and values as a dict; empty when there is none."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^(\w+):[ \t]*(.*)$", m.group(1), re.M)) if m else {}


def check_learning(root):
    """docs/learning: core/ and branches/ notes are kebab-case without dates; each branch names a parent that
    exists and links back with [[name]], and its depth is the parent's plus one (a core note is depth 0)."""
    base = root / "docs/learning"
    if not base.exists():
        return []
    errs = []
    if not (base / "log.md").exists():
        errs.append("learning/log.md missing; write it from references/log.template.md")
    notes = {}
    for kind in ("core", "branches"):
        for f in sorted((base / kind).glob("*")):
            if f.name.startswith("."):
                continue
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.md", f.name) or re.match(DATED, f.name):
                errs.append(f"learning/{kind}/{f.name}: name must be kebab-case <slug>.md with no date")
            else:
                notes[f.stem] = (kind, f)
    for name, (kind, f) in notes.items():
        if kind != "branches":
            continue
        fm = front(f.read_text())
        missing = [k for k in ("parent", "depth", "status") if k not in fm]
        if missing:
            errs.append(f"learning/branches/{f.name}: front matter missing {missing}")
            continue
        parent = notes.get(fm["parent"])
        if not parent:
            errs.append(f"learning/branches/{f.name}: parent {fm['parent']} not found in core/ or branches/")
            continue
        pkind, pf = parent
        pd = front(pf.read_text()).get("depth", "")
        pdepth = 0 if pkind == "core" else (int(pd) if pd.isdigit() else None)
        if pdepth is None:
            errs.append(f"learning/branches/{pf.name}: depth missing or not a number")
        elif not fm["depth"].isdigit() or int(fm["depth"]) != pdepth + 1:
            errs.append(f"learning/branches/{f.name}: depth must be parent depth + 1 ({pdepth + 1})")
        if not re.search(r"\[\[" + re.escape(name) + r"[\]|#]", pf.read_text()):
            errs.append(f"learning/{pkind}/{pf.name}: does not link [[{name}]]; link [[{name}|term]] at the term in the parent")
    return errs


def check_understanding(root):
    """understanding.md: level 0-4; level 2 or more needs an evidence link to a file under docs/learning/."""
    f = root / "docs/learning/understanding.md"
    if not f.exists():
        return []
    errs = []
    for ln in f.read_text().splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[1].isdigit() and cells[1] not in ("Level", "---") and not set(cells[1]) <= {"-"}:
            if len(cells) >= 5 and cells[0] not in ("Concept",) and not set(cells[0]) <= {"-"}:
                errs.append(f"understanding.md: {cells[0]}: level must be 0 to 4")
            continue
        if not cells[1].isdigit():
            continue
        lvl = int(cells[1])
        if lvl > 4:
            errs.append(f"understanding.md: {cells[0]}: level must be 0 to 4")
        m = re.search(r"\(([^)]+)\)|\[\[([^\]|]+)", cells[3])
        target = (m.group(1) or m.group(2)) if m else None
        if lvl >= 2 and not (target and (f.parent / target).exists()):
            errs.append(f"understanding.md: {cells[0]}: level {lvl} needs an evidence link to an existing file (relative to docs/learning/)")
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
    """Notes the user reads in Obsidian: front matter, mermaid blocks parse, embeds resolve, comments balanced."""
    errs = []
    base = root / "docs"
    files = [f for d in ("literature-review", "inputs", "learning") for f in sorted((base / d).rglob("*.md"))]
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
        if "```mermaid" in text and shutil.which("node"):
            r = subprocess.run(["node", str(Path(__file__).with_name("render_diagram.mjs")), str(f)], capture_output=True, text=True)
            errs += [f"{ln.replace(str(f), str(rel), 1)} (fix the Mermaid syntax)" for ln in r.stderr.splitlines() if ln.strip()] if r.returncode else []
        for e in re.findall(r"!\[\[([^\]|]+)", text):
            if not (f.parent / e).exists():
                errs.append(f"{rel}: embed not found: {e}")
        ids = lambda pat: set(re.findall(pat, text))
        opened, closed, threads = ids(r"<!--c:(\w+)-->"), ids(r"<!--/c:(\w+)-->"), ids(r"<!--co:(\w+)")
        if not (opened == closed == threads):
            errs.append(f"{rel}: unbalanced comment markers {sorted(opened ^ closed | opened ^ threads)}; restore them, never delete half a comment")
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
    return errs + check_raw(root) + check_readmes(root) + check_learning(root) + check_understanding(root) + check_notes(root)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/rstack").mkdir(parents=True)
        (root / "docs/literature-review/papers").mkdir(parents=True)
        (root / "docs/literature-review/papers/a.md").write_text("---\ncreated: x\nupdated: x\nkind: k\nvoice: v\npaper: a\n---\n")
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
        (root / "docs/inputs/2026-11-02_learning_ecg.md").write_text("---\ncreated: x\nupdated: x\nkind: k\nvoice: v\n---\n")
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
        (b / "README.md").write_text(fm + "![[figures/f.svg]]\n<!--c:q1-->t<!--/c:q1-->\n")
        e = " ".join(check(f))
        assert "embed not found: figures/f.svg" in e and "unbalanced comment markers ['q1']" in e, e
        (b / "figures").mkdir()
        if shutil.which("node"):
            (b / "README.md").write_text(fm + "```mermaid\nflowchart LR\n  A --> \n```\n")
            assert "papers/b/README.md:" in " ".join(check(f)) and "Mermaid syntax" in " ".join(check(f)), check(f)
        (b / "figures/f.svg").write_text("<svg/>")
        (b / "README.md").write_text(fm + "![[figures/f.svg]]\n<!--c:q1-->t<!--/c:q1-->\n<!--co:q1 by:me status:open\nme (x): hi\n-->\n")
        assert "papers/b" not in " ".join(check(f)), check(f)
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/literature-review/reports").mkdir(parents=True)
        (root / "docs/literature-review/reports/summary.md").write_text("x")
        e = " ".join(check_raw(root))
        assert "reports/summary.md" in e, e
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        L = root / "docs/learning"
        (L / "core").mkdir(parents=True)
        (L / "branches").mkdir()
        fm = "---\ncreated: x\nupdated: x\nkind: learning\nvoice: v\n"
        (L / "core/heart.md").write_text(fm + "---\nEnough means: x\n\nThe [[cell|heart muscle cell]] fires.\n")
        (L / "branches/cell.md").write_text(fm + "parent: heart\ndepth: 1\nstatus: unchecked\n---\nx\n")
        assert check_learning(root) == ["learning/log.md missing; write it from references/log.template.md"], check_learning(root)
        (L / "log.md").write_text("x")
        assert check_learning(root) == [], check_learning(root)
        (L / "branches/ion.md").write_text(fm + "parent: cell\ndepth: 3\nstatus: unchecked\n---\nx\n")
        (L / "branches/2026-11-04_x.md").write_text("x")
        (L / "branches/orphan.md").write_text(fm + "parent: nope\ndepth: 1\nstatus: unchecked\n---\nx\n")
        (L / "branches/bare.md").write_text(fm + "---\nx\n")
        e = " ".join(check_learning(root))
        assert "ion.md: depth must be parent depth + 1 (2)" in e and "cell.md: does not link [[ion]]" in e, e
        assert "2026-11-04_x.md: name must be" in e and "parent nope not found" in e and "bare.md: front matter missing" in e, e
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/learning/core").mkdir(parents=True)
        (root / "docs/learning/core/s.md").write_text("x")
        head = "| Concept | Level | Class | Evidence | Date |\n|---|---|---|---|---|\n"
        u = root / "docs/learning/understanding.md"
        u.write_text(head + "| a | 1 | unknown | | 2026-11-04 |\n| b | 2 | confirmed | [s](core/s.md) | 2026-11-04 |\n")
        assert check_understanding(root) == [], check_understanding(root)
        u.write_text(head + "| c | 3 | confirmed | | 2026-11-04 |\n| d | 2 | confirmed | [s](core/missing.md) | x |\n| e | 9 | x | | x |\n")
        e = " ".join(check_understanding(root))
        assert "c: level 3 needs" in e and "d: level 2 needs" in e and "e: level must be" in e, e
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
