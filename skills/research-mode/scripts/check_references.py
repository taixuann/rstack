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
KINDS = {"understanding", "learning", "supervisor", "result-thought", "interview", "inquiry", "brainstorm"}
SOURCES = {"chat", "interview", "supervisor-message", "assistant"}  # assistant: the inquiry and brainstorm notes it wrote
CONFIRMED = {"user", "supervisor", "no"}  # no: assistant-written, not yet confirmed
INPUT_FIELDS = {"created", "kind", "voice", "source", "topic", "report", "confirmed"}  # the body is never edited; only this front matter grows
DATED = r"\d{4}-\d{2}-\d{2}"
USED_IN = {"01_context", "02_aims-and-milestones"}


def check_raw(root):
    """Raw inputs and reports are dated; inputs carry a known kind. Files starting with . or README are skipped."""
    errs = []
    for f in sorted((root / "docs/inputs").glob("*")):
        if f.name.startswith(".") or f.name.startswith("README"):
            continue
        m = re.fullmatch(DATED + r"_([a-z-]+)_[a-z0-9-]+\.md", f.name)
        if not m or m.group(1) not in KINDS:
            errs.append(f"inputs/{f.name}: name must be <date>_<kind>_<slug>.md, kind in {sorted(KINDS)}")
            continue
        fm = front(f.read_text())
        miss = sorted(INPUT_FIELDS - set(fm))
        if miss:
            errs.append(f"inputs/{f.name}: front matter missing {miss}")
            continue
        if fm["kind"] != m.group(1):
            errs.append(f"inputs/{f.name}: kind '{fm['kind']}' differs from the kind in its name '{m.group(1)}'")
        if fm["source"] not in SOURCES:
            errs.append(f"inputs/{f.name}: source '{fm['source']}' must be one of {sorted(SOURCES)}")
        if fm["confirmed"] not in CONFIRMED:
            errs.append(f"inputs/{f.name}: confirmed '{fm['confirmed']}' must be one of {sorted(CONFIRMED)}")
        if fm["report"] != "none" and not (root / "docs/reports" / fm["report"]).is_dir():
            errs.append(f"inputs/{f.name}: report '{fm['report']}' is not a folder in docs/reports/ (use none if it feeds no report)")
    for f in sorted((root / "docs/literature-review/hyperresearch-reports").glob("*")):
        if f.name.startswith("."):
            continue
        if not re.fullmatch(DATED + r"_[a-z0-9-]+_[a-z0-9-]+\.md", f.name):
            errs.append(f"hyperresearch-reports/{f.name}: name must be <date>_<tool>_<slug>.md")
            continue
        link = front(f.read_text()).get("inquiry", "")
        if not link:
            errs.append(f"hyperresearch-reports/{f.name}: front matter needs inquiry: <file in docs/rstack/d-inquiry/>, or none, or TODO: unknown")
        elif link not in ("none", "TODO: unknown") and not (root / "docs/rstack/d-inquiry" / link).is_file():
            errs.append(f"hyperresearch-reports/{f.name}: inquiry '{link}' is not a file in docs/rstack/d-inquiry/")
    return errs


def front(text):
    """Front matter keys and values as a dict; empty when there is none."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(re.findall(r"^(\w+):[ \t]*(.*)$", m.group(1), re.M)) if m else {}


def check_readmes(root):
    """Every paper folder has a README.md, and the project README links it."""
    errs = []
    top = root / "README.md"
    rstack_top = root / "docs/rstack/README.md"
    top_text = (top.read_text() if top.exists() else "") + "\n" + (rstack_top.read_text() if rstack_top.exists() else "")
    has_readme = top.exists() or rstack_top.exists()
    for d in sorted((root / "docs/literature-review/papers").glob("*")):
        if not d.is_dir():
            continue
        rel = f"docs/literature-review/papers/{d.name}/README.md"
        short = f"../literature-review/papers/{d.name}/README.md"
        if not (d / "README.md").exists():
            errs.append(f"papers/{d.name}: README.md missing; write it from templates/literature/paper-readme.md")
        elif has_readme and rel not in top_text and short not in top_text:
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
        if "hyperresearch-reports" in f.parts:
            need = {"created", "kind", "tool", "source", "status"}  # raw leads, never edited, so no updated or voice
        if "inputs" in f.parts:
            need = {"created", "kind", "voice"}  # inputs are never edited, so no updated; check_raw checks the rest
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


LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
DOCPATH = re.compile(r"`(docs/[A-Za-z0-9_./-]+\.(?:md|tsv|yaml|csv|html))`")


def check_links(root):
    """A relative markdown link, or a backticked docs/ path, in a project document must exist. Catches renames done by hand."""
    errs = []
    for f in sorted((root / "docs").rglob("*.md")):
        rel = f.relative_to(root)
        if rel.parts[1] == "inputs" or "hyperresearch-reports" in rel.parts:
            continue  # raw: what came in is never edited, so its links are not ours to fix
        text = f.read_text()
        for m in LINK.findall(text):
            if re.match(r"[a-z]+:", m) or m.startswith("/"):
                continue
            if not (f.parent / m).exists():
                errs.append(f"{rel}: link not found: {m}")
        for m in DOCPATH.findall(text):
            if not (root / m).exists():
                errs.append(f"{rel}: path not found: {m}")
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
    return errs + check_raw(root) + check_readmes(root) + check_notes(root) + check_links(root)


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
        (root / "docs/inputs/2026-11-02_learning_ecg.md").write_text("---\ncreated: x\nkind: learning\nvoice: user\nsource: chat\ntopic: t\nreport: none\nconfirmed: user\n---\n")
        (root / "docs/inputs/notes.md").write_text("x")
        e = " ".join(check(f))
        assert "inputs/notes.md" in e and "2026-11-02_learning" not in e, e
        (root / "docs/inputs/2026-11-03_learning_bad.md").write_text("---\ncreated: x\nkind: learning\nvoice: user\nsource: chat\ntopic: t\nreport: nope\n---\n")
        e = " ".join(check(f))
        assert "2026-11-03_learning_bad.md: front matter missing ['confirmed']" in e, e
        (root / "docs/inputs/2026-11-03_learning_bad.md").write_text("---\ncreated: x\nkind: learning\nvoice: user\nsource: chat\ntopic: t\nreport: nope\nconfirmed: user\n---\n")
        assert "report 'nope' is not a folder" in " ".join(check(f))
        (root / "docs/inputs/2026-11-03_learning_bad.md").unlink()
        (root / "docs/literature-review/papers/b").mkdir()
        (root / "README.md").write_text("no links")
        e = " ".join(check(f))
        assert "papers/b: README.md missing" in e, e
        (root / "docs/literature-review/papers/b/README.md").write_text("x")
        (root / "docs/rstack/n.md").write_text("see `docs/inputs/brainstorm-old.md` and [x](gone.md)")
        e = " ".join(check(f))
        assert "path not found: docs/inputs/brainstorm-old.md" in e and "link not found: gone.md" in e, e
        (root / "docs/rstack/n.md").unlink()
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
        rp = root / "docs/literature-review/hyperresearch-reports"
        rp.mkdir(parents=True)
        (rp / "summary.md").write_text("x")
        e = " ".join(check_raw(root))
        assert "hyperresearch-reports/summary.md" in e, e
        (rp / "summary.md").unlink()
        r = rp / "2026-11-24_hyperresearch_roadmap.md"
        r.write_text("---\ncreated: x\n---\nx")
        e = " ".join(check_raw(root))
        assert "roadmap.md: front matter needs inquiry" in e, e
        r.write_text("---\ninquiry: 2026-11-05_brief.md\n---\nx")
        e = " ".join(check_raw(root))
        assert "inquiry '2026-11-05_brief.md' is not a file" in e, e
        (root / "docs/rstack/d-inquiry").mkdir(parents=True)
        (root / "docs/rstack/d-inquiry/2026-11-05_brief.md").write_text("x")
        assert "hyperresearch-reports" not in " ".join(check_raw(root))
        for ok in ("none", "TODO: unknown"):
            r.write_text(f"---\ninquiry: {ok}\n---\nx")
            assert "hyperresearch-reports" not in " ".join(check_raw(root))
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
