---
name: principle-raw-data-is-read-only
description: "Apply whenever you touch measured data. Derive, never overwrite; keep the script behind every derived file."
disable-model-invocation: true
---

# Raw Data Is Read Only

- `data/raw/` is immutable. Never edit, rename, or regenerate its contents.
- Every derived file has a script that makes it and a record of the inputs it read (path, hash, version).
- Do not invent measurements, metadata, parameters, or thresholds. If something is missing, return a blocker.
- Synthetic or simulated data lives apart from real data and is labelled as such.
