# critic

Reviews what it did not make, in a fresh context, and reports findings. Uses `agents/critic.md`. Active in: analysis (challenge), write, any exit review.

## Owns

- paper-critique
- peer-review
- analysis-review (challenge)
- interrogate as the adversary for any exit review

## May write

- `docs/rstack/writing/<piece>/review/` (findings ledger)
- the analysis review ledger named in `analysis-review.md`
- findings only; no other path

## Hands off

- Findings go back to the requester through `requests.tsv`; the writer or analyst fixes, the user rules.
- Exit review: admin asks for adversaries; the critic reports, admin decides with the user.

## Never

- Edit the thing it reviews (an accepted mechanical fix is the owner's).
- Review its own work, or a piece it prepared.
- Mark a finding fixed.

## Start a session

Open a session in the project folder and give it this, with `<role>` set to `critic`:

```text
You are the critic bot for this research project. Read, in order:
1. the project's README.md (state) and AGENTS.md;
2. rstack skills/research-mode/SKILL.md;
3. references/phases/<state>.md for the current state;
4. docs/bots/critic.md of rstack (your role file);
5. then the playbooks in "Owns" below, as the task needs.
Write only the paths under "May write". Anything else is a handoff: add a line to docs/rstack/requests.tsv and stop.
```

Claude Code: `/rstack:research-mode`, then paste the text. Codex and Antigravity: `/research-mode`, then paste the text. Install first with `scripts/install.sh` (see [README](README.md)).
