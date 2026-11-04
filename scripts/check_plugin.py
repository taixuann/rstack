#!/usr/bin/env python3
"""Check rstack's own consistency. Run from anywhere: scripts/check_plugin.py

1. Every skill-like name in backticks in a playbook is bundled or declared in references/skills-manifest.yaml.
2. The playbook list in research-mode/SKILL.md and the README table match the playbook files.
3. Counts in README.md and .claude-plugin/plugin.json match the folders.
Exit 1 and print each problem when a check fails.
"""
import json, re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MODE = SKILLS / "research-mode"
WORKFLOW = {"research-mode", "setup-research", "research-help", "arena", "swarm", "interrogate",
            "figure-it-out", "show-me-your-work", "reflect", "correct", "bro", "in-your-own-words", "unslop", "teach", "explain", "make-the-figure", "answer-comments", "make-me-roadmap", "branch", "evaluate-my-understanding", "paper-ingest", "init"}
# Backticked words in playbooks that are not skill names.
IGNORE = {"state", "tasks", "true", "false", "yaml", "unread", "snapshotted", "read", "candidate", "frozen",
          "supported", "rejected", "explore", "design", "progressing", "closed", "ready-for-publish",
          "todo", "model", "haiku", "main", "docs", "data", "raw", "wiki", "analysis", "unknown",
          "pele", "figures", "mermaid", "parts", "why", "updated", "created", "kind", "voice", "paper", "parent", "depth", "status", "pass", "repair", "blocked", "needs_review", "no_review", "manuscripts", "presentation",
          # plugin, repo, agent, and example names
          "claude-scientific-writer", "scientific-agent-skills", "annotations", "source-analyst", "paper-critic", "docx", "pdf", "pptx", "xlsx"}
NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


def skill_tokens(text):
    return {t for t in re.findall(r"`([^`\n]+)`", text) if NAME.match(t) and len(t) > 2}


def problems():
    errs = []
    bundled = {p.name for p in SKILLS.iterdir() if p.is_dir()}
    manifest = yaml.safe_load((MODE / "references/skills-manifest.yaml").read_text())
    external = {e["name"] for e in manifest["externals"]}
    pbs = sorted(MODE.glob("playbooks/*.md"))
    for pb in pbs:
        for t in sorted(skill_tokens(pb.read_text())):
            if t not in bundled | external | IGNORE:
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
    for s in stems:
        if f"| {s} |" not in readme:
            errs.append(f"README table has no row for {s}")
    domain = [d for d in bundled if d not in WORKFLOW and not d.startswith("principle-")]
    principles = [d for d in bundled if d.startswith("principle-")]
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())["description"]
    want = {"playbooks": len(stems), "principles": len(principles), "bundled domain skills": len(domain)}
    for label, n in want.items():
        for name, text in (("plugin.json", plugin), ("README.md", readme)):
            m = re.search(rf"(\d+) {label}", text)
            if m and int(m.group(1)) != n:
                errs.append(f"{name} says {m.group(1)} {label}, folders have {n}")
    return errs


if __name__ == "__main__":
    assert skill_tokens("use `swarm` and `a/b` and `x.md` and `State`") == {"swarm"}
    out = problems()
    print("\n".join(out) or "plugin consistent")
    sys.exit(1 if out else 0)
