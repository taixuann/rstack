const name = (v) => !v.intake ? "Proposal intake" : v.exit ? "Design" : v.review ? "State review passed"
  : v.synthesis ? "Proposal synthesis" : v.inquiry ? "Inquiry" : "Literature review";
export const title = "The explore state, from intake to design";
export const state = (v) => [name(v), v.reviewed > 0 ? "a paper has passed" : "no paper passed yet"];
export const group = (v) => v.exit ? "end" : v.review ? "ready" : "working";
export const colors = { working: "blue", ready: "teal", end: "tan" };
export const step = (a) => ({
  Intake: "proposal intake done", Register: "a paper goes into Zotero", Analyse: "the analyst freezes an analysis",
  CriticReview: "a separate critic passes it", FindLead: "a search report arrives as a lead",
  VerifyLead: "a reviewed paper confirms the lead", Inquire: "questions drawn from reviewed papers",
  Synthesise: "questions and methods written", StateReview: "the state review passes",
  Exit: "you approve the move to design", Done: "nothing more happens",
}[a]);
