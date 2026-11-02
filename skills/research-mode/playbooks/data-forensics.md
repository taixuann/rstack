### Data forensics

Diagnose an anomaly in captured data (noise bursts, drift, dropouts, label errors, a sensor artifact). The deliverable is a diagnosis, not a fix.

1. Describe the symptom precisely: which files, channels, times, and how it differs from expected.
2. Work on a copy or read-only view. Never edit `data/raw/`.
3. Run `exploratory-data-analysis` first, then targeted plots of the suspect segments next to a clean one.
4. List candidate causes (instrument, preprocessing, motion, mains interference, export bug) and test each with an observation that would separate them.
5. Report the cause with evidence, or the remaining candidates and the next measurement that would separate them.

**Reply:** diagnosis, evidence with paths, what was ruled out, and the recommended next step.
