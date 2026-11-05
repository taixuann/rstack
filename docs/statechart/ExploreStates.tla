---- MODULE ExploreStates ----
EXTENDS Naturals
\* The explore state of one project. Papers are counted, not named: two are enough to show the rules.
\* registered: papers in Zotero. analysed: frozen analysis exists. reviewed: an independent critic passed it.
\* lead: a deep-research or HyperResearch report exists (unverified) or was checked against a reviewed paper.
VARIABLES intake, registered, analysed, reviewed, lead, inquiry, synthesis, review, exit
vars == <<intake, registered, analysed, reviewed, lead, inquiry, synthesis, review, exit>>

MaxPapers == 2

Init == /\ intake = FALSE /\ registered = 0 /\ analysed = 0 /\ reviewed = 0
        /\ lead = "none" /\ inquiry = FALSE /\ synthesis = FALSE /\ review = FALSE /\ exit = FALSE

Intake == /\ ~intake /\ intake' = TRUE
          /\ UNCHANGED <<registered, analysed, reviewed, lead, inquiry, synthesis, review, exit>>

Register == /\ intake /\ ~exit /\ registered < MaxPapers /\ registered' = registered + 1
            /\ UNCHANGED <<intake, analysed, reviewed, lead, inquiry, synthesis, review, exit>>

\* The analyst reads blind to the user's annotations and freezes the analysis.
Analyse == /\ ~exit /\ analysed < registered /\ analysed' = analysed + 1
           /\ UNCHANGED <<intake, registered, reviewed, lead, inquiry, synthesis, review, exit>>

\* A fresh-context critic passes the analysis. A new passed paper makes an earlier state review stale.
CriticReview == /\ ~exit /\ reviewed < analysed /\ reviewed' = reviewed + 1 /\ review' = FALSE
                /\ UNCHANGED <<intake, registered, analysed, lead, inquiry, synthesis, exit>>

\* Discovery only produces leads.
FindLead == /\ intake /\ ~exit /\ lead = "none" /\ lead' = "lead"
            /\ UNCHANGED <<intake, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

\* A lead is used only after a reviewed paper confirms it.
VerifyLead == /\ lead = "lead" /\ reviewed > 0 /\ lead' = "verified"
              /\ UNCHANGED <<intake, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

Inquire == /\ ~exit /\ reviewed > 0 /\ ~inquiry /\ inquiry' = TRUE
           /\ UNCHANGED <<intake, registered, analysed, reviewed, lead, synthesis, review, exit>>

Synthesise == /\ ~exit /\ inquiry /\ ~synthesis /\ synthesis' = TRUE
              /\ UNCHANGED <<intake, registered, analysed, reviewed, lead, inquiry, review, exit>>

StateReview == /\ ~exit /\ synthesis /\ ~review /\ review' = TRUE
               /\ UNCHANGED <<intake, registered, analysed, reviewed, lead, inquiry, synthesis, exit>>

\* The user approves the move to design.
Exit == /\ review /\ ~exit /\ exit' = TRUE
        /\ UNCHANGED <<intake, registered, analysed, reviewed, lead, inquiry, synthesis, review>>

Done == UNCHANGED vars

Next == Intake \/ Register \/ Analyse \/ CriticReview \/ FindLead \/ VerifyLead
        \/ Inquire \/ Synthesise \/ StateReview \/ Exit \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == /\ intake \in BOOLEAN /\ registered \in 0..MaxPapers /\ analysed \in 0..MaxPapers
          /\ reviewed \in 0..MaxPapers /\ lead \in {"none", "lead", "verified"}
          /\ inquiry \in BOOLEAN /\ synthesis \in BOOLEAN /\ review \in BOOLEAN /\ exit \in BOOLEAN
\* Analysis comes from a registered paper; review comes from an analysed one (the critic is separate).
PaperChain == reviewed <= analysed /\ analysed <= registered
\* A lead becomes a claim only through a reviewed paper.
LeadNeedsPaper == lead = "verified" => reviewed > 0
InquiryNeedsReviewedPaper == inquiry => reviewed > 0
SynthesisNeedsInquiry == synthesis => inquiry
ExitNeedsReview == exit => (review /\ synthesis)
\* A new reviewed paper after the state review forces a new review before exit.
NoExitOnStaleReview == [][exit' => review']_vars
====
