#!/bin/bash

# Statusline palette, sourced by statusline-command.sh and subagent-statusline.sh.
# Catppuccin Frappe by default; when Claude uses a custom theme
# ("theme": "custom:<name>" in settings.json), each role is overridden by the
# matching key in themes/<name>.json. Built-in themes have no file to read, so
# they keep the default palette.

# Catppuccin Frappe palette (24-bit true color)
C_RED="\033[38;2;231;130;132m"
C_YELLOW="\033[38;2;229;200;144m"
C_GREEN="\033[38;2;166;209;137m"
C_TEAL="\033[38;2;129;200;190m"
C_BLUE="\033[38;2;140;170;238m"
C_MAUVE="\033[38;2;202;158;230m"
C_LAVENDER="\033[38;2;186;187;241m"
C_SUBTEXT="\033[38;2;165;173;206m"
RESET="\033[0m"

_cfg_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
# why: current Claude Code stores theme in settings.json; older ones in .claude.json
_theme=$(jq -rn '[inputs.theme // empty][0] // empty' \
    "$_cfg_dir/settings.json" "$_cfg_dir/.claude.json" 2>/dev/null)
_theme_file="$_cfg_dir/themes/${_theme#custom:}.json"

if [[ "$_theme" == custom:* ]] && [ -f "$_theme_file" ]; then
    while read -r _var _hex; do
        # why: missing key or non-#rrggbb value keeps the default colour
        [[ "$_hex" =~ ^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$ ]] || continue
        printf -v "$_var" '\\033[38;2;%d;%d;%dm' \
            "$((16#${BASH_REMATCH[1]}))" "$((16#${BASH_REMATCH[2]}))" "$((16#${BASH_REMATCH[3]}))"
    done < <(jq -r '.overrides as $o | {
        C_RED: "error", C_YELLOW: "warning", C_GREEN: "success", C_TEAL: "suggestion",
        C_BLUE: "claude", C_MAUVE: "pink_FOR_SUBAGENTS_ONLY",
        C_LAVENDER: "permission", C_SUBTEXT: "text"
    } | to_entries[] | "\(.key) \($o[.value] // "")"' "$_theme_file" 2>/dev/null)
fi
unset _cfg_dir _theme _theme_file _var _hex
