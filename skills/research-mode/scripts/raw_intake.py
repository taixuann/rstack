#!/usr/bin/env python3
"""Raw-data intake: check raw measurement filenames in data/raw/YYYY-MM-DD/, show a plan, apply it only on --apply.

Usage: raw_intake.py FOLDER [FOLDER ...] [--apply]   |   raw_intake.py --selftest
FOLDER is a date folder, or data/raw itself (every unsealed date folder under it).

Grammar: DDMMYY-HHMMSS_instrument.mode_[device-id]_library.study[_r.[remarks]][_f.[flags]][_NNN].ext
Rules (all fixes are mechanical; nothing is invented):
  - Date and time come from the file's own header, read through `raw-viewer files inspect` (profiles live in
    raw-viewer, not here). Without raw-viewer or a matching profile the filename's
    DDMMYY-HHMMSS is kept. A missing HHMMSS becomes 000000. A missing DDMMYY comes from the folder name.
  - r.x / f.x get brackets. The file moves to the date folder of its final DDMMYY. A date more than 31 days from
    its folder is not trusted: the file is left for the human.
  - Files matching a glob in <project>/data/profiles/intake.json "skip" are left exactly as they are.
  - backup*, *.tmp, ~* and empty (0-byte) files go to .quarantine/ untouched. Anything else that breaks the grammar is left for the human.
  - A folder holding .intake.log is sealed and skipped. Apply writes the log after every hash check passes.
"""
import fnmatch, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

FOLDER = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NAME = re.compile(r"^(\d{6})(?:-(\d{6}))?_(.*)\.([A-Za-z0-9]+)$")
TAIL = re.compile(r"^(?P<core>.*?)(?:_r\.(?P<r>\[[^\]]*\]|[^_\[\]]+))?(?:_f\.(?P<f>\[[^\]]*\]|[^_\[\]]+))?(?:_(?P<n>\d{3}))?$")
GRAMMAR = re.compile(r"^\d{6}-\d{6}_[a-z0-9-]+\.[a-z0-9-]+_\[[^\]]+\]_[a-z0-9-]+\.[a-z0-9-]+(_r\.\[[^\]]*\])?(_f\.\[[^\]]*\])?(_\d{3})?\.[A-Za-z0-9]+$")
ARTIFACT = re.compile(r"^(backup.*|.*\.tmp|~.*)$")
IGNORE = {".DS_Store", ".intake.log"}
RAW_VIEWER = shutil.which("raw-viewer")
STATS = {"tried": 0, "read": 0}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 16), b""):
            h.update(c)
    return h.hexdigest()


def header_stamp(p):
    """Return (DDMMYY, HHMMSS or None) from the file's own header, read through `raw-viewer files inspect`.
    Nothing is returned when raw-viewer is missing, has no profile for the file, or the header has no Date."""
    if not RAW_VIEWER:
        return None, None
    STATS["tried"] += 1
    project = p.parents[3]  # <project>/data/raw/<date>/<file>
    r = subprocess.run([RAW_VIEWER, "--json", "files", "inspect", "--project", str(project), "--file",
                        str(p.relative_to(project))], capture_output=True, text=True, timeout=30)
    try:
        meta = json.loads(r.stdout)["data"]["metadata"]
        day = datetime.strptime(meta["Date"].replace("-", "/"), "%Y/%m/%d")
    except (ValueError, KeyError, TypeError):
        return None, None
    STATS["read"] += 1
    tm = re.match(r"(\d{2}):(\d{2}):(\d{2})", meta.get("Time", ""))
    return day.strftime("%d%m%y"), "".join(tm.groups()) if tm else None


def skip_globs(folder):
    """Filename globs from <project>/data/profiles/intake.json: {"skip": ["*.ibw", "*_keysight-b1500a.*"]}."""
    cfg = folder.parent.parent / "profiles" / "intake.json"
    return json.loads(cfg.read_text()).get("skip", []) if cfg.exists() else []


def valid(dd, t):
    try:
        datetime.strptime(dd, "%d%m%y")
        datetime.strptime(t, "%H%M%S")
        return True
    except ValueError:
        return False


def iso(dd):
    return datetime.strptime(dd, "%d%m%y").strftime("%Y-%m-%d")


def plan_file(p, folder):
    """Return dict(kind, new, dest, tags) for one file. kind: ok|rename|quarantine|human."""
    name = p.name
    if ARTIFACT.match(name) or p.stat().st_size == 0:  # 0 bytes: an acquisition placeholder with no data
        return {"kind": "quarantine", "new": name, "dest": folder, "tags": ["quarantine-empty" if p.stat().st_size == 0 else "quarantine"]}
    tags = []
    m = NAME.match(name)
    if m:
        dd, t, rest, ext = m.groups()
    else:
        stem, ext = (name.rsplit(".", 1) + [""])[:2]
        dd, t, rest = None, None, stem
    tail = TAIL.match(rest)
    core = tail["core"]
    for key in ("r", "f"):
        v = tail[key]
        if v and not v.startswith("["):
            tags.append("remark-brackets")
            v = f"[{v}]"
        core += f"_{key}.{v}" if v else ""
    core += f"_{tail['n']}" if tail["n"] else ""
    hd, ht = header_stamp(p)
    fd = datetime.strptime(folder.name, "%Y-%m-%d").strftime("%d%m%y")
    if hd:
        if dd and hd != dd:
            tags.append("date-from-header(differs)")
        elif not dd or hd != dd:
            tags.append("date-from-header")
        dd = hd
    elif not dd:
        dd = fd
        tags.append("date-from-folder")
    if ht:
        if t != ht:
            tags.append("time-from-header")
        t = ht
    elif not t:
        t = "000000"
        tags.append("time-000000")
    new = f"{dd}-{t}_{core}.{ext}"
    if not valid(dd, t) or not GRAMMAR.match(new):
        return {"kind": "human", "new": new, "dest": folder, "tags": ["breaks-grammar"]}
    if abs((datetime.strptime(dd, "%d%m%y") - datetime.strptime(folder.name, "%Y-%m-%d")).days) > 31:
        return {"kind": "human", "new": new, "dest": folder, "tags": ["implausible-date"]}  # e.g. an instrument clock stuck in 2010
    dest = folder.parent / iso(dd)
    if dest != folder:
        tags.append("relocate")
    return {"kind": "ok" if new == name and dest == folder else "rename", "new": new, "dest": dest, "tags": tags}


def build(folder):
    items, skip = [], skip_globs(folder)
    for p in sorted(folder.iterdir()):
        if p.is_dir() or p.name in IGNORE:
            continue
        if any(fnmatch.fnmatch(p.name, g) for g in skip):
            items.append((p, {"kind": "skipped", "new": p.name, "dest": folder, "tags": ["skipped-by-config"]}))
            continue
        items.append((p, plan_file(p, folder)))
    seen = {}
    for p, pl in items:
        if pl["kind"] in ("rename", "ok"):
            key = pl["dest"] / pl["new"]
            seen.setdefault(key, []).append(p)
    for p, pl in items:
        if pl["kind"] == "rename":
            key = pl["dest"] / pl["new"]
            if len(seen[key]) > 1 or (key.exists() and key != p):
                pl.update(kind="human", tags=["name-collision"])
            elif pl["dest"].is_dir() and (pl["dest"] / ".intake.log").exists() and pl["dest"] != folder:
                pl.update(kind="human", tags=["destination-sealed"])
    return items


def report(folder, items):
    by = {}
    for p, pl in items:
        by.setdefault(pl["kind"], []).append((p, pl))
    print(f"\n{folder.name}: {len(items)} files  " + "  ".join(f"{k} {len(v)}" for k, v in sorted(by.items())))
    tagged = {}
    for p, pl in items:
        for t in set(pl["tags"]):
            tagged.setdefault(t, []).append((p, pl))
    for t, v in sorted(tagged.items()):
        print(f"  {t}: {len(v)}")
        for p, pl in (v if t in ("breaks-grammar", "name-collision", "destination-sealed", "implausible-date", "date-from-header(differs)") else v[:2])[:12]:
            to = {"quarantine": ".quarantine/", "human": "(left for you)", "skipped": "(untouched)"}.get(pl["kind"], f"{pl['dest'].name}/{pl['new']}")
            print(f"      {p.name}\n   -> {to}")


def apply(folder, items):
    done, log = [], []
    q = folder / ".quarantine"
    try:
        for p, pl in items:
            if pl["kind"] not in ("rename", "quarantine"):
                continue
            dst = (q / p.name) if pl["kind"] == "quarantine" else pl["dest"] / pl["new"]
            if dst == p:
                continue
            dst.parent.mkdir(exist_ok=True)
            before = sha256(p)
            os.rename(p, dst)
            done.append((dst, p))
            if sha256(dst) != before:
                raise RuntimeError(f"hash changed for {dst}")
            log.append((p.name, str(dst.relative_to(folder.parent)), before))
    except Exception:
        for dst, src in reversed(done):
            os.rename(dst, src)
        raise
    kinds = [pl["kind"] for _, pl in items]
    lines = [f"intake_at: '{datetime.now().astimezone().isoformat(timespec='seconds')}'", f"folder: '{folder.name}'",
             "status: VERIFIED", f"files_seen: {len(items)}", f"changed: {kinds.count('rename')}",
             f"quarantined: {kinds.count('quarantine')}", f"left_for_human: {kinds.count('human')}", f"skipped: {kinds.count('skipped')}", "moves:"]
    lines += [f"  - {{from: '{a}', to: '{b}', sha256: {h}}}" for a, b, h in log]
    (folder / ".intake.log").write_text("\n".join(lines) + "\n")
    return len(log)


def targets(args):
    out = []
    for a in args:
        p = Path(a).resolve()
        out += [p] if FOLDER.match(p.name) else sorted(c for c in p.iterdir() if c.is_dir() and FOLDER.match(c.name))
    return out


def main(argv):
    do_apply = "--apply" in argv
    for folder in targets([a for a in argv if a != "--apply"]):
        if (folder / ".intake.log").exists():
            print(f"{folder.name}: sealed (.intake.log), skipped")
            continue
        STATS.update(tried=0, read=0)
        items = build(folder)
        report(folder, items)
        print(f"  raw-viewer header date/time read for {STATS['read']} of {STATS['tried']} files" if RAW_VIEWER
              else "  raw-viewer not found: header date/time not used")
        if do_apply:
            print(f"  applied: {apply(folder, items)} moves, .intake.log written")
        elif any(pl["kind"] in ("rename", "quarantine", "human") for _, pl in items):
            print("  dry run: nothing changed. Re-run with --apply after approval.")


def selftest():
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw"
        d = raw / "2026-09-23"
        d.mkdir(parents=True)
        (Path(td) / "profiles").mkdir()
        (Path(td) / "profiles/intake.json").write_text(json.dumps({"skip": ["*.ibw", "*_keysight-b1500a.*"]}))

        def fake(p):  # stands in for raw-viewer: reads the LabVIEW Date/Time lines
            m = re.search(r"Date\t(\d{4})/(\d{2})/(\d{2})\nTime\t(\d{2}):(\d{2}):(\d{2})", p.read_text(errors="ignore"))
            return (f"{m[3]}{m[2]}{m[1][2:]}", m[4] + m[5] + m[6]) if m else (None, None)
        globals()["header_stamp"] = fake
        k = "LabVIEW Measurement\t\nDate\t2026/09/24\nTime\t10:36:15.79\n***End_of_Header***\n"
        files = {
            "230926-000000_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[x].txt": k,       # header moves date + time
            "230926-101010_autolab-usth.cv_[au]_cv.characterization_r.ph-8.4_001.txt": "a;b\n",  # brackets
            "230926_horiba-labram.raman_[p.1]_raman.sers.txt": "x\n",                         # missing HHMMSS
            "230926-120000_horiba-labram.raman_[p.2]_raman.sers.txt": "y\n",                  # compliant
            "backup_3.txt": "scratch", "230926-000000_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[empty].txt": "", "weird name.txt": "z", ".DS_Store": "",
        }
        for n, c in files.items():
            (d / n).write_text(c)
        items = dict((p.name, pl) for p, pl in build(d))
        assert items["230926-000000_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[x].txt"]["new"].startswith("240926-103615_")
        assert items["230926-000000_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[x].txt"]["dest"].name == "2026-09-24"
        assert items["230926-101010_autolab-usth.cv_[au]_cv.characterization_r.ph-8.4_001.txt"]["new"].endswith("r.[ph-8.4]_001.txt")
        assert items["230926_horiba-labram.raman_[p.1]_raman.sers.txt"]["new"].startswith("230926-000000_")
        assert items["230926-120000_horiba-labram.raman_[p.2]_raman.sers.txt"]["kind"] == "ok"
        far = d / "241110-160606_horiba-labram.raman_[s.1]_raman.sers.txt"
        far.write_text("i")
        assert dict((p.name, pl) for p, pl in build(d))[far.name]["tags"] == ["implausible-date"]
        far.unlink()
        for n in ("241110-160606_oxford-mfp.contact-afm_[s.1]_afm.step-height.ibw",
                  "190626-102850_keysight-b1500a.dual-sweep_[k.1]_iv.dual-sweep_r.x.csv"):
            (d / n).write_text("s")
            assert dict((p.name, pl) for p, pl in build(d))[n]["kind"] == "skipped"
            (d / n).unlink()
        assert items["230926-000000_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[empty].txt"]["tags"] == ["quarantine-empty"]
        assert items["backup_3.txt"]["kind"] == "quarantine" and items["weird name.txt"]["kind"] == "human"
        main([str(raw)])                                    # dry run changes nothing
        assert (d / "backup_3.txt").exists() and not (d / ".intake.log").exists()
        main([str(raw), "--apply"])
        assert (d / ".quarantine/backup_3.txt").exists() and (d / ".intake.log").exists()
        assert (raw / "2026-09-24/240926-103615_keithley-2400.dual-sweep_[a.1]_iv.dual-sweep_r.[x].txt").exists()
        assert not (d / ".quarantine/.intake.log").exists() and (d / "weird name.txt").exists()
        main([str(raw), "--apply"])                          # sealed: second run is a no-op
        # collision rolls back
        e = raw / "2026-10-01"
        e.mkdir()
        (e / "011026_horiba-labram.raman_[p.1]_raman.sers.txt").write_text("a")
        (e / "011026-000000_horiba-labram.raman_[p.1]_raman.sers.txt").write_text("b")
        assert sorted(pl["kind"] for _, pl in build(e)) == ["human", "ok"]  # the existing name is untouched, the colliding one waits for you
        # a hash mismatch rolls every rename back and writes no log
        f = raw / "2026-10-02"
        f.mkdir()
        (f / "021026_horiba-labram.raman_[p.1]_raman.sers.txt").write_text("a")
        orig, n = globals()["sha256"], [0]
        def lying(path):
            n[0] += 1
            return orig(path) + ("x" if n[0] % 2 == 0 else "")
        globals()["sha256"] = lying
        try:
            main([str(f), "--apply"])
            raise SystemExit("rollback did not fire")
        except RuntimeError:
            pass
        finally:
            globals()["sha256"] = orig
        assert (f / "021026_horiba-labram.raman_[p.1]_raman.sers.txt").exists() and not (f / ".intake.log").exists()
    print("selftest ok")


if __name__ == "__main__":
    selftest() if sys.argv[1:] == ["--selftest"] else main(sys.argv[1:]) if sys.argv[1:] else print(__doc__)
