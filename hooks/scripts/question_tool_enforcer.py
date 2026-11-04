#!/usr/bin/python3
"""Stop / SubagentStop hook.

If the last assistant message contains '?' and a typed decision confirms it
asks the user something, remind the agent to use an interactive question tool.
When the decision is unavailable, the '?' alone triggers the reminder.
"""

import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    decide_yes,
    emit_additional_context,
    get_by_key,
    get_hooks_logger,
    minify_markdown,
)

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

LOG = get_hooks_logger("QuestionToolEnforcer")

QUESTION_ID = "asks_user"
QUESTION_STATEMENT = (
    "The assistant message asks the user a question that requires the user's "
    "answer or decision."
)
# why: questions to the user close a message; the tail bounds latency and cost.
MAX_STATE_CHARS = 8000


def build_rule() -> str:
    """Build the interactive-question-tool reminder, honoring QUESTION_TOOL_LANG.

    Returns:
        str: the markdown rule text to inject as additional context.
    """
    lang = os.environ.get("QUESTION_TOOL_LANG", "").strip()
    lang_line = (
        f"MANDATORY: Ask questions in {lang}.\n"
        if lang
        else "Use the same language used by the user.\n"
    )
    with open(
        os.path.join(script_dir, "..", "markdown/INTERATIVE-QUESTION.md"),
        encoding="utf-8",
    ) as f:
        guides = f.read()
    return f"{guides}\n{lang_line}"


RULE = build_rule()


def last_assistant_from_transcript(path: str | None) -> str | None:
    """Reconstruct the last assistant turn's text from the JSONL transcript.

    Used when the payload's ``last_assistant_message`` is missing or truncated
    (Claude Code drops/clips that field for very large messages).

    Args:
        path: path to the JSONL transcript file, or None.

    Returns:
        str | None: the joined assistant text, or None if unavailable.
    """
    if not path:
        return None
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError as e:
        LOG.debug("Failed to read transcript %s: %s", path, e)
        return None

    collected = []
    for line in reversed(lines):
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        etype = entry.get("type")
        if etype == "assistant":
            content = entry.get("message", {}).get("content", [])
            texts = [b.get("text", "") for b in content if b.get("type") == "text"]
            joined = "\n".join(t for t in texts if t)
            if joined:
                collected.append(joined)
        elif etype in ("user", "system") and collected:
            break  # reached the start of the last assistant turn

    if not collected:
        return None
    return "\n".join(reversed(collected))


def asks_user(message: str) -> bool:
    """Decide whether a message containing '?' really asks the user something.

    Args:
        message: the assistant message.

    Returns:
        bool: the decision, or True when no decision is available, so a backend
            failure degrades to the plain '?' check instead of losing the rule.
    """
    return decide_yes(message[-MAX_STATE_CHARS:], QUESTION_ID, QUESTION_STATEMENT)


def main() -> None:
    """Read the hook payload from stdin and emit the reminder if warranted."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        LOG.debug("Failed to parse JSON: %s", e)
        sys.exit(0)

    if get_by_key(payload, "stop_hook_active"):
        LOG.debug("Skipping: stop_hook_active set")
        sys.exit(0)

    event = get_by_key(payload, "hook_event_name") or "Stop"

    last_message = get_by_key(payload, "last_assistant_message")
    if not last_message:
        # Field dropped/clipped for very large messages: reconstruct from transcript.
        last_message = last_assistant_from_transcript(
            get_by_key(payload, "transcript_path")
        )
    if not last_message:
        LOG.debug("Skipping: no assistant message found")
        sys.exit(0)
    if "?" not in last_message:
        LOG.debug("Skipping: no '?' in message")
        sys.exit(0)
    if not asks_user(last_message):
        LOG.debug("Skipping: message does not ask the user")
        sys.exit(0)

    emit_additional_context(event, minify_markdown(RULE), LOG)
    sys.exit(0)


if __name__ == "__main__":
    main()
