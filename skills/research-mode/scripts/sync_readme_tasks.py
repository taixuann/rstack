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


def phase(state, tasks_text):
    m = re.search(rf"^## Phase: {re.escape(state)}\s*$(.*?)(?=^## Phase:|\Z)", tasks_text, re.M | re.S)
    return m.group(1) if m else ""


def block(state, tasks_text):
    tasks_text = phase(state, tasks_text)
    items = re.findall(r"^\s*- \[([ xX])\] (.+)$", tasks_text, re.M)
    done = sum(1 for m, _ in items if m != " ")
    openq = [t for m, t in items if m == " "][:SHOW]
    lines = [START, f"**Tasks ({state}): {done}/{len(items)} done.** Full list: [docs/rstack/tasks.md](docs/rstack/tasks.md)", ""]
    lines += [f"- [ ] {t}" for t in openq] or ["All tasks done. Review the exit check."]
    lines.append(END)
    return "\n".join(lines)


def sync(project):
    readme = Path(project) / "README.md"
    text = readme.read_text()
    state = re.search(r"^state:\s*(\S+)", text, re.M).group(1)
    tasks = Path(project) / "docs/rstack/tasks.md"
    if not tasks.exists():
        sys.exit(f"missing {tasks}")
    if START not in text or END not in text:
        sys.exit("README has no task markers")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block(state, tasks.read_text()), text, flags=re.S)
    readme.write_text(new)
    print(f"synced {readme} from {tasks}")


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
