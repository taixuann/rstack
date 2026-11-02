---
name: principle-separate-before-serializing-shared-state
description: "Apply when parallel workers might write the same file, table, or output. Give each its own location, then merge."
disable-model-invocation: true
---

# Separate Before Serializing Shared State

Assign each worker its own output path or worktree. Merge results in one step after all workers finish. Two workers editing one notebook, table, or manuscript is a race, not a collaboration.
