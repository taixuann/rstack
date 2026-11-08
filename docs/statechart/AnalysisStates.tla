---- MODULE AnalysisStates ----
EXTENDS Naturals
\* One analysis, from plan to claim. plan: none, written, interrogated, approved.
\* check, main, verify: the README task groups, each open or done (one task each for the model).
\* challenged: the challenge review ran on the verified result. claimed: the result is cited.
VARIABLES plan, check, main, verify, challenged, claimed
vars == <<plan, check, main, verify, challenged, claimed>>

Init == /\ plan = "none" /\ check = "open" /\ main = "open" /\ verify = "open"
        /\ challenged = FALSE /\ claimed = FALSE

WritePlan == /\ plan = "none" /\ plan' = "written" /\ UNCHANGED <<check, main, verify, challenged, claimed>>
InterrogatePlan == /\ plan = "written" /\ plan' = "interrogated" /\ UNCHANGED <<check, main, verify, challenged, claimed>>
Approve == /\ plan = "interrogated" /\ plan' = "approved" /\ UNCHANGED <<check, main, verify, challenged, claimed>>
RunCheck == /\ plan = "approved" /\ check = "open" /\ check' = "done" /\ UNCHANGED <<plan, main, verify, challenged, claimed>>
RunMain == /\ check = "done" /\ main = "open" /\ main' = "done" /\ UNCHANGED <<plan, check, verify, challenged, claimed>>
RunVerify == /\ main = "done" /\ verify = "open" /\ verify' = "done" /\ UNCHANGED <<plan, check, main, challenged, claimed>>
Challenge == /\ verify = "done" /\ ~challenged /\ challenged' = TRUE /\ UNCHANGED <<plan, check, main, verify, claimed>>
Claim == /\ challenged /\ ~claimed /\ claimed' = TRUE /\ UNCHANGED <<plan, check, main, verify, challenged>>
\* An input file or the code changes after results exist: every result is stale and the claim goes with it.
InputChanges == /\ check = "done" /\ check' = "open" /\ main' = "open" /\ verify' = "open"
                /\ challenged' = FALSE /\ claimed' = FALSE /\ UNCHANGED plan
Done == claimed /\ UNCHANGED vars

Next == WritePlan \/ InterrogatePlan \/ Approve \/ RunCheck \/ RunMain \/ RunVerify
        \/ Challenge \/ Claim \/ InputChanges \/ Done
Spec == Init /\ [][Next]_vars

TypeOK == /\ plan \in {"none", "written", "interrogated", "approved"}
          /\ {check, main, verify} \subseteq {"open", "done"} /\ {challenged, claimed} \subseteq BOOLEAN
NoRunBeforeApproval == check = "done" => plan = "approved"
NoMainBeforeCheck == main = "done" => check = "done"
NoVerifyBeforeMain == verify = "done" => main = "done"
ChallengeNeedsVerify == challenged => verify = "done"
ClaimNeedsReview == claimed => (challenged /\ verify = "done")
====
