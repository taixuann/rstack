#!/usr/bin/env python3
"""Create the rstack project layout and its three front docs. Never overwrites.

Usage: init_project.py PROJECT_DIR [--title TITLE]   |   init_project.py --selftest
Creates the standard folders (with .gitkeep), then README.md, AGENTS.md, CLAUDE.md from
../references/*.template.*, then docs/rstack/tasks.md, then syncs the README task block.
Anything that already exists is skipped and reported, so it also adds rstack to an existing project.
"""
import argparse, re, subprocess, sys, tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / "templates/project"
FOLDERS = ["data/raw", "docs/rstack", "docs/reports", "docs/literature-review/papers",
           "docs/literature-review/hyperresearch-reports", "docs/writing", "docs/figures",
           "docs/inputs", "docs/understanding", "analysis"]
EXPLORE_TASKS = """# Tasks

Phase > Goal > Task. Only the Project admin playbook edits this file.

## Phase: explore

### Goal: Proposal intake
- [ ] Run the project interview
- [ ] Fill Context, Aim, and Milestones in `README.md`
- [ ] Confirm the open points with the supervisor

### Goal: Scope
- [ ] Run `interrogate` on the proposal: aims, what the user knows, the gaps
- [ ] Quick scoping search: register a few papers in Zotero, check what already exists
- [ ] Scope check: the question is narrow, a gap is named, feasibility is judged

### Goal: Deepen
- [ ] Ingest and review the key papers; run the inquiry

### Goal: Report init
- [ ] Open each question's report folder (`docs/reports/<question>/README.md`)
- [ ] Fill Intention, scope (`fundamental/`, `method/`, `analysis/`, `results/` or `N/A`), and candidate hypotheses
- [ ] Assemble the proposal chain and run `interrogate` on it
"""


def readme(title):
    t = (TPL / "README.md").read_text()
    t = t.replace("YYYY-MM-DD", date.today().isoformat()).replace("<Project title>", title)
    t = t.replace("<One sentence on where the project stands.>", "Just initialised. The project interview comes first.")
    t = t.replace("<Goal, background, problem statement, scope, resources, and constraints. Anything not decided stays `TODO: unknown` with an owner.>", "TODO: unknown (run the project interview via `/rstack:init`).")
    t = t.replace("<Overall aim and key milestones with targets and dates.>", "TODO: unknown (run the project interview via `/rstack:init`).")
    # the per-question blocks are filled after the interview; drop the template placeholders
    return re.sub(r"## <Work package name>.*?(?=## State history)", "", t, flags=re.S)


def init(project, title=None):
    p = Path(project).resolve()
    title = title or p.name.replace("res_", "").replace("-", " ").replace("_", " ").capitalize()
    made, skipped = [], []

    def put(rel, text):
        f = p / rel
        if f.exists():
            skipped.append(rel)
            return
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
        made.append(rel)

    for d in FOLDERS:
        (p / d).mkdir(parents=True, exist_ok=True)
        g = p / d / ".gitkeep"
        if not any((p / d).iterdir()):
            g.touch()
    put("README.md", readme(title))
    put("AGENTS.md", (TPL / "AGENTS.md").read_text().replace("<project>", p.name))
    put("CLAUDE.md", (TPL / "CLAUDE.md").read_text())
    put("docs/rstack/README.md", (TPL / "rstack-README.md").read_text().replace("YYYY-MM-DD", date.today().isoformat()))
    put("docs/rstack/tasks.md", EXPLORE_TASKS)
    # an existing README without the task markers cannot be synced; the caller reports it
    r = subprocess.run([sys.executable, str(HERE / "sync_readme_tasks.py"), str(p)], capture_output=True, text=True)
    if r.returncode:
        skipped.append("README task block not synced: " + (r.stderr or r.stdout).strip().splitlines()[-1])
    return made, skipped


def selftest():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "res_demo-device"
        made, skipped = init(proj)
        assert {"README.md", "AGENTS.md", "CLAUDE.md", "docs/rstack/README.md", "docs/rstack/tasks.md"} <= set(made), made
        r = (proj / "README.md").read_text()
        rr = (proj / "docs/rstack/README.md").read_text()
        assert "state: explore" in r and "Demo device" in r and "<Project title>" not in r and "<Work package name>" not in r
        assert "Tasks (explore): 0/10 done" in rr, rr
        assert "res_demo-device" in (proj / "AGENTS.md").read_text()
        for dead in ("00_interview.md", "references.yaml"):
            assert dead not in r, dead
        for f in ("data/raw", "docs/reports", "docs/understanding", "docs/literature-review/hyperresearch-reports", "docs/rstack"):
            assert (proj / f).is_dir()
        (proj / "README.md").write_text("mine")
        made2, skipped2 = init(proj)
        assert (proj / "README.md").read_text() == "mine" and "README.md" in skipped2 and not made2, (made2, skipped2)
        assert any("not synced" in s for s in skipped2), skipped2
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        ap = argparse.ArgumentParser(description="Create the rstack project layout and front docs. Never overwrites.")
        ap.add_argument("project")
        ap.add_argument("--title")
        args = ap.parse_args()
        made, skipped = init(args.project, args.title)
        print("created:", ", ".join(made) or "nothing")
        print("skipped (already exist):", ", ".join(skipped) or "nothing")
