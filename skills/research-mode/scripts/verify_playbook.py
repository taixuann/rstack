#!/usr/bin/env python3
"""Check that a playbook run left what its `## Done when` list asks for.

  verify_playbook.py start PLAYBOOK [--project DIR] [key=value ...]   write the marker
  verify_playbook.py check [--project DIR]                           report; clears the marker on pass
  verify_playbook.py hook                                            Stop hook (reads the hook JSON on stdin)
  verify_playbook.py --selftest

Done-when lines in playbooks/<name>.md:  `- file GLOB` (at least one match), `- cmd COMMAND` (exit 0),
`- decision` (decisions.tsv has a new row since start). {key} fills from start's key=value; {scripts} is this folder.
"""
import glob, json, os, re, shlex, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLAYBOOKS = HERE.parent / "playbooks"
MARK = ".rstack/active-playbook.json"


def rows(project):
    f = Path(project) / "docs/rstack/decisions.tsv"
    return len(f.read_text().splitlines()) if f.is_file() else 0


def done_when(name):
    text = (PLAYBOOKS / f"{name}.md").read_text()
    m = re.search(r"^## Done when\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"{name}: no '## Done when' section")
    return [l[2:].strip() for l in m.group(1).splitlines() if l.startswith("- ")]


def start(name, project, args):
    done_when(name)
    p = Path(project) / MARK
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"playbook": name, "started": time.time(), "decisions": rows(project), "args": args}))
    print(f"marker written: {p}")


def check(project):
    p = Path(project) / MARK
    mk = json.loads(p.read_text())
    fill = dict(mk["args"], scripts=str(HERE))
    miss = []
    for item in done_when(mk["playbook"]):
        kind, _, rest = item.partition(" ")
        rest = rest.format(**fill)
        if kind == "file" and not glob.glob(str(Path(project) / rest)):
            miss.append(f"missing file: {rest}")
        elif kind == "cmd":
            r = subprocess.run(rest, shell=True, cwd=project, capture_output=True, text=True)
            if r.returncode:
                miss.append(f"command failed ({rest}): {(r.stdout + r.stderr).strip()[-300:]}")
        elif kind == "decision" and rows(project) <= mk["decisions"]:
            miss.append("no new row in docs/rstack/decisions.tsv")
        elif kind not in ("file", "cmd", "decision"):
            miss.append(f"unknown Done-when item: {item}")
    if not miss:
        p.unlink()
    return mk["playbook"], miss


def find_marker(cwd):
    cwd = Path(cwd)
    for d in [cwd, *cwd.parents]:
        if (d / MARK).is_file():
            return d
    hits = list(cwd.glob("projects/*/" + MARK))
    return hits[0].parents[1] if hits else None


def hook():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    proj = find_marker(data.get("cwd") or os.getcwd())
    if not proj:
        return 0
    name, miss = check(proj)
    if not miss:
        return 0
    msg = f"Playbook '{name}' is not done:\n- " + "\n- ".join(miss)
    if data.get("stop_hook_active"):
        print(msg + "\n(reported once already; stopping)", file=sys.stderr)
        return 0
    print(msg + "\nFinish these, or tell the user what is left and why.", file=sys.stderr)
    return 2


def selftest():
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "docs/rstack").mkdir(parents=True)
        start("experimental-design", d, {})
        assert check(d)[1], "empty project must fail"
        assert hook.__name__
        des = Path(d) / "docs/rstack/design"
        des.mkdir()
        (des / "README.md").write_text("x"); (des / "e01_a.md").write_text("x")
        (Path(d) / "docs/rstack/samples.csv").write_text("unit\n")
        (Path(d) / "docs/rstack/decisions.tsv").write_text("row\n")
        name, miss = check(d)
        assert not miss, miss
        assert not (Path(d) / MARK).exists(), "marker cleared on pass"
    print("selftest ok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["--selftest"]:
        selftest()
    elif a[:1] == ["hook"]:
        sys.exit(hook())
    elif a[:1] in (["start"], ["check"]):
        proj = a[a.index("--project") + 1] if "--project" in a else os.getcwd()
        rest = [x for i, x in enumerate(a) if x != "--project" and (i == 0 or a[i - 1] != "--project")]
        if a[0] == "start":
            start(rest[1], proj, dict(x.split("=", 1) for x in rest[2:]))
        else:
            name, miss = check(proj)
            print("\n".join(miss) or f"{name}: done")
            sys.exit(1 if miss else 0)
    else:
        sys.exit(__doc__)
