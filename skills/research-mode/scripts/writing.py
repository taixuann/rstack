#!/usr/bin/env python3
"""State of one piece of writing: where it is, who owes what, and the only way through a gate.

  writing.py status PROJECT PIECE
  writing.py gate PROJECT PIECE report-approved|draft-ready|critique-passed|back-to-prepare --approved-by-user
  writing.py finding PROJECT PIECE add --round N --mode MODE --severity blocks|should-fix|note --location FILE:LINE --text "..."
  writing.py finding PROJECT PIECE set ID fixed|rejected|open [--reason "..."]
  writing.py --selftest

`gate` is the only writer of `stage` in docs/rstack/writing/PIECE/target.md. It refuses when a check fails, and it refuses
without --approved-by-user: pass that flag only after the user has said so in this conversation.
Findings live in docs/rstack/writing/PIECE/findings.tsv, one row per confirmed finding, kept across critique rounds.
Standard library plus PyYAML; uses number_check.py from the number-check skill.
"""
import argparse, csv, datetime, re, shutil, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "number-check/scripts"))
import number_check as nc  # noqa: E402

COLS = ["id", "round", "mode", "severity", "location", "finding", "status", "reason"]
LOG = ["ts", "stage", "decision", "why", "evidence", "result"]
fails = lambda lines: [l for l in lines if l.startswith("FAIL")]


def control(project, piece):
    return Path(project) / "docs/rstack/writing" / piece


def text_path(project, piece, kind):
    """Slides are checked in docs/presentation/PIECE; a paper in main.tex and sections/ (number_check's default)."""
    return Path(project) / "docs/presentation" / piece if kind == "slides" else None


def set_keys(target, **kv):
    """Rewrite front-matter keys in place, line by line, so the comments in target.md survive."""
    head, body = target.read_text().split("\n---", 1)
    lines = head.split("\n")
    for k, v in kv.items():
        lines = [l for l in lines if not re.match(rf"#?\s*{k}:", l)]
        if v is not None:
            lines.append(f"{k}: {v}")
    target.write_text("\n".join(lines) + "\n---" + body)


def log(project, piece, stage, decision, why, evidence, result):
    f = control(project, piece) / "decisions.tsv"
    new = not f.is_file()
    with f.open("a", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        if new:
            w.writerow(LOG)
        w.writerow([datetime.datetime.now().astimezone().isoformat(timespec="seconds"), stage, decision, why, evidence, result])


def init(project, piece, kind):
    """Create the folders for one piece and copy the target template. Never writes into a folder that already holds files."""
    project = Path(project)
    ctl = control(project, piece)
    text = project / ("docs/presentation" if kind == "slides" else "docs/writing") / piece
    for d in (text,):
        if d.exists() and any(d.iterdir()):
            sys.exit(f"refused: {d} already holds files; ask the user")
    for d in (ctl / "scaffold", ctl / "review", text / ("sections" if kind == "paper" else "")):
        d.mkdir(parents=True, exist_ok=True)
    t = ctl / "target.md"
    if not t.exists():
        tpl = Path(__file__).resolve().parents[1] / "templates/writing/target.md"
        t.write_text(tpl.read_text())
        set_keys(t, piece=f'"{piece}"', kind=kind)
    return f"created {ctl} and {text}; report: set `report` in target.md to the folder under docs/reports/"


def findings(project, piece):
    f = control(project, piece) / "findings.tsv"
    return list(csv.DictReader(f.open(), delimiter="\t")) if f.is_file() else []


def write_findings(project, piece, rows):
    with (control(project, piece) / "findings.tsv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, COLS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def finding_add(project, piece, a):
    rows = findings(project, piece)
    clean = lambda s: " ".join(str(s).split())
    row = dict(id=f"F{len(rows) + 1:03d}", round=a.round, mode=a.mode, severity=a.severity, location=clean(a.location),
               finding=clean(a.text), status="open", reason="")
    write_findings(project, piece, rows + [row])
    return row["id"]


def finding_set(project, piece, fid, status, reason):
    rows = findings(project, piece)
    row = next((r for r in rows if r["id"] == fid), None)
    if not row:
        sys.exit(f"refused: no finding {fid}")
    if status == "rejected" and not reason:
        sys.exit("refused: a rejected finding needs --reason, in the user's words")
    row["status"], row["reason"] = status, " ".join((reason or "").split())
    write_findings(project, piece, rows)
    if status == "rejected":
        log(project, piece, "critique", f"rejected finding {fid}", row["reason"], f"findings.tsv {fid}", "rejected")


def status(project, piece):
    target, report, writing, _ = nc.paths(project, piece)
    if not target.is_file():
        return [f"no piece {piece!r}: {target} does not exist. Use the init skill."]
    t = nc.front(target)
    kind, stage = t.get("kind"), t.get("stage")
    out = [f"piece: {piece} ({kind})   stage: {stage}"]
    rep = nc.check_report(project, piece)
    changed = [f for f, h in (t.get("report_hashes") or {}).items() if not (report / f).is_file() or nc.sha(report / f) != h]
    if t.get("report_approved") and not changed:
        out.append(f"report: approved {t['report_approved']}, files unchanged")
    elif changed:
        out.append(f"report: CHANGED since approval ({', '.join(changed)}); gate back-to-prepare, then approve again")
    else:
        out.append(f"report: not approved; the report check has {len(fails(rep))} FAIL")
    path = text_path(project, piece, kind)
    files = (sorted(path.rglob("*.md")) + sorted(path.rglob("*.tex")) if path and path.is_dir() else
             sorted((writing / "sections").glob("*.tex")) + sorted((writing / "sections").glob("*.md")))
    out.append("text:" + ("" if files else " nothing written yet"))
    for f in files:
        res = nc.check_draft(project, piece, f)
        words = int(re.search(r"(\d+) words", res[-1]).group(1))
        scaffold = (control(project, piece) / "scaffold" / f"{f.stem}.md").is_file()
        nfail = len([l for l in fails(res) if str(f) in l])
        out.append(f"  {f.name:24} scaffold {'yes' if scaffold else 'no '}  {words:5} words  number check: {nfail} FAIL")
    rows = findings(project, piece)
    opened = [r for r in rows if r["status"] == "open"]
    blocks = [r for r in opened if r["severity"] == "blocks"]
    rounds = sorted({r["round"] for r in rows})
    out.append(f"findings: {len(opened)} open ({len(blocks)} block), {sum(r['status'] == 'fixed' for r in rows)} fixed, "
               f"{sum(r['status'] == 'rejected' for r in rows)} rejected; rounds: {', '.join(rounds) or 'none'}")
    todo = control(project, piece) / "todo.md"
    open_items = len(re.findall(r"^- \[ \]", todo.read_text(), re.M)) if todo.is_file() else 0
    out.append(f"todo: {open_items} open items")
    you, me = {
        "prepare": ("answer the open items; read the report; say when you approve it",
                    f"fix the {len(fails(rep))} FAIL of the report check; ask the open items one topic at a time"),
        "write": ("state the main points; write the sections; say when the draft is ready",
                  "scaffold each section; ask questions; run the number check after each edit"),
        "critique": ("decide each open finding: fix it, or reject it with a reason; edit the text",
                     "run the checks and the critic; confirm each finding; record it in the ledger"),
    }.get(stage, ("set the stage with the init skill", "nothing until the piece is set up"))
    if t.get("critique_passed"):
        you, me = "review by co-authors and supervisor, then submission", "nothing: the critique passed"
    out += [f"next, you: {you}", f"next, assistant: {me}"]
    return out


def gate(project, piece, name, approved):
    target, report, writing, _ = nc.paths(project, piece)
    if not target.is_file():
        sys.exit(f"refused: {target} does not exist")
    if not approved:
        sys.exit("refused: a gate passes only on the user's word. Ask, then pass --approved-by-user")
    t = nc.front(target)
    stage, today = t.get("stage"), datetime.date.today().isoformat()
    need = {"report-approved": "prepare", "draft-ready": "write", "critique-passed": "critique"}
    if name in need and stage != need[name]:
        sys.exit(f"refused: {name} needs stage {need[name]}, the piece is in {stage}")
    if name == "back-to-prepare":
        set_keys(target, stage="prepare", report_approved=None, report_hashes=None, draft_ready=None, critique_passed=None)
        log(project, piece, stage, "back to preparation", "the report needs a change", str(target), "stage: prepare")
        return "stage: prepare. The report may be changed; approve it again when it is complete."
    if name == "report-approved":
        res = nc.check_report(project, piece)
        if fails(res):
            sys.exit("refused: the report check fails\n" + "\n".join(fails(res)))
        hashes = ", ".join(f"{l.split()[1]}: {l.split()[2]}" for l in res if l.startswith("HASH"))
        set_keys(target, report_approved=today, report_hashes="{" + hashes + "}", stage="write")
        log(project, piece, "prepare", "report approved by the user", "report check passed", str(report), "stage: write")
        return "stage: write. The report is frozen."
    draft = nc.check_draft(project, piece, text_path(project, piece, t.get("kind")))
    if any("no .tex or .md file" in l for l in draft):
        sys.exit("refused: there is no text yet")
    if name == "draft-ready":
        if any("changed since the report was approved" in l for l in draft):
            sys.exit("refused: a report file changed since approval\n" + "\n".join(fails(draft)))
        set_keys(target, draft_ready=today, stage="critique")
        log(project, piece, "write", "draft ready for critique, said the user", f"{len(fails(draft))} FAIL open in the number check", str(writing), "stage: critique")
        return f"stage: critique. The number check has {len(fails(draft))} FAIL to clear first."
    if fails(draft):
        sys.exit("refused: the number check fails\n" + "\n".join(fails(draft)))
    review = control(project, piece) / "review"
    missing = [m for m in ("reader", "evidence") if not list(review.glob(f"*-{m}.md"))]
    if missing:
        sys.exit(f"refused: no critic file for {' and '.join(missing)} in {review}")
    blocks = [r for r in findings(project, piece) if r["status"] == "open" and r["severity"] == "blocks"]
    if blocks:
        sys.exit("refused: findings that block are still open: " + ", ".join(r["id"] for r in blocks))
    set_keys(target, critique_passed=today)
    log(project, piece, "critique", "critique passed", "number check clean, no open finding blocks", str(review), "critique_passed")
    return "critique passed. Next: review by co-authors and supervisor."


def selftest():
    fx = Path(__file__).resolve().parents[2] / "number-check/tests/fixture"

    def refused(fn, *a):
        try:
            fn(*a)
        except SystemExit as e:
            return str(e)
        return ""

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "p"
        shutil.copytree(fx, p)
        t = control(p, "demo-paper") / "target.md"
        t.write_text(t.read_text().replace("stage: write", "stage: prepare"))
        assert "stage: prepare" in status(p, "demo-paper")[0] and "not approved" in status(p, "demo-paper")[1]
        assert "user's word" in refused(gate, p, "demo-paper", "report-approved", False)
        assert "needs stage write" in refused(gate, p, "demo-paper", "draft-ready", True)
        assert "stage: write" in gate(p, "demo-paper", "report-approved", True)
        f = nc.front(t)
        assert f["stage"] == "write" and len(f["report_hashes"]) == len(nc.EVIDENCE) and "# Target" in t.read_text()
        s = status(p, "demo-paper")
        assert "files unchanged" in s[1] and any("results.tex" in l and "0 FAIL" in l for l in s), s
        assert "stage: critique" in gate(p, "demo-paper", "draft-ready", True)
        assert "no critic file" in refused(gate, p, "demo-paper", "critique-passed", True)
        review = control(p, "demo-paper") / "review"
        review.mkdir(parents=True)
        for m in ("reader", "evidence"):
            (review / f"2026-01-01-{m}.md").write_text("fixture\n")
        a = argparse.Namespace(round="1", mode="evidence", severity="blocks", location="results.tex:3", text="fixture\tfinding")
        assert finding_add(p, "demo-paper", a) == "F001"
        assert "still open: F001" in refused(gate, p, "demo-paper", "critique-passed", True)
        assert "needs --reason" in refused(finding_set, p, "demo-paper", "F001", "rejected", None)
        finding_set(p, "demo-paper", "F001", "rejected", "out of scope for this paper")
        assert "1 rejected" in " ".join(status(p, "demo-paper"))
        assert "critique passed" in gate(p, "demo-paper", "critique-passed", True)
        log_rows = (control(p, "demo-paper") / "decisions.tsv").read_text().splitlines()
        assert len(log_rows) == 5 and log_rows[0].split("\t") == LOG, log_rows
        claims = p / "docs/reports/demo-paper/claims.yaml"
        claims.write_text(claims.read_text() + "\n")
        assert "CHANGED since approval" in status(p, "demo-paper")[1]
        gate(p, "demo-paper", "back-to-prepare", True)
        assert nc.front(t)["stage"] == "prepare" and "report_hashes" not in nc.front(t)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
        sys.exit(0)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("status", "gate", "finding", "init"):
        s = sub.add_parser(name)
        s.add_argument("project")
        s.add_argument("piece")
        if name == "init":
            s.add_argument("kind", choices=["paper", "slides"])
        if name == "gate":
            s.add_argument("name", choices=["report-approved", "draft-ready", "critique-passed", "back-to-prepare"])
            s.add_argument("--approved-by-user", action="store_true")
        if name == "finding":
            s.add_argument("action", choices=["add", "set"])
            s.add_argument("id", nargs="?")
            s.add_argument("new_status", nargs="?", choices=["fixed", "rejected", "open"])
            s.add_argument("--round")
            s.add_argument("--mode", choices=["numbers", "reader", "evidence", "referee", "prose", "people"])
            s.add_argument("--severity", choices=["blocks", "should-fix", "note"])
            s.add_argument("--location")
            s.add_argument("--text")
            s.add_argument("--reason")
    a = ap.parse_args()
    if a.cmd == "init":
        print(init(a.project, a.piece, a.kind))
    elif a.cmd == "status":
        print("\n".join(status(a.project, a.piece)))
    elif a.cmd == "gate":
        print(gate(a.project, a.piece, a.name, a.approved_by_user))
    elif a.action == "add":
        if not all((a.round, a.mode, a.severity, a.location, a.text)):
            sys.exit("refused: add needs --round --mode --severity --location --text")
        print(finding_add(a.project, a.piece, a))
    else:
        if not (a.id and a.new_status):
            sys.exit("refused: set needs ID and fixed|rejected|open")
        finding_set(a.project, a.piece, a.id, a.new_status, a.reason)
        print(f"{a.id}: {a.new_status}")
