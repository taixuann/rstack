---- MODULE LearningStates ----
EXTENDS Naturals
\* One topic's learning in Notion, light loop. The user writes the page.
\* wrote: the user has written a passage. asked: the user asked about it and the talk is open.
\* satisfied: the user said they are satisfied. rewritten: the assistant rewrote the passage in the user's way.
\* open: Raw pages now open (the page plus its branches). level: 0 not checked, 2 explained.
VARIABLES wrote, asked, satisfied, rewritten, open, level
vars == <<wrote, asked, satisfied, rewritten, open, level>>

MaxOpen == 4   \* the page plus branches down to depth 3

Init == /\ wrote = FALSE /\ asked = FALSE /\ satisfied = FALSE /\ rewritten = FALSE
        /\ open = 0 /\ level = 0

UserWrites == /\ open = 0 /\ open' = 1 /\ wrote' = TRUE
              /\ UNCHANGED <<asked, satisfied, rewritten, level>>

\* The user asks. teach or explain answer in chat. The page does not change.
UserAsks == /\ wrote /\ ~asked /\ asked' = TRUE /\ satisfied' = FALSE
            /\ UNCHANGED <<wrote, rewritten, open, level>>

\* A question the user wants opened up becomes a new Raw page.
Branch == /\ open \in 1..(MaxOpen - 1) /\ open' = open + 1
          /\ UNCHANGED <<wrote, asked, satisfied, rewritten, level>>

UserSatisfied == /\ asked /\ ~satisfied /\ satisfied' = TRUE
                 /\ UNCHANGED <<wrote, asked, rewritten, open, level>>

\* Only after the user is satisfied, the assistant edits the passage.
Rewrite == /\ satisfied /\ rewritten' = TRUE /\ asked' = FALSE /\ satisfied' = FALSE
           /\ UNCHANGED <<wrote, open, level>>

\* A check runs only on request and only on a page the user wrote.
Check == /\ wrote /\ \E l \in {0, 2} : level' = l
         /\ UNCHANGED <<wrote, asked, satisfied, rewritten, open>>

Ingest == /\ open > 0 /\ ~asked /\ open' = open - 1
          /\ UNCHANGED <<wrote, asked, satisfied, rewritten, level>>

Done == UNCHANGED vars

Next == UserWrites \/ UserAsks \/ Branch \/ UserSatisfied \/ Rewrite \/ Check \/ Ingest \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == /\ {wrote, asked, satisfied, rewritten} \subseteq BOOLEAN
          /\ open \in 0..MaxOpen /\ level \in {0, 2}
\* The assistant rewrites nothing the user did not write.
RewriteNeedsPage == rewritten => wrote
\* Satisfied needs an open talk.
SatisfiedNeedsTalk == satisfied => asked
\* A page edit happens only after the user is satisfied.
EditOnlyWhenSatisfied == [][rewritten' /= rewritten => satisfied]_vars
\* A level is recorded only for a page the user wrote.
LevelNeedsPage == level = 2 => wrote
\* Ingest never closes a page while a talk is open.
NoIngestWithOpenTalk == [][open' < open => ~asked]_vars
====
