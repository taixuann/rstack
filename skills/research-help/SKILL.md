---
name: research-help
description: "Guides the user through rstack setup, /research-mode, and picking the skill, playbook, or principle for a task. Use for /research-help with a question, when the user asks what research mode can do, which playbook fits, how to start a project, or how to phrase a research request."
disable-model-invocation: true
---

# Research help

Answer the user's question about rstack, hand them a prompt they can send, and name the file the answer came from. For a help question, don't start the work. A research run spends real tokens, so let the user send the prompt.

A message that asks for work ("design a study for X") is not a help question. Read [`research-mode`](../research-mode/SKILL.md) and do the work under it.

Read the file you route to before you quote it. If the user's need is unclear, ask one question with these options: Get set up, Start a task, Pick a skill for a situation, Fix a run that went wrong.

State that changes the answer, mentioned only when it does:
- No `research-profile.md` in the research-space root means `/setup-research` has not run.
- No `~/.claude/rules/rstack-models.md` means every role uses the session model.

## Get set up
1. Install: `/plugin marketplace add <path to research-space>`, then `/plugin install rstack@research-space`.
2. Run [`/setup-research`](../setup-research/SKILL.md).
3. Start a real task with `/research-mode`, a goal, and a check that can pass or fail.

## Start a task
`/research-mode` states the question, matches a playbook, copies its steps into the todo list, and runs other skills as the steps need them. A good prompt states the goal and how to tell it is done. It does not list skills. Read [`references/prompting.md`](references/prompting.md) before you help word one.

## Pick a skill
Default answer: `/research-mode`. Name a skill directly when the user wants more or less than a playbook gives.

| The user wants to | Skill |
|---|---|
| Do any research task with rigor | `research-mode` |
| Run parallel workers, one per paper or dataset | `swarm` |
| Compare competing designs or drafts and combine the best | `arena` |
| Stress-test a design, analysis, or draft | `interrogate` |
| Plan a bespoke workflow when no playbook fits | `figure-it-out` |
| Keep a decision trail for long or unattended work | `show-me-your-work` |
| Set defaults and models | `setup-research` |

For recipes and common mistakes, read [`references/recipes.md`](references/recipes.md). The guide in `docs/guide/` walks through a first real task.
