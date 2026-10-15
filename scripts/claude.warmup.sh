#!/usr/bin/env bash
# Cron job: for each saved Claude account, hit the oauth usage endpoint
# directly to keep the session clock alive. Execute every 30 minutes.
# SCRIPT="$AI_PROJECT_ROOT_DIR/scripts/claude.warmup.sh"
# CRON_LINE="*/30 * * * * $SCRIPT >> /tmp/warmup.log 2>&1"
# ( crontab -l 2>/dev/null | grep -vF "$SCRIPT" ; echo "$CRON_LINE" ) | crontab -
set -euo pipefail

CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
ACCOUNTS_DIR="${ACCOUNTS_DIR:-$CLAUDE_CONFIG_DIR/accounts}"
LOCK_FILE="${TMPDIR:-/tmp}/claude.warmup.lock"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

command -v jq >/dev/null 2>&1 || { log "error: jq required"; exit 1; }
command -v curl >/dev/null 2>&1 || { log "error: curl required"; exit 1; }
command -v flock >/dev/null 2>&1 || { log "error: flock required"; exit 1; }

exec 9>"$LOCK_FILE"
flock -n 9 || { log "error: another warmup run is already in progress, skipping"; exit 0; }

# shellcheck source=claude.accounts.sh
source "$(dirname "${BASH_SOURCE[0]}")/claude.accounts.sh"
save_current_account

[ -d "$ACCOUNTS_DIR" ] || { log "error: $ACCOUNTS_DIR not found"; exit 1; }

for account_file in "$ACCOUNTS_DIR"/*.json; do
    [ -f "$account_file" ] || continue
    email="$(basename "$account_file" .json)"
    token="$(jq -r '.claudeAiOauth.accessToken // empty' "$account_file")"
    [ -n "$token" ] || { log "$email: no accessToken, skipping"; continue; }

    log "$email: checking /usage"
    usage="$(curl -sS \
        -H 'Accept: application/json, text/plain, */*' \
        -H "Authorization: Bearer $token" \
        -H 'Anthropic-Beta: oauth-2025-04-20' \
        -H 'User-Agent: claude-cli/2.1.300 (external, cli)' \
        'https://api.anthropic.com/api/oauth/usage')"
    utilization="$(jq -r '.five_hour.utilization // 0' <<<"$usage")"
    log "$email: five_hour.utilization=$utilization"

    # utilization 0 means the 5h session window is cold (no requests yet);
    # /usage itself doesn't count as usage, so fire a real tiny message to warm it.
    # The request must look like real Claude Code CLI traffic (claude-code-20250219
    # beta flag + x-claude-code-session-id header) or the server books it under the
    # 7-day API usage bucket instead of activating the 5h session window.
    if jq -e --arg u "$utilization" '($u | tonumber) == 0' <<<"$utilization" >/dev/null 2>&1; then
        log "$email: utilization 0, warming with a message"
        session_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
        prompt_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
        request_id="$(uuidgen 2>/dev/null || cat /proc/sys/kernel/random/uuid)"
        code="$(curl -sS -o /dev/null -w '%{http_code}' -X POST 'https://api.anthropic.com/v1/messages?beta=true' \
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
            }')"
        log "$email: warmup message HTTP $code"
    fi
done
