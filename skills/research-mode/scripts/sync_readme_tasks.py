#!/usr/bin/env python3
"""Mirror the current state's tasks.md into the README task block.

Usage: sync_readme_tasks.py PROJECT_DIR   |   sync_readme_tasks.py --selftest
Reads `state:` from PROJECT_DIR/README.md front matter and checkbox lines from
PROJECT_DIR/docs/rstack/<state>/tasks.md, then rewrites the text between
<!-- tasks:start --> and <!-- tasks:end --> in the README. tasks.md stays the source of truth.
"""
import re, sys
from pathlib import Path

START, END, SHOW = "<!-- tasks:start -->", "<!-- tasks:end -->", 5


def block(state, tasks_text):
    items = re.findall(r"^\s*- \[([ xX])\] (.+)$", tasks_text, re.M)
    done = sum(1 for m, _ in items if m != " ")
    openq = [t for m, t in items if m == " "][:SHOW]
    lines = [START, f"**Tasks ({state}): {done}/{len(items)} done.** Full list: [docs/rstack/{state}/tasks.md](docs/rstack/{state}/tasks.md)", ""]
    lines += [f"- [ ] {t}" for t in openq] or ["All tasks done. Review the exit check."]
    lines.append(END)
    return "\n".join(lines)


def sync(project):
    readme = Path(project) / "README.md"
    text = readme.read_text()
    state = re.search(r"^state:\s*(\S+)", text, re.M).group(1)
    tasks = Path(project) / "docs/rstack" / state / "tasks.md"
    if not tasks.exists():
        sys.exit(f"missing {tasks}")
    if START not in text or END not in text:
        sys.exit("README has no task markers")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block(state, tasks.read_text()), text, flags=re.S)
    readme.write_text(new)
    print(f"synced {readme} from {tasks}")


def selftest():
    b = block("explore", "- [x] a\n- [ ] b\n- [ ] c\n")
    assert "1/3 done" in b and "- [ ] b" in b and "- [ ] a" not in b and b.startswith(START) and b.endswith(END)
    assert "All tasks done" in block("design", "- [x] a\n")
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    elif len(sys.argv) == 2:
        sync(sys.argv[1])
    else:
        sys.exit(__doc__)
