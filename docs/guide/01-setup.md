# Set up rstack

1. Install the plugin: `/plugin marketplace add <path to research-space>`, then `/plugin install rstack@research-space` (or `bash rstack/scripts/install.sh [claude|codex|antigravity|all]`).
2. Run `/rstack:setup-research`. It writes `research-profile.md` (citation style, statistics defaults, figure conventions) in the research-space root, optionally `~/.claude/rules/rstack-models.md`, and checks which external tools/skills are missing.
3. Open a project and start with `/rstack:using-rstack` (if intent is unclear) or `/rstack:research-mode`.

## External tools and skills (where each lives)

| Tool / Skill | Scope & Path | Install / Update |
|---|---|---|
| `zotero-cli` | Global (`PATH`, `~/.local/bin/zotero-cli`) | `uv tool install zotero-mcp-server` |
| `qmd` | Global (`PATH`) | `npm install -g @tobilu/qmd` (update: `npm update -g @tobilu/qmd`) |
| `raw-viewer` | Global (`PATH`, `~/.local/bin/raw-viewer`) | Install per `taixuann/raw-viewer` README |
| `doc-coauthoring` | Global (`~/.claude/skills/`) or project (`.claude/skills/`) | Copy `doc-coauthoring` from `anthropics/skills` |
| `figrecipe` | Workspace `research-space/tools/figrecipe/` (`.venv/bin/python`) | Install in `tools/figrecipe/` with `.venv` (`uv sync` / `pip install -e .`) |
| `hyperresearch` | Shared vault folder (`~/academic-space` or `research-space`) | `pip install hyperresearch && hyperresearch install` in that folder |

Installing changes nothing until you invoke a skill.
