const names = { explore: "Explore", design: "Design", progressing: "Progressing", publish: "Ready for publish" };
export const title = "A research project, from first idea to closed";
export const state = (v) =>
  v.phase === "closed"
    ? ["Closed", v.reason === "published" ? "Published" : "Abandoned"]
    : [names[v.phase], v.gate ? "Review passed" : "Review pending"];
export const group = (v) => (v.phase === "closed" ? "end" : v.gate ? "ready" : "working");
export const colors = { working: "blue", ready: "teal", end: "tan" };
export const step = (a, from, to) => ({
  ClearGate: "the state review passes",
  Advance: "you move to the next state",
  Submit: "the paper is submitted",
  Abandon: "you abandon the project",
  GoBack: "you go back, and log why",
  Done: "nothing more happens",
}[a]);
