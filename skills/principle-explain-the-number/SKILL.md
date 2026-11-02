---
name: principle-explain-the-number
description: "Apply before you trust, report, or act on a measured number: an effect size, accuracy, p-value, rate, or fit. Find what limits it and rule out that it measured something other than what you think."
disable-model-invocation: true
---

# Explain The Number

- **Write the decision before you run.** Name the result that would change a decision and the noise floor. Stop when run-to-run or subject-to-subject spread exceeds the effect.
- **Ask "why not better or worse?"** Name what bounds the value: sample size, instrument error, sampling rate, units, baseline, preprocessing. A guess from reading the code is not a limiter.
- **List what else the number could be measuring** and rule out each with evidence: leakage, filtered or dropped samples, a default setting left untuned, artifacts, a unit error, a subset too small to matter.
- **Keep the evidence with the number.** Put n, spread, interval, and the limiter in the notes or a linked artifact.

A surprising number is a bug until shown otherwise. Distinct from [Prove It Works](../principle-prove-it-works/SKILL.md), which checks that an output is real.
