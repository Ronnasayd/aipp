#!/usr/bin/env bash
# Cron job: for each saved Claude account in SECRETS_JSON, hit the oauth usage
# endpoint directly to keep the session clock alive. Execute every 30 minutes.
# SCRIPT="$AI_PROJECT_ROOT_DIR/scripts/claude.warmup.sh"
# CRON_LINE="*/30 * * * * $SCRIPT >> /tmp/warmup.log 2>&1"
# ( crontab -l 2>/dev/null | grep -vF "$SCRIPT" ; echo "$CRON_LINE" ) | crontab -
set -euo pipefail

# why: per-file accounts dir under ~/.claude/accounts caused race conditions
# with other processes writing the same files; SECRETS_JSON is a single file
# owned only by this account-rotation workflow.
SECRETS_JSON="${CLAUDE_SECRETS_JSON:-$HOME/.secrets/claude.json}"
LOCK_FILE="${TMPDIR:-/tmp}/claude.warmup.lock"
# why: fixed public client_id for the official Claude Code CLI OAuth app.
CLIENT_ID="9d1c250a-e61b-44d9-88ed-5944d1962f5e"
TOKEN_URL="https://platform.claude.com/v1/oauth/token"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }

command -v jq >/dev/null 2>&1 || { log "error: jq required"; exit 1; }
command -v curl >/dev/null 2>&1 || { log "error: curl required"; exit 1; }
command -v flock >/dev/null 2>&1 || { log "error: flock required"; exit 1; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "error: another warmup run is already in progress, skipping"; exit 0; }

[ -f "$SECRETS_JSON" ] || { log "error: $SECRETS_JSON not found"; exit 1; }

# do_refresh_token <email> <refresh_token> -> prints new access_token, or empty on failure.
# Updates SECRETS_JSON in place on success.
do_refresh_token() {
    local email="$1" old_refresh_token="$2"
    local response access_token new_refresh_token expires_in expires_at tmp

    response="$(curl -sS -X POST \
        -H 'Accept: application/json, text/plain, */*' \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: claude-cli/2.1.300 (external, cli)' \
        --data-binary "$(jq -nc --arg rt "$old_refresh_token" --arg cid "$CLIENT_ID" \
            '{grant_type:"refresh_token",refresh_token:$rt,client_id:$cid,scope:"user:profile user:inference user:sessions:claude_code user:mcp_servers user:file_upload user:plugins"}')" \
        "$TOKEN_URL")"

    access_token="$(jq -r '.access_token // empty' <<<"$response")"
    if [ -z "$access_token" ]; then
        log "$email: refresh failed: $response"
        return 1
    fi

    new_refresh_token="$(jq -r '.refresh_token // empty' <<<"$response")"
    [ -n "$new_refresh_token" ] || new_refresh_token="$old_refresh_token"
    expires_in="$(jq -r '.expires_in // 0' <<<"$response")"
    expires_at="$(( $(date +%s%3N) + expires_in * 1000 ))"

    tmp="$(mktemp)"
    jq --arg email "$email" --arg at "$access_token" --arg rt "$new_refresh_token" --argjson exp "$expires_at" \
        '(.tokens[] | select(has($email))[$email]) |= (.accessToken = $at | .refreshToken = $rt | .expiresAt = $exp)' \
        "$SECRETS_JSON" >"$tmp"
    mv "$tmp" "$SECRETS_JSON"
    chmod 600 "$SECRETS_JSON"

    log "$email: refreshed, expires_at=$expires_at"
    printf '%s' "$access_token"
}

# warmup_request <token> -> prints HTTP status code.
warmup_request() {
    local token="$1"
    local session_id prompt_id request_id
    session_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
    prompt_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
    request_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
    curl -sS -o /dev/null -w '%{http_code}' -X POST 'https://api.anthropic.com/v1/messages?beta=true' \
        -H 'Accept: application/json' \
        -H "Authorization: Bearer $token" \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: claude-cli/2.1.300 (external, sdk-cli)' \
        -H 'Anthropic-Beta: oauth-2025-04-20,claude-code-20250219' \
        -H 'Anthropic-Version: 2023-06-01' \
        -H 'Anthropic-Dangerous-Direct-Browser-Access: true' \
        -H 'X-App: cli' \
        -H "X-Claude-Code-Session-Id: $session_id" \
        -H "X-Claude-Code-Prompt-Id: $prompt_id" \
        -H 'X-Claude-Code-Request-Class: main' \
        -H "X-Client-Request-Id: $request_id" \
        --data-binary '{
            "model": "claude-haiku-4-5",
            "messages": [{"role": "user", "content": [{"type": "text", "text": "hi"}]}],
            "system": [{"type": "text", "text": "You are Claude Code, Anthropic'"'"'s official CLI for Claude."}],
            "max_tokens": 16,
            "thinking": {"type": "disabled"},
            "stream": false
        }'
}

while IFS=$'\t' read -r email token refresh; do
    [ -n "$email" ] || continue
    [ -n "$token" ] || { log "$email: no accessToken, skipping"; continue; }

    log "$email: checking /usage"
    usage="$(curl -sS -w '\n%{http_code}' \
        -H 'Accept: application/json, text/plain, */*' \
        -H "Authorization: Bearer $token" \
        -H 'Anthropic-Beta: oauth-2025-04-20' \
        -H 'User-Agent: claude-cli/2.1.300 (external, cli)' \
        'https://api.anthropic.com/api/oauth/usage')"
    http_code="$(tail -n1 <<<"$usage")"
    usage_body="$(sed '$d' <<<"$usage")"

    if [ "$http_code" = "401" ]; then
        log "$email: 401 on /usage, refreshing token"
        [ -n "$refresh" ] || { log "$email: no refreshToken, cannot recover from 401, skipping"; continue; }
        new_token="$(do_refresh_token "$email" "$refresh")" || continue
        [ -n "$new_token" ] || continue
        token="$new_token"
        usage_body="$(curl -sS \
            -H 'Accept: application/json, text/plain, */*' \
            -H "Authorization: Bearer $token" \
            -H 'Anthropic-Beta: oauth-2025-04-20' \
            -H 'User-Agent: claude-cli/2.1.300 (external, cli)' \
            'https://api.anthropic.com/api/oauth/usage')"
    fi

    utilization="$(jq -r '.five_hour.utilization // 0' <<<"$usage_body")"
    resets_at="$(jq -r '.five_hour.resets_at // empty' <<<"$usage_body")"
    log "$email: five_hour.utilization=$utilization resets_at=${resets_at:-none}"

    # why: resets_at is null only while the 5h window is cold; utilization is not a
    # usable signal because a tiny warmup message leaves it at 0.0 in a live window.
    # /usage itself doesn't count as usage, so fire a real tiny message to warm it.
    # The request must look like real Claude Code CLI traffic (claude-code-20250219
    # beta flag + x-claude-code-session-id header) or the server books it under the
    # 7-day API usage bucket instead of activating the 5h session window.
    if [ -z "$resets_at" ]; then
        log "$email: 5h window cold, warming with a message"
        code="$(warmup_request "$token")"
        if [ "$code" = "401" ] && [ -n "$refresh" ]; then
            log "$email: 401 on warmup message, refreshing token"
            new_token="$(do_refresh_token "$email" "$refresh")" || { log "$email: warmup message HTTP $code"; continue; }
            [ -n "$new_token" ] || { log "$email: warmup message HTTP $code"; continue; }
            code="$(warmup_request "$new_token")"
        fi
        log "$email: warmup message HTTP $code"
    fi
done < <(jq -r '.tokens[] | to_entries[0] | [.key, .value.accessToken, .value.refreshToken] | @tsv' "$SECRETS_JSON")
