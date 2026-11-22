---- MODULE FigureItOutStates ----
EXTENDS Naturals
\* figure-it-out on a task with two units. framed: the done predicate and rigor are stated.
\* found: each unit's source is chosen from the reuse ladder. harness: baseline and checks exist.
\* approved: the human accepted the workflow list. v: units verified. inc: units inconclusive.
VARIABLES framed, found, harness, approved, v, inc, whole, handed
vars == <<framed, found, harness, approved, v, inc, whole, handed>>

N == 2

Init == /\ framed = FALSE /\ found = FALSE /\ harness = FALSE /\ approved = FALSE
        /\ v = 0 /\ inc = 0 /\ whole = FALSE /\ handed = FALSE

Frame == /\ ~framed /\ framed' = TRUE /\ UNCHANGED <<found, harness, approved, v, inc, whole, handed>>
FindExisting == /\ framed /\ ~found /\ found' = TRUE /\ UNCHANGED <<framed, harness, approved, v, inc, whole, handed>>
BuildHarness == /\ found /\ ~harness /\ harness' = TRUE /\ UNCHANGED <<framed, found, approved, v, inc, whole, handed>>
Approve == /\ harness /\ ~approved /\ approved' = TRUE /\ UNCHANGED <<framed, found, harness, v, inc, whole, handed>>
\* One unit: hypothesis, smallest change, measure on the real artifact.
Verify == /\ approved /\ v + inc < N /\ v' = v + 1 /\ UNCHANGED <<framed, found, harness, approved, inc, whole, handed>>
Inconclusive == /\ approved /\ v + inc < N /\ inc' = inc + 1 /\ UNCHANGED <<framed, found, harness, approved, v, whole, handed>>
\* An inconclusive unit is retried; it is never counted as a pass.
Retry == /\ inc > 0 /\ ~handed /\ inc' = inc - 1 /\ whole' = FALSE /\ UNCHANGED <<framed, found, harness, approved, v, handed>>
CheckWhole == /\ v = N /\ ~whole /\ whole' = TRUE /\ UNCHANGED <<framed, found, harness, approved, v, inc, handed>>
Handback == /\ whole /\ ~handed /\ handed' = TRUE /\ UNCHANGED <<framed, found, harness, approved, v, inc, whole>>
Done == UNCHANGED vars

Next == Frame \/ FindExisting \/ BuildHarness \/ Approve \/ Verify \/ Inconclusive \/ Retry
        \/ CheckWhole \/ Handback \/ Done
Spec == Init /\ [][Next]_vars

TypeOK == /\ {framed, found, harness, approved, whole, handed} \subseteq BOOLEAN /\ v \in 0..N /\ inc \in 0..N
HarnessNeedsSources == harness => found
NoRunBeforeApproval == (v > 0 \/ inc > 0) => approved
InconclusiveNotPass == v + inc <= N
HandbackNeedsAllVerified == handed => (whole /\ v = N)
====
