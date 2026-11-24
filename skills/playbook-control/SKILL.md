---
name: playbook-control
description: "Meta-control router for designing, fixing, upgrading, model-checking, and authoring rstack workflows, playbooks, and skills. Routes to figure-it-out, correct, reflect, statechart, or authoring-a-skill + skill-creator based on the user's goal. Use for /playbook-control or meta-level workflow governance."
---

# Playbook control

Meta-layer governance for `rstack`, separate from running scientific phases in `research-mode`. Direct shortcuts (`/figure-it-out`, `/correct`, `/reflect`, `/statechart`, `/skill-creator`) remain available anytime; use `/playbook-control` when deciding which meta-action fits the situation.

## Route by goal

| Goal | Route to | What it produces |
|---|---|---|
| Task matches no existing playbook, or needs a bespoke auditable workflow | `figure-it-out` | A framed, hypothesis-driven workflow with `show-me-your-work` trail and verification predicate |
| Agents keep repeating the same mistake | `correct` | Structural fix (folder/schema/check script/test) + rule table entry; proved against a past mistake |
| Upgrade, simplify, or retire playbooks/skills from how a session went | `reflect` | 3-reviewer + synthesizer audit routed to edits in `research-space/rstack/` |
| Verify phase transitions, gates, or a stateful workflow against deadlocks/invariants | `statechart` | TLA+ / TLC model check (`docs/references/statechart/`) + shortest bug path or Mermaid statechart |
| Create or edit a skill or playbook | `references/authoring-a-skill.md` + `skill-creator` | Reuse-first sourcing ladder (bundled → installed → upstream → write), then verification gate |

## Mandatory Verification & Impact Gate

Before declaring any `playbook-control` change done (`correct`, `reflect`, `figure-it-out`, `statechart`, or skill/playbook edits):

1. **Root & manifest check:** Verify `rstack/README.md`, `rstack/.claude-plugin/plugin.json`, `rstack/.codex-plugin/plugin.json`, and workspace `AGENTS.md` / `CLAUDE.md` stay accurate.
2. **`rstack/docs/` sync:** Check `rstack/docs/README.md`, `rstack/docs/guide/`, `rstack/docs/bots/`, and `rstack/docs/references/` (including `playbooks.md` and `statechart/` TLA+ models when phase transitions change).
3. **Cross-file blast radius & principles:** Search `rstack/` (`rg`) for every renamed, moved, or removed skill, playbook, or file path across `scripts/`, `templates/`, and `references/` so no stale references remain. For any edited or new playbook, verify it declares `Specific principles:` (or `none (general only)`) alongside the general principles in `research-mode/SKILL.md`, and that every `principle-*` resolves in `research-mode/principles/`.
4. **Prove the check can fail (from `pstack` verification principles):** Whenever you add a new check, rule, or `Done when` gate, prove it fails on a real past mistake or temporary scratch break before confirming it passes, and prefer **synthetic known-answer tests** for calculation/script checks (so wrong formulas or units fail even when outputs look plausible). Always run `python3 rstack/scripts/check_plugin.py` and `claude plugin validate rstack`, then sync to `~/.gemini/config/plugins/rstack/` (never edit `~/.claude/plugins/cache/`).
