---
description: Toggle readonly mode (blocks Write/Edit/MultiEdit/NotebookEdit)
allowed-tools: Bash(f=*)
---

!`f="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}/.claude/readonly"; if [ -f "$f" ]; then rm "$f" && echo "readonly OFF"; else touch "$f" && echo "readonly ON"; fi`

Only confirm the state above to the user. Do nothing else.
