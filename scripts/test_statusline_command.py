"""Tests for the disabled MCP and next-task lines of statusline-command.sh."""

import json
import os
from pathlib import Path
import subprocess

SCRIPT = Path(__file__).parent / "statusline-command.sh"
LABEL = "mcp/disabled"


def run_statusline(tmp_path: Path, projects: dict, tasks: dict | None = None) -> str:
    """Run the script against a fake config dir.

    Args:
        tmp_path: Directory that holds the fake config and serves as cwd.
        projects: Value of the `projects` key in the fake .claude.json.
        tasks: Content of the fake .taskmaster/tasks/tasks.json, if any.

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
    payload = {"workspace": {"current_dir": "/proj/a", "project_dir": "/proj/a"}}
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
