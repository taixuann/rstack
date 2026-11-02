---
name: principle-prove-it-works
description: "Apply after completing a task, before declaring done. Verify against the real artifact: open the file, rerun the script, read the actual value, not a proxy or self-report."
disable-model-invocation: true
---

# Prove It Works

Verify every output by checking the real thing directly. Do not infer from file timestamps, agent self-reports, cached figures, or "the script ran without error".

- Read the value from the file the manuscript or report cites.
- Rerun the script from a clean state and diff against the saved output.
- When a check passes too easily, suspect the observation method before the result.

The strongest proof is a deterministic script a reviewer can rerun. Keep its output next to the result (see [show-me-your-work](../show-me-your-work/SKILL.md)).
