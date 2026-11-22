# State charts

Charts of things that move between states, each checked with TLC through `/rstack:statechart`. Pictures that only show structure (the playbook map, for example) are in [../overview/](../overview/README.md).

| Chart | What it shows |
|---|---|
| [research-lifecycle/](research-lifecycle/README.md) | A project from first idea to closed, with the rules each state change must keep |
| [explore/](explore/README.md) | One lesson and two papers in the explore state |
| [analysis/](analysis/README.md) | One analysis from plan to claim (run gate, tick, review) |
| [figure-it-out/](figure-it-out/README.md) | The figure-it-out workflow (draft) |

Each folder holds the TLA+ model (`.tla`, `.cfg`), the view file, and a README with the rules and the command to rebuild.
