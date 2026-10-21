#!/usr/bin/env bash
# Prints the --project path for `uv run`: repo toplevel if it owns a
# pyproject.toml (e.g. this is a clone of this repo), else the fixed
# AI_PROJECT_ROOT_DIR install (hooks symlinked into an unrelated repo).
set -euo pipefail
toplevel="$(git rev-parse --show-toplevel)"
if [ -f "$toplevel/pyproject.toml" ]; then
  echo "$toplevel"
else
  echo "$AI_PROJECT_ROOT_DIR"
fi
