#!/usr/bin/env python3
"""Mirror the current phase of docs/rstack/tasks.md into the README task block.

Usage: sync_readme_tasks.py PROJECT_DIR   |   sync_readme_tasks.py --selftest
Reads `state:` from PROJECT_DIR/README.md front matter and the checkbox lines under
`## Phase: <state>` in PROJECT_DIR/docs/rstack/tasks.md (Phase > `### Goal:` > task), then rewrites
the text between <!-- tasks:start --> and <!-- tasks:end --> in the README. tasks.md stays the source of truth.
"""
import re, sys
from pathlib import Path

START, END, SHOW = "<!-- tasks:start -->", "<!-- tasks:end -->", 5


OLD = {"analysis": "progressing", "write": "ready-for-publish"}  # names used before 0.34.0


def phase(state, tasks_text):
    names = "|".join(re.escape(n) for n in (state, OLD.get(state, state)))
    m = re.search(rf"^## Phase: (?:{names})\s*$(.*?)(?=^## Phase:|\Z)", tasks_text, re.M | re.S)
    return m.group(1) if m else ""


def block(state, tasks_text, tasks_link="tasks.md"):
    tasks_text = phase(state, tasks_text)
    items = re.findall(r"^\s*- \[([ xX])\] (.+)$", tasks_text, re.M)
    done = sum(1 for m, _ in items if m != " ")
    openq = [t for m, t in items if m == " "][:SHOW]
    lines = [START, f"**Tasks ({state}): {done}/{len(items)} done.** Full list: [{tasks_link}]({tasks_link})", ""]
    lines += [f"- [ ] {t}" for t in openq] or ["All tasks done. Review the exit check."]
    lines.append(END)
    return "\n".join(lines)


def sync(project):
    p = Path(project)
    root_readme = p / "README.md"
    state = re.search(r"^state:\s*(\S+)", root_readme.read_text(), re.M).group(1)
    state = {v: k for k, v in OLD.items()}.get(state, state)
    tasks = p / "docs/rstack/tasks.md"
    if not tasks.exists():
        sys.exit(f"missing {tasks}")
    rstack_readme = p / "docs/rstack/README.md"
    if rstack_readme.exists() and START in rstack_readme.read_text() and END in rstack_readme.read_text():
        target, link = rstack_readme, "tasks.md"
    elif START in root_readme.read_text() and END in root_readme.read_text():
        target, link = root_readme, "docs/rstack/tasks.md"
    else:
        sys.exit("README has no task markers")
    text = target.read_text()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block(state, tasks.read_text(), link), text, flags=re.S)
    target.write_text(new)
    print(f"synced {target} from {tasks}")


def selftest():
    t = "## Phase: explore\n### Goal: G\n- [x] a\n- [ ] b\n- [ ] c\n## Phase: design\n### Goal: H\n- [x] z\n"
    b = block("explore", t)
    assert "1/3 done" in b and "- [ ] b" in b and "- [ ] a" not in b and "z" not in b and b.startswith(START) and b.endswith(END)
    assert "All tasks done" in block("design", t) and "0/0" in block("closed", t)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        sync(sys.argv[1])
    else:
        sys.exit(__doc__)
