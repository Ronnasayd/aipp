"""Tests for the disabled MCP servers line of statusline-command.sh."""

import json
import os
from pathlib import Path
import subprocess

SCRIPT = Path(__file__).parent / "statusline-command.sh"
LABEL = "disabled MCP"


def run_statusline(tmp_path: Path, projects: dict) -> str:
    """Run the script against a fake config dir.

    Args:
        tmp_path: Directory that holds the fake config and serves as cwd.
        projects: Value of the `projects` key in the fake .claude.json.

    Returns:
        The stdout of the script.
    """
    config_dir = tmp_path / "config"
    (config_dir / "logs").mkdir(parents=True)
    (config_dir / ".claude.json").write_text(json.dumps({"projects": projects}))
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
    assert f"{LABEL} 2" in output
    assert "aipp:sqlite" not in output


def test_ignores_other_projects(tmp_path):
    projects = {
        "/proj/a": {"disabledMcpServers": ["aipp:sqlite"]},
        "/proj/b": {"disabledMcpServers": ["aipp:github", "aipp:notion"]},
    }
    assert f"{LABEL} 1" in run_statusline(tmp_path, projects)


def test_omits_line_when_nothing_disabled(tmp_path):
    projects = {"/proj/a": {"disabledMcpServers": []}, "/proj/b": {}}
    assert LABEL not in run_statusline(tmp_path, projects)


def test_omits_line_when_project_is_unknown(tmp_path):
    assert LABEL not in run_statusline(tmp_path, {})
