#!/usr/bin/env python3
"""Offline check that tasks.md and the Todoist map agree. Usage: check_map.py PROJECT_DIR | --selftest

Rules (see references/admin/tasks.md): open checkboxes sit directly under a `### Goal:` heading
(no nesting), a task starting Learn, Ask, Build, Get, Agree, Finish, Write or Stress-test has a `Detail: Done when ...` line, every goal with open tasks and every open task has a map row, a task's row is under
its goal's row with the same text, and no map row points at a done or missing task.
Checks titles (7 words or more) and repeated After lines.
Checks the current phase and any other phase whose goals are already in the map. Exit 1 and name each problem.
"""
import re, sys
from pathlib import Path

OLD = {"analysis": "progressing", "write": "ready-for-publish"}  # names used before 0.34.0


def phase_text(tasks_text, state):
    names = "|".join(re.escape(n) for n in (state, OLD.get(state, state)))
    m = re.search(rf"^## Phase: (?:{names})\s*$(.*?)(?=^## Phase:|\Z)", tasks_text, re.M | re.S)
    return m.group(1) if m else None


PREFIX = re.compile(r"^(?:Basic|Core|Advanced): ")
GATING = re.compile(r"^(?:(?:Basic|Core|Advanced): )?(?:Learn|Ask|Build|Get|Agree|Finish|Write|Stress-test)\b")


def parse_tasks(text):
    """Return (errors, {goal: [open task text]}). A gating task (Learn, Ask, Build, Get, Agree, Finish, Write, Stress-test) needs a 'Detail: Done when ...' line."""
    errs, goals, cur, pend, afters = [], {}, None, None, {}

    def close():
        if pend and len(PREFIX.sub("", pend[0]).split()) < 7:
            errs.append(f"phase line {pend[1]}: title '{pend[0][:50]}' is too short to read alone; name the action, the thing and what it is about (7 words or more)")
        if pend and GATING.match(pend[0]) and not pend[2]:
            errs.append(f"phase line {pend[1]}: task '{pend[0][:50]}' has no 'Detail: Done when ...' line (name its output and what it changes)")

    for n, line in enumerate(text.splitlines(), 1):
        g = re.match(r"^### Goal:\s*(.+?)\s*$", line)
        if g:
            close(); pend = None
            cur = g.group(1)
            goals.setdefault(cur, [])
            continue
        a = re.match(r"^\s+Detail:\s*(After.*)$", line)
        if a:
            afters.setdefault(a.group(1), []).append(n)
        d = re.match(r"^\s+Detail:\s*Done when", line)
        if d and pend:
            pend[2] = True
            continue
        m = re.match(r"^(\s*)- \[([ xX])\] (.+)$", line)
        if m:
            close(); pend = None
            indent, mark, item = m.groups()
            if indent:
                errs.append(f"phase line {n}: nested checkbox '{item[:40]}'; Todoist has two levels, so use an indented 'Detail:' line")
            elif cur is None:
                errs.append(f"phase line {n}: checkbox before any '### Goal:' heading")
            elif mark == " ":
                goals[cur].append(item.strip())
                pend = [item.strip(), n, False]
    close()
    for text, lines in afters.items():
        if len(lines) > 1:
            errs.append(f"phase lines {lines}: the same 'After' line is repeated; write it once, on the last task of the group")
    return errs, goals


def parse_map(text):
    rows = [l.split("\t") for l in text.splitlines() if l and not l.startswith("#")]
    return [(r + [""] * 4)[:4] for r in rows]


def check(phase_body, map_text):
    errs, goals = parse_tasks(phase_body)
    by_text = {r[3]: r for r in parse_map(map_text) if r[0] == "task"}
    for goal, items in goals.items():
        if not items:
            continue
        grow = by_text.get(goal)
        if not grow or grow[2]:
            errs.append(f"goal '{goal}' has open tasks but no top-level map row")
            continue
        for item in items:
            r = by_text.get(item)
            if not r:
                errs.append(f"open task '{item[:50]}' under '{goal}' has no map row (push it)")
            elif r[2] != grow[1]:
                errs.append(f"map row for '{item[:50]}' is not under goal '{goal}'")
    open_all = {i for items in goals.values() for i in items}
    mine = {by_text[g][1] for g in goals if g in by_text}  # only rows under this phase's goals
    for r in by_text.values():
        if r[2] in mine and r[3] not in open_all:
            errs.append(f"map row '{r[3][:50]}' matches no open task (done, renamed or removed; sync it)")
    return errs


def selftest():
    def fx(*titles):
        """A goal with open tasks (given titles) and a map that matches."""
        body = "### Goal: G\n" + "".join(f"- [ ] {x}\n" for x in titles)
        return body, "# project 1\ntask\t1\t\tG\n" + "".join(f"task\t{i + 2}\t1\t{x}\n" for i, x in enumerate(titles))

    A = "Read the first paper on the signal chain"
    t, m = fx(A)
    assert check(t, m) == []
    assert check(t + "  - [ ] sub\n", m), "nested checkbox must fail"
    assert check(t.replace("first", "second"), m), "renamed task must fail"
    assert check(t + "- [ ] Read the second paper on the signal chain\n", m), "unmapped task must fail"
    assert check("### Goal: G\n- [x] " + A + "\n", m), "done task with a row must fail"
    G = "Ask the supervisor for a meeting about the project plan"
    assert check(*fx(G)), "gating task without Done when must fail"
    assert check(*fx("Core: " + G.replace("Ask", "Learn"))[:1], fx(G)[1].replace(G, "Core: " + G.replace("Ask", "Learn"))), "Learn without Done when must fail"
    ok = "### Goal: G\n- [ ] " + G + "\n  Detail: Done when: a meeting day is fixed\n"
    assert check(ok, fx(G)[1]) == []
    F = "Finish the context document and give each unknown an owner"
    assert check(*fx(F)), "Finish without Done when must fail"
    S = "Get answers from the supervisor"
    assert check("### Goal: G\n- [ ] " + S + "\n  Detail: Done when: x\n", fx(S)[1]), "short title must fail"
    L1, L2 = "Learn how the first thing in the study works", "Learn how the second thing in the study works"
    two = "### Goal: G\n" + "".join(f"- [ ] {x}\n  Detail: Done when: a\n  Detail: After: same\n" for x in (L1, L2))
    assert check(two, fx(L1, L2)[1]), "repeated After must fail"
    assert phase_text("## Phase: explore\nX\n## Phase: design\nY\n", "explore").strip() == "X"
    assert phase_text("## Phase: progressing\nZ\n", "analysis").strip() == "Z"


if __name__ == "__main__":
    selftest()
    if sys.argv[1:] == ["--selftest"]:
        print("selftest ok"); sys.exit(0)
    p = Path(sys.argv[1])
    state = re.search(r"^state:\s*(\S+)", (p / "README.md").read_text(), re.M).group(1)
    tasks_text = (p / "docs/rstack/tasks.md").read_text()
    mp = p / "docs/rstack/todoist-map.tsv"
    if not mp.exists():
        sys.exit("no docs/rstack/todoist-map.tsv yet: the first push to Todoist needs the user's yes (see references/admin/tasks.md)")
    map_text = mp.read_text()
    if phase_text(tasks_text, state) is None:
        sys.exit(f"no '## Phase: {state}' section in docs/rstack/tasks.md")
    mapped = {r[3] for r in parse_map(map_text) if r[0] == "task"}
    out = []
    for name in re.findall(r"^## Phase: (\S+)\s*$", tasks_text, re.M):  # current phase, plus any phase already pushed (early pilot)
        body = phase_text(tasks_text, name)
        if name == state or mapped & set(parse_tasks(body)[1]):
            out += check(body, map_text)
    print("\n".join(out) or "tasks.md and todoist-map agree")
    sys.exit(1 if out else 0)
