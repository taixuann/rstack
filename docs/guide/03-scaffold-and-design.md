# Scaffold and design

**Init.** `/rstack:init` creates `data/raw`, `docs/literature-review`, `docs/inputs`, `analysis`. `data/raw` is immutable.

**Design.** The Experimental design playbook writes into the question's folder `docs/reports/<question>/` (opened by Report bootstrap, whose `README.md` is the index): `method/design.md` (one `## E<n>` block per experiment), `method/resources.md` (chemicals, stocks, equipment and the characterization menu) and `method/samples.csv`. Each experiment block holds the purpose and falsifiable hypothesis, the design, the materials and stock solutions, a preparation plan that shows what runs in parallel, the protocol, the characterization tiers chosen before any result, risks, and an as-run section filled afterwards. Units go into the folder's `method/samples.csv`; what was done goes into `method/log.md`. Use `/arena` when two designs are plausible and `/interrogate` to attack the final one.
