#!/usr/bin/env python3
"""Check rstack's own consistency. Run from anywhere: scripts/check_plugin.py

1. Every skill-like name in backticks in a playbook is bundled or declared in references/skills-manifest.yaml.
2. The playbook list in research-mode/SKILL.md and docs/references/playbooks.md match the playbook files.
3. Counts in README.md and .claude-plugin/plugin.json match the folders.
4. No text names a retired skill, playbook, folder or phase list (RETIRED below). A rename adds its old name there, so every leftover fails here.
6. Every backticked path into the plugin (skills/, references/, templates/, playbooks/, scripts/, agents/, assets/) names a file that exists.
5. The "Allowed" line of templates/project/AGENTS.md lists the same playbooks per phase as the table in research-mode/SKILL.md.
Exit 1 and print each problem when a check fails.
"""
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MODE = SKILLS / "research-mode"
PRINCIPLES = MODE / "principles"
WORKFLOW = {"research-mode", "setup-research", "research-help", "using-rstack", "learn-mode", "wiki-mode",
            "playbook-control", "arena", "swarm", "interrogate", "figure-it-out", "show-me-your-work",
            "reflect", "correct", "unslop", "init", "statechart"}
# Backticked words in playbooks that are not skill names.
IGNORE = {"state", "tick", "check", "critic", "show", "nature-single", "new", "replay", "load", "style", "tasks", "true", "false", "yaml", "unread", "snapshotted", "read", "candidate", "frozen",
          "supported", "rejected", "explore", "design", "analysis", "closed", "write",
          "todo", "model", "haiku", "main", "docs", "data", "raw", "wiki", "analysis", "unknown",
          "pele", "figures", "mermaid", "parts", "label", "legend", "path", "nature-open", "nature-heatmap", "nature-violin", "figrecipe", "why", "updated", "created", "kind", "voice", "paper", "parent", "depth", "status", "review", "pass", "repair", "blocked", "needs_review", "no_review", "manuscripts", "presentation",
          # plugin, repo, agent, and example names
          "claude-scientific-writer", "scientific-agent-skills", "experiment", "operator", "inputs", "mode", "question", "source", "critique-passed", "draft-ready", "report-approved", "progressing", "ready-for-publish", "annotations", "docx", "pdf", "pptx", "xlsx"}
# Old name -> what replaced it. Add a row in the same change as a rename or removal.
RETIRED = {
    r"proposal-synthesis|report-bootstrap|Report bootstrap": "report-init",
    r"playbooks/prototype|\*\*Prototype\*\*": "dropped; a pilot is an experiment of type pilot",
    r"docs/rstack/p-(explore|design|analysis|write|closed)": "flat docs/rstack/ with phase: in front matter",
    r"\bwstack\b": "folded into rstack",
    r"/tutor:teach|make-me-roadmap|evaluate-my-understanding|/rstack:(teach|explain|branch|paper-ingest)": "removed; learning notes use doc-coauthoring",
    r"\bNotion\b|notion-search": "tasks are in Todoist",
    r"design, progressing": "the phases are explore, design, analysis, write, closed",
    r"playbooks/(hillclimb|reproduce)": "moved to bundled skills (hillclimb, reproduce)",
    r"03_literature-map|04_questions-and-hypotheses|05_methods-and-feasibility": "retired; questions, hypotheses, and methods live in docs/reports/<question>/",
}
RETIRED_SKIP = {"check_plugin.py", "check_layout.py"}  # define the names / test the flag on purpose
NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def skill_tokens(text):
    return {t for t in re.findall(r"`([^`\n]+)`", text) if NAME.match(t) and len(t) > 2}


def problems():
    errs = []
    bundled = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    principles = sorted(p.stem for p in PRINCIPLES.glob("*.md"))
    principle_tokens = {f"principle-{p}" for p in principles}
    manifest = yaml.safe_load((MODE / "references/skills-manifest.yaml").read_text())
    external = {e["name"] for e in manifest["externals"]}
    pbs = sorted(MODE.glob("playbooks/*.md"))
    for pb in pbs:
        for t in sorted(skill_tokens(pb.read_text())):
            if t not in bundled | external | principle_tokens | IGNORE:
                errs.append(f"{pb.name}: `{t}` is not bundled, not in the manifest, and not ignored")
    stems = [p.stem for p in pbs]
    mode_text = (MODE / "SKILL.md").read_text()
    section = mode_text.split("## Playbooks", 1)[1]
    titles = re.findall(r"^- \*\*(.+?)\.\*\*", section, re.M)
    if len(titles) != len(stems):
        errs.append(f"research-mode lists {len(titles)} playbooks, folder has {len(stems)}")
    for s in stems:
        words = set(s.split("-"))
        if not any(words <= set(re.findall(r"[a-z]+", t.lower())) for t in titles):
            errs.append(f"playbook {s} has no matching bullet in research-mode/SKILL.md")
    readme = (ROOT / "README.md").read_text()
    table = (ROOT / "docs/references/playbooks.md").read_text()
    for s in stems:
        if f"| {s} |" not in table:
            errs.append(f"docs/references/playbooks.md has no row for {s}")
    domain = [d for d in bundled if d not in WORKFLOW]
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["description"]
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
    for k in ("name", "version", "description"):
        if claude[k] != codex[k]:
            errs.append(f".codex-plugin/plugin.json {k} differs from .claude-plugin/plugin.json")
    want = {"playbooks": len(stems), "principles": len(principles), "bundled domain skills": len(domain)}
    for label, n in want.items():
        for name, text in (("plugin.json", plugin), ("README.md", readme)):
            m = re.search(rf"(\d+) {label}", text)
            if m and int(m.group(1)) != n:
                errs.append(f"{name} says {m.group(1)} {label}, folders have {n}")
    errs += retired_names() + template_allowed(mode_text) + dead_paths()
    return errs


def retired_names():
    errs = []
    files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".md", ".py", ".yaml", ".json", ".html", ".sh", ".mjs")
             and not {"vendor", ".git"} & set(p.parts) and p.name not in RETIRED_SKIP]
    outer = ROOT.parent / "AGENTS.md"  # the research-space instructions, when rstack sits inside it
    if outer.exists():
        files.append(outer)
    for f in files:
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for pat, now in RETIRED.items():
                if re.search(pat, line):
                    errs.append(f"{f.relative_to(ROOT.parent)}:{n} names a retired thing /{pat}/ ({now})")
    return errs


PLUGIN_ROOTS = ("skills/", "references/", "templates/", "playbooks/", "scripts/", "agents/", "assets/")
DEAD_SKIP = ("skill-creator", "zotero-cli/reference.md")  # upstream text and a generated file


def dead_paths():
    """A backticked path into the plugin must resolve from the plugin, research-mode, the file's folder or its skill."""
    errs = []
    for f in ROOT.rglob("*"):
        if not f.is_file() or f.suffix not in (".md", ".py") or {"vendor", ".git"} & set(f.parts) or any(s in str(f) for s in DEAD_SKIP):
            continue
        skill = SKILLS / f.relative_to(SKILLS).parts[0] if SKILLS in f.parents else ROOT
        for n, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            for tok in re.findall(r"`([^`\s]+)`", line):
                if not tok.startswith(PLUGIN_ROOTS) or re.search(r"[<>*{}$|]", tok) or not re.search(r"\.\w+$", tok):
                    continue
                if not any((base / tok).exists() for base in (ROOT, MODE, f.parent, skill)):
                    errs.append(f"{f.relative_to(ROOT)}:{n} `{tok}` does not exist")
    return errs


def template_allowed(mode_text):
    """The per-phase playbooks in templates/project/AGENTS.md must be the ones in the phase table of research-mode/SKILL.md."""
    norm = lambda x: re.sub(r"[^a-z]+", " ", re.sub(r"\(.*?\)", "", x.lower())).strip()
    table = {m[0]: {norm(x) for x in m[1].split(",")}
             for m in re.findall(r"^\| (explore|design|analysis|write|closed) \|[^|]*\| ([^|]*) \|", mode_text, re.M)}
    line = next((l for l in (MODE / "templates/project/AGENTS.md").read_text().splitlines() if "Allowed" in l), "")
    errs = []
    for ph, want in table.items():
        m = re.search(rf"{ph} → ([^.]*)\.", line)
        got = {norm(x) for x in m.group(1).split(",")} if m else set()
        if got != want:
            errs.append(f"templates/project/AGENTS.md allows {sorted(got)} in {ph}, SKILL.md table has {sorted(want)}")
    return errs


if __name__ == "__main__":
    assert skill_tokens("use `swarm` and `a/b` and `x.md` and `State`") == {"swarm"}
    assert template_allowed("| design | x | Experimental design, Prototype |\n"), "template check must fail on a changed phase table"
    assert re.search(r"\.\w+$", "skills/x/y.md") and not (ROOT / "skills/x/y.md").exists(), "dead-path lint must see a missing file"
    assert any(re.search(pat, "see proposal-synthesis") for pat in RETIRED), "retired check must match an old name"
    out = problems()
    print("\n".join(out) or "plugin consistent")
    sys.exit(1 if out else 0)
