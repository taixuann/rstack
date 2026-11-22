#!/usr/bin/env python3
"""Check a report and a draft against it. Standard library plus PyYAML.

  number_check.py report PROJECT PIECE          is docs/reports/PIECE/ complete for docs/rstack/writing/PIECE/target.md? prints file hashes
  number_check.py draft PROJECT PIECE [PATH]    every number, unit, uncertainty and citation key in the text is in the report.
                                                PATH is a file or folder; default main.tex and sections/ of docs/writing/PIECE/
  number_check.py --selftest                    runs both on tests/fixture

A target may name another piece's report with `report: <piece>` in its front matter (slides made from a paper's report).

Prints `FAIL file:line: message` and exits 1 on any FAIL. WARN and UNCHECKED never fail.
Rules are in skills/research-mode/references/report-schema.md.
"""
import hashlib, re, shutil, sys, tempfile
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, ROUND_HALF_UP
from pathlib import Path
import yaml

EVIDENCE = ["claims.yaml", "methods.yaml", "figures.yaml", "citations.yaml", "limitations.md"]
# shortcut: only a leading SI prefix is converted (mA to A, mV/s to V/s). mA/cm2 to A/m2 is not; upgrade to pint if that hurts.
PREFIX = {"": 0, "k": 3, "M": 6, "G": 9, "c": -2, "m": -3, "µ": -6, "n": -9, "p": -12, "f": -15}
NUM = r"\d+(?:\.\d+)?(?:[eE][-+]?\d+|\s*[×x]\s*10\^?\{?-?\d+\}?)?"
TOKEN = re.compile(rf"(?<![\w.^{{_])(-)?({NUM})(?:\s*±\s*({NUM}))?(?:\s?([%°µΩA-Za-z][A-Za-z0-9°µΩ/·.^{{}}-]*))?")
LABELS = r"\b(?:Fig(?:ure|s)?|Tables?|Tab|Eqs?|Equations?|Sections?|Sec|Schemes?|Refs?|Chapters?|Steps?|Supplementary \w+)\.?[\s~]*S?\d+[a-z]?(?:\s*(?:[,–-]|and)\s*S?\d+[a-z]?)*"


def dec(text):
    """'1.2 × 10^-3' or '1.2e-3' or 3.24 -> Decimal, keeping the digits as written."""
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*[×x]\s*10\^?\{?(-?\d+)\}?", str(text).strip())
    return Decimal(m.group(1)).scaleb(int(m.group(2))) if m else Decimal(str(text).strip())


def norm(unit):
    return re.sub(r"[\s^{}]", "", str(unit or "")).replace("μ", "µ").replace("²", "2").replace("³", "3")


def conv(draft_unit, report_unit):
    """Power of ten e with: draft value * 10**e is in the report's unit. None when the units differ."""
    d, r = norm(draft_unit), norm(report_unit)
    if d == r:
        return 0
    for pd, ed in PREFIX.items():
        for pr, er in PREFIX.items():
            if pd != pr and d.startswith(pd) and r.startswith(pr) and d[len(pd):] == r[len(pr):] != "":
                return ed - er
    return None


def same(d, r):
    """True, False, or 'digits' when the draft writes more decimal places than the report has."""
    nd, nr = max(0, -d.as_tuple().exponent), max(0, -r.as_tuple().exponent)
    if nd > nr:
        return "digits" if d == r else False
    q = Decimal(1).scaleb(-nd)
    return d in (r.quantize(q, ROUND_HALF_UP), r.quantize(q, ROUND_HALF_EVEN))


def front(path):
    text = path.read_text()
    return (yaml.safe_load(text.split("---", 2)[1]) or {}) if text.startswith("---") else {}


def paths(project, piece):
    """-> target.md, report folder, writing folder, bibliography. The report and its bibliography are the piece's own unless target.md names another piece."""
    docs = Path(project) / "docs"
    target = docs / "rstack" / "writing" / piece / "target.md"
    other = front(target).get("report") if target.is_file() else None
    return target, docs / "reports" / (other or piece), docs / "writing" / piece, docs / "writing" / (other or piece) / "references.bib"


def load(report, target):
    """-> entries [(id, value, unit, uncertainty or None, claim id)], set of n, citation keys, target front matter."""
    target = front(target) if target.is_file() else {}
    read = lambda f: (yaml.safe_load((report / f).read_text()) or []) if (report / f).is_file() else []
    entries, ns = [], set()
    for c in read("claims.yaml"):
        for n in c.get("numbers") or []:
            try:
                unc = n.get("uncertainty")
                entries.append((n["id"], dec(n["value"]), n.get("unit") or "", None if unc in (None, "none") else dec(unc), c["id"]))
            except (InvalidOperation, KeyError, TypeError):
                continue  # `report` names these
            if isinstance(n.get("n"), int):
                ns.add(n["n"])
    for m in read("methods.yaml"):
        if "value" in m:
            try:
                entries.append((m["id"], dec(m["value"]), m.get("unit") or "", None, None))
            except InvalidOperation:
                pass
    keys = {c["key"] for c in read("citations.yaml") if isinstance(c, dict) and "key" in c}
    return entries, ns, keys, target


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def in_source(root, source, value):
    """Is the value written in its source file, digit for digit? The link from report to analysis, checked."""
    try:
        return re.search(rf"(?<![\d.]){re.escape(str(value).strip())}(?!\d)", (root / source).read_text()) is not None
    except (OSError, UnicodeDecodeError):
        return False


def check_report(project, piece):
    root = Path(project)
    tpath, report, writing, bibfile = paths(root, piece)
    out, todo = [], lambda v: v is None or "TODO" in str(v)
    fail = lambda f, msg: out.append(f"FAIL {report / f}: {msg}")
    out += [f"FAIL {f}: missing" for f in [tpath, bibfile] + [report / e for e in EVIDENCE] if not f.is_file()]
    if out:
        return out
    target = front(tpath)
    keys = ("kind", "venue", "audience", "key_message", "claims", "stage") + (("article_type",) if target.get("kind") == "paper" else ())
    for k in keys:
        if todo(target.get(k)) or target.get(k) == []:
            out.append(f"FAIL {tpath}: front matter `{k}` is missing or TODO")
    for i, line in enumerate(tpath.read_text().splitlines(), 1):
        if "TODO" in line and not line.startswith(keys):
            out.append(f"FAIL {tpath}:{i}: still TODO")
    read = lambda f: yaml.safe_load((report / f).read_text()) or []
    claims, figures = {c.get("id"): c for c in read("claims.yaml")}, {f.get("id"): f for f in read("figures.yaml")}
    for cid in target.get("claims") or []:
        c = claims.get(cid)
        if not c:
            fail("claims.yaml", f"target.md selects {cid}, which is not here")
            continue
        if todo(c.get("statement")):
            fail("claims.yaml", f"{cid}: statement is missing or TODO")
        if c.get("figure") not in figures:
            fail("claims.yaml", f"{cid}: figure {c.get('figure')!r} is not in figures.yaml")
        if not c.get("numbers"):
            fail("claims.yaml", f"{cid}: no numbers")
        for n in c.get("numbers") or []:
            nid = n.get("id", f"{cid}.?")
            for k in ("id", "quantity", "value", "uncertainty", "uncertainty_kind", "n", "source"):
                if todo(n.get(k)):
                    fail("claims.yaml", f"{nid}: `{k}` is missing or TODO")
            if "unit" not in n or todo(n["unit"]) and n["unit"] is not None:
                fail("claims.yaml", f"{nid}: `unit` is missing or TODO (write '' for a pure number)")
            for k in ("value", "uncertainty"):
                try:
                    n.get(k) in (None, "none") or todo(n[k]) or dec(n[k])
                except InvalidOperation:
                    fail("claims.yaml", f"{nid}: `{k}` is not a number")
            if n.get("source") and not todo(n["source"]):
                if not (root / n["source"]).is_file():
                    fail("claims.yaml", f"{nid}: source {n['source']} does not exist")
                else:
                    for k in ("value", "uncertainty"):
                        if n.get(k) not in (None, "none") and not todo(n[k]) and not in_source(root, n["source"], n[k]):
                            fail("claims.yaml", f"{nid}: {k} {n[k]} is not written in {n['source']}")
    for m in read("methods.yaml"):
        for k in ("id", "fact", "source"):
            if todo(m.get(k)):
                fail("methods.yaml", f"{m.get('id', '?')}: `{k}` is missing or TODO")
        if todo(m.get("value", 0)):
            fail("methods.yaml", f"{m.get('id', '?')}: `value` is TODO")
        if m.get("source") and not todo(m["source"]):
            if not (root / m["source"]).is_file():
                fail("methods.yaml", f"{m.get('id')}: source {m['source']} does not exist")
            elif "value" in m and not todo(m["value"]) and not in_source(root, m["source"], m["value"]):
                fail("methods.yaml", f"{m.get('id')}: value {m['value']} is not written in {m['source']}")
    for f in figures.values():
        if todo(f.get("shows")):
            fail("figures.yaml", f"{f.get('id')}: `shows` is missing or TODO")
        if todo(f.get("path")) or not (root / f["path"]).is_file():
            fail("figures.yaml", f"{f.get('id')}: path {f.get('path')} does not exist")
    bib = set(re.findall(r"@\w+\{\s*([^,\s]+)", bibfile.read_text()))
    for c in read("citations.yaml"):
        if c.get("key") not in bib:
            fail("citations.yaml", f"{c.get('key')}: not in {bibfile}")
        if todo(c.get("supports")):
            fail("citations.yaml", f"{c.get('key')}: `supports` is missing or TODO")
    out += [f"HASH {f} {sha(report / f)}" for f in EVIDENCE]
    return out


def clean(line, tex):
    if tex:
        line = re.sub(r"(?<!\\)%.*", "", line)
    line = re.sub(r"<!--.*?-->|`[^`]*`", " ", line)
    line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"https?://\S+|\b10\.\d{4,}/\S+", " ", line)
    line = re.sub(r"\\(?:cite\w*|ref|eqref|autoref|[cC]ref|label|includegraphics|input|begin|end)(?:\[[^\]]*\])*\{[^}]*\}", " ", line)
    line = re.sub(r"\[[^\]]*@[^\]]*\]|\[\d+(?:\s*[,–-]\s*\d+)*\]", " ", line)
    line = re.sub(LABELS, " ", line, flags=re.I)
    line = re.sub(r"\b\d{4}-\d{2}-\d{2}\b|^\s*\d+[.)]\s|^(#+)\s*\d+(?:\.\d+)*\s", " ", line)
    for a, b in ((r"\\(?:mathrm|text|textrm)\{([^}]*)\}", r"\1"), (r"\\[,;]|~|\$", " "), (r"\\pm|\+/-", "±"), (r"\\times", "×"),
                 (r"\\mu\b|μ", "µ"), (r"\\Omega\b", "Ω"), (r"\\%", "%"), ("−", "-"), (rf"\(\s*({NUM}\s*±\s*{NUM})\s*\)", r"\1")):
        line = re.sub(a, b, line)
    return re.sub(r"\s+", " ", line)


def nearest(d, unit, entries):
    pool = [e for e in entries if unit and conv(unit, e[2]) is not None] or entries
    if not pool:
        return ""
    e = min(pool, key=lambda e: abs(e[1].scaleb(-(conv(unit, e[2]) or 0)) - d))
    return f" (nearest {e[0]} = {e[1]} {e[2]}{f' ± {e[3]}' if e[3] is not None else ''})".replace("  ", " ")


def check_draft(project, piece, path=None):
    tpath, report, writing, _ = paths(project, piece)
    entries, ns, keys, target = load(report, tpath)
    out, used, words, exempt = [], set(), 0, 0
    for f, h in (target.get("report_hashes") or {}).items():
        if not (report / f).is_file() or sha(report / f) != h:
            out.append(f"FAIL {report / f}: changed since the report was approved; go back to preparation")
    units = {norm(e[2]) for e in entries if e[2]}
    is_unit = lambda t: t == "%" or any(conv(t, u) is not None for u in units)
    texts = lambda d: sorted(p for p in d.rglob("*") if p.suffix in (".md", ".tex"))
    if path:
        files = texts(Path(path)) if Path(path).is_dir() else [Path(path)]
    else:
        files = [f for f in [writing / "main.tex"] if f.is_file()] + texts(writing / "sections")
    if not files:
        out.append(f"FAIL {path or writing}: no .tex or .md file to check")
    for path in files:
        code = False
        lines = path.read_text().splitlines()
        skip_to = lines.index("---", 1) if lines[:1] == ["---"] and "---" in lines[1:] else -1
        for i, raw in enumerate(lines, 1):
            if raw.lstrip().startswith("```"):
                code = not code
            if code or raw.lstrip().startswith("```") or i - 1 <= skip_to:
                continue
            if "rstack: not-a-result" in raw:
                exempt += 1
                continue
            at = f"{path}:{i}:"
            cited = re.findall(r"@([A-Za-z][\w:+-]*)", " ".join(re.findall(r"\[[^\]]*@[^\]]*\]", raw)))
            for group in re.findall(r"\\cite\w*(?:\[[^\]]*\])*\{([^}]*)\}", raw):
                cited += [k.strip() for k in group.split(",")]
            out += [f"FAIL {at} citation {k} is not in citations.yaml" for k in cited if k not in keys]
            line = clean(raw, path.suffix == ".tex")
            words += len(re.findall(r"[A-Za-z]{2,}", line))
            for m in re.finditer(r"\b[nN]\s*=\s*(\d+)", line):
                if int(m.group(1)) not in ns:
                    out.append(f"FAIL {at} n = {m.group(1)} is not an n in the report")
            line = re.sub(r"\b[nN]\s*=\s*\d+", " ", line)
            for m in TOKEN.finditer(line):
                sign, num, unc, tok = m.groups()
                if line[max(0, m.start() - 2):m.start()] in ("^-", "{-"):
                    continue
                if sign and m.start() and line[m.start() - 1].isalnum():
                    sign = None  # a range or a hyphen, not a minus
                tok = (tok or "").rstrip(".,;:-")
                unit = tok if tok and is_unit(tok) else ""
                if not unit and not unc and "." not in num and "e" not in num.lower() and "×" not in num:
                    out.append(f"UNCHECKED {at} {num}")
                    continue
                d = dec(num) * (-1 if sign else 1)
                shown = f"{'-' if sign else ''}{num}{f' ± {unc}' if unc else ''}{' ' + unit if unit else ''}"
                hit = digits = None
                for e in entries:
                    exp = conv(unit, e[2]) if unit else (0 if not e[2] else None)
                    if exp is None:
                        continue
                    for val, is_unc in ((e[1], False), (e[3], True)):
                        r = same(d, val.scaleb(-exp)) if val is not None else False
                        digits = digits or (r == "digits" and e)
                        if r is True and not hit:
                            hit = (e, exp, is_unc)
                if hit:
                    e, exp, is_unc = hit
                    used.add(e[0])
                    if unc and (is_unc or e[3] is None or same(dec(unc), e[3].scaleb(-exp)) is not True):
                        out.append(f"FAIL {at} {shown}: the uncertainty does not match {e[0]} = {e[1]} ± {e[3]} {e[2]}")
                    elif not unc and not is_unc and e[3] is not None:
                        out.append(f"WARN {at} {shown}: {e[0]} has an uncertainty (± {e[3]} {e[2]}) the draft leaves out")
                elif digits:
                    out.append(f"FAIL {at} {shown} has more digits than the report ({digits[0]} = {digits[1]} {digits[2]})")
                else:
                    other = next((e for e in entries if same(d, e[1]) is True), None)
                    if other:
                        why = f"is written with the unit {unit}" if unit else "is written with no unit, or with a unit the report does not use"
                        out.append(f"FAIL {at} {shown} {why}; the report has {other[0]} = {other[1]} {other[2] or '(no unit)'}")
                    else:
                        out.append(f"FAIL {at} {shown} is not in the report{nearest(d, unit, entries)}")
    chosen = target.get("claims")
    for e in entries:
        if e[4] and e[0] not in used and (not chosen or e[4] in chosen):
            out.append(f"WARN {report / 'claims.yaml'}: {e[0]} = {e[1]} {e[2]} never appears in the draft")
    out.append(f"INFO {len(files)} files, {words} words, {exempt} lines exempted with `rstack: not-a-result`")
    return out


def selftest():
    fx = Path(__file__).resolve().parent.parent / "tests/fixture"
    fails = lambda lines: [l for l in lines if l.startswith("FAIL")]
    assert conv("mA", "A") == -3 and conv("mV/s", "V/s") == -3 and conv("m", "mm") == 3 and conv("V", "A") is None
    assert same(Decimal("3.2"), Decimal("3.24")) is True and same(Decimal("3.240"), Decimal("3.24")) == "digits"
    assert dec("1.2 × 10^-3") == Decimal("0.0012")
    r = check_report(fx, "demo-paper")
    assert not fails(r) and sum(l.startswith("HASH") for l in r) == len(EVIDENCE), r
    good = check_draft(fx, "demo-paper")
    assert not fails(good), good
    assert sum(l.startswith("UNCHECKED") for l in good) == 2 and "1 lines exempted" in good[-1], good
    assert not fails(check_report(fx, "demo-talk")) and not fails(check_draft(fx, "demo-talk", fx / "docs/presentation/demo-talk")), "slides on the paper's report"
    bad = fails(check_draft(fx, "demo-paper", fx / "bad/results.tex"))
    want = ["is not in the report (nearest C1.n1", "is written with the unit mV", "uncertainty does not match", "more digits",
            "8.5 % is not in the report", "written with no unit", "n = 6 is not an n", "citation jones1999"]
    assert len(bad) == len(want), bad
    for n, (line, text) in enumerate(zip(bad, want), 1):
        assert f"results.tex:{n}:" in line and text in line, (n, line)
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "p"
        shutil.copytree(fx, p)
        t, c = p / "docs/rstack/writing/demo-paper/target.md", p / "docs/reports/demo-paper/claims.yaml"
        t.write_text(t.read_text().replace("stage: write", f"stage: write\nreport_hashes: {{claims.yaml: {sha(c)}}}"))
        assert not fails(check_draft(p, "demo-paper"))
        c.write_text(c.read_text().replace("value: '3.24'", "value: '3.25'"))
        assert any("changed since the report was approved" in l for l in check_draft(p, "demo-paper"))
        assert any("C1.n1: value 3.25 is not written in analysis/cv/summary.csv" in l for l in check_report(p, "demo-paper"))
        c.write_text(c.read_text().replace("uncertainty: '0.05'", "uncertainty: 'TODO: unknown'"))
        assert any("C1.n1: `uncertainty` is missing or TODO" in l for l in check_report(p, "demo-paper"))
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
        sys.exit(0)
    if a[:1] == ["report"] and len(a) == 3:
        res = check_report(a[1], a[2])
    elif a[:1] == ["draft"] and len(a) in (3, 4):
        res = check_draft(*a[1:])
    else:
        sys.exit(__doc__)
    print("\n".join(res))
    sys.exit(1 if any(l.startswith("FAIL") for l in res) else 0)
