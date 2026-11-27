"""Tests for install.sh ordering on a project's first install."""

import json
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parent.parent


def _write_exec(path: Path, body: str) -> None:
    path.write_text(f"#!/usr/bin/env bash\n{body}\n", encoding="utf-8")
    path.chmod(0o755)


def _fake_source(tmp_path: Path) -> Path:
    """Copy install.sh and the real settings CLI; stub the claude backend."""
    source = tmp_path / "aipp"
    (source / "scripts").mkdir(parents=True)
    (source / "claude").mkdir()
    (source / "hooks/scripts").mkdir(parents=True)
    shutil.copy(REPO / "install.sh", source / "install.sh")
    for name in ("_git-exclude.sh", "aipp_settings.py"):
        shutil.copy(REPO / "scripts" / name, source / "scripts" / name)
    (source / "claude/aipp-default-settings.json").write_text(
        json.dumps({"skills": {}, "agents": {}, "instructions": {"x.md": True}}),
        encoding="utf-8",
    )
    # why: the real claude.install.sh reads aipp-settings.json at this point
    _write_exec(
        source / "scripts/claude.install.sh",
        'if [ -f "$CLAUDE_CONFIG_DIR/aipp-settings.json" ]; then '
        "echo SETTINGS_PRESENT; else echo SETTINGS_MISSING; fi",
    )
    return source


def _run_first_install(tmp_path: Path) -> subprocess.CompletedProcess:
    source = _fake_source(tmp_path)
    home, bindir, project = tmp_path / "home", tmp_path / "bin", tmp_path / "proj"
    for d in (home / ".local/bin", bindir, project):
        d.mkdir(parents=True)
    (home / ".local/bin/aipp").symlink_to(source / "install.sh")
    # why: strip uv's flags and run the script with this interpreter (has pyyaml)
    _write_exec(
        bindir / "uv",
        'while [ "$1" != python3 ]; do shift; done; shift; exec '
        f'"{sys.executable}" "$@"',
    )
    env = {
        "HOME": str(home),
        "PATH": f"{bindir}:/usr/bin:/bin",
        "CLAUDE_CONFIG_DIR": str(home / ".claude"),
    }
    return subprocess.run(
        ["bash", str(home / ".local/bin/aipp"), "--claude"],
        env=env,
        cwd=project,
        capture_output=True,
        text=True,
        check=False,
    )


def test_settings_exist_before_backend_install(tmp_path: Path) -> None:
    r = _run_first_install(tmp_path)
    assert "SETTINGS_PRESENT" in r.stdout, r.stdout + r.stderr


def test_settings_seeded_for_project_on_first_install(tmp_path: Path) -> None:
    _run_first_install(tmp_path)
    data = json.loads(
        (tmp_path / "home/.claude/aipp-settings.json").read_text(encoding="utf-8")
    )
    entry = data["projects"][str(tmp_path / "proj")]
    assert entry["instructions"] == {"x.md": True}
