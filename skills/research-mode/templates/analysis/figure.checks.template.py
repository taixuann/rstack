"""Checks for __FIGURE__. Exit 0 passes. Write them from the criteria in docs/method.md before the first run."""
import os
import pathlib

out = pathlib.Path(os.environ["RSTACK_OUTPUTS"]) / "figures/__FIGURE__"
assert (out / "__FIGURE___data").is_dir(), "figure data missing"
# figrecipe writes the plotted points to __FIGURE___data/<id>_x.csv and _y.csv, with no header row.
raise SystemExit("TODO: add the executable checks from docs/method.md, then delete this line")
