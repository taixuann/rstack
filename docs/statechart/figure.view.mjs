const name = (v) => v.handed ? "Handed back" : v.whole ? "Whole checked" : v.approved ? "Run the loop"
  : v.harness ? "Workflow awaiting approval" : v.found ? "Build the harness" : v.framed ? "Find what exists" : "Frame";
export const title = "figure-it-out, from frame to hand-back";
export const state = (v) => [name(v), v.approved ? `${v.v} verified` : "before the run"];
export const group = (v) => v.handed ? "end" : v.approved ? "working" : "ready";
export const colors = { ready: "teal", working: "blue", end: "tan" };
export const step = (a) => ({
  Frame: "predicate and rigor stated", FindExisting: "each unit's source chosen", BuildHarness: "baseline and checks built",
  Approve: "the human accepts the workflow", Verify: "a unit is verified on the real artifact",
  Inconclusive: "a unit is inconclusive", Retry: "an inconclusive unit is retried",
  CheckWhole: "the whole is checked against the predicate", Handback: "hand back", Done: "nothing more happens",
}[a]);
