### Task tracking

The only writer of `docs/rstack/tasks.md` and of the project's tasks in Notion. **Project docs** reads the file, **State review** turns findings into tasks through this playbook. Do not edit `tasks.md` elsewhere.

**The file.** One file, three levels, no deeper:

```
## Phase: explore
### Goal: Proposal intake
- [x] Run the project interview
- [ ] Get answers from the supervisor
```

Phase is a research state. A goal is an outcome of a few tasks. A task is one checkbox in plain words; detail and file names go in brackets at the end.

**Notion.** Three databases in the user's Second Brain: Projects, Milestones (goals), Tasks. The goal's Notion name carries the phase: `Explore · Proposal intake`. `docs/rstack/notion-map.tsv` ties each goal and task to its Notion page id: `# project <page id>`, then `goal|task<TAB>id<TAB>parent id<TAB>text`. No map: find the project in Projects (`notion-search`), confirm it with the user, then create the map. Never guess a page.

**Rules**

1. Local is the master. Notion is where the user sees and ticks tasks away from the desk.
2. Never invent a task. Tasks come from the user, the init defaults, a gate review finding, or a pull. Ask the user to write or confirm theirs.
3. Never set due dates, priorities, or status beyond Not Started and Complete. The user sets those.
4. Never delete a task or goal on either side. A task that vanished from one side is shown to the user, who decides.
5. Writing to Notion needs the user's yes for the first sync of a project. After that, a push mirrors only what the user already changed in `tasks.md`.

**Flow**

1. **Pull first.** Read the project's goals and tasks from Notion. For each mapped task: Complete in Notion and open locally → tick it locally. Changed title → show both and keep the local text unless the user picks Notion's.
2. **New in Notion.** A Notion task with no map row is the user's own addition. List them, then add each under its goal (or under `### Goal: Inbox` in the current phase if it has none) and add its map row. Do not reword it.
3. **Then push.** A local line with no map row: create the Notion task under its goal's page (create the goal first, with the phase prefix). A local line ticked: set Complete. A local line changed: update the Notion title. Do the same for a new goal.
4. **Conflict.** Both sides changed one task: the local file wins; name the task to the user.
5. Run `scripts/sync_readme_tasks.py <project>` after any change so the README block matches.
6. Append a row to `docs/rstack/decisions.tsv` when a pull added or ticked anything.

**Gate use.** At a state exit, **State review** passes only when every goal of the phase is all-ticked or the user marked its open tasks deferred. A new phase section is added here when the state changes, seeded from the defaults in **Project docs**.

**Reply:** what you pulled, what you pushed, any conflict or vanished task, then one question if the user must decide.
