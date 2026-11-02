---
name: principle-sequence-verifiable-units
description: "Apply to multi-step work such as load, QC, model, figure, or a sweep over datasets. Break it into small units that each end in a check, and verify each before the next."
disable-model-invocation: true
---

# Sequence Verifiable Units

Order the work so each step ends in a check: loaded row counts match the source, QC flags are plausible, the model recovers a synthetic ground truth, the figure matches the table. Fix an error where it first appears, not at the end.

Prefer many small checked outputs over one large unchecked run.
