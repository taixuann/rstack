# Procedure

The frozen experimental procedure (SOP) for this question: one `## E<n>` block per experiment (for multi-stage SOPs, index `procedure/<NN>-<slug>.md` files from here). Do not edit sections 1 to 6 once frozen; record every deviation in [log.md](log.md). Lab inventory for this report is in [resources.md](resources.md); planned and executed units are in [samples.csv](samples.csv).

## E1: <name>

State: design. Status: planned. Serves: TODO: link to ../README.md objective and hypothesis.

Self-contained: **every** procedure file (whether `procedure.md` or each `procedure/<NN>-<slug>.md`) must be completely self-contained—including its own Materials/Solutions/Instrument Setup and Phase-structured steps—with every quantity having a value, unit, tolerance, and source copied in full. No wiki link or cross-file reference stands in for a bench number or setup step.

### 1. Objective and scope

- **Objective:** TODO: exact objective from `../README.md`.
- **Decision it supports:** TODO: one sentence (**principle-question-first**).
- **Hypothesis and refutation (if applicable):** TODO: falsifiable statement and what refutes it (**principle-exploratory-vs-confirmatory**).
- **Primary endpoint:** TODO: the measurement or check that decides.

### 2. Safety, pre-checks, and calibration

- **Hazards and PPE:** TODO (chemicals, thermal/electrical hazards, fume hood, PPE).
- **Pre-checks and instrument calibration:** TODO (zeroing, reference standard, compliance limits, environmental conditions).

### 3. Materials, solutions, and instrument setup

- **Materials / solutions / stocks:** TODO (reagents, grade, concentration, recipe, volume, overage from `resources.md`).
- **Instrument setup:** TODO (equipment model, key settings, ranges, compliance/booking limits from `resources.md`).
- **Specimen / unit specifications:** TODO (dimensions, substrate, cleaning, naming convention `<experiment>_<unit>_<technique>`).

### 4. Phase-structured procedure

#### Phase 1: Setup / mounting

1. TODO (order of operations, parallel steps, alignment, exact parameters/tolerances).

#### Phase 2: Execution

1. TODO (exact parameters, units, tolerances, hold times).

#### Phase 3: Post-test and storage

1. TODO (unloading, cleanup, waste disposal, raw file export path).

### 5. Acceptance, failure criteria, and what to record

- **Pass / acceptance criteria:** TODO.
- **Failure criteria and fallback:** TODO (when to abort or repeat, what to do next).
- **Mandatory log fields:** TODO (values `experiment-log` must capture in `log.md`).

### 6. Data and analysis handoff

- **Raw data destination:** `data/raw/` (via `raw-intake`).
- **Downstream analysis:** `analysis/<name>/` (or `N/A` if setup-only).

### 7. As-run log

Recorded in [log.md](log.md). Never rewrite sections 1 to 6 after freeze; log deviations in `log.md`.
