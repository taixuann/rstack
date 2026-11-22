---- MODULE ExploreV3 ----
EXTENDS Naturals
\* Explore, starting at interrogate. interrogated: aims and gaps are written down. roadmap: the user's overview page exists (the name is from the retired Roadmap section).
\* lessons: Raw pages ingested in Notion. synced: lessons already carried into docs/rstack/explore/.
\* registered, analysed, reviewed: papers, as in ExploreStates.
VARIABLES scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review, exit
vars == <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

MaxL == 1
MaxP == 2

Init == /\ scoped = FALSE /\ intake = FALSE /\ interrogated = FALSE /\ roadmap = FALSE /\ lessons = 0 /\ synced = 0
        /\ registered = 0 /\ analysed = 0 /\ reviewed = 0
        /\ inquiry = FALSE /\ synthesis = FALSE /\ review = FALSE /\ exit = FALSE

Intake == /\ ~intake /\ intake' = TRUE /\ UNCHANGED <<scoped, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

\* Interrogate the proposal. Run again when the aims change: the roadmap and the review go stale.
Interrogate == /\ intake /\ ~exit /\ interrogated' = TRUE /\ roadmap' = FALSE /\ review' = FALSE /\ scoped' = FALSE
               /\ UNCHANGED <<intake, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, exit>>

MakeRoadmap == /\ interrogated /\ ~roadmap /\ ~exit /\ roadmap' = TRUE
               /\ UNCHANGED <<scoped, intake, interrogated, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

\* Teach, then ingest one Raw page. New learning makes the state documents and the review stale.
IngestLesson == /\ roadmap /\ ~exit /\ lessons < MaxL /\ lessons' = lessons + 1 /\ review' = FALSE
                /\ UNCHANGED <<scoped, intake, interrogated, roadmap, synced, registered, analysed, reviewed, inquiry, synthesis, exit>>

\* What the ingested pages show goes into docs/rstack/explore/.
SyncDocs == /\ ~exit /\ synced < lessons /\ synced' = lessons
            /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

\* Scope loop ends: the question is narrow, a gap is named, feasibility is judged. Needs a quick search (one paper registered).
Scope == /\ interrogated /\ registered > 0 /\ ~scoped /\ ~exit /\ scoped' = TRUE
         /\ UNCHANGED <<intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review, exit>>

\* The search serves the gaps interrogate found.
Register == /\ interrogated /\ ~exit /\ registered < MaxP /\ registered' = registered + 1
            /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, analysed, reviewed, inquiry, synthesis, review, exit>>
Analyse == /\ scoped /\ ~exit /\ analysed < registered /\ analysed' = analysed + 1
           /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, reviewed, inquiry, synthesis, review, exit>>
CriticReview == /\ scoped /\ ~exit /\ reviewed < analysed /\ reviewed' = reviewed + 1 /\ review' = FALSE
                /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, inquiry, synthesis, exit>>

Inquire == /\ ~exit /\ scoped /\ reviewed > 0 /\ ~inquiry /\ inquiry' = TRUE
           /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, synthesis, review, exit>>
Synthesise == /\ ~exit /\ inquiry /\ ~synthesis /\ synthesis' = TRUE
              /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, review, exit>>
StateReview == /\ ~exit /\ synthesis /\ synced = lessons /\ ~review /\ review' = TRUE
               /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, exit>>
Exit == /\ review /\ ~exit /\ exit' = TRUE
        /\ UNCHANGED <<scoped, intake, interrogated, roadmap, lessons, synced, registered, analysed, reviewed, inquiry, synthesis, review>>
Done == UNCHANGED vars

Next == Intake \/ Interrogate \/ Scope \/ MakeRoadmap \/ IngestLesson \/ SyncDocs \/ Register \/ Analyse
        \/ CriticReview \/ Inquire \/ Synthesise \/ StateReview \/ Exit \/ Done
Spec == Init /\ [][Next]_vars

TypeOK == /\ {scoped, intake, interrogated, roadmap, inquiry, synthesis, review, exit} \subseteq BOOLEAN
          /\ lessons \in 0..MaxL /\ synced \in 0..MaxL /\ registered \in 0..MaxP /\ analysed \in 0..MaxP /\ reviewed \in 0..MaxP
InterrogateFirst == (roadmap \/ registered > 0 \/ inquiry) => interrogated
LessonNeedsRoadmap == lessons > 0 => interrogated
ScopeFirst == (analysed > 0 \/ inquiry) => interrogated
DeepenNeedsScope == (inquiry \/ synthesis \/ exit) => interrogated
PaperChain == reviewed <= analysed /\ analysed <= registered
SyncNeedsLesson == synced <= lessons
InquiryNeedsPaper == inquiry => reviewed > 0
ExitNeedsFreshReview == exit => interrogated /\ (review /\ synthesis /\ synced = lessons)
\* Exit never follows a lesson or a new paper without a new state review.
NoExitOnStaleReview == [][exit' => review']_vars
\* A lesson ingested after the state review voids it.
LessonVoidsReview == [][lessons' > lessons => ~review']_vars
\* Blind analysis, critic review and inquiry only ever run on a scoped question.
DeepenOnlyScoped == [][(analysed' > analysed \/ reviewed' > reviewed \/ inquiry' /= inquiry) => scoped]_vars
====
