#!/usr/bin/env bash
# Install or update rstack on every host found: Claude Code, Codex, Antigravity.
# Usage: scripts/install.sh [claude|codex|antigravity|all]   (default all). Safe to re-run.
set -uo pipefail
REPO="taixuann/rstack"
HOSTS="${1:-all}"
want() { [ "$HOSTS" = all ] || [ "$HOSTS" = "$1" ]; }

if want claude && command -v claude >/dev/null; then
  echo "==> Claude Code"
  claude plugin marketplace add "$REPO" 2>&1 | tail -1
  claude plugin marketplace update rstack | tail -1
  claude plugin install rstack@rstack 2>&1 | tail -1 || true
  claude plugin update rstack@rstack | tail -1
fi

if want codex && command -v codex >/dev/null; then
  echo "==> Codex"
  codex plugin marketplace add "$REPO" 2>&1 | tail -1
  codex plugin marketplace upgrade 2>&1 | tail -1
  codex plugin add rstack@rstack 2>&1 | tail -1
fi

if want antigravity && [ -d "$HOME/.gemini/config/plugins" ]; then
  echo "==> Antigravity"
  D="$HOME/.gemini/config/plugins/rstack"
  if [ -d "$D/.git" ]; then git -C "$D" fetch -q origin main && git -C "$D" reset -q --hard origin/main
  else git clone -q "https://github.com/$REPO.git" "$D"; fi
  cp "$D/.claude-plugin/plugin.json" "$D/plugin.json"
  echo "rstack at $(git -C "$D" rev-parse --short HEAD)"
fi
