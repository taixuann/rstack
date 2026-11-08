"""Read an input in this package. It replaces the project's load.py, which needs raw-viewer and the project's profiles.
The raw files were read once when the package was built and the tables saved under data/derived/, so nothing here needs
raw-viewer. Same call as in the project:

    from load import load
    df, tokens = load("x")      # "x" is an id selected for this figure (RSTACK_INPUTS)
"""
import json
import os
from pathlib import Path

import pandas as pd


def load(input_id):
    sel = json.loads(Path(os.environ["RSTACK_INPUTS"]).read_text())["inputs"]
    m = next((x for x in sel if x["id"] == input_id), None)
    if m is None:
        raise KeyError(f"{input_id!r} is not selected for this figure; selected: {[x['id'] for x in sel]}")
    root = Path(os.environ["RSTACK_PROJECT"])
    if m.get("missing"):
        raise FileNotFoundError(f"{input_id}: {m['path']} is not in this package ({m['missing']}); see README, Not included")
    if m.get("derived"):
        return pd.read_csv(root / m["derived"]), json.loads((root / m["tokens"]).read_text())
    return pd.read_csv(root / m["path"]), {}
