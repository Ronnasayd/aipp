"""Regression suite for the SubagentStop response format gate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

GATE = Path(__file__).parent / "subagent_response_format_gate.py"


def run_gate(root: Path, message: str) -> str:
    """Run the hook with a subagent payload.

    Args:
        root: project root for the hook, also holds its loop counters.
        message: the subagent's final message.

    Returns:
        str: the hook's stdout.
    """
    payload = {
        "agent_type": "general-purpose",
        "agent_id": "test-agent",
        "cwd": str(root),
        "last_assistant_message": message,
    }
    result = subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(root)},
    )
    return result.stdout


def test_block_reason_keeps_previous_output(tmp_path: Path) -> None:
    """A rewrite must not drop the deliverable a forked skill already wrote.

    Args:
        tmp_path: isolated project root.
    """
    output = json.loads(run_gate(tmp_path, "```\nfix: something\n```"))

    assert output["decision"] == "block"
    assert "verbatim" in output["reason"]


def test_block_reason_template_path_is_readable(tmp_path: Path) -> None:
    """The template path stays a separate token in the block reason.

    Args:
        tmp_path: isolated project root.
    """
    output = json.loads(run_gate(tmp_path, "no fields here"))

    template = f"{tmp_path}/.claude/hooks/markdown/SUBAGENT-RESPONSE-TEMPLATE.md"
    assert f" {template}" in output["reason"]


def test_report_with_status_passes(tmp_path: Path) -> None:
    """A report carrying status is not blocked.

    Args:
        tmp_path: isolated project root.
    """
    assert run_gate(tmp_path, "status: success\nsummary: done") == ""
