#!/usr/bin/env python3
"""Offline check that tasks.md and the Todoist map agree. Usage: check_map.py PROJECT_DIR | --selftest

Rules (see todoist-sync/SKILL.md): open checkboxes sit directly under a heading (no nesting),
every open item has a map row under its heading's row with the same text, and no map row
points at a done or missing item. Exit 1 and name each problem.
"""
import re, sys
from pathlib import Path


def parse_tasks(text):
    """Return (errors, {heading: [open item text]}, done set)."""
    errs, heads, done, cur = [], {}, set(), None
    for n, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^(\s*)- \[([ xX])\] (.+)$", line)
        if m:
            indent, mark, item = m.groups()
            if indent:
                errs.append(f"tasks.md:{n}: nested checkbox '{item[:40]}'; Todoist has two levels, so move it into an indented 'Detail:' line")
            elif cur is None:
                errs.append(f"tasks.md:{n}: checkbox before any heading")
            elif mark == " ":
                heads[cur].append(item.strip())
            else:
                done.add(item.strip())
        elif line.strip() and not line.startswith((" ", "#", "-", "<")):
            cur = line.strip()
            heads.setdefault(cur, [])
    return errs, heads, done


def parse_map(text):
    rows = [l.split("\t") for l in text.splitlines() if l and not l.startswith("#")]
    return [(r + [""] * 4)[:4] for r in rows]


def check(tasks_text, map_text):
    errs, heads, done = parse_tasks(tasks_text)
    rows = parse_map(map_text)
    tasks = [r for r in rows if r[0] == "task"]
    by_text = {r[3]: r for r in tasks}
    for head, items in heads.items():
        if not items:
            continue
        key = next((t for t in by_text if head == t or head.startswith(t + " (")), None)
        hrow = by_text.get(key) if key else None
        if not hrow or hrow[2]:
            errs.append(f"heading '{head}' has open items but no top-level map row")
            continue
        for item in items:
            r = by_text.get(item)
            if not r:
                errs.append(f"open item '{item[:50]}' under '{head}' has no map row (push it)")
            elif r[2] != hrow[1]:
                errs.append(f"map row for '{item[:50]}' is not under heading '{head}'")
    open_all = {i for items in heads.values() for i in items}
    for r in tasks:
        if r[2] and r[3] not in open_all:
            errs.append(f"map row '{r[3][:50]}' matches no open item (done, renamed or removed; sync it)")
    return errs


def selftest():
    t = "Intake\n- [ ] A\n- [x] B\n"
    m = "task\t1\t\tIntake\ntask\t2\t1\tA\n"
    assert check(t, m) == []
    assert check(t + "  - [ ] sub\n", m), "nested checkbox must fail"
    assert check(t.replace("A", "A2"), m), "renamed item must fail"
    assert check(t + "- [ ] C\n", m), "unmapped item must fail"
    assert check("Intake\n- [x] A\n", m), "done item with a row must fail"


if __name__ == "__main__":
    selftest()
    if sys.argv[1:] == ["--selftest"]:
        print("selftest ok"); sys.exit(0)
    p = Path(sys.argv[1])
    state = re.search(r"^state:\s*(\S+)", (p / "README.md").read_text(), re.M).group(1)
    out = check((p / "docs/rstack" / state / "tasks.md").read_text(), (p / "docs/rstack/todoist-map.tsv").read_text())
    print("\n".join(out) or "tasks.md and todoist-map agree")
    sys.exit(1 if out else 0)
