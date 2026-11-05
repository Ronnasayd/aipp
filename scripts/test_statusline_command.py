"""Tests for the disabled MCP and next-task lines of statusline-command.sh."""

import json
import os
from pathlib import Path
import subprocess
import uuid

SCRIPT = Path(__file__).parent / "statusline-command.sh"
LABEL = "mcp/disabled"


def run_statusline(
    tmp_path: Path,
    projects: dict,
    tasks: dict | None = None,
    extra: dict | None = None,
) -> str:
    """Run the script against a fake config dir.

    Args:
        tmp_path: Directory that holds the fake config and serves as cwd.
        projects: Value of the `projects` key in the fake .claude.json.
        tasks: Content of the fake .taskmaster/tasks/tasks.json, if any.
        extra: Keys merged into the JSON payload sent to the script.

    Returns:
        The stdout of the script.
    """
    config_dir = tmp_path / "config"
    (config_dir / "logs").mkdir(parents=True)
    (config_dir / ".claude.json").write_text(json.dumps({"projects": projects}))
    if tasks is not None:
        tasks_file = tmp_path / ".taskmaster" / "tasks" / "tasks.json"
        tasks_file.parent.mkdir(parents=True)
        tasks_file.write_text(json.dumps(tasks))
    payload = {
        "workspace": {"current_dir": "/proj/a", "project_dir": "/proj/a"},
        **(extra or {}),
    }
    result = subprocess.run(
        ["bash", str(SCRIPT)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env={
            **os.environ,
            "CLAUDE_CONFIG_DIR": str(config_dir),
            "CLAUDE_PROJECT_DIR": str(tmp_path),
        },
        check=True,
    )
    return result.stdout


def test_shows_only_total_for_current_project(tmp_path):
    projects = {"/proj/a": {"disabledMcpServers": ["aipp:sqlite", "claude.ai Gmail"]}}
    output = run_statusline(tmp_path, projects)
    assert f"{LABEL}(2)" in output
    assert "aipp:sqlite" not in output


def test_ignores_other_projects(tmp_path):
    projects = {
        "/proj/a": {"disabledMcpServers": ["aipp:sqlite"]},
        "/proj/b": {"disabledMcpServers": ["aipp:github", "aipp:notion"]},
    }
    assert f"{LABEL}(1)" in run_statusline(tmp_path, projects)


def test_omits_line_when_nothing_disabled(tmp_path):
    projects = {"/proj/a": {"disabledMcpServers": []}, "/proj/b": {}}
    assert LABEL not in run_statusline(tmp_path, projects)


def test_omits_line_when_project_is_unknown(tmp_path):
    assert LABEL not in run_statusline(tmp_path, {})


def test_next_task_line_shows_total_tasks_of_each_tag(tmp_path):
    tasks = {
        "feat-a": {
            "tasks": [
                {"id": 1, "title": "done one", "status": "done"},
                {"id": 2, "title": "next one", "status": "pending"},
                {"id": 3, "title": "later one", "status": "pending"},
            ]
        },
        "feat-b": {"tasks": [{"id": 7, "title": "only one", "status": "pending"}]},
    }
    output = run_statusline(tmp_path, {}, tasks)
    assert "feat-a(3): #2 next one" in output
    assert "feat-b(1): #7 only one" in output


def test_next_task_line_omits_tag_without_pending_tasks(tmp_path):
    tasks = {"feat-a": {"tasks": [{"id": 1, "title": "t", "status": "done"}]}}
    assert "feat-a" not in run_statusline(tmp_path, {}, tasks)


SESSION = {
    "model": {"id": "claude-opus-5-5", "display_name": "Opus 5.5"},
    "effort": {"level": "high"},
}


def run_served(tmp_path: Path, content: dict | None) -> str:
    """Run the script with a served file for a fresh session.

    Args:
        tmp_path: Directory that holds the fake config and serves as cwd.
        content: JSON written to the served file; None leaves it absent.

    Returns:
        The stdout of the script.
    """
    session_id = str(uuid.uuid4())
    # why: the script reads a fixed /tmp path, so tmp_path cannot hold this file
    path = Path(f"/tmp/claude-served-{session_id}.json")
    if content is not None:
        path.write_text(json.dumps(content), encoding="utf-8")
    try:
        extra = {**SESSION, "session_id": session_id}
        return run_statusline(tmp_path, {}, extra=extra)
    finally:
        path.unlink(missing_ok=True)


def test_served_line_shows_model_and_effort_when_effort_differs(tmp_path):
    output = run_served(tmp_path, {"model": "claude-opus-5-5", "effort": "low"})
    assert "claude-opus-5-5" in output
    assert "▰▱▱▱▱ low" in output


def test_served_line_shows_model_and_effort_when_model_differs(tmp_path):
    output = run_served(tmp_path, {"model": "haiku", "effort": "high"})
    assert "haiku" in output
    assert output.count("▰▰▰▱▱ high") == 2


def test_served_line_shows_model_alone_when_file_has_no_effort(tmp_path):
    output = run_served(tmp_path, {"model": "haiku"})
    assert "haiku" in output
    assert output.count("▰▰▰▱▱ high") == 1


def test_served_line_omitted_when_both_match_session(tmp_path):
    output = run_served(tmp_path, {"model": "claude-opus-5-5", "effort": "high"})
    assert "claude-opus-5-5" not in output
    assert output.count("▰▰▰▱▱ high") == 1


def test_served_line_omitted_after_turn_without_effort(tmp_path):
    assert "claude-opus-5-5" not in run_served(tmp_path, {"model": "claude-opus-5-5"})


def test_served_line_omitted_without_file(tmp_path):
    assert "claude-opus-5-5" not in run_served(tmp_path, None)
