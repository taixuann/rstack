#!/usr/bin/env python3
"""Figure rules for analysis figures: no title, 3-5 ticks per axis, decimal tick labels, SI-prefixed units.

Import beside the figure code:
    from figrules import si_scale, check
    y, unit = si_scale(current_in_amps, "A")       # -> values in uA, "uA"
    ...plot, set labels...
    check(fig)                                      # raises ValueError listing every violation
Call check(fig) before the figure is saved. `python3 figrules.py --selftest` tests the pure parts.
"""
import math, re, sys

PREFIX = {-15: "f", -12: "p", -9: "n", -6: "µ", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}
SCI = re.compile(r"\d[eE][+-]?\d|×\s*10|\\times")


def si_scale(values, unit):
    """Scale values so the largest magnitude lies in [1, 1000) of a prefixed unit. Returns (values, unit)."""
    vals = list(values)
    top = max((abs(v) for v in vals if v and math.isfinite(v)), default=0)
    exp = 0 if top == 0 else max(-15, min(9, 3 * math.floor(math.log10(top) / 3)))
    return [v / 10 ** exp for v in vals], PREFIX[exp] + unit


def visible(axis):
    """(location, label text) of the major ticks inside the view; the locator also returns ticks outside it, which are not drawn."""
    lo, hi = sorted(axis.get_view_interval())
    eps = 1e-9 * ((hi - lo) or 1)
    return [(x, t.get_text()) for x, t in zip(axis.get_majorticklocs(), axis.get_ticklabels()) if lo - eps <= x <= hi + eps]


def violations(axes):
    """axes: iterable of matplotlib-like Axes. Returns a list of rule violations."""
    out = []
    for i, ax in enumerate(axes):
        if ax.get_title():
            out.append(f"axes {i}: has a title; the caption carries the claim")
        for name, axis in (("x", ax.xaxis), ("y", ax.yaxis)):
            shown = visible(axis)
            n = len(shown)
            if not 3 <= n <= 5:
                out.append(f"axes {i}: {name} axis has {n} major ticks, want 3 to 5")
            if any(SCI.search(s) for _, s in shown) or axis.get_offset_text().get_text():
                out.append(f"axes {i}: {name} tick labels use scientific notation; rescale the unit instead")
    return out


def check(fig):
    fig = getattr(fig, "fig", fig)  # figrecipe's RecordingFigure keeps the matplotlib figure in .fig; its .axes holds wrappers
    fig.canvas.draw()  # tick labels exist only after a draw
    bad = violations(fig.axes)
    if bad:
        raise ValueError("figure rules:\n  " + "\n  ".join(bad))


def selftest():
    v, u = si_scale([2e-6, 5e-7], "A")
    assert u == "µA" and abs(v[0] - 2) < 1e-9 and abs(v[1] - 0.5) < 1e-9, (v, u)
    assert si_scale([1500.0], "V")[1] == "kV" and si_scale([0, 0], "V")[1] == "V" and si_scale([0.02], "V")[1] == "mV"

    class T:  # minimal stand-ins for matplotlib objects
        def __init__(self, s): self.s = s
        def get_text(self): return self.s

    class Axis:
        def __init__(self, ticks, labels, off=""): self.t, self.l, self.o = ticks, labels, off
        def get_majorticklocs(self): return self.t
        def get_view_interval(self): return (min(self.t), max(self.t))
        def get_ticklabels(self): return [T(s) for s in self.l]
        def get_offset_text(self): return T(self.o)

    class Ax:
        def __init__(self, title, x, y): self.title, self.xaxis, self.yaxis = title, x, y
        def get_title(self): return self.title

    ok = Axis([0, 1, 2, 3], ["0", "1", "2", "3"])
    assert violations([Ax("", ok, ok)]) == []
    assert any("title" in m for m in violations([Ax("T", ok, ok)]))
    assert any("2 major ticks" in m for m in violations([Ax("", Axis([0, 1], ["0", "1"]), ok)]))
    assert any("6 major ticks" in m for m in violations([Ax("", ok, Axis(range(6), list("012345")))]))
    assert any("scientific" in m for m in violations([Ax("", Axis([0, 1, 2], ["0", "1e-6", "2e-6"]), ok)]))
    assert any("scientific" in m for m in violations([Ax("", ok, Axis([0, 1, 2], ["0", "1", "2"], "1e-6"))]))
    class Wide(Axis):  # the locator returns ticks beyond the view; only the three inside count
        def get_view_interval(self): return (1, 3)
    assert violations([Ax("", Wide(range(6), list("012345")), ok)]) == [], "ticks outside the view were counted"
    print("selftest ok (duck-typed; also exercised on real figrecipe figures through style.save_figure)")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        sys.exit(__doc__)
