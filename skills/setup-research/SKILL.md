---
name: setup-research
description: "Set up the user's research defaults and, optionally, which models rstack uses per role. Use for /setup-research, 'set up research mode', 'configure my research preferences', changing citation style, journals, statistics defaults, slide template, or model choices, or when research-mode finds no research-profile.md. Writes research-profile.md in the research-space root and ~/.claude/rules/rstack-models.md."
---

# Setup research

Two outputs. The profile says how THIS user works. The model rule says which model each role uses.

## 1. Profile

1. Look for `research-profile.md` in the research-space root. If it exists, show it and ask what to change instead of starting over.
2. Ask one question at a time, recommended option first. Cover: field and typical study types; citation style and reference manager; target journals and format needs; statistics defaults (alpha, preferred tests, frequentist vs Bayesian, effect-size reporting, Python or R); preregistration habit; figure conventions (palette, font, size, format); slide and poster template and talk lengths; writing voice (person, tense, spelling); when the agent should ask versus decide.
3. Write `research-profile.md` as short bullet sections, one line per decision, with a date. Never write credentials, API keys, or personal identifiers.

## 2. Models (optional)

Ask whether to set models now. If no, say every role keeps the session model and stop.

1. Ask for a budget with AskUserQuestion: `unlimited` (max reasoning), `large` (xhigh), `medium` (high), `small` (medium). The effort value for each role starts from this.
2. Show the roles with defaults and ask whether to accept or change specific ones. Valid values are `opus`, `sonnet`, `haiku`, `fable`, or `inherit-parent` (omit `model`), each with the budget's effort.
3. Write `~/.claude/rules/rstack-models.md`, overwriting the whole file. No frontmatter. Shape:

```
# rstack model configuration. One line per role. Delete a line to fall back to the session model.
# budget: large (xhigh)
analysis and code: sonnet xhigh
judgment and prose: opus xhigh
hardest analysis: opus xhigh
literature workers: sonnet xhigh
swarm workers: sonnet xhigh
arena runners: opus xhigh, sonnet xhigh
interrogate reviewers: opus xhigh, sonnet xhigh
```

A panel role's list sets the fan-out: one subagent per entry.

## 3. Confirm

Read both files back and report their paths. Say the rule applies to new sessions. Re-running this skill updates both.
