---- MODULE LearningStates ----
EXTENDS Naturals
\* One topic's learning in Notion. Raw pages are lessons; ingesting a Raw page closes it.
\* roadmap: the Roadmap section exists. open: Raw pages now open (the lesson plus its branches).
\* thread: a comment the user left is unanswered. ingested: an ingested page exists.
\* testing: the open page holds answers to an understanding test. level: 0 not explained, 2 explained.
VARIABLES roadmap, open, thread, ingested, testing, level
vars == <<roadmap, open, thread, ingested, testing, level>>

MaxOpen == 4   \* the lesson page plus branches down to depth 3

Init == /\ roadmap = FALSE /\ open = 0 /\ thread = FALSE
        /\ ingested = FALSE /\ testing = FALSE /\ level = 0

MakeRoadmap == /\ ~roadmap /\ roadmap' = TRUE /\ UNCHANGED <<open, thread, ingested, testing, level>>

OpenLesson == /\ roadmap /\ open = 0 /\ ~testing
              /\ open' = 1 /\ UNCHANGED <<roadmap, thread, ingested, testing, level>>

\* A branch is a new Raw page, linked to its parent.
Branch == /\ open \in 1..(MaxOpen - 1) /\ ~testing
          /\ open' = open + 1 /\ UNCHANGED <<roadmap, thread, ingested, testing, level>>

UserComments == /\ open > 0 /\ ~thread /\ thread' = TRUE
                /\ UNCHANGED <<roadmap, open, ingested, testing, level>>

AnswerComment == /\ thread /\ thread' = FALSE
                 /\ UNCHANGED <<roadmap, open, ingested, testing, level>>

\* The understanding test writes the user's answers onto a new Raw page.
StartTest == /\ ingested /\ open = 0 /\ ~testing
             /\ open' = 1 /\ testing' = TRUE
             /\ UNCHANGED <<roadmap, thread, ingested, level>>

\* Ingest rewrites one Raw page into its ingested page and closes the Raw page.
\* The level changes only when the closing page was a test page.
Ingest == /\ open > 0 /\ ~thread
          /\ open' = open - 1 /\ ingested' = TRUE
          /\ IF testing /\ open = 1
               THEN /\ testing' = FALSE /\ \E l \in {0, 2} : level' = l
               ELSE /\ UNCHANGED <<testing, level>>
          /\ UNCHANGED <<roadmap, thread>>

Done == UNCHANGED vars

Next == MakeRoadmap \/ OpenLesson \/ Branch \/ UserComments \/ AnswerComment
        \/ StartTest \/ Ingest \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == /\ roadmap \in BOOLEAN /\ open \in 0..MaxOpen /\ thread \in BOOLEAN
          /\ ingested \in BOOLEAN /\ testing \in BOOLEAN /\ level \in {0, 2}
\* No lesson before a roadmap.
NoLessonWithoutRoadmap == open > 0 => roadmap
\* A comment thread exists only on an open page.
ThreadOnOpenPage == thread => open > 0
\* Explained needs an ingested page that carries the Understanding section.
ExplainedNeedsIngested == level = 2 => ingested
\* Only a closing test page may change the level (re-ingest keeps Understanding).
LevelChangesOnlyByTest == [][level' /= level => testing]_vars
\* Ingest never runs with an unanswered comment.
NoIngestWithOpenComment == [][open' < open => ~thread]_vars
====
