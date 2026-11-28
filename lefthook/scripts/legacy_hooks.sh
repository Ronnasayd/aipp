#!/usr/bin/env bash
# Keeps git hooks that existed before lefthook alive.
#   preserve <hook>...   move each non-lefthook <hook> to <hook>.old.<N> (first free N)
#   run <hook> [args]    run <hook>.old and <hook>.old.<N> in numeric order, same args and stdin
# why: `lefthook install` renames a foreign hook to <hook>.old once and errors if .old exists;
# numbered backups never collide, and `run` is wired into lefthook.yml so they still execute.
set -euo pipefail

hooks_dir="$(git rev-parse --git-path hooks)"

preserve() {
  local hook path n
  for hook in "$@"; do
    path="$hooks_dir/$hook"
    [ -f "$path" ] || continue
    grep -q "call_lefthook" "$path" && continue
    n=1
    while [ -e "$path.old.$n" ]; do n=$((n + 1)); done
    mv "$path" "$path.old.$n"
    echo "legacy hook: $path -> $path.old.$n"
  done
}

list_legacy() {
  local hook="$1"
  [ -f "$hooks_dir/$hook.old" ] && echo "$hooks_dir/$hook.old"
  # why: -V orders .old.2 before .old.10; plain sort would not
  find "$hooks_dir" -maxdepth 1 -name "$hook.old.*" -type f | grep -E "\.old\.[0-9]+$" | sort -V || true
}

run() {
  local hook="$1" stdin_file legacy
  shift
  stdin_file="$(mktemp)"
  # why: expanded now; the EXIT trap fires after the local goes out of scope
  trap "rm -f '$stdin_file'" EXIT
  # why: stdin (pre-push refs) can be read once; buffer it so every legacy hook gets a copy
  [ -t 0 ] || cat >"$stdin_file"
  while IFS= read -r legacy; do
    [ -x "$legacy" ] || continue
    "$legacy" "$@" <"$stdin_file"
  done < <(list_legacy "$hook")
}

cmd="${1:-}"
shift || true
case "$cmd" in
  preserve) preserve "$@" ;;
  run) run "$@" ;;
  *) echo "usage: $0 preserve <hook>... | run <hook> [args]" >&2; exit 2 ;;
esac
