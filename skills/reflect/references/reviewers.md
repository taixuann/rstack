# Reviewer prompts

Substitute `<transcript>` with the transcript path or digest. Each reviewer returns findings only: quote or cite the transcript line, say what went wrong or right, and propose one concrete edit target (a principle, a playbook step, a skill description, a script or template).

## Judgment reviewer

Read `<transcript>`. Find places where the agent's judgment was corrected or should have been: a wrong question answered, a premise not attacked, a number reported without its limiter, a post-hoc finding not labelled, a stop-and-ask that a pilot could have settled. For each, name the principle or playbook step that should have prevented it and whether it exists but was skipped or is missing.

## Tooling reviewer

Read `<transcript>`. Find friction in tools and skills: a skill that did not trigger, a playbook step that named a missing skill, repeated manual steps that a script would remove, failed commands, wrong paths, unit or format errors. For each, propose the script, template, or description change.

## Divergent reviewer

Read `<transcript>`. Argue the opposite case: which playbook steps were wasted ceremony, which principles added no value here, and what a leaner or different workflow would have done. Flag anything worth deleting.

## Synthesizer

Merge the three outputs. Spot-check each finding against the transcript. Return three lists. **Accepted:** specific, evidenced, recurring, with a routing (trivial edit, substantive edit, new playbook, delete playbook, tune description, or structure). **Rejected:** one-offs, unsupported, or already covered, with the reason. **Backlog:** valid but larger than one edit. Drop any item that happened only once unless it is severe.
