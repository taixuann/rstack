---
method: critic or interrogate, swarm, arena
date: YYYY-MM-DD
runs: {}
outcome: accepted
blocking: 0
---

Part of [README](../README.md). The review of the whole analysis. `runs` maps each accepted figure to the run reviewed, for example `runs: {iv-per-device: 20261108-113531}`. It must equal the runs in `docs/results/`; if a result is re-run and accepted, this review is stale.

## Do the claims agree?

TODO: each claim against the others; any contradiction between a check and a main result.

## Is every hypothesis decided?

TODO: each hypothesis from the README table, the result that decides it, and the figure it rests on.

## Anything chosen or left out?

TODO: runs chosen among several, units excluded, results not shown, post-hoc findings and how they are labelled.

## Findings

| # | Severity | Finding | Evidence | Repair |
|---|---|---|---|---|

## Outcome

TODO: accepted, rejected, or new-run. `blocking` is the count of open blocking findings; a blocker is closed by a new verified run or by a `waiver:` line the user wrote.
