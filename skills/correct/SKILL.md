---
name: correct
description: "Find the mistakes agents keep repeating in this research project and make each one impossible. Try folder structure first, then a schema or template, then a check script whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat each time the operator corrects you. Use for /correct."
disable-model-invocation: true
---

# Correct

The operator keeps correcting agents for the same mistakes. Change the project so the next agent can't make them.

Assume every contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that runs. Design the project so a step that looks right from one file is right for the whole study.

## Find the mistake classes

Read recent decision logs (`show-me-your-work`), reviewer comments, `AGENTS.md`, and comments that explain workarounds. Group the mistakes into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with structure.** One home folder per output, one script per derived file, one source of truth for constants and sample lists. Make `data/raw` read-only. Delete old scripts and drafts an agent would copy.
2. **Enforce it with a schema or template.** Typed loaders, a design-note template with required fields, a results table with required columns. If a bad state still gets through, add a check script whose error names the file, column, or function to use instead.
3. **Test the behavior.** A synthetic-data test that recovers a known answer. Delete tests that pass when the analysis is wrong.
4. **Write docs or rules last, only for judgment calls.** Nothing fails when an agent skips them.

## Fix and prove

Fix the most frequent classes now, one change each. Prove each new check fails on a real past mistake. Exceptions go on the offending line with a reason and a date.

## Keep the rule table

Keep a table in `AGENTS.md` that pairs each rule with what enforces it. When the operator corrects you, fix the mistake and add the rule. If the rule was already there and nothing enforces it, that is a repeat, so fix it at the highest level in the same change. Drop a rule once its mistake can't happen.

**Reply:** each class with its evidence, the level you picked, and why a higher level didn't work.
