# Scaffold and design

**Init.** `/rstack:init` creates `data/raw`, `docs/literature-review`, `docs/inputs`, `analysis`. `data/raw` is immutable.

**Design.** The Experimental design playbook writes `docs/rstack/design/`: a `README.md` map, `resources.md` (chemicals, stocks, equipment and the characterization menu), and one note per experiment (`e01_<slug>.md`). Each note holds the purpose and falsifiable hypothesis, the design, the materials and stock solutions, a preparation plan that shows what runs in parallel, the protocol, the characterization tiers chosen before any result, risks, and an as-run section filled afterwards. Units go into `docs/rstack/samples.csv`. Use `/arena` when two designs are plausible and `/interrogate` to attack the final one.
