---- MODULE ResearchStates ----
EXTENDS Naturals
VARIABLES phase, gate, frozen, accepted, reason
vars == <<phase, gate, frozen, accepted, reason>>

Phases == {"explore", "design", "progressing", "publish", "closed"}
Next1 == [explore |-> "design", design |-> "progressing", progressing |-> "publish"]
Prev1 == [design |-> "explore", progressing |-> "design", publish |-> "progressing"]

Init == /\ phase = "explore" /\ gate = FALSE /\ frozen = FALSE /\ accepted = FALSE /\ reason = "none"

\* The state review passes. Design freezes the hypotheses; progressing accepts the results.
ClearGate ==
  /\ phase \in {"explore", "design", "progressing", "publish"} /\ ~gate
  /\ gate' = TRUE
  /\ frozen' = IF phase = "design" THEN TRUE ELSE frozen
  /\ accepted' = IF phase = "progressing" THEN TRUE ELSE accepted
  /\ UNCHANGED <<phase, reason>>

Advance ==
  /\ phase \in {"explore", "design", "progressing"} /\ gate
  /\ phase' = Next1[phase] /\ gate' = FALSE
  /\ UNCHANGED <<frozen, accepted, reason>>

Submit ==
  /\ phase = "publish" /\ gate
  /\ phase' = "closed" /\ reason' = "published" /\ gate' = FALSE
  /\ UNCHANGED <<frozen, accepted>>

Abandon ==
  /\ phase \in {"explore", "design", "progressing", "publish"}
  /\ phase' = "closed" /\ reason' = "abandoned" /\ gate' = FALSE
  /\ UNCHANGED <<frozen, accepted>>

\* Moving back is allowed; what the later state froze or accepted is undone.
GoBack ==
  /\ phase \in {"design", "progressing", "publish"}
  /\ phase' = Prev1[phase] /\ gate' = FALSE
  /\ frozen' = IF phase \in {"design", "progressing"} THEN FALSE ELSE frozen
  /\ accepted' = FALSE
  /\ UNCHANGED reason

Done == phase = "closed" /\ UNCHANGED vars

Next == ClearGate \/ Advance \/ Submit \/ Abandon \/ GoBack \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == /\ phase \in Phases /\ gate \in BOOLEAN /\ frozen \in BOOLEAN /\ accepted \in BOOLEAN
          /\ reason \in {"none", "published", "abandoned"}
\* No analysis starts before the design is frozen.
NoWorkBeforeFrozenDesign == phase \in {"progressing", "publish"} => frozen
\* No write-up before every result has a disposition.
NoWriteUpBeforeAccepted == phase = "publish" => accepted
\* A project is only published with its results accepted.
PublishedMeansAccepted == reason = "published" => accepted
\* A closed project has a reason, and only a closed one.
ClosedHasReason == (phase = "closed") <=> (reason /= "none")
====
