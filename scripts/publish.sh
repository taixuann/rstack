#!/usr/bin/env bash
# Publish rstack: check, mirror into a clone of the GitHub repo, commit.
# Usage: scripts/publish.sh [-m "message"] [--push]
# Env: RSTACK_MIRROR (default ~/academic-space/rstack-github)
# Without --push nothing leaves the machine. With --push it also pushes and updates the installed plugin.
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)"
MIRROR="${RSTACK_MIRROR:-$HOME/academic-space/rstack-github}"
MSG="" PUSH=0
while [ $# -gt 0 ]; do
  case "$1" in
    -m) MSG="$2"; shift 2 ;;
    --push) PUSH=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
[ -d "$MIRROR/.git" ] || { echo "no git clone at $MIRROR (set RSTACK_MIRROR)" >&2; exit 1; }
python3 "$SRC/scripts/check_plugin.py"
claude plugin validate "$SRC" | tail -1
VERSION="$(python3 -c "import json,sys; print(json.load(open('$SRC/.claude-plugin/plugin.json'))['version'])")"
rsync -a --delete --exclude .git --exclude .DS_Store "$SRC/" "$MIRROR/"
cd "$MIRROR"
git add -A
if git diff --cached --quiet; then echo "mirror already up to date at $VERSION"; else
  git commit -q -m "rstack $VERSION${MSG:+: $MSG}"
  echo "committed rstack $VERSION in $MIRROR"
fi
if [ "$PUSH" = 1 ]; then
  git push origin main
  claude plugin marketplace update rstack | tail -1
  claude plugin update rstack@rstack | tail -1
else
  echo "not pushed. Re-run with --push to push and update the installed plugin."
fi
