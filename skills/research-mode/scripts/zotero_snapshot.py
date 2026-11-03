#!/usr/bin/env python3
"""Snapshot Zotero items and their colour-coded annotations into docs/literature-review/papers/.

Usage: zotero_snapshot.py --out DIR (--collection KEY | ITEM_KEY ...) [--refresh]
       zotero_snapshot.py --selftest
Needs the `zotero-cli` command. Writes OUT/<slug>/annotations.md per item; skips existing
files unless --refresh. The PDF is never copied; Zotero stays the library.
"""
import argparse, datetime, json, re, subprocess, sys, tempfile
from pathlib import Path

# Highlight colour -> meaning. Yellow is an assumed "general note"; change with the user.
COLORS = [
    ("Purple", "Interpretation and context"),
    ("Orange", "Methods"),
    ("Green", "Results"),
    ("Blue", "Mechanism"),
    ("Red", "Unclear or doubtful"),
    ("Yellow", "General notes"),
]


def cli(*args):
    out = subprocess.run(["zotero-cli", *args], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def slug(meta):
    first = (meta.get("creators") or [{}])[0].get("lastName", "anon")
    year = (meta.get("date") or "")[:4] or "nd"
    return re.sub(r"[^a-z0-9]+", "", first.lower()) + year


def render(key, meta, version, anns, today):
    authors = "; ".join(f'{c.get("lastName","")}, {c.get("firstName","")}'.strip(", ") for c in meta.get("creators", []))
    lines = ["---", f"zotero_key: {key}", f"zotero_version: {version}", f"snapshot: {today}",
             f"doi: {meta.get('DOI','')}", "---", "", f"# {meta.get('title','')}", "",
             f"{authors} ({(meta.get('date') or '')[:4]}). {meta.get('publicationTitle','')}", "",
             f"{len(anns)} annotations. Snapshot of Zotero; do not edit. Re-run with --refresh.", ""]
    known = {c for c, _ in COLORS}
    groups = [(c, m) for c, m in COLORS] + [(c, "Other") for c in sorted({a["color_category"] for a in anns} - known)]
    for color, meaning in groups:
        items = sorted((a for a in anns if a["color_category"] == color),
                       key=lambda a: (int(a.get("page_index") or 0), a["annotation_key"]))
        if not items:
            continue
        lines += [f"## {color}: {meaning}", ""]
        for a in items:
            text = (a.get("text") or "").strip() or f"[{a['type']}]"
            lines.append(f"- p.{a.get('page','?')}: \"{text}\"")
            if a.get("comment"):
                lines.append("  - Comment: " + " ".join(a["comment"].split()))
        lines.append("")
    return "\n".join(lines)


def paper_path(out, name, key):
    """One folder per paper: OUT/<slug>/annotations.md. A slug used by another paper gets the key appended."""
    path = Path(out) / name / "annotations.md"
    if path.exists():
        m = re.search(r"^zotero_key: (\S+)", path.read_text(), re.M)
        if m and m.group(1) != key:
            path = Path(out) / f"{name}-{key}" / "annotations.md"
    return path


def snapshot(key, out, refresh):
    data = cli("--json", "get", "metadata", key)["data"]
    meta = data["data"]
    version = data.get("version", meta.get("version", ""))
    anns = json.loads(subprocess.run(["zotero-cli", "ann", "list", "--item-key", key, "--format", "json"],
                                     capture_output=True, text=True, check=True).stdout)
    path = paper_path(out, slug(meta), key)
    if path.exists() and not refresh:
        print(f"exists, skipped: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render(key, meta, version, anns, datetime.date.today().isoformat()))
    print(f"wrote {path} ({len(anns)} annotations)")


def selftest():
    anns = [{"color_category": "Orange", "type": "highlight", "page": "2", "page_index": 2, "annotation_key": "A",
             "text": "gel-free patch", "comment": "check\nmaterial"},
            {"color_category": "Teal", "type": "note", "page": "1", "page_index": 1, "annotation_key": "B",
             "text": "", "comment": ""}]
    md = render("K", {"title": "T", "creators": [{"lastName": "Lee", "firstName": "A"}], "date": "2023-01-01"}, 5, anns, "2026-01-01")
    assert "## Orange: Methods" in md and "Comment: check material" in md and "## Teal: Other" in md and "[note]" in md
    assert slug({"creators": [{"lastName": "Van Dyke"}], "date": "2020"}) == "vandyke2020"
    with tempfile.TemporaryDirectory() as d:
        a = paper_path(d, "lee2020", "K1")
        assert a == Path(d) / "lee2020" / "annotations.md"
        a.parent.mkdir(); a.write_text("---\nzotero_key: K1\n---\n")
        assert paper_path(d, "lee2020", "K1") == a
        assert paper_path(d, "lee2020", "K2") == Path(d) / "lee2020-K2" / "annotations.md"
    print("selftest ok")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("keys", nargs="*")
    p.add_argument("--collection")
    p.add_argument("--out")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest(); sys.exit()
    if not a.out or not (a.keys or a.collection):
        p.error("need --out and --collection or item keys")
    keys = a.keys or [i["key"] for i in cli("--json", "get", "collection-items", a.collection)["data"]["items"]]
    for k in keys:
        snapshot(k, a.out, a.refresh)
