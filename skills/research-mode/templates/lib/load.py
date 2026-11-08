"""Read an input of the current run into a table. Copied from rstack into <project>/analysis/lib/; the project owns this copy.

    from load import load
    df, tokens = load("x")      # "x" is an id from inputs.yaml that this run selected

A derived table already in the project (a .csv outside data/raw/) is read as it is. A file under
data/raw/ goes through raw-viewer: the filename grammar gives `tokens` (device, study, date, ...) and the
matched instrument profile gives the measurement data (`raw-viewer files export`). With no matching
profile this raises and names the fix; it never guesses a format.
"""
import io
import json
import os
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import yaml


def _selected(input_id):
    menu = yaml.safe_load(Path(os.environ["RSTACK_INPUTS"]).read_text())["inputs"]
    for m in menu:
        if m["id"] == input_id:
            return m
    raise KeyError(f"{input_id!r} is not selected in this run; selected: {[m['id'] for m in menu]}")


def _raw_viewer(args):
    exe = shutil.which("raw-viewer")
    if not exe:
        raise RuntimeError("raw-viewer is not on PATH; it reads files under data/raw/")
    r = subprocess.run([exe, *args], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"raw-viewer {' '.join(args[:3])} failed: {(r.stderr or r.stdout).strip()}\n"
                           "Add or enable an instrument profile for this file under data/instruments/ "
                           "(raw-viewer profiles, rawview-setup-profile).")
    return r.stdout


def load(input_id):
    m = _selected(input_id)
    project, rel = Path(os.environ["RSTACK_PROJECT"]), m["path"]
    if rel.endswith(".csv") and not rel.startswith("data/raw/"):
        return pd.read_csv(project / rel), {}
    base = ["files", "match", "--project", str(project), "--file", rel]
    tokens = json.loads(_raw_viewer(["--json", *base]))["data"].get("tokens", {})
    csv = _raw_viewer(["files", "export", "--project", str(project), "--file", rel, "--format", "csv", "--out", "-"])
    return pd.read_csv(io.StringIO(csv)), tokens
