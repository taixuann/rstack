---
name: reflect
description: Spawn three parallel review subagents over the active session, surface learnings, and route each to a concrete edit on an existing skill or playbook, or a new one. Use when the user says reflect or /reflect, or wants to upgrade, modify, or retire playbooks based on how work went.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill and playbook edits. Skip when the session is trivial or already covered by a skill that was followed correctly. One-offs are not learnings.

## 1. Locate the transcript

Find this session's transcript under `~/.claude/projects/<slug>/`, where `<slug>` is the workspace path with each `/` and `.` changed to `-`. The newest `.jsonl` directly in that folder is the current session. Read only this workspace's folder. If you cannot find it, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

One message, three `Agent` calls, in the background. Use the prompts in [`references/reviewers.md`](references/reviewers.md) verbatim, with the transcript path or digest substituted. Reviewers return findings in their response. Use the models from `~/.claude/rules/rstack-models.md` (`judgment and prose`) if it exists, else omit `model`.

## 3. Synthesize

One more `Agent` call with `references/reviewers.md` section "Synthesizer", each reviewer's full output inlined. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a script, template, or check would enforce more reliably to Backlog, then run the **correct** skill on it (**principle-encode-lessons-in-structure**).

## 5. Apply

Present the full Accepted / Rejected / Backlog output and wait for explicit approval before editing. The user picks the subset and may redirect routings.

Edit only the canonical copy at `research-space/rstack/`. Never edit the installed copy under `~/.claude/plugins/cache/`. Never push.

Follow each approved row's routing:
- **Trivial edit** (a bullet, a tightened sentence, a stale fact): do it directly.
- **Substantive edit** (a new section or step list): use `skill-creator` and its draft, test, iterate loop.
- **New playbook:** run `figure-it-out` once on the task. If the phase list proved itself, save it as `skills/research-mode/playbooks/<title>.md`.
- **Delete a playbook:** grep for references first, then remove the file, its line in `skills/research-mode/SKILL.md`, and its README row.
- **Tune description:** the skill exists but did not trigger when it should have. Use `skill-creator`'s description loop.

After edits: update the playbook list, README table, and counts in `.claude-plugin/plugin.json`. Run `claude plugin validate rstack`, bump the version, run `claude plugin update rstack@research-space`.

## 6. Summarize

Short list, no preamble: edits applied (path, one line each), new skills or playbooks created, backlog items, and dropped findings with the synthesizer's reason.
