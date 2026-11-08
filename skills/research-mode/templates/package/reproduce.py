#!/usr/bin/env python3
"""Run every figure of this package again and compare with what was recorded. Standard library only.

    pip install -r requirements.txt
    python reproduce.py [--figure NAME] [--python PATH]

Checks first that every file still matches manifest.json, then runs each figure's script in a fresh work folder with the
recorded inputs, runs its checks script, and compares the figure data and tables with the recorded hashes. It writes
nothing into the package; results go to a temporary folder that it prints. Exit 0 only if everything matches.
A figure image can differ at the pixel level between machines; the data files are what is compared.
"""
import argparse, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--figure")
    ap.add_argument("--python", default=sys.executable)
    a = ap.parse_args()
    m = json.loads((HERE / "manifest.json").read_text())
    bad = [f"{rel}: {'missing' if not (HERE / rel).is_file() else 'differs from the manifest'}"
           for rel, d in m["files"].items() if not (HERE / rel).is_file() or sha(HERE / rel) != d]
    work = Path(tempfile.mkdtemp(prefix="reproduce-"))
    for fig, f in m["figures"].items():
        if a.figure and a.figure != fig:
            continue
        wd = work / fig
        wd.mkdir()
        env = dict(os.environ, RSTACK_INPUTS=str(HERE / f["inputs"]), RSTACK_RUN_DIR=str(wd), RSTACK_PROJECT=str(HERE),
                   RSTACK_FIGURE=fig, RSTACK_PRESETS=str(HERE / "presets"), MPLBACKEND="Agg",
                   PYTHONPATH=os.pathsep.join([str(HERE / "lib")] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])))
        r = subprocess.run([a.python, str(HERE / "scripts" / f"{fig}.py")], cwd=wd, env=env, capture_output=True, text=True)
        if r.returncode:
            bad.append(f"{fig}: the script failed\n{r.stderr.strip()}")
            continue
        checks = HERE / "scripts" / f"{fig}.checks.py"
        if checks.is_file():
            c = subprocess.run([a.python, str(checks)], cwd=wd, env=dict(env, RSTACK_OUTPUTS=str(wd)), capture_output=True, text=True)
            if c.returncode:
                bad.append(f"{fig}: its checks failed\n{(c.stdout + c.stderr).strip()}")
        for rel, digest in f["outputs"].items():
            if not (wd / rel).is_file() or sha(wd / rel) != digest:
                bad.append(f"{fig}: {rel} {'was not written' if not (wd / rel).is_file() else 'differs from the recorded run'}")
    print("\n".join(bad) or "reproduced: every file matches and every figure's data matches its recorded run")
    print(f"work folder: {work}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
