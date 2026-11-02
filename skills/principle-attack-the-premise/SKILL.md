---
name: principle-attack-the-premise
description: "Apply when two or more analyses or fixes fail for the same reason. Write the shared assumption down and test it before another attempt."
disable-model-invocation: true
---

# Attack The Premise

Two failures with one premise are one failure. Stop, write the premise down, and test it directly (sanity plot, synthetic data, a known-answer case) before you try a third variant.

Typical premises to test: the data are what the metadata says, the units and sampling rate are right, the labels are correct, the preprocessing preserved the signal, the instrument was calibrated.
