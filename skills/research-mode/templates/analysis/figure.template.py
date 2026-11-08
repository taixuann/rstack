"""__FIGURE__: TODO what it shows. Run through rstack_run.py, never by hand."""
from load import load
from style import new_figure, save_figure, si_scale

df, tokens = load("TODO-input-id")  # an id from inputs.yaml that the run selects
# Frame: "nature-single" (closed box) for data that crosses zero, loops, spectra, matrices; "nature-open" (L-frame)
# for distributions, kinetics, dose-response. Write the choice and the reason in docs/method.md.
fig, ax = new_figure("nature-single", axes_width_mm=60, axes_height_mm=50)
# TODO: compute, then draw. Rescale data and unit together with si_scale, e.g. y, unit = si_scale(values, "A").
ax.plot(df.iloc[:, 0], df.iloc[:, 1], id="TODO-name")
ax.set_xlabel("TODO quantity (unit)")
ax.set_ylabel("TODO quantity (unit)")
save_figure(fig, "__FIGURE__")
