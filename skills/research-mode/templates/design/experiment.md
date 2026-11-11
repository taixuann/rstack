# e01: <name>

Wiki source: TODO: path @ commit, or none.
State: design. Status: planned. Serves: TODO: question and hypothesis (link to the README).

Self-contained: every quantity below has a value, unit and source, copied in full. No link stands in for a number.

## 1. Purpose

- **Question:** TODO: one sentence.
- **Decision it supports:** TODO: one sentence (**principle-question-first**).
- **Type:** baseline or repeat / sweep (same recipe, one number changed) / confirmation / pilot.
- **Hypothesis and what would refute it:** TODO: a falsifiable sentence and the result that refutes it. Label exploratory or confirmatory (**principle-exploratory-vs-confirmatory**).
- **Primary endpoint:** TODO: the one measurement that decides.

## 2. Design

- **Unit** (sample, device, subject, session) and the level at which a true independent replicate exists: TODO.
- **Factors and levels:** TODO. **Held constant:** TODO. **Controls:** TODO (what differs from the control in only one thing).
- **Replicates** per condition and repeat measurements, with the spread you will accept: TODO.
- **Randomisation and run order:** seed, method, and the nuisance factors blocked (batch, day, operator, position): TODO. Made with the `experimental-design` skill scripts; keep the script call here.
- **Alternative design considered** and why this one: TODO (short tradeoff table).
- **Sample size:** TODO (replicates for devices and materials; a power calculation only for subject comparisons).
- **Pre-stated analysis:** the comparisons and how results are shown, written before data: TODO.

Unit rows go to `../samples.csv` with this experiment's id.

## 3. Materials

| item (from resources.md) | grade / lot | amount per unit | units | overage | total to prepare |
|---|---|---|---|---|---|
| TODO | | | | | |

Stock solutions to make:

| stock | concentration | volume | solvent | made on | used by step |
|---|---|---|---|---|---|
| TODO | | | | | |

Check against `resources.md`: enough on hand, not expired. Anything short is a task, not a surprise.

## 4. Preparation plan

Mark what can run in parallel and what only waits (drying, ageing, cooling). The longest chain of dependent steps sets the earliest finish; start it first.

| step | depends on | hands-on | wait | equipment or place | can run in parallel with |
|---|---|---|---|---|---|
| P1 Clean and dry glassware | none | 15 min | 60 min drying | sink, oven | P2, P3 |
| P2 Weigh solids | none | 20 min | | balance | P1 |
| P3 TODO | | | | | |

Run sheet (day by day, in start order): TODO.

## 5. Protocol

Step by step, as someone else would run it. For each step the setting, what to record, and the failure criterion. Naming of units and files: TODO (`<experiment>_<unit>_<technique>`).

1. TODO

## 6. Characterization tiers

Which units get which measurements, set before any result exists. A selection rule such as "control, each level, replicate 1 go to the expensive tier; the rest get the cheap tier" is fine. Choosing units after seeing the numbers is not, unless it is declared exploratory.

| tier | techniques | units (rule or list) | answers which claim |
|---|---|---|---|
| cheap (all units) | TODO | all | TODO |
| mid | TODO | TODO | TODO |
| expensive | TODO | TODO | TODO |

A mechanism claim needs a measurement of the mechanism. If no technique here measures it, the claim stays an interpretation.

## 7. Risks and fallbacks

| risk | trigger | fallback |
|---|---|---|
| TODO | | |

## 8. As run

Filled after the work. Deviations from sections 2 to 6 with the reason, units dropped or added, measurements skipped, anomalies. Raw files live in `data/raw/` (see **Raw intake**).

TODO: after the run.
