const name = (v) => !v.intake ? "Proposal intake" : !v.interrogated ? "Interrogate" : v.exit ? "Design" : v.review ? "State review passed"
  : v.synthesis ? "Proposal synthesis" : v.inquiry ? "Inquiry" : (v.scoped ? "Deepen: key papers and lessons" : "Scope: question, gap, feasibility");
export const title = "Explore: scope, then deepen";
export const state = (v) => [name(v), v.roadmap ? "roadmap written" : "no roadmap"];
export const group = (v) => v.exit ? "end" : v.review ? "ready" : "working";
export const colors = { working: "blue", ready: "teal", end: "tan" };
export const step = (a) => ({
  Intake: "proposal intake done", Interrogate: "aims and gaps written down", MakeRoadmap: "roadmap written from the gaps",
  IngestLesson: "a lesson is ingested in Notion", SyncDocs: "state documents updated from Notion",
  Register: "a paper goes into Zotero", Analyse: "the analyst freezes an analysis", CriticReview: "a separate critic passes it",
  Scope: "the question is narrow, a gap is named",
  Inquire: "questions from reviewed papers", Synthesise: "questions and methods written",
  StateReview: "the state review passes", Exit: "you approve the move to design", Done: "nothing more happens",
}[a]);
