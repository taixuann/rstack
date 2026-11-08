const name = (v) => v.plan === "none" ? "No plan yet" : v.plan === "written" ? "Plan written"
  : v.plan === "interrogated" ? "Plan interrogated, awaiting approval"
  : v.claimed ? "Claim made" : v.challenged ? "Challenge review passed" : v.verify === "done" ? "Verified, ready for challenge"
  : v.main === "done" ? "Verify tasks to run" : v.check === "done" ? "Main tasks to run" : "Check tasks to run";
export const title = "One analysis, from plan to claim";
export const state = (v) => name(v);
export const group = (v) => v.claimed ? "end" : v.plan === "approved" ? "working" : "ready";
export const colors = { ready: "teal", working: "blue", end: "tan" };
export const step = (a) => ({
  WritePlan: "you and the assistant write the README and method", InterrogatePlan: "the plan is interrogated",
  Approve: "you approve the plan", RunCheck: "the check tasks pass", RunMain: "the main figures and tables are made",
  RunVerify: "the verify tasks pass", Challenge: "the challenge review finds nothing open",
  Claim: "the result is cited", InputChanges: "an input or the code changes, so results are stale",
  Done: null,
}[a]);
