#!/usr/bin/env bash
# Cron job: for each saved Claude account token, fire /usage via haiku to
# keep the session clock alive. Execute this script every 30 minutes.
# SCRIPT="$AI_PROJECT_ROOT_DIR/scripts/claude.warmup.sh"
# CRON_LINE="*/30 * * * * $SCRIPT >> /tmp/warmup.log 2>&1"
# ( crontab -l 2>/dev/null | grep -vF "$SCRIPT" ; echo "$CRON_LINE" ) | crontab -
set -euo pipefail

# Project root derived from this script's own location (scripts/.. ), not from
# AI_PROJECT_ROOT_DIR — cron runs a non-login shell where that env var isn't set yet.
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Cron runs a non-interactive, non-login shell, so ~/.bashrc's "not interactive -> return"
# guard skips every export in it (CLAUDE_CONFIG_DIR, PATH additions, etc). Re-exec this
# script through an interactive login shell once, but only when those exports are
# actually missing, so a manual `bash claude.warmup.sh` run doesn't pay for it twice.
if [ -z "${WARMUP_REEXECED:-}" ] && [ -z "${CLAUDE_CONFIG_DIR:-}" ]; then
    export WARMUP_REEXECED=1
    exec bash -lic "$(printf '%q ' "$0" "$@")"
fi

TOKENS_FILE="${TOKENS_FILE:-$HOME/.secrets/claude.json}"
LOCK_FILE="${TMPDIR:-/tmp}/claude.warmup.lock"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

command -v jq >/dev/null 2>&1 || { log "error: jq required"; exit 1; }
command -v claude >/dev/null 2>&1 || { log "error: claude CLI required"; exit 1; }
command -v flock >/dev/null 2>&1 || { log "error: flock required"; exit 1; }

[ -f "$TOKENS_FILE" ] || { log "error: $TOKENS_FILE not found"; exit 1; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "error: another warmup run is already in progress, skipping"; exit 0; }

jq -c '.tokens[] | to_entries[0]' "$TOKENS_FILE" | while IFS= read -r entry; do
    email="$(jq -r '.key' <<<"$entry")"
    token="$(jq -r '.value' <<<"$entry")"

    log "$email: running /usage"
    CLAUDE_CODE_OAUTH_TOKEN="$token" claude -p "/usage" --model haiku </dev/null >/dev/null
done
