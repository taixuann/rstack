#!/usr/bin/env python3
"""Create the rstack project layout and its three front docs. Never overwrites.

Usage: init_project.py PROJECT_DIR [--title TITLE]   |   init_project.py --selftest
Creates the standard folders (with .gitkeep), then README.md, AGENTS.md and CLAUDE.md from
../references/*.template.*, then docs/rstack/explore/tasks.md, then syncs the README task block.
Anything that already exists is skipped and reported, so it also adds rstack to an existing project.
"""
import argparse, re, subprocess, sys, tempfile
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "references"
FOLDERS = ["data/raw", "docs/literature-review/papers", "docs/inputs", "docs/literature-review/cross-papers", "docs/literature-review/reports",
           "docs/rstack/explore", "analysis", "manuscripts", "presentation"]
EXPLORE_TASKS = """# Tasks: explore

Proposal intake
- [ ] Run the project interview
- [ ] Write context (`01_context.md`)
- [ ] Write aims and milestones (`02_aims-and-milestones.md`)
- [ ] Confirm the open points with the supervisor

Literature review
- [ ] Register the Zotero collection, ingest and review the papers, and run the inquiry
- [ ] Write the literature map (`03_literature-map.md`): themes, search log, and the gap

Proposal synthesis
- [ ] Write questions and hypotheses (`04_questions-and-hypotheses.md`)
- [ ] Write methods and feasibility (`05_methods-and-feasibility.md`)
- [ ] Assemble the proposal chain and run `interrogate` on it
"""


def readme(title):
    t = (REF / "README.template.md").read_text()
    t = t.replace("YYYY-MM-DD", date.today().isoformat()).replace("<Project title>", title)
    t = t.replace("<One sentence on where the project stands.>", "Just initialised. The project interview comes first.")
    # day one has only tasks.md and the literature-review folder: drop links to files that do not exist yet
    t = re.sub(r"^- Explore:.*$", "- Explore: [tasks](docs/rstack/explore/tasks.md)", t, flags=re.M)
    t = re.sub(r"^- Literature review:.*$", "- Literature review: [docs/literature-review/](docs/literature-review/)", t, flags=re.M)
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
    put("AGENTS.md", (REF / "AGENTS.template.md").read_text().replace("<project>", p.name))
    put("CLAUDE.md", (REF / "CLAUDE.template.md").read_text())
    put("docs/rstack/explore/tasks.md", EXPLORE_TASKS)
    # an existing README without the task markers cannot be synced; the caller reports it
    r = subprocess.run([sys.executable, str(HERE / "sync_readme_tasks.py"), str(p)], capture_output=True, text=True)
    if r.returncode:
        skipped.append("README task block not synced: " + (r.stderr or r.stdout).strip().splitlines()[-1])
    return made, skipped


def selftest():
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d) / "res_demo-device"
        made, skipped = init(proj)
        assert {"README.md", "AGENTS.md", "CLAUDE.md", "docs/rstack/explore/tasks.md"} <= set(made), made
        r = (proj / "README.md").read_text()
        assert "state: explore" in r and "Demo device" in r and "<Project title>" not in r and "<Work package name>" not in r
        assert "Tasks (explore): 0/9 done" in r, r
        assert "res_demo-device" in (proj / "AGENTS.md").read_text()
        for dead in ("00_interview.md", "03_literature-map.md", "references.yaml"):
            assert dead not in r, dead
        for f in ("data/raw", "docs/literature-review/reports", "docs/rstack/explore"):
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
