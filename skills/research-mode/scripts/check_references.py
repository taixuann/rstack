#!/usr/bin/env python3
"""Check docs/rstack/references.yaml against the files on disk.

Usage: check_references.py REFERENCES_YAML   |   check_references.py --selftest
Paths are relative to the project root (two levels above docs/rstack/).
Exit 1 and print each problem when a check fails.
"""
import sys, tempfile
from pathlib import Path
import yaml

STATUS = {"unread", "snapshotted", "read"}
REVIEW = {"needs_review", "pass", "repair", "blocked", "no_review"}
USED_IN = {"01_context", "02_aims-and-milestones", "03_literature-map",
           "04_questions-and-hypotheses", "05_methods-and-feasibility"}


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
        for f in ("snapshot", "wiki"):
            if p.get(f) and not (root / p[f]).exists():
                errs.append(f"{k}: {f} path not found: {p[f]}")
        if p.get("review") and p["review"] not in REVIEW:
            errs.append(f"{k}: review must be one of {sorted(REVIEW)}")
        if p.get("status") == "read" and p.get("review") in ("needs_review", "repair", "blocked"):
            errs.append(f"{k}: status read but review is {p['review']}")
        if p.get("status") in ("snapshotted", "read") and not p.get("snapshot"):
            errs.append(f"{k}: status {p['status']} needs a snapshot")
        if p.get("status") == "read" and not p.get("wiki"):
            errs.append(f"{k}: status read needs a wiki page")
        for u in p.get("used_in") or []:
            if u not in USED_IN:
                errs.append(f"{k}: unknown used_in {u}")
    return errs


def selftest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "docs/rstack").mkdir(parents=True)
        (root / "docs/raw/papers").mkdir(parents=True)
        (root / "docs/raw/papers/a.md").write_text("x")
        good = {"zotero": {"collection_key": "C"}, "papers": [
            {"key": "A", "cite": "X 2020", "status": "snapshotted", "snapshot": "docs/raw/papers/a.md", "used_in": ["01_context"], "review": "needs_review"}]}
        f = root / "docs/rstack/references.yaml"
        f.write_text(yaml.safe_dump(good))
        assert check(f) == [], check(f)
        good["papers"][0].update(status="read", snapshot="docs/raw/papers/missing.md", used_in=["nope"])
        f.write_text(yaml.safe_dump(good))
        e = " ".join(check(f))
        assert "not found" in e and "unknown used_in" in e and "needs a wiki" in e and "review is needs_review" in e, e
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
