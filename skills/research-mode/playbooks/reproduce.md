### Reproduce

Reproduce a paper's result, a prior run, or a claim before building on it.

1. Freeze the target and the success criterion (what number, within what tolerance) before running.
2. Use the `reproduce` skill. Run the canonical code path before any substitute. Capture inputs, environment, seeds, and commands.
3. Verdict from a fixed set: reproduced, reproduced within tolerance, partially reproduced, not reproduced, untestable.
4. For a mismatch, apply Attack the Premise: test shared assumptions (version, preprocessing, units) before changing the method.

**Reply:** verdict, the target versus achieved numbers, the exact commands, and every deviation.
