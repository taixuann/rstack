#!/usr/bin/env python3
"""Run one figure of an analysis and record its provenance.

Usage:
  rstack_run.py run ANALYSIS_DIR --stage check|main|verify --figure NAME [--ids a,b] [--python PY] [--note TEXT]
  rstack_run.py replay RUN_DIR [--python PY]
  rstack_run.py new PROJECT_DIR NAME [--figure stage:name ...]
  rstack_run.py diff RUN_DIR_A RUN_DIR_B
  rstack_run.py lib PROJECT_DIR
  rstack_run.py tick ANALYSIS_DIR --figure NAME --approved-by-user [--run RUN_ID]
  rstack_run.py check ANALYSIS_DIR
  rstack_run.py show ANALYSIS_DIR
  rstack_run.py package ANALYSIS_DIR [--out DIR] [--replace] [--max-raw-mb N] [--exclude-raw ID,ID] [--python PY]
  rstack_run.py export ANALYSIS_DIR --figure NAME [--run RUN_ID] [--out DIR]
  rstack_run.py --selftest

ANALYSIS_DIR is <project>/analysis/<name>/ with inputs.yaml (the menu: id, path, label, legend, paths
relative to the project), README.md (a `## Tasks` section with `### Check`, `### Main`, `### Verify`
groups; each task names its figure) and scripts/<figure>.py, one script per figure or table.
new makes analysis/NAME/ from templates/analysis/ (README, inputs.yaml, docs/, scripts/), installs the lib, and for each
--figure check:iv adds scripts/iv.py, scripts/iv.checks.py and a task under ### Check. Nothing existing is overwritten.
diff lists what differs between two runs of a figure: inputs, scripts, lib, environment, outputs.
run is refused unless a task for the figure exists in --stage's group, main is refused while a check
task is open, verify while a check or main task is open.

Each run writes <project>/.rstack/provenance/<name>_<figure>/<YYYYMMDD-HHMMSS>/ holding inputs.yaml
(selected files + sha256; raw inputs are hashed, not copied; derived inputs up to 5 MB are also copied to inputs/),
scripts/ (copy), config/ (the preset the script loaded, copied by style.new_figure), env.txt, command.txt, log.txt, outputs/ (copies of what the run made), checks.txt, run.yaml.
The script runs with ANALYSIS_DIR as the working directory and RSTACK_INPUTS, RSTACK_RUN_DIR,
RSTACK_PROJECT, RSTACK_FIGURE in its environment. It may write only figures/<figure>/ and
tables/<figure>*. A figure folder must hold <figure>.yaml, <figure>_data/ and a png or pdf (what figrecipe's fr.save writes).
<project>/analysis/lib/ (shared helpers: load.py, style.py, figrules.py) is copied into each run as lib/, is on the
script's PYTHONPATH, and replay uses the copy. `lib` installs the templates from rstack's templates/lib/ into
analysis/lib/ (never overwriting; it lists files that differ). RSTACK_PRESETS is the folder of presets (replay uses the original run's config/). Style overrides the script
recorded (style_overrides.json) go into run.yaml and the warnings; they do not change the status. A warning appears
when .rstack/ is git-ignored.
The default interpreter is tools/figrecipe/.venv/bin/python above the project, else this one; it must import
figrecipe, matplotlib and pandas (use `python -m figrecipe`; the venv's console scripts have a stale shebang).
scripts/<figure>.checks.py, if present, runs after the script with RSTACK_OUTPUTS set to the run's
outputs/; exit 0 means pass. Status: failed (script error), rejected (wrong outputs), check-failed,
completed (no checks script), verified. Only a verified run gets figures/<figure>/run.txt.
tick ticks the figure's task in the README, adds a row to its Runs table and writes docs/results/<figure>.md; it needs
a verified run and --approved-by-user, which the user gives after seeing the figure and checks.txt. On a task that is
already ticked it records a re-run: the old run is listed as superseded in the results file.
show writes ANALYSIS_DIR/provenance.html: one card per figure (objective, why, runs, inputs, checks, code, log, environment), read
from what is already stored; it runs nothing. The page comes from templates/provenance.html, which gets the data from collect().
run is also refused until docs/method.md gives the figure an Objective and a Why (a `### <figure>` block with those two lines).
A run that is not verified leaves figures/ and tables/ as they were before it (what it wrote stays in its own outputs/).
tick --run RUN_ID accepts that earlier verified run instead of the latest one and puts its files back in figures/.
docs/results/<figure>.md records claim_for (the run the claim was written against; edit it once you have re-checked the claim
after a re-run) and cited (true when a manuscript will cite it). A review of a run is <run>/review.md, front matter
case, method, outcome, blocking (open blocking findings), waiver. A review that still has TODO in it, or whose blocking count differs from its 'blocks acceptance' rows, is refused. A review counts for the run it sits in, or for a later run whose
inputs, scripts, lib and figure data are identical. docs/review.md (front matter runs: {figure: run_id}, outcome, blocking, waiver)
is the whole-analysis review. check also fails a cited result whose current run has no usable review, whose claim is stale or still TODO,
or when the analysis review is missing or stale; and a figures/ folder with no verified run.
package builds ANALYSIS_DIR/package/ (or --out) from the accepted runs in docs/results/: figures named by run id, the scripts, lib and presets
the runs used, the inputs (raw files copied and hashed, plus the tables raw-viewer read from them, so raw-viewer is not needed),
a requirements.txt, a standalone reproduce.py, the provenance of each run, and a README and manifest.json generated from files. It is
refused unless every accepted result has a verified run, a claim that is not TODO and was written for that run, an Objective and a Why,
`check` passes, and all runs used the same lib. A raw file over --max-raw-mb (default 100) or named in --exclude-raw is listed, not copied.
export copies the accepted run's png and pdf (hash-checked against run.yaml) to DIR (default ANALYSIS_DIR/export) as
<run id>_<figure>.png/.pdf, so the file name is the provenance folder name. Live figures/ keeps its stable name.
replay reruns a run's saved scripts on its saved selection, refuses if an input changed, and compares
<figure>_data/ and tables/ with the original run.
"""
import argparse, ast, hashlib, json, os, platform, re, shutil, subprocess, sys, tempfile
from datetime import datetime
from pathlib import Path

import yaml

OUT = ("figures", "tables")
BEFORE = {"check": [], "main": ["check"], "verify": ["check", "main"]}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(base):
    return {str(f.relative_to(base)): sha256(f) for d in OUT if (base / d).is_dir()
            for f in sorted((base / d).rglob("*")) if f.is_file() and f.name != "run.txt"}


def project_of(analysis):
    return analysis.parents[1]


def key(analysis, figure):
    return f"{analysis.name}_{figure}"


def owned(rel, figure):
    return rel.startswith(f"figures/{figure}/") or (rel.startswith("tables/") and Path(rel).name.startswith(figure))


def select(analysis, ids):
    menu = yaml.safe_load((analysis / "inputs.yaml").read_text())["inputs"]
    known = {m["id"] for m in menu}
    if ids and (bad := set(ids) - known):
        sys.exit(f"unknown ids: {sorted(bad)}; inputs.yaml has {sorted(known)}")
    chosen = [dict(m) for m in menu if not ids or m["id"] in ids]
    root = project_of(analysis)
    for m in chosen:
        f = root / m["path"]
        if not f.is_file():
            sys.exit(f"{m['id']}: {m['path']} does not exist")
        digest = sha256(f)
        if m.get("sha256") not in (None, digest):
            sys.exit(f"{m['id']}: {m['path']} changed (inputs.yaml has a different sha256)")
        m["sha256"] = digest
    return chosen


def presets_dir(root):
    for d in [root, *root.parents]:
        if (d / "tools/figrecipe/presets").is_dir():
            return d / "tools/figrecipe/presets"
    return None


def rstack_ignored(root):
    r = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", ".rstack/provenance/x"], capture_output=True)
    return r.returncode == 0


COPY_MAX = 5 * 1024 * 1024


def new_run_dir(root, name):
    base = root / ".rstack/provenance" / name
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run, n = base / stamp, 1
    while run.exists():
        n += 1
        run = base / f"{stamp}-{n}"
    run.mkdir(parents=True)
    return run


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else f"unavailable ({cmd[0]})"


def earlier_hash_warnings(root, name, run, chosen):
    prev = sorted(p for p in (root / ".rstack/provenance" / name).glob("*/inputs.yaml") if p.parent != run)
    if not prev:
        return []
    old = {m["path"]: m["sha256"] for m in yaml.safe_load(prev[-1].read_text())["inputs"]}
    return [f"{m['path']} changed since run {prev[-1].parent.name}" for m in chosen if old.get(m["path"], m["sha256"]) != m["sha256"]]


def default_python(root):
    for d in [root, *root.parents]:
        cand = d / "tools/figrecipe/.venv/bin/python"
        if cand.is_file():
            return str(cand)
    return sys.executable


def preflight(py):
    try:
        r = subprocess.run([py, "-c", "import figrecipe, matplotlib, pandas"], capture_output=True, text=True)
    except OSError as e:
        r = subprocess.CompletedProcess([], 1, "", str(e))
    if r.returncode:
        sys.exit(f"refused: {py} cannot import figrecipe, matplotlib and pandas ({(r.stderr.strip().splitlines() or ['?'])[-1]}). "
                 "Pass --python tools/figrecipe/.venv/bin/python; never run the `figrecipe` command, its shebang is stale, use `python -m figrecipe`.")


def install_lib(project):
    src = Path(__file__).resolve().parent.parent / "templates/lib"
    dst = project / "analysis/lib"
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.glob("*.py")):
        if not (dst / f.name).exists():
            shutil.copy(f, dst / f.name)
            print(f"installed {f.name}")
        elif sha256(dst / f.name) != sha256(f):
            print(f"{f.name}: differs from the rstack template; the project copy is kept")


def new_analysis(project, name, figures):
    tpl = Path(__file__).resolve().parent.parent / "templates/analysis"
    a = project / "analysis" / name

    def put(rel, text):
        f = a / rel
        if f.exists():
            print(f"kept {rel}")
            return False
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
        print(f"created {rel}")
        return True

    put("README.md", (tpl / "README.md").read_text().replace("<Analysis name>", name))
    put("inputs.yaml", (tpl / "inputs.yaml").read_text())
    put("docs/method.md", (tpl / "method.md").read_text())
    put("docs/plan-review.md", (tpl / "plan-review.md").read_text())
    install_lib(project)
    for spec in figures:
        stage, _, fig = spec.partition(":")
        if stage not in BEFORE or not re.fullmatch(r"[\w-]+", fig):
            sys.exit(f"--figure wants stage:name with stage in {list(BEFORE)}, got {spec!r}")
        put(f"scripts/{fig}.py", (tpl / "figure.template.py").read_text().replace("__FIGURE__", fig))
        put(f"scripts/{fig}.checks.py", (tpl / "figure.checks.template.py").read_text().replace("__FIGURE__", fig))
        m = a / "docs/method.md"
        if not re.search(rf"^### {re.escape(fig)}\s*$", m.read_text(), re.M):
            m.write_text(re.sub(r"(?=^## Limits)", f"### {fig}\n\n- Objective: TODO what this figure shows or decides\n- Why: TODO the hypothesis or check it serves\n\n", m.read_text(), count=1, flags=re.M))
        text = (a / "README.md").read_text()
        if not any(names(x, fig) for _, _, x in task_list(text)):
            text = re.sub(rf"(^### {stage.capitalize()}\s*\n)", rf"\1- [ ] `{fig}` TODO: what it shows\n", text, count=1, flags=re.M)
            (a / "README.md").write_text(text)
            print(f"added task {fig!r} under {stage}")


def diff_runs(a, b):
    """Print what differs between two runs; return the number of differences."""
    out = []
    ya, yb = (yaml.safe_load((r / "run.yaml").read_text()) for r in (a, b))
    ia, ib = ({m["path"]: m["sha256"] for m in yaml.safe_load((r / "inputs.yaml").read_text())["inputs"]} for r in (a, b))
    out += [f"input {k}: {'changed' if k in ia and k in ib else 'only in ' + ('first' if k in ia else 'second')}" for k in sorted(set(ia) | set(ib)) if ia.get(k) != ib.get(k)]
    for d in ("scripts", "lib"):
        fa, fb = ({str(f.relative_to(r / d)): sha256(f) for f in sorted((r / d).rglob("*")) if f.is_file() and "__pycache__" not in f.parts} if (r / d).is_dir() else {} for r in (a, b))
        out += [f"{d}/{k}: differs" for k in sorted(set(fa) | set(fb)) if fa.get(k) != fb.get(k)]
    ea, eb = ((r / "env.txt").read_text().splitlines() for r in (a, b))
    out += [f"env: {x}" for x in sorted(set(ea) ^ set(eb))]
    oa, ob = ya["outputs"], yb["outputs"]
    out += [f"output {k}: {'differs' if k in oa and k in ob else 'only in ' + ('first' if k in oa else 'second')}" for k in sorted(set(oa) | set(ob)) if oa.get(k) != ob.get(k)]
    print("\n".join(out) or "no differences")
    return len(out)


def figrecipe_problems(outputs, figure):
    """Judge what this run wrote, not what an earlier run left in the folder."""
    mine = [k for k in outputs if k.startswith(f"figures/{figure}/")]
    if not mine:
        return []
    out = []
    if f"figures/{figure}/{figure}.yaml" not in mine:
        out.append(f"figures/{figure}/{figure}.yaml not written: save the figure with figrecipe (style.save_figure)")
    if not any(k.startswith(f"figures/{figure}/{figure}_data/") for k in mine):
        out.append(f"figures/{figure}/{figure}_data/ not written: save the figure with figrecipe (style.save_figure)")
    if not any(k.endswith((".png", ".pdf")) for k in mine):
        out.append(f"figures/{figure}/ has no png or pdf from this run")
    return out


def execute(analysis, figure, stage, ids, scripts, py, note, command, expect=None, lib=None, presets=None):
    root, name = project_of(analysis), key(analysis, figure)
    script = scripts / f"{figure}.py"
    if not script.is_file():
        sys.exit(f"missing {script}: one script per figure, named after it")
    chosen = select(analysis, ids)
    for m in chosen:
        if expect and expect.get(m["path"], m["sha256"]) != m["sha256"]:
            sys.exit(f"replay: {m['path']} differs from the original run")
    run = new_run_dir(root, name)
    warns = earlier_hash_warnings(root, name, run, chosen)
    if rstack_ignored(root):
        warns.append(".rstack/ is git-ignored: provenance is not tracked; remove it from .gitignore")
    for m in chosen:  # raw files are immutable and hashed; a derived file can be regenerated, so keep small ones
        f = root / m["path"]
        if not m["path"].startswith("data/raw/") and f.stat().st_size <= COPY_MAX:
            (run / "inputs" / m["path"]).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, run / "inputs" / m["path"])
            m["copy"] = f"inputs/{m['path']}"
    (run / "inputs.yaml").write_text(yaml.safe_dump({"inputs": chosen}, sort_keys=False))
    shutil.copytree(scripts, run / "scripts")
    lib = analysis.parent / "lib" if lib is None else lib
    if lib.is_dir():
        shutil.copytree(lib, run / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    (run / "command.txt").write_text(command + "\n")
    (run / "env.txt").write_text("\n".join([
        f"python: {sys.version.split()[0] if py == sys.executable else sh([py, '--version'])}",
        f"platform: {platform.platform()}",
        f"project git commit: {sh(['git', 'rev-parse', 'HEAD'], root)}",
        f"project git dirty: {bool(sh(['git', 'status', '--porcelain'], root))}",
        f"raw-viewer: {sh(['raw-viewer', '--version'])}",
        "packages:", sh([py, "-m", "pip", "freeze"]), ""]))
    before = tree(analysis)
    backup = Path(tempfile.mkdtemp())
    for rel in before:
        (backup / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(analysis / rel, backup / rel)
    started = datetime.now()
    env = dict(os.environ, RSTACK_INPUTS=str(run / "inputs.yaml"), RSTACK_RUN_DIR=str(run),
               RSTACK_PROJECT=str(root), RSTACK_FIGURE=figure, MPLBACKEND="Agg")
    if lib.is_dir():
        env["PYTHONPATH"] = os.pathsep.join([str(run / "lib")] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    presets = presets if presets is not None else presets_dir(root)
    if presets:
        env["RSTACK_PRESETS"] = str(presets)
    r = subprocess.run([py, str(script)], cwd=analysis, env=env, capture_output=True, text=True)
    ended = datetime.now()
    (run / "log.txt").write_text(f"start: {started.isoformat()}\nend: {ended.isoformat()}\nexit: {r.returncode}\n"
                                 f"--- stdout ---\n{r.stdout}--- stderr ---\n{r.stderr}")
    over = run / "style_overrides.json"
    style_overrides = json.loads(over.read_text()) if over.is_file() else []
    warns += [f"style override: {o}" for o in style_overrides]
    after = tree(analysis)
    # an identical rewrite still counts: new content or touched since start
    outputs = {k: v for k, v in after.items() if before.get(k) != v or (analysis / k).stat().st_mtime >= started.timestamp()}
    for rel in outputs:
        (run / "outputs" / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(analysis / rel, run / "outputs" / rel)
    problems = []
    if r.returncode == 0:
        problems += [f"{k}: outside figures/{figure}/ and tables/{figure}*; one run makes one figure" for k in outputs if not owned(k, figure)]
        problems += figrecipe_problems(outputs, figure)
        if not outputs:
            problems.append("the script wrote nothing")
    if r.returncode:
        status = "failed"
    elif problems:
        status = "rejected"
    else:
        checks = run / "scripts" / f"{figure}.checks.py"
        if checks.is_file():
            c = subprocess.run([py, str(checks)], cwd=analysis, capture_output=True, text=True,
                               env=dict(env, RSTACK_OUTPUTS=str(run / "outputs")))
            (run / "checks.txt").write_text(f"exit: {c.returncode}\n--- stdout ---\n{c.stdout}--- stderr ---\n{c.stderr}")
            status = "verified" if c.returncode == 0 else "check-failed"
        else:
            status = "completed"
            warns.append(f"scripts/{figure}.checks.py missing: the run cannot be verified or ticked")
    if status != "verified":  # a failed or rejected run must not leave its files in figures/ and tables/
        for rel in outputs:
            live = analysis / rel
            if (backup / rel).is_file():
                shutil.copy2(backup / rel, live)
            else:
                live.unlink(missing_ok=True)
                for d in live.parents:
                    if d.parent == analysis or any(d.iterdir()):
                        break
                    d.rmdir()
        warns.append(f"{status}: figures/ and tables/ restored to how they were before this run; its outputs are in {run.name}/outputs/")
    shutil.rmtree(backup, ignore_errors=True)
    if status == "verified":
        for top in {analysis / "figures" / figure} if (analysis / "figures" / figure).is_dir() else ():
            (top / "run.txt").write_text(f"{run.name}\n{os.path.relpath(run, top)}\n")
    (run / "run.yaml").write_text(yaml.safe_dump({
        "run_id": run.name, "analysis": analysis.name, "figure": figure, "stage": stage, "status": status,
        "exit_code": r.returncode, "started": started.isoformat(), "ended": ended.isoformat(),
        "selected_ids": [m["id"] for m in chosen], "outputs": outputs, "problems": problems,
        "lib": {f.name: sha256(f) for f in sorted((run / "lib").glob("*.py"))} if (run / "lib").is_dir() else {},
        "presets": sorted(f.name for f in (run / "config").glob("*")) if (run / "config").is_dir() else [],
        "style_overrides": style_overrides,
        "warnings": warns, "note": note or "", "approved_by_user": None}, sort_keys=False))
    for w in warns + problems:
        print("warning:", w)
    print(f"run {run.name}: {status.upper()}; {len(outputs)} outputs; {run}")
    return run, status


def front(path):
    """Front matter of a markdown file as a dict ({} if none)."""
    t = Path(path).read_text() if Path(path).is_file() else ""
    return (yaml.safe_load(t.split("---", 2)[1]) or {}) if t.startswith("---") and t.count("---") >= 2 else {}


def png_text(path, keyword="rstack-run"):
    """The text chunk `keyword` of a png, else None."""
    try:
        b = Path(path).read_bytes()
    except OSError:
        return None
    if not b.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    i = 8
    while i + 8 <= len(b):
        n, t = int.from_bytes(b[i:i + 4], "big"), b[i + 4:i + 8]
        if t == b"tEXt":
            k, _, v = b[i + 8:i + 8 + n].partition(b"\0")
            if k.decode("latin1") == keyword:
                return v.decode("latin1")
        i += 12 + n
    return None


def evidence(run):
    """What a result depends on: selected inputs, scripts, lib, and the figure data and tables."""
    h = lambda d: {str(f.relative_to(run / d)): sha256(f) for f in sorted((run / d).rglob("*")) if f.is_file() and "__pycache__" not in f.parts} if (run / d).is_dir() else {}
    return {"inputs": {m["path"]: m["sha256"] for m in yaml.safe_load((run / "inputs.yaml").read_text())["inputs"]},
            "scripts": h("scripts"), "lib": h("lib"),
            "outputs": {k: v for k, v in yaml.safe_load((run / "run.yaml").read_text())["outputs"].items() if comparable(k)}}


def review_usable(fm):
    return bool(fm.get("outcome")) and (int(fm.get("blocking") or 0) == 0 or bool(fm.get("waiver")))


def review_defects(path):
    """Ways a review file is not a real review: an untouched template, or a blocking count that the findings table contradicts."""
    t = Path(path).read_text()
    body = t.split("---", 2)[2] if t.startswith("---") else t
    out = ["still contains TODO"] if "TODO" in body else []
    rows = [l for l in body.splitlines() if re.match(r"\|[^|]*\|\s*blocks acceptance\s*\|", l)]
    n = int(front(path).get("blocking") or 0)
    if len(rows) != n:
        out.append(f"blocking is {n} but its findings table has {len(rows)} 'blocks acceptance' row(s)")
    return out


def review_state(root, analysis, figure):
    """(state, front matter, path): current, carried from <run>, stale, none, or no result."""
    res = analysis / "docs/results" / f"{figure}.md"
    if not res.is_file():
        return "no result", {}, None
    base = root / ".rstack/provenance" / key(analysis, figure)
    cur = base / str(front(res).get("run"))
    if (cur / "review.md").is_file():
        return "current", front(cur / "review.md"), cur / "review.md"
    older = sorted((r.parent for r in base.glob("*/review.md") if r.parent != cur), key=lambda r: r.name, reverse=True)
    if cur.is_dir():
        for r in older:
            if evidence(r) == evidence(cur):
                return f"carried from {r.name}", front(r / "review.md"), r / "review.md"
    return ("stale", front(older[0] / "review.md"), older[0] / "review.md") if older else ("none", {}, None)


def review_problems(analysis):
    """Cited results need a usable review on their current run and a claim written against it; then the whole analysis needs one."""
    root, out, cited = project_of(analysis), [], False
    for res in sorted((analysis / "docs/results").glob("*.md")):
        fm, fig = front(res), res.stem
        if not fm.get("cited"):
            continue
        cited = True
        state, rv, rpath = review_state(root, analysis, fig)
        if not state.startswith(("current", "carried")):
            out.append(f"cited result {fig}: review is {state} for run {fm.get('run')}; run a challenge review on that run")
        else:
            out += [f"cited result {fig}: its review {d}" for d in review_defects(rpath)]
            if not review_usable(rv):
                out.append(f"cited result {fig}: its review has {rv.get('blocking', 'unknown')} open blocking finding(s) and no waiver")
        if fm.get("claim_for", fm.get("run")) != fm.get("run"):
            out.append(f"cited result {fig}: the claim was written for run {fm.get('claim_for')}, the result is run {fm.get('run')}; re-check it, then set claim_for")
        if res.read_text().split("---", 2)[2].strip().startswith("TODO"):
            out.append(f"cited result {fig}: the claim is still TODO")
    if cited:
        rv = front(analysis / "docs/review.md")
        now = {r.stem: front(r).get("run") for r in (analysis / "docs/results").glob("*.md")}
        if not rv:
            out.append("cited results exist but docs/review.md (the whole-analysis review) is missing")
        elif rv.get("runs") != now:
            out.append("docs/review.md covers other runs than the accepted results now are; review the analysis again")
        else:
            out += [f"docs/review.md {d}" for d in review_defects(analysis / "docs/review.md")]
        if rv and rv.get("runs") == now and not review_usable(rv):
            out.append(f"docs/review.md has {rv.get('blocking', 'unknown')} open blocking finding(s) and no waiver")
    return out


def check(analysis):
    bad = []
    for d in sorted(p for p in (analysis / "figures").glob("*") if p.is_dir() and not (p / "run.txt").is_file()):
        bad.append(f"figures/{d.name}: no verified run (run.txt missing); run it, or remove the folder")
    for rt in sorted((analysis / "figures").glob("*/run.txt")):
        run = (rt.parent / rt.read_text().splitlines()[1]).resolve()
        ry = run / "run.yaml"
        if not ry.is_file():
            bad.append(f"{rt.parent.name}: run {run.name} not found")
            continue
        for rel, digest in yaml.safe_load(ry.read_text())["outputs"].items():
            if rel.startswith(f"figures/{rt.parent.name}/") and (not (analysis / rel).is_file() or sha256(analysis / rel) != digest):
                bad.append(f"{rel}: differs from run {run.name}")
        for png in (analysis / "figures" / rt.parent.name).glob("*.png"):
            if png_text(png) not in (None, run.name):
                bad.append(f"{png.relative_to(analysis)}: embedded run {png_text(png)} is not {run.name}")
    bad += review_problems(analysis)
    print("\n".join(bad) or "figures match their runs")
    return 1 if bad else 0


def task_list(text):
    """(group, done, text) for each checkbox under `## Tasks`; a group is a `### Name` heading."""
    sec = re.search(r"^## Tasks\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not sec:
        sys.exit("README has no '## Tasks' section; write the plan first (Analysis plan playbook)")
    out, group = [], None
    for line in sec.group(1).splitlines():
        if m := re.match(r"###\s+(\S+)", line):
            group = m.group(1).lower()
        elif m := re.match(r"\s*- \[([ xX])\] (.+)", line):
            out.append((group, m.group(1) != " ", m.group(2)))
    return out


def names(text, figure):
    return re.search(rf"(?<![\w-]){re.escape(figure)}(?![\w-])", text) is not None


def gate(analysis, stage, figure):
    """Refuse a run with no task of its own, or while an earlier group has open tasks."""
    tasks = task_list((analysis / "README.md").read_text())
    if not any(g == stage and names(t, figure) for g, _, t in tasks):
        sys.exit(f"refused: README Tasks has no {stage} task naming {figure!r}; add it in the plan first")
    for before in BEFORE[stage]:
        left = [t for g, done, t in tasks if g == before and not done]
        if left:
            sys.exit(f"refused: {len(left)} open {before} task(s) in {analysis.name}/README.md, first: {left[0]!r}. "
                     f"Run and tick the {before} tasks, or record a deviation in docs/method.md and remove the task.")


def figure_notes(analysis):
    """{figure: {"objective": str, "why": str}} from the `### <figure>` blocks of docs/method.md."""
    m = analysis / "docs/method.md"
    out = {}
    for fig, body in re.findall(r"^### ([\w-]+)\s*$(.*?)(?=^#{1,3} |\Z)", m.read_text() if m.is_file() else "", re.M | re.S):
        out[fig] = {k.lower(): v.strip() for k, v in re.findall(r"^- (Objective|Why):\s*(.*)$", body, re.M)}
    return out


def objective_gate(analysis, figure):
    n = figure_notes(analysis).get(figure, {})
    bad = [k for k in ("objective", "why") if not n.get(k) or n[k].startswith("TODO")]
    if bad:
        sys.exit(f"refused: docs/method.md needs a '### {figure}' block with '- Objective:' and '- Why:' ({', '.join(bad)} missing or TODO)")


def collect(analysis):
    """Everything the provenance page shows, read from files. Shape:
    {"analysis", "question", "analysis_review": {state none|current|stale, front, text}, "problems": [strings, what `check` would fail on for reviews],
     "figures": [{"figure", "stage", "done", "task", "objective", "why", "claim", "result": {run, claim_for, cited, superseded} or null,
      "claim_stale": bool, "review_state": "none"|"stale"|"current"|"carried from <run>"|"no result", "review": front matter dict of the review that counts,
      "lib_changed": [lib files whose live copy differs from the current run's], "runs": [
      {"run_id", "status", "approved", "note", "stage", "started", "selected_ids", "inputs": [{id, path, label, sha256}],
       "checks", "log", "env", "overrides", "warnings", "problems", "review" (the run's review.md text or null), "scripts": {name: text}, "lib": {name: text},
       "image": data-URI of the figure png or null}]}]} with runs newest first."""
    import base64
    root = project_of(analysis)
    readme = (analysis / "README.md").read_text()
    q = re.search(r"^## Question\s*$(.*?)(?=^## )", readme, re.M | re.S)
    notes = figure_notes(analysis)
    figs = []
    for stage, done, text in task_list(readme):
        m = re.match(r"`([\w-]+)`", text)
        if not m:
            continue
        fig = m.group(1)
        res = analysis / "docs/results" / f"{fig}.md"
        claim = res.read_text().split("---", 2)[2].strip() if res.is_file() else ""
        runs = []
        for ry_f in sorted((root / ".rstack/provenance" / key(analysis, fig)).glob("*/run.yaml"), reverse=True):
            run, ry = ry_f.parent, yaml.safe_load(ry_f.read_text())
            rd = lambda f: (run / f).read_text() if (run / f).is_file() else ""
            png = run / "outputs/figures" / fig / f"{fig}.png"
            runs.append({
                "run_id": ry["run_id"], "status": ry["status"], "approved": ry.get("approved_by_user"), "note": ry.get("note", ""),
                "stage": ry["stage"], "started": ry["started"], "selected_ids": ry["selected_ids"],
                "inputs": yaml.safe_load(rd("inputs.yaml") or "inputs: []")["inputs"],
                "checks": rd("checks.txt"), "log": rd("log.txt"), "env": rd("env.txt"),
                "overrides": ry.get("style_overrides", []), "warnings": ry.get("warnings", []), "problems": ry.get("problems", []),
                "scripts": {f.name: f.read_text() for f in sorted((run / "scripts").glob("*.py"))} if (run / "scripts").is_dir() else {},
                "lib": {f.name: f.read_text() for f in sorted((run / "lib").glob("*.py"))} if (run / "lib").is_dir() else {},
                "review": rd("review.md") or None,
                "image": "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode() if png.is_file() else None})
        rf = front(res)
        cur = root / ".rstack/provenance" / key(analysis, fig) / str(rf.get("run"))
        live_lib = {f.name: sha256(f) for f in sorted((analysis.parent / "lib").glob("*.py"))}
        state, rv, _ = review_state(root, analysis, fig)
        figs.append({"figure": fig, "stage": stage, "done": done, "task": text, "claim": claim, "runs": runs,
                     "result": {"run": rf.get("run"), "claim_for": rf.get("claim_for"), "cited": bool(rf.get("cited")), "superseded": rf.get("superseded", [])} if rf else None,
                     "claim_stale": bool(rf) and rf.get("claim_for", rf.get("run")) != rf.get("run"),
                     "review_state": state, "review": rv,
                     "lib_changed": sorted(k for k, v in (yaml.safe_load((cur / "run.yaml").read_text()).get("lib", {}) if (cur / "run.yaml").is_file() else {}).items() if live_lib.get(k) != v),
                     "objective": notes.get(fig, {}).get("objective", ""), "why": notes.get(fig, {}).get("why", "")})
    ar = analysis / "docs/review.md"
    now = {r.stem: front(r).get("run") for r in (analysis / "docs/results").glob("*.md")}
    return {"analysis": analysis.name, "question": q.group(1).strip() if q else "", "figures": figs,
            "analysis_review": {"state": "none" if not ar.is_file() else "current" if front(ar).get("runs") == now else "stale",
                                "front": front(ar), "text": ar.read_text() if ar.is_file() else ""},
            "problems": review_problems(analysis)}


def show(analysis):
    tpl = Path(__file__).resolve().parent.parent / "templates/provenance.html"
    out = analysis / "provenance.html"
    out.write_text(tpl.read_text().replace("/*__DATA__*/null", json.dumps(collect(analysis)).replace("</", "<\\/")))
    print(f"wrote {out}")


def write_result(analysis, figure, ry):
    """docs/results/<figure>.md: one accepted result. A re-run keeps the claim and lists the old run as superseded."""
    f = analysis / "docs/results" / f"{figure}.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    claim, superseded, claim_for, cited = "TODO: the claim this figure supports, with n and what the spread is.", [], ry["run_id"], False
    if f.is_file():
        _, head, body = f.read_text().split("---", 2)
        old = yaml.safe_load(head)
        superseded = [r for r in old.get("superseded", []) + [old["run"]] if r != ry["run_id"]]
        claim, claim_for, cited = body.strip(), old.get("claim_for", old["run"]), bool(old.get("cited"))
    head = {"figure": figure, "run": ry["run_id"], "accepted": ry["approved_by_user"], "stage": ry["stage"],
            "inputs": ry["selected_ids"], "path": f"figures/{figure}/{figure}.png", "claim_for": claim_for, "cited": cited,
            "objective": figure_notes(analysis).get(figure, {}).get("objective", "")}
    if superseded:
        head["superseded"] = superseded
    f.write_text("---\n" + yaml.safe_dump(head, sort_keys=False) + "---\n\n" + claim + "\n")
    return superseded[-1] if superseded else None


def tick(analysis, figure, approved, run_id=None):
    if not approved:
        sys.exit("refused: show the user the figure and checks.txt first, then pass --approved-by-user")
    root, name = project_of(analysis), key(analysis, figure)
    runs = sorted((root / ".rstack/provenance" / name).glob("*/run.yaml"), key=lambda p: p.parent.name)
    if not runs:
        sys.exit(f"refused: no run of {figure!r} yet")
    if run_id:
        runs = [r for r in runs if r.parent.name == run_id]
        if not runs:
            sys.exit(f"refused: no run {run_id!r} of {figure!r}")
    ry = yaml.safe_load(runs[-1].read_text())
    if ry["status"] != "verified":
        sys.exit(f"refused: run {ry['run_id']} is {ry['status']}, not verified")
    if front(analysis / "docs/results" / f"{figure}.md").get("run") == ry["run_id"]:
        sys.exit(f"refused: run {ry['run_id']} was already approved and is the accepted result; run the figure again for a new result")
    if run_id:  # accepting an earlier run: put its files back
        for rel, digest in ry["outputs"].items():
            src = runs[-1].parent / "outputs" / rel
            if not src.is_file() or sha256(src) != digest:
                sys.exit(f"refused: {rel} in run {run_id} no longer matches its recorded hash")
        for d in (analysis / "figures" / figure, *analysis.glob(f"tables/{figure}*")):
            shutil.rmtree(d) if d.is_dir() else d.unlink(missing_ok=True)
        for rel in ry["outputs"]:
            if owned(rel, figure):
                (analysis / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(runs[-1].parent / "outputs" / rel, analysis / rel)
        (analysis / "figures" / figure / "run.txt").write_text(f"{ry['run_id']}\n{os.path.relpath(runs[-1].parent, analysis / 'figures' / figure)}\n")
    readme = analysis / "README.md"
    text = readme.read_text()
    mine = [(done, t) for g, done, t in task_list(text) if g == ry["stage"] and names(t, figure)]
    if len(mine) != 1:
        sys.exit(f"refused: expected one {ry['stage']} task naming {figure!r}, found {len(mine)}")
    done, task = mine[0]
    if not done:
        text = re.sub(rf"^(\s*- \[) (\] {re.escape(task)})$", r"\1x\2", text, count=1, flags=re.M)
    ry["approved_by_user"] = ry.get("approved_by_user") or datetime.now().isoformat()
    replaced = write_result(analysis, figure, ry)
    note = f"re-run, replaces {replaced}" if done else (ry["note"] or figure)
    row = f"| {ry['run_id']} | {','.join(ry['selected_ids']) or 'all'} | {note} | verified |\n"
    if re.search(r"^## Runs\s*$", text, re.M):
        text = re.sub(r"(^## Runs\s*$.*?)(?=^## |\Z)", lambda m: m.group(1).rstrip("\n") + "\n" + row + "\n", text, count=1, flags=re.M | re.S)
    else:
        text = text.rstrip("\n") + "\n\n## Runs\n\n| run | inputs | note | status |\n|---|---|---|---|\n" + row
    readme.write_text(text)
    runs[-1].write_text(yaml.safe_dump(ry, sort_keys=False))
    print(f"{'recorded a re-run of' if done else 'ticked'} {task!r}; run {ry['run_id']} in the Runs table; docs/results/{figure}.md written")


PACKAGE_TEMPLATES = Path(__file__).resolve().parent.parent / "templates/package"


def _package(analysis, out=None, max_raw_mb=100, exclude=(), replace=False, py=None):
    root, out = project_of(analysis), Path(out) if out else analysis / "package"
    results = sorted((analysis / "docs/results").glob("*.md"))
    if not results:
        sys.exit("refused: docs/results/ has no accepted result; tick a verified run first")
    notes, accepted, problems = figure_notes(analysis), {}, []
    qm = re.search(r"^## Question\s*$(.*?)(?=^## )", (analysis / "README.md").read_text(), re.M | re.S)
    if not qm or qm.group(1).strip().startswith("TODO") or not qm.group(1).strip():
        problems.append("the analysis README has no Question; the package never writes one for you")
    for r in results:
        fm, fig = front(r), r.stem
        run = root / ".rstack/provenance" / key(analysis, fig) / str(fm.get("run"))
        ry = yaml.safe_load((run / "run.yaml").read_text()) if (run / "run.yaml").is_file() else {}
        claim = r.read_text().split("---", 2)[2].strip()
        if ry.get("status") != "verified":
            problems.append(f"{fig}: run {fm.get('run')} is not a verified run")
        if not claim or claim.startswith("TODO"):
            problems.append(f"{fig}: the claim in docs/results/{fig}.md is still TODO; the package never writes a claim for you")
        if fm.get("claim_for", fm.get("run")) != fm.get("run"):
            problems.append(f"{fig}: the claim was written for run {fm.get('claim_for')}, the result is run {fm.get('run')}; re-check it and set claim_for")
        if any(not notes.get(fig, {}).get(k) or notes[fig][k].startswith("TODO") for k in ("objective", "why")):
            problems.append(f"{fig}: docs/method.md has no Objective and Why for it")
        accepted[fig] = (run, ry, claim, fm)
    if not problems:
        runs = list(accepted.values())
        for what, getter in (("lib", lambda run, ry: ry.get("lib", {})),
                             ("preset", lambda run, ry: {f.name: sha256(f) for f in sorted((run / "config").glob("*"))} if (run / "config").is_dir() else {})):
            seen = {}
            for fig, (run, ry, _, _) in accepted.items():
                for name, digest in getter(run, ry).items():
                    if seen.setdefault(name, (digest, fig))[0] != digest:
                        problems.append(f"{what} {name} differs between {seen[name][1]} and {fig}; run the older figure again so all use one version")
    if check(analysis):
        problems.append("rstack_run.py check fails (see above)")
    if problems:
        sys.exit("refused:\n  " + "\n  ".join(problems))
    if out.exists() and any(out.iterdir()):
        if not replace:
            sys.exit(f"refused: {out} is not empty; the package is derived, so pass --replace to rebuild it")
        shutil.rmtree(out)
    for d in ("figures", "provenance", "scripts", "lib", "presets", "inputs", "data", "docs"):
        (out / d).mkdir(parents=True, exist_ok=True)
    manifest_figs, excluded = {}, []
    py = py or default_python(root)
    for fig, (run, ry, claim, fm) in accepted.items():
        export(analysis, fig, fm["run"], out / "figures")
        prov = out / "provenance" / fig
        shutil.copytree(run / "outputs", prov / "outputs")
        for f in ("run.yaml", "inputs.yaml", "checks.txt", "env.txt", "log.txt", "command.txt", "review.md"):
            if (run / f).is_file():
                shutil.copy2(run / f, prov / f)
        for f in (f"{fig}.py", f"{fig}.checks.py"):
            if (run / "scripts" / f).is_file():
                shutil.copy2(run / "scripts" / f, out / "scripts" / f)
        for f in sorted((run / "lib").glob("*.py")) if (run / "lib").is_dir() else ():
            if f.name != "load.py":
                shutil.copy2(f, out / "lib" / f.name)
        if (run / "config").is_dir():
            for f in (run / "config").glob("*"):
                shutil.copy2(f, out / "presets" / f.name)
        pkg_inputs = []
        for m in yaml.safe_load((run / "inputs.yaml").read_text())["inputs"]:
            rel, entry = m["path"], {k: m[k] for k in ("id", "path", "label", "legend", "sha256") if k in m}
            src = run / m["copy"] if m.get("copy") else root / rel
            if not src.is_file() or sha256(src) != m["sha256"]:
                sys.exit(f"refused: {rel} ({m['id']}) no longer matches the hash recorded by run {run.name}")
            raw = rel.startswith("data/raw/")
            why = "excluded by --exclude-raw" if m["id"] in exclude else f"larger than {max_raw_mb} MB" if raw and src.stat().st_size > max_raw_mb * 1048576 else None
            if why:
                entry["missing"] = why
                excluded.append(f"{m['id']} ({rel}): {why}")
            else:
                (out / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, out / rel)
                if raw and (run / "lib/load.py").is_file():
                    export_derived(run, root, m, out, entry, py)
            pkg_inputs.append(entry)
        (out / "inputs" / f"{fig}.json").write_text(json.dumps({"inputs": pkg_inputs}, indent=1))
        manifest_figs[fig] = {"run": fm["run"], "stage": ry["stage"], "inputs": f"inputs/{fig}.json", "selected_ids": ry["selected_ids"],
                              "outputs": {k: v for k, v in ry["outputs"].items() if comparable(k)}}
    shutil.copy2(PACKAGE_TEMPLATES / "load.py", out / "lib/load.py")
    shutil.copy2(PACKAGE_TEMPLATES / "reproduce.py", out / "reproduce.py")
    (out / "requirements.txt").write_text("\n".join(requirements(py, [*(out / "scripts").glob("*.py"), *(out / "lib").glob("*.py")], {f.stem for f in (out / "lib").glob("*.py")})) + "\n")
    for src, dst in (("README.md", "docs/analysis-README.md"), ("docs/method.md", "docs/method.md"), ("docs/review.md", "docs/review.md")):
        if (analysis / src).is_file():
            shutil.copy2(analysis / src, out / dst)
    shutil.copytree(analysis / "docs/results", out / "docs/results", dirs_exist_ok=True)
    pyver = next((l.split(":", 1)[1].strip().removeprefix("Python ") for run, *_ in accepted.values() for l in (run / "env.txt").read_text().splitlines() if l.startswith("python:")), "unknown")
    todo = [t for _, _, t in task_list((analysis / "README.md").read_text()) if not any(names(t, f) for f in accepted)]
    (out / "README.md").write_text(package_readme(analysis, accepted, notes, excluded, todo, pyver, root))
    files = {str(f.relative_to(out)): sha256(f) for f in sorted(out.rglob("*")) if f.is_file() and "__pycache__" not in f.parts}
    (out / "manifest.json").write_text(json.dumps({
        "analysis": analysis.name, "built": datetime.now().isoformat(timespec="seconds"), "python": pyver,
        "figures": manifest_figs, "excluded_inputs": excluded,
        "replaced": {"lib/load.py": "the project's loader needs raw-viewer; this one reads the tables exported at build time"},
        "files": files}, indent=1))
    print(f"package built: {out} ({len(files)} files, {len(manifest_figs)} figures); prove it with: python {out / 'reproduce.py'}")
    return out


def package(analysis, out=None, max_raw_mb=100, exclude=(), replace=False, py=None):
    """Build the package; a build that is refused halfway leaves no folder behind."""
    dst = Path(out) if out else analysis / "package"
    kept = dst.exists() and any(dst.iterdir()) and not replace
    try:
        return _package(analysis, out, max_raw_mb, exclude, replace, py)
    except SystemExit:
        if not kept:
            shutil.rmtree(dst, ignore_errors=True)
        raise


def requirements(py, files, local):
    """name==version of the packages the scripts and lib import, as installed for the interpreter the runs used."""
    mods = set()
    for f in files:
        for n in ast.walk(ast.parse(f.read_text())):
            if isinstance(n, ast.Import):
                mods |= {a.name.split(".")[0] for a in n.names}
            elif isinstance(n, ast.ImportFrom) and not n.level and n.module:
                mods.add(n.module.split(".")[0])
    mods -= local | set(sys.stdlib_module_names)
    code = "import sys, importlib.metadata as m; d = m.packages_distributions(); [print(n + '==' + m.version(n)) for x in sys.argv[1:] for n in sorted(set(d.get(x, [])))]"
    r = subprocess.run([py, "-c", code, *sorted(mods)], capture_output=True, text=True)
    return sorted(set(r.stdout.split()))


def export_derived(run, root, m, out, entry, py):
    """Read one raw input through the project's own load.py (raw-viewer) and save the table and tokens in the package."""
    d = out / "data/derived"
    d.mkdir(parents=True, exist_ok=True)
    sel = out / "data/derived" / f".{m['id']}.select.json"
    sel.write_text(json.dumps({"inputs": [m]}))
    code = ("import json,sys; from load import load; df, t = load(sys.argv[1]); "
            "df.to_csv(sys.argv[2], index=False); open(sys.argv[3], 'w').write(json.dumps(t))")
    env = dict(os.environ, RSTACK_INPUTS=str(sel), RSTACK_PROJECT=str(root), PYTHONPATH=str(run / "lib"))
    r = subprocess.run([py, "-c", code, m["id"], str(d / f"{m['id']}.csv"), str(d / f"{m['id']}.tokens.json")], env=env, capture_output=True, text=True)
    sel.unlink()
    if r.returncode:
        sys.exit(f"refused: could not read {m['id']} ({m['path']}) the way the run did: {(r.stderr or r.stdout).strip().splitlines()[-1]}")
    entry["derived"], entry["tokens"] = f"data/derived/{m['id']}.csv", f"data/derived/{m['id']}.tokens.json"


def package_readme(analysis, accepted, notes, excluded, todo, pyver, root):
    """Built only from files. Claims, objectives and run ids are copied, never written here."""
    q = re.search(r"^## Question\s*$(.*?)(?=^## )", (analysis / "README.md").read_text(), re.M | re.S)
    out = [f"# {analysis.name}: results package", "",
           "Built by `rstack_run.py package` from the accepted runs of this analysis. Every claim, objective and run id below is copied from the file named; nothing is worded by hand.",
           "", "## Question", "", (q.group(1).strip() if q else "TODO: not in the analysis README"), "",
           "## Run it", "", f"Python {pyver} was used. Install what the scripts need, then rerun every figure and compare:", "",
           "```", "pip install -r requirements.txt", "python reproduce.py", "```", "",
           "`reproduce.py` checks every file against `manifest.json`, runs each script on the recorded inputs, runs its checks, and compares the figure data. No virtual environment is included. `requirements.txt` lists the packages the scripts import, at the versions used; the full environment of each run is in `provenance/<figure>/env.txt`.", "",
           "## Figures", ""]
    for fig, (run, ry, claim, fm) in accepted.items():
        ids = ", ".join(f"{i}" for i in ry["selected_ids"]) or "all inputs"
        rv = review_state(root, analysis, fig)
        out += [f"### {fig}", "", f"![{fig}](figures/{fm['run']}_{fig}.png)", "",
                f"- Objective (docs/method.md): {notes[fig]['objective']}", f"- Why (docs/method.md): {notes[fig]['why']}",
                f"- Claim (docs/results/{fig}.md): {claim}", f"- Run: `{fm['run']}`, inputs: {ids}",
                f"- Review: {rv[0]}" + (f", outcome {rv[1].get('outcome')}" if rv[1] else ""), f"- Provenance: `provenance/{fig}/`", ""]
    out += ["## Not included", ""]
    out += [f"- Raw input {x}" for x in excluded] + [f"- Task with no accepted result: {t}" for t in todo] or ["- Nothing."]
    out += ["", "## Contents", "", "`figures/` images named by run id; `scripts/` and `lib/` the code the runs used (`lib/load.py` reads the tables in `data/derived/`); "
            "`presets/` figure presets; `data/` the inputs; `inputs/` per-figure selections; `provenance/` each run's record; `docs/` plan, method, results and reviews; `manifest.json` every file's hash.", ""]
    return "\n".join(out)


def export(analysis, figure, run_id=None, out=None):
    root = project_of(analysis)
    res = front(analysis / "docs/results" / f"{figure}.md")
    run_id = run_id or res.get("run")
    if not run_id:
        sys.exit(f"refused: {figure!r} has no accepted result; tick a verified run first")
    run = root / ".rstack/provenance" / key(analysis, figure) / run_id
    ry = yaml.safe_load((run / "run.yaml").read_text()) if (run / "run.yaml").is_file() else {}
    if ry.get("status") != "verified":
        sys.exit(f"refused: run {run_id} is not a verified run of {figure!r}")
    out = Path(out) if out else analysis / "export"
    out.mkdir(parents=True, exist_ok=True)
    made = []
    for rel, digest in ry["outputs"].items():
        src = run / "outputs" / rel
        if rel.startswith(f"figures/{figure}/{figure}.") and rel.endswith((".png", ".pdf")):
            if not src.is_file() or sha256(src) != digest:
                sys.exit(f"refused: {rel} in run {run_id} no longer matches its recorded hash")
            dst = out / f"{run_id}_{figure}{src.suffix}"
            shutil.copy2(src, dst)
            made.append(dst)
    if not made:
        sys.exit(f"refused: run {run_id} has no png or pdf for {figure!r}")
    print("\n".join(f"exported {m}" for m in made))
    return made


def comparable(rel):
    return "_data/" in rel or rel.startswith("tables/")


def replay(run, py, command):
    ry = yaml.safe_load((run / "run.yaml").read_text())
    lib = run / "lib"
    analysis = run.parents[3] / "analysis" / ry["analysis"]
    old = {m["path"]: m["sha256"] for m in yaml.safe_load((run / "inputs.yaml").read_text())["inputs"]}
    new, status = execute(analysis, ry["figure"], ry["stage"], ry["selected_ids"], run / "scripts", py, f"replay of {run.name}", command, old, lib, run / "config" if (run / "config").is_dir() else None)
    ny = yaml.safe_load((new / "run.yaml").read_text())
    diff = sorted(k for k, v in ry["outputs"].items() if comparable(k) and ny["outputs"].get(k) != v)
    ny.update(reproduces=run.name, differences=diff)
    (new / "run.yaml").write_text(yaml.safe_dump(ny, sort_keys=False))
    print("reproduced: figure data and tables match" if not diff else "NOT reproduced, differs: " + ", ".join(diff))
    return 0 if status == "verified" and not diff else 1


def selftest():
    def script(body):
        return "import os, yaml, pathlib\nids = [i['id'] for i in yaml.safe_load(open(os.environ['RSTACK_INPUTS']))['inputs']]\n" + body

    good = script("from helper import tag\nassert os.path.isdir(os.environ['RSTACK_PRESETS'])\n"
                  "pathlib.Path(os.environ['RSTACK_RUN_DIR'], 'style_overrides.json').write_text('[\"axes 0 line a: width 3.00 pt, preset 0.99 pt\"]')\nf = pathlib.Path('figures/f1'); (f/'f1_data').mkdir(parents=True, exist_ok=True)\n"
                  "(f/'f1.png').write_text(','.join(ids)); (f/'f1.yaml').write_text('x: 1\\n'); (f/'f1_data/d.csv').write_text(tag(ids))\n")
    checks = ("import os, pathlib\nassert pathlib.Path(os.environ['RSTACK_OUTPUTS'], 'figures/f1/f1.yaml').exists()\n")
    readme = ("# A\n\n## Question\n\nDo the devices differ?\n\n## Tasks\n\n### Check\n- [ ] `f1` per-device\n\n### Main\n- [ ] `f2` main\n\n### Verify\n- [ ] `f3` drop one\n\n"
              "## Runs\n\n| run | inputs | note | status |\n|---|---|---|---|\n")
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / "proj"
        a = root / "analysis/demo"
        (a / "scripts").mkdir(parents=True)
        (root / "data/raw").mkdir(parents=True)
        (root / "data/raw/x.csv").write_text("1,2\n")
        (root / "data/raw/y.csv").write_text("3,4\n")
        (root / "tools/figrecipe/presets").mkdir(parents=True)
        (root / "tools/figrecipe/presets/nature-single.yaml").write_text("axes: {width_mm: 59.1}\n")
        (a / "inputs.yaml").write_text(yaml.safe_dump({"inputs": [
            {"id": "x", "path": "data/raw/x.csv", "label": "X", "legend": "x"},
            {"id": "y", "path": "data/raw/y.csv", "label": "Y", "legend": "y"},
            {"id": "d", "path": "analysis/demo/d.csv", "label": "D", "legend": "d"}]}))
        (a / "d.csv").write_text("a,b\n1,2\n")
        (a / "README.md").write_text(readme)
        (a / "docs").mkdir()
        (a / "docs/method.md").write_text("# Method\n\n## Figures and tables\n\n### f1\n\n- Objective: TODO x\n- Why: y\n\n## Limits\n")
        refused_obj = lambda: objective_gate(a, "f1")
        (a.parent / "lib").mkdir()
        (a.parent / "lib/helper.py").write_text("def tag(ids):\n    return ','.join(ids)\n")
        (a.parent / "lib/load.py").write_text("from pathlib import Path\nclass T:\n    def to_csv(self, p, index=False): Path(p).write_text('c\\n1\\n')\ndef load(i):\n    return T(), {'tok': i}\n")
        (a / "scripts/f1.py").write_text(good)
        (a / "scripts/f1.checks.py").write_text(checks)

        def refused(fn, word):
            try:
                fn()
                raise AssertionError(f"not refused: {word}")
            except SystemExit as e:
                assert word in str(e), e

        try:
            refused_obj()
            raise AssertionError("TODO objective passed")
        except SystemExit as e:
            assert "Objective" in str(e) or "objective" in str(e), e
        (a / "docs/method.md").write_text("# Method\n\n## Figures and tables\n\n### f1\n\n- Objective: compare devices\n- Why: H1\n\n## Limits\n")
        objective_gate(a, "f1")
        # the gate: a task must exist, earlier groups must be done
        refused(lambda: gate(a, "check", "nope"), "no check task")
        refused(lambda: gate(a, "main", "f2"), "open check")
        refused(lambda: gate(a, "verify", "f3"), "open check")
        gate(a, "check", "f1")

        run, st = execute(a, "f1", "check", ["x", "d"], a / "scripts", sys.executable, "first", "selftest")
        assert st == "verified" and run.parent.name == "demo_f1", (st, run)
        for f in ("inputs.yaml", "scripts/f1.py", "inputs/analysis/demo/d.csv", "style_overrides.json", "env.txt", "command.txt", "log.txt", "checks.txt",
                  "outputs/figures/f1/f1.yaml", "outputs/figures/f1/f1_data/d.csv", "lib/helper.py"):
            assert (run / f).exists(), f
        assert "sha256" in (run / "inputs.yaml").read_text() and (a / "figures/f1/run.txt").read_text().startswith(run.name)
        assert not (run / "inputs/data/raw/x.csv").exists(), "a raw input was copied"
        ry0 = yaml.safe_load((run / "run.yaml").read_text())
        assert ry0["style_overrides"] and any("style override" in w for w in ry0["warnings"]), ry0
        assert check(a) == 0
        (a / "figures/f1/f1.png").write_text("tampered")
        assert check(a) == 1

        # tick needs the user's ok, a verified run, and moves the README
        refused(lambda: tick(a, "f1", False), "approved-by-user")
        (a / "figures/f1/f1.png").write_text("x")
        tick(a, "f1", True)
        t = (a / "README.md").read_text()
        assert "- [x] `f1` per-device" in t and run.name in t and "- [ ] `f2`" in t, t
        assert yaml.safe_load((run / "run.yaml").read_text())["approved_by_user"]
        refused(lambda: tick(a, "f1", True), "already approved")
        res = (a / "docs/results/f1.md").read_text()
        assert "run: " + run.name in res and "TODO: the claim" in res and "superseded" not in res, res
        gate(a, "main", "f2")  # check group now done
        # a re-run of a ticked figure is recorded: the claim stays, the old run is superseded
        (a / "docs/results/f1.md").write_text(res.replace("TODO: the claim this figure supports, with n and what the spread is.", "Current rises with voltage (n = 2)."))
        rerun, st = execute(a, "f1", "check", ["x", "d"], a / "scripts", sys.executable, "again", "selftest")
        assert st == "verified"
        tick(a, "f1", True)
        res2 = (a / "docs/results/f1.md").read_text()
        assert "run: " + rerun.name in res2 and run.name in res2.split("superseded")[1] and "Current rises" in res2, res2
        assert f"re-run, replaces {run.name}" in (a / "README.md").read_text() and "- [x] `f1`" in (a / "README.md").read_text()

        assert yaml.safe_load(res2.split("---")[1])["claim_for"] == run.name
        assert collect(a)["figures"][0]["claim_stale"], "a claim written for another run was not flagged"
        # accept an earlier verified run: its files come back and the claim stays
        (a / "figures/f1/f1.png").write_text("not the first run")
        tick(a, "f1", True, run.name)
        assert (a / "figures/f1/f1.png").read_text() == (run / "outputs/figures/f1/f1.png").read_text() and (a / "figures/f1/run.txt").read_text().startswith(run.name)
        refused(lambda: tick(a, "f1", True, run.name), "already approved")
        tick(a, "f1", True, rerun.name)
        # reviews: cited results need one on their current run, a claim written for it, and an analysis review
        assert check(a) == 0, "an uncited result needs no review"
        fm = lambda t: "---\n" + yaml.safe_dump(t) + "---\n\nbody\n"
        rf = a / "docs/results/f1.md"
        t0 = rf.read_text()
        rf.write_text(t0.replace("cited: false", "cited: true").replace("claim_for: " + run.name, "claim_for: " + rerun.name))
        assert review_state(root, a, "f1")[0] == "none" and check(a) == 1
        (rerun / "review.md").write_text(fm({"case": "challenge", "outcome": "accepted", "blocking": 1}))
        assert review_state(root, a, "f1")[0] == "current" and not review_usable(review_state(root, a, "f1")[1])
        (rerun / "review.md").write_text(fm({"case": "challenge", "outcome": "accepted", "blocking": 0}).replace("body", "TODO fill in"))
        assert any("TODO" in x for x in review_problems(a)), "an untouched review template passed"
        (rerun / "review.md").write_text(fm({"case": "challenge", "outcome": "accepted", "blocking": 0}) + "\n| 1 | blocks acceptance | a number does not reproduce | f.py:3 | fix |\n")
        assert any("findings table has 1" in x for x in review_problems(a)), "a hidden blocker passed"
        (rerun / "review.md").write_text(fm({"case": "challenge", "outcome": "accepted", "blocking": 0}))
        assert any("docs/review.md" in x for x in review_problems(a)), "a cited result passed without an analysis review"
        (a / "docs/review.md").write_text(fm({"runs": {"f1": rerun.name}, "outcome": "accepted", "blocking": 0}))
        assert check(a) == 0 and collect(a)["analysis_review"]["state"] == "current"
        same, _ = execute(a, "f1", "check", ["x", "d"], a / "scripts", sys.executable, "same inputs", "selftest")
        tick(a, "f1", True)
        assert review_state(root, a, "f1")[0].startswith("carried"), "identical evidence lost its review"
        (a / "scripts/f1.py").write_text(good + "# edited\n")
        edited, _ = execute(a, "f1", "check", ["x", "d"], a / "scripts", sys.executable, "edited", "selftest")
        tick(a, "f1", True)
        (a / "scripts/f1.py").write_text(good)
        assert review_state(root, a, "f1")[0] == "stale" and check(a) == 1, "a changed script kept the review"
        rf.write_text(rf.read_text().replace("cited: true", "cited: false"))
        (a / "docs/review.md").unlink()

        # replay reproduces, and refuses when an input changed
        (a.parent / "lib/helper.py").write_text("def tag(ids):\n    return 'changed live lib'\n")
        assert replay(run, sys.executable, "selftest") == 0, "replay did not use the snapshot lib"
        (a.parent / "lib/helper.py").write_text("def tag(ids):\n    return ','.join(ids)\n")
        (root / "data/raw/x.csv").write_text("changed\n")
        refused(lambda: replay(run, sys.executable, "selftest"), "differs")
        run2, st = execute(a, "f1", "check", [], a / "scripts", sys.executable, "", "selftest")
        assert yaml.safe_load((run2 / "run.yaml").read_text())["warnings"], "changed input must warn"

        # outputs that break the structure are rejected, not verified
        live = (a / "figures/f1/f1.png").read_text()
        (a / "scripts/f1.py").write_text(script("f = pathlib.Path('figures/f1'); f.mkdir(parents=True, exist_ok=True); (f/'f1.png').write_text('p')\n"))
        _, st = execute(a, "f1", "check", ["y"], a / "scripts", sys.executable, "", "selftest")
        assert st == "rejected", "a figure without figrecipe files passed"
        assert (a / "figures/f1/f1.png").read_text() == live, "a rejected run left its file in figures/"
        (a / "scripts/f1.py").write_text(good + "pathlib.Path('figures/other').mkdir(exist_ok=True); pathlib.Path('figures/other/o.png').write_text('p')\n")
        _, st = execute(a, "f1", "check", ["y"], a / "scripts", sys.executable, "", "selftest")
        assert st == "rejected", "a stray output passed"
        assert not (a / "figures/other").exists() and (a / "figures/f1/f1_data/d.csv").read_text() != "", "a stray output stayed"
        (a / "scripts/f1.py").write_text(good)
        (a / "scripts/f1.checks.py").write_text("raise SystemExit(1)\n")
        _, st = execute(a, "f1", "check", ["y"], a / "scripts", sys.executable, "", "selftest")
        assert st == "check-failed"
        (a / "scripts/f1.checks.py").unlink()
        _, st = execute(a, "f1", "check", ["y"], a / "scripts", sys.executable, "", "selftest")
        assert st == "completed"
        refused(lambda: tick(a, "f1", True), "not verified")
        (a / "scripts/f1.py").write_text("raise SystemExit(3)\n")
        _, st = execute(a, "f1", "check", ["y"], a / "scripts", sys.executable, "", "selftest")
        assert st == "failed"
        refused(lambda: select(a, ["nope"]), "unknown ids")
        refused(lambda: preflight("/nonexistent/python"), "cannot import")
        # diff names the changed input, script and output between two runs
        (a / "scripts/f1.checks.py").write_text(checks)
        (a / "scripts/f1.py").write_text(good)
        (root / "data/raw/x.csv").write_text("1,2\n")
        r_a, _ = execute(a, "f1", "check", ["x"], a / "scripts", sys.executable, "", "selftest")
        (a / "scripts/f1.py").write_text(good + "# edited\n")
        (root / "data/raw/x.csv").write_text("9,9\n")
        r_b, _ = execute(a, "f1", "check", ["x"], a / "scripts", sys.executable, "", "selftest")
        assert diff_runs(r_a, r_a) == 0
        assert diff_runs(r_a, r_b) >= 2, "diff missed a changed input or script"  # the outputs are the same for the same ids
        # export names the file after its run
        ex = export(a, "f1", out=Path(d) / "exp")
        assert [m.name for m in ex] == [f"{front(a / 'docs/results/f1.md')['run']}_f1.png"], ex
        refused(lambda: export(a, "nope", out=Path(d) / "exp"), "no accepted result")
        # package: refuses what is not settled, then builds a folder that reproduces on its own
        pk, rf1 = Path(d) / "pkg", a / "docs/results/f1.md"
        rd0 = (a / "README.md").read_text()
        (a / "README.md").write_text(rd0.replace("Do the devices differ?", "TODO: one sentence"))
        refused(lambda: package(a, pk, py=sys.executable), "no Question")
        (a / "README.md").write_text(rd0)
        refused(lambda: package(a, pk, py=sys.executable), "claim was written for")
        cur = front(rf1)["run"]
        rf1.write_text(re.sub(r"claim_for: \S+", f"claim_for: {cur}", rf1.read_text()))
        refused(lambda: package(a, pk, py=sys.executable), "no longer matches the hash")  # x.csv was edited after the accepted run
        assert not pk.exists(), "a refused build left a folder behind"
        (root / "data/raw/x.csv").write_text("1,2\n")
        package(a, pk, py=sys.executable)
        readme_txt = (pk / "README.md").read_text()
        assert "Current rises with voltage (n = 2)." in readme_txt and "compare devices" in readme_txt and f"{cur}_f1.png" in readme_txt, readme_txt
        assert "`f2` main" in readme_txt, "a task with no accepted result was not listed"
        assert (pk / "data/derived/x.csv").is_file() and (pk / "data/raw/x.csv").is_file() and (pk / "lib/load.py").read_text().count("raw-viewer") >= 1
        assert "PyYAML==" in (pk / "requirements.txt").read_text() and "helper" not in (pk / "requirements.txt").read_text()
        rp = subprocess.run([sys.executable, str(pk / "reproduce.py")], capture_output=True, text=True)
        assert rp.returncode == 0 and "reproduced" in rp.stdout, rp.stdout + rp.stderr
        refused(lambda: package(a, pk, py=sys.executable), "not empty")
        (pk / "data/raw/x.csv").write_text("tampered")
        rp = subprocess.run([sys.executable, str(pk / "reproduce.py")], capture_output=True, text=True)
        assert rp.returncode == 1 and "data/raw/x.csv" in rp.stdout, rp.stdout
        package(a, pk, replace=True, exclude=["x"], py=sys.executable)
        assert "excluded by --exclude-raw" in (pk / "README.md").read_text() and not (pk / "data/raw/x.csv").exists()
        rf1.write_text(rf1.read_text().replace("Current rises with voltage (n = 2).", "TODO: later"))
        refused(lambda: package(a, Path(d) / "pkg2", py=sys.executable), "still TODO")
        rf1.write_text(rf1.read_text().replace("TODO: later", "Current rises with voltage (n = 2)."))
        # collect and show read stored runs without running anything
        data = collect(a)
        f1 = next(f for f in data["figures"] if f["figure"] == "f1")
        assert f1["objective"] == "compare devices" and f1["runs"] and f1["runs"][0]["scripts"], f1
        assert "Current rises" in f1["claim"] and [f["figure"] for f in data["figures"]] == ["f1", "f2", "f3"]
        show(a)
        assert "compare devices" in (a / "provenance.html").read_text()
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        assert not rstack_ignored(root)
        (root / ".gitignore").write_text(".rstack\n")
        assert rstack_ignored(root), "a git-ignored .rstack was not noticed"
        proj2 = Path(d) / "p2"
        (proj2 / "analysis").mkdir(parents=True)
        install_lib(proj2)
        names = sorted(f.name for f in (proj2 / "analysis/lib").glob("*.py"))
        assert names == ["figrules.py", "load.py", "style.py"], names
        (proj2 / "analysis/lib/style.py").write_text("mine\n")
        install_lib(proj2)
        assert (proj2 / "analysis/lib/style.py").read_text() == "mine\n", "install overwrote a project file"
        # new scaffolds an analysis whose task the gate recognises, and a second call changes nothing
        new_analysis(proj2, "iv", ["check:dev", "main:summary"])
        before = (proj2 / "analysis/iv/README.md").read_text()
        new_analysis(proj2, "iv", ["check:dev", "main:summary"])
        assert (proj2 / "analysis/iv/README.md").read_text() == before and before.count("`dev`") == 1
        for f in ("inputs.yaml", "docs/method.md", "docs/plan-review.md", "scripts/dev.py", "scripts/dev.checks.py"):
            assert (proj2 / "analysis/iv" / f).is_file(), f
        assert "- Objective: TODO" in (proj2 / "analysis/iv/docs/method.md").read_text()
        refused(lambda: objective_gate(proj2 / "analysis/iv", "dev"), "Objective")
        gate(proj2 / "analysis/iv", "check", "dev")
        refused(lambda: gate(proj2 / "analysis/iv", "main", "summary"), "open check")
        refused(lambda: new_analysis(proj2, "iv", ["bogus:x"]), "stage:name")
    print("selftest ok")


def main():
    if sys.argv[1:] == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("analysis"); r.add_argument("--stage", required=True, choices=list(BEFORE))
    r.add_argument("--figure", required=True); r.add_argument("--ids", default=""); r.add_argument("--python"); r.add_argument("--note", default="")
    p = sub.add_parser("replay"); p.add_argument("run_dir"); p.add_argument("--python")
    li = sub.add_parser("lib"); li.add_argument("project")
    nw = sub.add_parser("new"); nw.add_argument("project"); nw.add_argument("name"); nw.add_argument("--figure", action="append", default=[])
    df = sub.add_parser("diff"); df.add_argument("run_a"); df.add_argument("run_b")
    t = sub.add_parser("tick"); t.add_argument("analysis"); t.add_argument("--figure", required=True); t.add_argument("--approved-by-user", action="store_true"); t.add_argument("--run")
    c = sub.add_parser("check"); c.add_argument("analysis")
    sh_ = sub.add_parser("show"); sh_.add_argument("analysis")
    pk_ = sub.add_parser("package"); pk_.add_argument("analysis"); pk_.add_argument("--out"); pk_.add_argument("--replace", action="store_true")
    pk_.add_argument("--max-raw-mb", type=float, default=100); pk_.add_argument("--exclude-raw", default=""); pk_.add_argument("--python")
    ex_ = sub.add_parser("export"); ex_.add_argument("analysis"); ex_.add_argument("--figure", required=True); ex_.add_argument("--run"); ex_.add_argument("--out")
    a = ap.parse_args()
    cmd = " ".join(sys.argv)
    if a.cmd == "run":
        an = Path(a.analysis).resolve()
        gate(an, a.stage, a.figure)
        objective_gate(an, a.figure)
        py = a.python or default_python(project_of(an))
        preflight(py)
        sys.exit(0 if execute(an, a.figure, a.stage, [i for i in a.ids.split(",") if i], an / "scripts", py, a.note, cmd)[1] == "verified" else 1)
    if a.cmd == "replay":
        run = Path(a.run_dir).resolve()
        py = a.python or default_python(run.parents[3])
        preflight(py)
        sys.exit(replay(run, py, cmd))
    if a.cmd == "new":
        return new_analysis(Path(a.project).resolve(), a.name, a.figure)
    if a.cmd == "diff":
        return diff_runs(Path(a.run_a).resolve(), Path(a.run_b).resolve())
    if a.cmd == "lib":
        return install_lib(Path(a.project).resolve())
    if a.cmd == "tick":
        return tick(Path(a.analysis).resolve(), a.figure, a.approved_by_user, a.run)
    if a.cmd == "package":
        an = Path(a.analysis).resolve()
        py = a.python or default_python(project_of(an))
        preflight(py)
        package(an, a.out, a.max_raw_mb, [i for i in a.exclude_raw.split(",") if i], a.replace, py)
        return None
    if a.cmd == "export":
        return export(Path(a.analysis).resolve(), a.figure, a.run, a.out) and None
    if a.cmd == "show":
        return show(Path(a.analysis).resolve())
    sys.exit(check(Path(a.analysis).resolve()))


if __name__ == "__main__":
    main()
