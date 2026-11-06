---- MODULE LearningStates ----
EXTENDS Naturals
\* One topic's learning in Notion. Zettelkasten, light version.
\* asked: the draft holds a question the assistant has not answered yet. answered: the assistant answered in chat.
\* updated: the draft parts were updated after the answer (small edits). structure: the user gave a structure.
\* notes: permanent notes written. splitSaid: the user said "split".
VARIABLES draft, asked, answered, updated, structure, notes, splitSaid
vars == <<draft, asked, answered, updated, structure, notes, splitSaid>>

MaxNotes == 3

Init == /\ draft = FALSE /\ asked = FALSE /\ answered = FALSE /\ updated = FALSE
        /\ structure = FALSE /\ notes = 0 /\ splitSaid = FALSE

UserWrites == /\ draft' = TRUE /\ asked' = TRUE /\ answered' = FALSE /\ updated' = FALSE
              /\ UNCHANGED <<structure, notes, splitSaid>>

\* The answer comes first, in chat. The page does not change yet.
Answer == /\ asked /\ ~answered /\ answered' = TRUE /\ asked' = FALSE
          /\ UNCHANGED <<draft, updated, structure, notes, splitSaid>>

\* Small updates to the draft parts, only after the answer.
UpdateDraft == /\ answered /\ ~updated /\ updated' = TRUE
               /\ UNCHANGED <<draft, asked, answered, structure, notes, splitSaid>>

UserGivesStructure == /\ answered /\ ~structure /\ structure' = TRUE
                      /\ UNCHANGED <<draft, asked, answered, updated, notes, splitSaid>>

WritePermanent == /\ answered /\ structure /\ notes = 0 /\ notes' = 1
                  /\ UNCHANGED <<draft, asked, answered, updated, structure, splitSaid>>

UserSaysSplit == /\ notes >= 1 /\ ~splitSaid /\ splitSaid' = TRUE
                 /\ UNCHANGED <<draft, asked, answered, updated, structure, notes>>

Split == /\ splitSaid /\ notes < MaxNotes /\ notes' = notes + 1 /\ splitSaid' = FALSE
         /\ UNCHANGED <<draft, asked, answered, updated, structure>>

Done == UNCHANGED vars

Next == UserWrites \/ Answer \/ UpdateDraft \/ UserGivesStructure \/ WritePermanent
        \/ UserSaysSplit \/ Split \/ Done

Spec == Init /\ [][Next]_vars

TypeOK == /\ {draft, asked, answered, updated, structure, splitSaid} \subseteq BOOLEAN /\ notes \in 0..MaxNotes
AnswerNeedsDraft == answered => draft
UpdateNeedsAnswer == updated => answered
NoteNeedsDraft == notes > 0 => draft
\* The page changes only after the answer.
EditOnlyAfterAnswer == [][(updated' /\ ~updated) => answered]_vars
\* The first permanent note needs an answer and the user's structure.
FirstNoteNeedsBasis == [][(notes = 0 /\ notes' > 0) => (answered /\ structure)]_vars
\* More than one note only when the user said split.
SplitOnlyWhenTold == [][(notes > 0 /\ notes' > notes) => splitSaid]_vars
====
