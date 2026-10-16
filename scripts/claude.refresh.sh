#!/usr/bin/env bash
# Refresh OAuth access tokens for saved Claude accounts, directly against the
# platform.claude.com token endpoint (same flow as the official CLI refresh).
# SCRIPT="$AI_PROJECT_ROOT_DIR/scripts/claude.refresh.sh"
# CRON_LINE="0 * * * * $SCRIPT >> /tmp/claude-refresh.log 2>&1"
# ( crontab -l 2>/dev/null | grep -vF "$SCRIPT" ; echo "$CRON_LINE" ) | crontab -
set -euo pipefail

CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
ACCOUNTS_DIR="${ACCOUNTS_DIR:-$CLAUDE_CONFIG_DIR/accounts}"
LOCK_FILE="${TMPDIR:-/tmp}/claude.refresh.lock"
# why: fixed public client_id for the official Claude Code CLI OAuth app.
CLIENT_ID="9d1c250a-e61b-44d9-88ed-5944d1962f5e"
TOKEN_URL="https://platform.claude.com/v1/oauth/token"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

command -v jq >/dev/null 2>&1 || { log "error: jq required"; exit 1; }
command -v curl >/dev/null 2>&1 || { log "error: curl required"; exit 1; }
command -v flock >/dev/null 2>&1 || { log "error: flock required"; exit 1; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "error: another refresh run is already in progress, skipping"; exit 0; }

# shellcheck source=claude.accounts.sh
source "$(dirname "${BASH_SOURCE[0]}")/claude.accounts.sh"
save_current_account

[ -d "$ACCOUNTS_DIR" ] || { log "error: $ACCOUNTS_DIR not found"; exit 1; }

for account_file in "$ACCOUNTS_DIR"/*.json; do
    [ -f "$account_file" ] || continue
    email="$(basename "$account_file" .json)"
    refresh_token="$(jq -r '.claudeAiOauth.refreshToken // empty' "$account_file")"
    [ -n "$refresh_token" ] || { log "$email: no refreshToken, skipping"; continue; }

    log "$email: refreshing token"
    response="$(curl -sS -X POST \
        -H 'Accept: application/json, text/plain, */*' \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: claude-cli/2.1.300 (external, cli)' \
        --data-binary "$(jq -nc --arg rt "$refresh_token" --arg cid "$CLIENT_ID" \
            '{grant_type:"refresh_token",refresh_token:$rt,client_id:$cid,scope:"user:profile user:inference user:sessions:claude_code user:mcp_servers user:file_upload user:plugins"}')" \
        "$TOKEN_URL")"

    access_token="$(jq -r '.access_token // empty' <<<"$response")"
    if [ -z "$access_token" ]; then
        log "$email: refresh failed: $response"
        continue
    fi

    new_refresh_token="$(jq -r '.refresh_token // empty' <<<"$response")"
    [ -n "$new_refresh_token" ] || new_refresh_token="$refresh_token"
    expires_in="$(jq -r '.expires_in // 0' <<<"$response")"
    expires_at="$(( $(date +%s%3N) + expires_in * 1000 ))"

    tmp="$(mktemp)"
    jq --arg at "$access_token" --arg rt "$new_refresh_token" --argjson exp "$expires_at" \
        '.claudeAiOauth.accessToken = $at | .claudeAiOauth.refreshToken = $rt | .claudeAiOauth.expiresAt = $exp' \
        "$account_file" >"$tmp"
    mv "$tmp" "$account_file"
    chmod 600 "$account_file"

    log "$email: refreshed, expires_at=$expires_at"
done
