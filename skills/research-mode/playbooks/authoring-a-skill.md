### Authoring or modifying a skill or playbook

Writing or editing a SKILL.md or a playbook. Reuse upstream skills before writing new ones.

**Sourcing ladder.** Take the first rung that works:
1. **Bundled.** A folder in `skills/` already does it. Use it.
2. **Installed elsewhere.** Another installed plugin or user skill does it. Name it in the playbook and declare it in `references/skills-manifest.yaml` as an external.
3. **Upstream.** Search K-Dense `scientific-agent-skills`, `anthropics/skills`, `claude-scientific-writer`, and the plugin catalog. Before adopting, read it in full and check: the licence allows redistribution (Anthropic's `docx`, `pdf`, `pptx`, `xlsx` do not), it needs no runtime tools Claude Code lacks (the OpenScience skills needed `compute_job`), and it fits a materials and devices workflow. Then either bundle it with the licence and a credit in `LICENSE`, or declare it external.
4. **Write it.** Use `skill-creator`: draft, test on a real task, iterate. Keep only prose that changes a decision, and delegate to other skills by name.

**Steps**
1. Decide the rung, and record the decision in the manifest or in the playbook's first lines.
2. Edit the skill or playbook. Update the playbook list in `skills/research-mode/SKILL.md` and the README table.
3. Run `scripts/check_plugin.py` from the plugin root, then `claude plugin validate rstack`. Fix what they report.
4. A workflow you keep hitting but is not captured: use `/reflect` to route it. If it is one-off, use `figure-it-out`.

**Reply:** what the skill does, the rung you chose and why, and the validation result.
