"""Tests for the settings.local.json env block written by scripts/claude.install.sh."""

import json
from pathlib import Path
import subprocess

INSTALLER = Path(__file__).parent / "claude.install.sh"


def _settings_jq_line():
    # why: only the env jq line runs; the full installer needs a real ~/.claude
    lines = [
        ln
        for ln in INSTALLER.read_text(encoding="utf-8").splitlines()
        if ln.startswith('jq --arg dir "$LOCAL"')
    ]
    assert len(lines) == 1
    return lines[0]


def _run(tmp_path, initial):
    local = tmp_path / "proj"
    (local / ".claude").mkdir(parents=True)
    settings = local / ".claude" / "settings.local.json"
    settings.write_text(json.dumps(initial), encoding="utf-8")
    result = subprocess.run(
        ["bash", "-c", _settings_jq_line()],
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "LOCAL": str(local),
            "SOURCE": str(tmp_path / "aipp"),
            "LOCAL_SETTINGS": str(settings),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(settings.read_text(encoding="utf-8"))["env"], local


def test_writes_ai_project_root_dir_from_source(tmp_path):
    env, _ = _run(tmp_path, {})
    assert env["AI_PROJECT_ROOT_DIR"] == str(tmp_path / "aipp")


def test_keeps_existing_env_keys(tmp_path):
    env, local = _run(tmp_path, {"env": {"PROTECT_FILES_EXTRA_ALLOWED": "/x"}})
    assert env["CLAUDE_PROJECT_DIR"] == str(local)
    assert env["PROTECT_FILES_EXTRA_ALLOWED"] == "/x"
