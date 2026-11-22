---
name: academic-humanizer
description: "Audit academic prose for the marks of AI-assisted writing and for claims worded more strongly than their evidence: inflated verbs, significance hype, empty intensifiers, formulaic openers, connective overuse, clause-stacked sentences. It lists each pattern with its location; the author rewrites. Use in Paper critique (prose mode), when coaching a section, or when the user asks whether a passage reads as machine-written."
license: MIT
metadata:
  adapted-from: "AIScientists-Dev/academic-humanizer 0.3.3 (MIT), which builds on blader/humanizer (MIT)"
  changes: "audit only: the rewrite step is removed; examples rewritten for materials and devices; funding-proposal mode removed"
---

# Academic humanizer (audit)

Academic writing already has a human voice: neutral, exact, first-person plural, every claim tied to its evidence. This skill finds where a text leaves that voice. It does not rewrite. In rstack the author writes every sentence, so the output is a list of findings and the author repairs them. It is not a tool for hiding AI use; the venue's disclosure rule in `target.md` still applies.

## Process

1. **Read** the text, and a sample of the author's own earlier writing if there is one.
2. **Audit.** List each pattern below with file and line, the words that triggered it, and the kind of repair it needs (cut, quantify from the report, name the evidence, split, calibrate the verb). Do not give the repaired sentence.
3. **Check each claim** against the report: is there a number, figure or citation behind it, and is the verb no stronger than that evidence?
4. **Report** the findings by layer, with counts. Say what was left alone on purpose (Layer 3).

The examples below show the pattern and what a repair achieves. They are illustrations with invented values. Never offer them, or sentences like them, to the author as text to use.

## Layer 1: general patterns

Inflated significance ("marks a pivotal moment"); "-ing" tails that fake depth ("..., highlighting the role of..."); promotional words (rich, vibrant, groundbreaking, remarkable); vague attribution ("researchers have shown" with no citation); stock vocabulary (delve, underscore, intricate, tapestry, testament, landscape, pivotal, showcase, foster, leverage, realm, seamless); "serves as" where "is" would do; "not just X, but Y"; lists of three made for rhythm; a second and third name for one thing; filler ("it is worth noting that", "in order to"); em-dashes used as a habit.

## Layer 2: academic patterns

| Pattern | Watch for | What the repair does |
|---|---|---|
| Over-claiming verbs | demonstrate, prove, establish, confirm, guarantee; "significantly" with no test | the verb matches what was measured |
| Significance hype | paves the way, a crucial step toward, has the potential to revolutionise, opens new avenues, sheds light on, bridges the gap | names the one thing the work changes |
| Empty intensifiers | extensive, comprehensive, thorough, a wide range of, numerous, various | gives the count: which samples, how many devices |
| Novelty padding | "novel" more than once a section; "to the best of our knowledge"; "for the first time" | says what earlier work did not do, with the citation |
| Formulaic openers | "In recent years, X has attracted increasing attention"; "With the rapid development of" | opens on the specific problem |
| Connective overuse | consecutive sentences starting Moreover, Furthermore, Additionally | the logic carries the link |
| Contribution cliches | "a novel method, extensive experiments, strong results" | each contribution names its result |
| Citation dumping | "many groups have studied this [3, 7, 9, 12, 15]" | cites the works that matter and says why |
| Hedging by vagueness | somewhat, relatively, fairly, to some extent, quite | a number from the report, or cut |
| Boilerplate emphasis | "It is worth noting that", "Notably,", "Importantly," | the sentence shows it |
| Clause-stacked sentences | past about 30 words, or three or more subordinate clauses | one idea per sentence |

Illustration (invented values). Pattern: *"Our films demonstrate remarkably enhanced conductivity, paving the way for next-generation wearables."* After the author's repair, the same claim reads as a measured value with its unit, its uncertainty, its n and its figure, compared with the reference film, and the sentence about wearables is gone or is tied to a requirement the device meets.

## Layer 3: leave these alone

- **Hedging tied to evidence** is correct: suggests, is consistent with, we attribute, may indicate, when the claim really is uncertain. Flag the opposite error too: a hedge removed where the data do not carry the stronger verb.
- **Passive voice** where the actor does not matter: "Films were annealed at ...".
- **"We"** is standard.
- **Semicolons and an occasional list of three.**
- **Definitions, named methods, technical terms, equations and symbols** stay as they are.
- A number, an equation or a citation is never a style finding.

## Layer 4: claim and evidence

For each empirical claim: (a) is it backed by a number, figure, table or citation in the text, and is that number in the report; (b) does the verb match the strength of the evidence?

- Unbacked claim: say what evidence is missing. If the report has it, name the entry; if not, it is a gap for the analysis.
- Verb stronger than the evidence: name the verb and the evidence.
- Vague magnitude ("a large improvement"): name the report entry that gives the number.
- A comparison should lead with the strongest comparator, not the weakest.

## Layer 5: the author's voice

With a sample of the author's earlier papers, note their sentence length, how they open sections, how and where they hedge, and their recurring terms. A passage that departs from that voice is a finding ("this paragraph does not read like sections 2 and 3"), with the features that differ. Without a sample, say that voice was not checked.

## Output

A table: layer, pattern, file:line, the triggering words, the kind of repair. Then the counts per layer, what was left alone under Layer 3, and what could not be checked.
