"""Regression suite for the subagent guidelines PreToolUse hook."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from typing import TYPE_CHECKING
import uuid

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

if TYPE_CHECKING:
    from collections.abc import Iterator

HOOK = Path(__file__).parent / "subagent_guidelines.py"


def marker_for(session: str) -> Path:
    """Locate the once-per-session marker the hook writes.

    Args:
        session: session id sent to the hook.

    Returns:
        Path: the marker file path.
    """
    return Path(f"/tmp/subagent_guidelines_{session[:8]}")


@pytest.fixture(name="session")
def session_fixture() -> Iterator[str]:
    """Provide a unique session id and remove its marker afterwards.

    Yields:
        str: the session id.
    """
    session = uuid.uuid4().hex
    yield session
    marker_for(session).unlink(missing_ok=True)


def write_markdown(root: Path) -> None:
    """Create the two markdown files the hook injects.

    Args:
        root: project root for the hook.
    """
    markdown = root / ".claude/hooks/markdown"
    markdown.mkdir(parents=True)
    (markdown / "SUBAGENT-GUIDELINES.md").write_text("guideline body\n")
    (markdown / "SUBAGENT-RESPONSE-TEMPLATE.md").write_text("template body\n")


def run_hook(
    root: Path, session: str, tool_name: str = "Agent", event: str = "PreToolUse"
) -> subprocess.CompletedProcess[str]:
    """Run the hook with a PreToolUse payload.

    Args:
        root: project root for the hook.
        session: session id sent to the hook.
        tool_name: tool the payload reports.
        event: hook event the payload reports.

    Returns:
        subprocess.CompletedProcess[str]: the finished hook process.
    """
    payload = {
        "hook_event_name": event,
        "tool_name": tool_name,
        "session_id": session,
        "cwd": str(root),
    }
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(root)},
    )


def read_context(stdout: str, event: str) -> str:
    """Extract the injected context, checking the event it was emitted for.

    Args:
        stdout: the hook's stdout.
        event: event name the output must declare.

    Returns:
        str: the additionalContext string.
    """
    output = json.loads(stdout)["hookSpecificOutput"]
    assert output["hookEventName"] == event
    return str(output["additionalContext"])


def test_first_agent_call_injects_only_guidelines(tmp_path: Path, session: str) -> None:
    """The caller gets the launch guidelines, not the subagent's template.

    Args:
        tmp_path: isolated project root.
        session: unique session id.
    """
    write_markdown(tmp_path)

    context = read_context(run_hook(tmp_path, session).stdout, "PreToolUse")

    assert "guideline body" in context
    assert "template body" not in context


def test_subagent_start_injects_only_template(tmp_path: Path, session: str) -> None:
    """The subagent gets the response template, not the launch guidelines.

    Args:
        tmp_path: isolated project root.
        session: unique session id.
    """
    write_markdown(tmp_path)

    result = run_hook(tmp_path, session, event="SubagentStart")
    context = read_context(result.stdout, "SubagentStart")

    assert "template body" in context
    assert "guideline body" not in context


def test_every_subagent_gets_the_template(tmp_path: Path, session: str) -> None:
    """Each subagent has its own context, so no once-per-session marker applies.

    Args:
        tmp_path: isolated project root.
        session: unique session id.
    """
    write_markdown(tmp_path)
    run_hook(tmp_path, session, event="SubagentStart")

    result = run_hook(tmp_path, session, event="SubagentStart")

    assert "template body" in result.stdout
    assert not marker_for(session).exists()


def test_subagent_start_survives_missing_markdown(tmp_path: Path, session: str) -> None:
    """A partial install must not crash the subagent launch.

    Args:
        tmp_path: project root without the markdown files.
        session: unique session id.
    """
    result = run_hook(tmp_path, session, event="SubagentStart")

    assert result.returncode == 0
    assert result.stdout == ""
    assert "Traceback" not in result.stderr


def test_second_agent_call_stays_silent(tmp_path: Path, session: str) -> None:
    """Guidelines are injected once per session.

    Args:
        tmp_path: isolated project root.
        session: unique session id.
    """
    write_markdown(tmp_path)
    run_hook(tmp_path, session)

    assert run_hook(tmp_path, session).stdout == ""


def test_other_tools_skip_the_markdown_files(tmp_path: Path, session: str) -> None:
    """The hook fires on every tool, so others must not depend on the files.

    Args:
        tmp_path: project root without the markdown files.
        session: unique session id.
    """
    result = run_hook(tmp_path, session, tool_name="Bash")

    assert result.returncode == 0
    assert result.stderr == ""


def test_missing_markdown_exits_clean(tmp_path: Path, session: str) -> None:
    """A partial install must not crash the agent call.

    Args:
        tmp_path: project root without the markdown files.
        session: unique session id.
    """
    result = run_hook(tmp_path, session)

    assert result.returncode == 0
    assert result.stdout == ""
    assert "Traceback" not in result.stderr


def test_failed_read_keeps_the_session_retryable(tmp_path: Path, session: str) -> None:
    """A failed read must not consume the once-per-session injection.

    Args:
        tmp_path: project root, markdown files added after the first call.
        session: unique session id.
    """
    run_hook(tmp_path, session)
    write_markdown(tmp_path)

    assert "guideline body" in run_hook(tmp_path, session).stdout
