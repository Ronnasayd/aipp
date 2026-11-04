#!/usr/bin/python3
"""Inject subagent instructions, each one where its reader can see it.

PreToolUse: launch guidelines go to the caller, once per session.
SubagentStart: the response template goes to every subagent.
"""

from __future__ import annotations

import contextlib
import json
import os
from pathlib import Path
import sys
from typing import TYPE_CHECKING, Any

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    get_by_key,
    get_hooks_logger,
    get_session_id_short,
    minify_markdown,
    project_dir,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

LOG = get_hooks_logger("SubagentGuidelines")


AGENT_TOOL_NAMES = {"agent", "task"}


def read_markdown(payload: Mapping[str, Any], name: str) -> str | None:
    """Read one injected markdown file.

    Args:
        payload: hook payload, used to resolve the project root.
        name: file name inside the hooks markdown directory.

    Returns:
        str | None: the file content, None when it cannot be read.
    """
    path = Path(project_dir(payload)) / ".claude/hooks/markdown" / name
    try:
        return path.read_text(encoding="utf-8")
    except OSError as e:
        LOG.debug("Failed to read %s: %s", path, e)
        return None


def emit_context(event: str, markdown: str) -> None:
    """Print the hook output that adds context for the given event.

    Args:
        event: hook event name.
        markdown: context to inject.
    """
    output = {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": minify_markdown(markdown),
        }
    }
    LOG.debug("[additionalContext]: %s", json.dumps(output, ensure_ascii=False))
    print(json.dumps(output, ensure_ascii=False))  # noqa: T201 - hook stdout protocol


def inject_template(payload: Mapping[str, Any]) -> None:
    """Give a starting subagent the response format its stop gate enforces.

    Args:
        payload: hook payload.
    """
    template = read_markdown(payload, "SUBAGENT-RESPONSE-TEMPLATE.md")
    if template is not None:
        emit_context("SubagentStart", template)


def inject_guidelines(payload: Mapping[str, Any]) -> None:
    """Give the caller the launch guidelines on its first agent call.

    Args:
        payload: hook payload.
    """
    tool_name = get_by_key(payload, "tool_name")
    if not tool_name or tool_name.lower() not in AGENT_TOOL_NAMES:
        return

    session_id = get_session_id_short(get_by_key(payload, "session_id") or "")
    marker = Path(f"/tmp/subagent_guidelines_{session_id}")  # noqa: S108
    if marker.exists():
        return

    # why: reading before the touch keeps a failed read retryable this session
    guidelines = read_markdown(payload, "SUBAGENT-GUIDELINES.md")
    if guidelines is None:
        return

    with contextlib.suppress(OSError):
        marker.touch()
    emit_context("PreToolUse", guidelines)


def main() -> None:
    """Execute the subagent guidelines hook."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        LOG.debug("Failed to parse JSON: %s", e)
        sys.exit(0)

    if get_by_key(payload, "hook_event_name") == "SubagentStart":
        inject_template(payload)
    else:
        inject_guidelines(payload)
    sys.exit(0)


if __name__ == "__main__":
    main()
