---
name: todoist-sync
description: Keeps a project's open tasks in Todoist (for the phone and the day-to-day) and in tasks.md (the master) in step. Use for /todoist-sync, when the user says "push tasks to Todoist", "sync Todoist", "I ticked things off in Todoist", or after tasks.md changes in a project that has a Todoist map.
---

# Todoist sync

`docs/rstack/<state>/tasks.md` is the master. Todoist is where the user sees and ticks tasks away from the desk. Deep analysis stays in the files. Only task lists cross over.

## Rules

1. **Every open task goes to Todoist.** Done tasks stay local. The user sets all dates. Never set a due date, deadline, priority or label.
2. **Plain words.** A task title is a short sentence a person understands without opening a file. Say "Get answers from the supervisor", not "Confirm with the supervisor: ML task, ethics...". Put the detail in the Todoist description. File names go in the description or in brackets at the end.
3. **The state is the section.** One Todoist section per research state, named `Phase - <State>` (`Phase - Explore`, `Phase - Design`, ...). Create a state's section when its `tasks.md` starts. Do not create sections for states without tasks. A `Project admin` section holds the weekly Sunday check (recurring, user-requested). It lives only in Todoist: leave it alone, and leave it out of counts and the map.
4. **Headings are tasks, items are subtasks.** Each `tasks.md` heading (Proposal intake, Scope, ...) is one top-level task in the state's section. Each open checkbox under it is a subtask of that task. Two levels only. A sub-point inside an item goes in the Todoist description, not a third level. In `tasks.md` it is an indented `Detail:` line under the item, which is not a checkbox.
5. **The map ties them.** `docs/rstack/todoist-map.tsv` holds the Todoist project id and, for each task and section, the Todoist id and the `tasks.md` line it was made from. Without a map, ask which Todoist project to use (or create one named after the project), then create the map. Never guess a project.
6. **Delete only what you created or the user names.** Leftovers you did not create (a project template, old sections) are not yours to remove or to keep silently: list them once and ask. Never create a duplicate: look the line up in the map first.
7. **Nothing leaves this machine except task text.** No signals, subject data, or file contents. Descriptions carry the same plain words as the task, nothing more.

## Run it

1. Read `state` in the project `README.md`, then `tasks.md` and the map.
2. Read the Todoist project (`find-tasks`, `find-sections`) with the project id from the map.
3. **Pull first.** A task checked off in Todoist and open in `tasks.md`: tick it in `tasks.md`. Do the same for its subtasks. A heading task whose subtasks are all done stays open until the user ticks it. Tell the user what you ticked.
4. **Then push.** A line in `tasks.md` with no map row: create it (`add-tasks`, parents before subtasks) and add a row. A line whose text changed since the map row: update the Todoist task (`update-tasks`) and the row. A task ticked in `tasks.md`: complete it in Todoist (`complete-tasks`). A new heading: add its parent task first.
5. **Conflicts.** If both sides changed one task, `tasks.md` wins, and you name the task to the user.
6. Run `research-mode/scripts/sync_readme_tasks.py <project>` after any change to `tasks.md`.
7. Log a pull or a conflict in `docs/rstack/decisions.tsv` when the run was long or unattended (`show-me-your-work`).

## Map format

Tab-separated. First line: `# project <todoist project id>`. Then one row per state section, heading task or item:

```
section	<id>		Phase - <State>
task	<id>	<parent id or empty>	<heading, or tasks.md line text>
```

## Check before you hand it over

- Run `todoist-sync/scripts/check_map.py <project>`. It fails on a nested checkbox, an open item with no map row, a row under the wrong heading, or a row for a done item. Fix `tasks.md` or the map until it passes. It checks the map, not Todoist itself, so also compare the `find-tasks` count to the open items.
- No due date, deadline, priority or label was set by you.
- Every created id is in the map.

**Reply:** what you pushed, what you ticked from Todoist, any conflict, then one question if the user must decide.
