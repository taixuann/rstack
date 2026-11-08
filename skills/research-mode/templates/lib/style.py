"""Figure style for every analysis script. Copied from rstack into <project>/analysis/lib/; the project owns this copy.

    from style import new_figure, save_figure, si_scale
    fig, ax = new_figure("nature-single", axes_width_mm=60, axes_height_mm=50)
    ...draw...
    save_figure(fig, "iv-sweep")        # in a script named scripts/iv-sweep.py

new_figure takes the preset by name from tools/figrecipe/presets (RSTACK_PRESETS): nature-single is a closed box,
nature-open an open L-frame (principle-frame-follows-the-data). It copies the preset into the run's config/ folder
and loads that copy. save_figure sets about 4 major ticks on linear axes, checks the figure rules (figrules.check
raises ValueError naming each violation), saves with figrecipe into figures/<figure>/ (<figure>.png, <figure>.yaml,
<figure>_data/*.csv, <figure>.pdf), and records every line width or marker size that differs from the preset in the
run's style_overrides.json. Overrides are allowed; the reviewer reads the list.
"""
import json
import os
import shutil
from pathlib import Path

import figrecipe as fr
import figrules
import yaml
from figrules import si_scale  # noqa: F401  (re-exported for scripts)
from matplotlib.ticker import MaxNLocator

_preset = {}


def new_figure(preset, **subplots_kwargs):
    src = Path(os.environ["RSTACK_PRESETS"]) / f"{preset}.yaml"
    if not src.is_file():
        raise FileNotFoundError(f"preset {preset!r} not found in {src.parent}")
    dst = Path(os.environ["RSTACK_RUN_DIR"]) / "config"
    dst.mkdir(exist_ok=True)
    shutil.copy(src, dst / src.name)
    _preset["path"] = dst / src.name
    fr.load_style(str(dst / src.name))
    subplots_kwargs.setdefault("constrained_layout", False)  # otherwise figrecipe discards the mm sizing
    return fr.subplots(**subplots_kwargs)


def overrides(fig):
    """Lines whose width, or markers whose size, differ from the loaded preset."""
    p = yaml.safe_load(_preset["path"].read_text())
    mm = 72 / 25.4
    widths = [p["lines"][k] * mm for k in ("linewidth_mm", "signal_linewidth_mm", "trace_mm") if p["lines"].get(k)]
    marker = p["markers"]["size_mm"] * mm
    out = []
    for i, ax in enumerate(getattr(fig, "fig", fig).axes):
        for j, line in enumerate(ax.lines):
            name = line.get_label() if not line.get_label().startswith('_') else f'#{j}'
            lw = line.get_linewidth()
            if not any(abs(lw - w) <= 0.05 * w for w in widths):
                out.append(f"axes {i} line {name}: width {lw:.2f} pt, preset {widths[0]:.2f} pt")
            if line.get_marker() not in (None, "None", "none", " ", "") and abs(line.get_markersize() - marker) > 0.05 * marker:
                out.append(f"axes {i} line {name}: marker {line.get_markersize():.2f} pt, preset {marker:.2f} pt")
    return out


def save_figure(fig, figure, ticks=4):
    """ticks: target number of major ticks on linear axes (the preset alone gives 7); None keeps the axes as drawn."""
    if ticks:
        for a in getattr(fig, "fig", fig).axes:
            for axis, scale in ((a.xaxis, a.get_xscale()), (a.yaxis, a.get_yscale())):
                if scale == "linear":
                    axis.set_major_locator(MaxNLocator(nbins=ticks))
    figrules.check(fig)
    if "path" in _preset and os.environ.get("RSTACK_RUN_DIR"):
        (Path(os.environ["RSTACK_RUN_DIR"]) / "style_overrides.json").write_text(json.dumps(overrides(fig)))
    out = Path("figures") / figure
    out.mkdir(parents=True, exist_ok=True)
    run_id = Path(os.environ["RSTACK_RUN_DIR"]).name if os.environ.get("RSTACK_RUN_DIR") else None
    fr.save(fig, out / f"{figure}.png")
    if run_id:  # a copy of the figure still says which run made it; a hint only, rstack_run.py check compares hashes
        from PIL import Image, PngImagePlugin
        png = out / f"{figure}.png"
        info = PngImagePlugin.PngInfo()
        im = Image.open(png)
        for k, v in getattr(im, "text", {}).items():
            info.add_text(k, v)
        info.add_text("rstack-run", run_id)
        im.save(png, pnginfo=info, dpi=im.info.get("dpi"))
    fig.savefig(out / f"{figure}.pdf", format="pdf", dpi=600, metadata={"Subject": f"rstack run {run_id}"} if run_id else None)
