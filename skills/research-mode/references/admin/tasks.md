# Tasks job (advisor)

The advisor for the project's tasks, and the only writer of `docs/rstack/tasks.md` and `docs/rstack/todoist-map.tsv`. It also changes the project's tasks in Todoist. It runs when the user asks, and also on its own when project-admin runs or a session starts on a project: it reads Todoist and the project, then tells the user what it sees. Do not edit `tasks.md` anywhere else.

**The file.** One file, three levels, no deeper:

```
## Phase: explore
### Goal: Proposal intake
- [x] Run the project interview
- [ ] Get answers from the supervisor
  Detail: ask about the ML task and the ethics route
```

Phase is a research phase. A goal is an outcome of a few tasks. A task is one checkbox in plain words; file names go in brackets at the end. A sub-point is an indented `Detail:` line, never a nested checkbox.

**Task title.** A title reads alone, to someone who does not know the intention. It names the action, the thing acted on, and what it is about or where it lives. "Get answers from the supervisor" fails (answers to what?). "Get the supervisor's answers on machine learning, ethics, equipment and prototype goals (the open points in 01_context.md)" passes. Name files and topics in the title; keep the steps in the `Detail:` lines. `check_map.py` fails a title under 7 words (not counting a Basic, Core or Advanced prefix) and an `After` line repeated on several tasks; write it once, on the last task of the group.

**Task shape.** A goal is a chain: prepare, do, capture, follow on. Write the chain inside the task, as `Detail:` lines, never as extra tasks. A task keeps one line; its `Detail:` lines say `Before` (what must exist), `Steps` (when it has several), `Done when` (its output) and `After` (what the result changes or feeds). A task that starts with Learn, Ask, Build, Get, Agree, Finish, Write or Stress-test carries `Detail: Done when ...`; `check_map.py` fails on one without it. Add a task only for a separate outcome the user would tick on its own. A step that waits on something the user does not control (a meeting day, a part arriving) gets no date. Dates: a due date is the day the user plans to work; a deadline is only a real external cutoff; reminders only for fixed events. The user sets all three. An optional `When and where` line is written by the user.

**Todoist.** One Todoist project per research project, with the same two levels as the file:

- A phase is a section named `Phase - <State>` (`Phase - Explore`). Create it when that phase starts in `tasks.md`.
- A goal is a top-level task in its phase's section.
- A task is a subtask of its goal. A `Detail:` line goes in the Todoist description.
- The `Project admin` section holds the project-wide goals (for example `Maintain scope`), kept in `tasks.md` under `## Phase: admin`. They outlive the phases and sit outside the phase gates; the exit review still reads them. The weekly Sunday check also sits there. It lives only in Todoist: leave it alone and leave it out of counts and the map.
- Tools: `find-projects`, `find-sections`, `find-tasks`, `add-sections`, `add-tasks`, `update-tasks`, `complete-tasks`, `uncomplete-tasks`.

`docs/rstack/todoist-map.tsv` ties them. Tab-separated; the first line is `# project <todoist project id>`, then one row per section, goal or task:

```
section	<id>		Phase - Explore
task	<id>		<goal name, without "Goal: ">
task	<id>	<goal id>	<task text from tasks.md>
```

No map: find the project (`find-projects`), or offer to create one named after the research project, confirm it with the user, then create the map. Never guess a project.

**Rules**

1. Local is the master. Todoist is where the user sees and ticks tasks away from the desk, so only open tasks go there. Done tasks stay local.
2. Advise, never decide. The user sets every due date, deadline and reminder: set one only when the user names the day or asks you to assign dates, and never set a priority or label. Never delete a task or goal on either side, except one you created that the user asked you to remove. Never invent a task. A task comes from the user, the phase's starting tasks, an exit-review finding, or a pull. Suggestions are labelled as suggestions.
3. The first push of a project to Todoist needs the user's yes. After that, write to Todoist only what the user already changed in `tasks.md` or approved in an advice round. Never write a suggestion unapproved.
4. A task that vanished from one side is shown to the user, who decides.
5. Never create a duplicate: look the line up in the map first. Delete only what you created or the user names. Leftovers you did not create (a project template, old sections) are listed once, then you ask.
6. Nothing leaves this machine except task text in plain words. No signals, subject data or file contents. A description carries the same words as the task, nothing more.

**Flow**

1. **Pull.** Read the project's sections and tasks from Todoist every time (`find-sections`, `find-tasks` with the project id from the map). For each mapped task: completed in Todoist and open locally → tick it locally. A goal whose tasks are all done stays open until the user ticks it. Changed title → show both and keep the local text unless the user picks Todoist's. A Todoist task with no map row is the user's own addition: add it under its goal (or `### Goal: Inbox` in the current phase) with a map row, without rewording.
2. **Assess.** Compare the task list with `references/phases/<phase>.md` (starting tasks, playbooks in order, exit gate angles), the `docs/rstack/` documents with that `phase:`, `docs/reports/<question>/`, `analysis/<name>/docs/results/`, `decisions.tsv` and the README. Look for:
   - the task blocking the most others, and the playbook that is next;
   - starting tasks or gate findings with no task;
   - tasks that look done in the files but are unticked, or ticked with no evidence;
   - stale tasks, duplicates, goals out of order, a phase nearly ready for its exit review;
   - work in the files that no task covers;
   - tasks whose title does not read alone (see Task title) or that break the Task shape: a gating task with no `Done when`, or chain steps written as separate tasks (merge them into the parent's `Detail:` lines).
3. **Advise.** Tell the user, in a short numbered list with the recommendation first: what you see, what you suggest (reorder, add, defer, tick, split, start the exit review), and why, each pointing to the file or Todoist item it came from. Ask only about choices that are the user's. Stop there when the user did not ask for changes.
4. **Apply what the user approves.** Write each chain as `Detail:` lines on its one task, and copy those lines into the Todoist description (`update-tasks`). Add a task only for a separate outcome. Edit `tasks.md`, then push to Todoist: parents before subtasks (`add-tasks`), changed text with `update-tasks`, ticked tasks with `complete-tasks`; add every created id to the map. Then run `scripts/sync_readme_tasks.py <project>` so the README block matches. Both sides changed one task: the local file wins; name the task.
5. **Check.** Run `scripts/check_map.py <project>`. It fails on a nested checkbox, an open task with no map row, a row under the wrong goal, or a row for a done task. It checks the map, not Todoist, so also compare the `find-tasks` count to the open tasks.
6. **Record.** Update `docs/rstack/` so it matches what is now decided, without asking when it only records the user's decision or a pulled fact: the phase notes (for example a deferred task and its reason, an accepted result and its tick), and a row in `decisions.tsv` for each pull, tick, deferral or reorder. Anything that is your own judgment, not the user's, is shown first.

**Gate use.** At a phase exit, the exit review passes only when every goal of the phase is all-ticked or the user marked its open tasks deferred. Goals under `## Phase: admin` are not part of that rule, but the review reads them (for example the scope check). A new phase section is added here when the phase changes, seeded from `references/phases/<phase>.md`, and its Todoist section is created at the next push.

**Reply:** what you pulled, what you see, your suggestions as a numbered list, what you recorded in `docs/rstack/`, then one question if the user must decide.
