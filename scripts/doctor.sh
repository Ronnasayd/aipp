#!/usr/bin/env bash
# aipp --doctor: report health of the aipp install. Exit 1 if any [fail].
# Usage: doctor.sh <aipp_source_dir>   (run from the project dir to check its .claude/)
SOURCE="${1:?usage: doctor.sh <aipp_source_dir>}"
LOCAL="$(pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MIN_NODE_MAJOR=24
FAILS=0

ok()   { echo "[ok]   $1"; }
warn() { echo "[warn] $1"; }
fail() { echo "[fail] $1"; FAILS=$((FAILS + 1)); }

check_tool() {
  local level="$1" bin="$2"
  if command -v "$bin" >/dev/null 2>&1; then ok "$bin"; return; fi
  "$level" "$bin not found in PATH"
}

echo "== tools"
for t in uv git claude jq; do check_tool fail "$t"; done
for t in serena rtk rag-rat codebase-memory-mcp bat fzf lefthook ai-memory tlc; do check_tool warn "$t"; done
node_major="$(node -v 2>/dev/null | sed 's/^v//' | cut -d. -f1)"
if [ -n "$node_major" ] && [ "$node_major" -ge "$MIN_NODE_MAJOR" ]; then
  ok "node v$node_major"
else
  warn "node >= $MIN_NODE_MAJOR required (found: ${node_major:-none})"
fi

echo "== install"
if [ "$(readlink -f "$HOME/.local/bin/aipp" 2>/dev/null)" = "$(readlink -f "$SOURCE/install.sh")" ]; then
  ok "aipp symlink"
else
  fail "aipp symlink: $HOME/.local/bin/aipp does not point to $SOURCE/install.sh"
fi
if [ -d "$SOURCE/.venv" ]; then ok "venv"; else fail "venv missing: run 'uv sync --project $SOURCE'"; fi
case ":$PATH:" in
  *":$HOME/.local/bin:"*) ok "~/.local/bin in PATH" ;;
  *) warn "~/.local/bin not in PATH" ;;
esac
if [ "$(readlink -f "${AI_PROJECT_ROOT_DIR:-/nonexistent}" 2>/dev/null)" = "$(readlink -f "$SOURCE")" ]; then
  ok "AI_PROJECT_ROOT_DIR"
else
  warn "AI_PROJECT_ROOT_DIR is '${AI_PROJECT_ROOT_DIR:-unset}', expected $SOURCE"
fi
if [ -n "$CLAUDE_CONFIG_DIR" ]; then ok "CLAUDE_CONFIG_DIR"; else warn "CLAUDE_CONFIG_DIR unset"; fi
if [ -e "$HOME/.aipp.alias.zshrc" ]; then ok "~/.aipp.alias.zshrc"; else warn "~/.aipp.alias.zshrc missing"; fi

echo "== claude plugins"
plugins_json="$CLAUDE_DIR/plugins/installed_plugins.json"
for p in rag-rat@rag-rat caveman@caveman ponytail@ponytail; do
  if jq -e --arg p "$p" '.plugins | has($p)' "$plugins_json" >/dev/null 2>&1; then
    ok "plugin $p"
  else
    warn "plugin $p not installed"
  fi
done

echo "== project ($LOCAL)"
if [ -d "$LOCAL/.claude" ]; then
  # why: -xtype is GNU-only; with -L, BSD and GNU find both report only links that do not resolve
  broken="$(find -L "$LOCAL/.claude" -type l 2>/dev/null)"
  if [ -z "$broken" ]; then ok "no broken symlinks in .claude/"; fi
  while IFS= read -r l; do [ -n "$l" ] && warn "broken symlink: $l"; done <<< "$broken"
else
  warn "no .claude/ here: run 'aipp --claude' to link this project"
fi

echo
if [ "$FAILS" -gt 0 ]; then echo "$FAILS check(s) failed"; exit 1; fi
echo "All required checks passed"
