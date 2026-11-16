"""Tests for scripts/doctor.sh (aipp --doctor)."""

import json
from pathlib import Path
import shutil
import subprocess

DOCTOR = Path(__file__).parent / "doctor.sh"
TOOLS = [
    "uv",
    "git",
    "claude",
    "jq",
    "serena",
    "rtk",
    "rag-rat",
    "codebase-memory-mcp",
    "bat",
    "fzf",
    "lefthook",
    "ai-memory",
    "tlc",
]


def _stub(bindir, name, body="echo 1.0"):
    f = bindir / name
    f.write_text(f"#!/bin/sh\n{body}\n", encoding="utf-8")
    f.chmod(0o755)


def _healthy(tmp_path):
    """Build a fake HOME + aipp SOURCE where every check passes."""
    home, source, bindir = tmp_path / "home", tmp_path / "aipp", tmp_path / "bin"
    for d in (
        home / ".local/bin",
        source / ".venv",
        bindir,
        home / ".claude/plugins",
        tmp_path / ".claude",
    ):
        d.mkdir(parents=True)
    (source / "install.sh").write_text("", encoding="utf-8")
    (source / ".aipp.alias.zshrc").write_text("", encoding="utf-8")
    (home / ".local/bin/aipp").symlink_to(source / "install.sh")
    (home / ".aipp.alias.zshrc").symlink_to(source / ".aipp.alias.zshrc")
    plugins = {
        k: [] for k in ("rag-rat@rag-rat", "caveman@caveman", "ponytail@ponytail")
    }
    (home / ".claude/plugins/installed_plugins.json").write_text(
        json.dumps({"plugins": plugins}), encoding="utf-8"
    )
    for t in TOOLS:
        _stub(bindir, t)
    _stub(bindir, "node", "echo v24.1.0")
    # why: jq stub must behave for real; link the system binary instead
    (bindir / "jq").unlink()
    (bindir / "jq").symlink_to(shutil.which("jq"))
    env = {
        "HOME": str(home),
        "PATH": f"{bindir}:{home}/.local/bin:/usr/bin:/bin",
        "AI_PROJECT_ROOT_DIR": str(source),
        "CLAUDE_CONFIG_DIR": str(home / ".claude"),
    }
    return source, bindir, env


def _run(source, env, cwd):
    return subprocess.run(
        ["bash", str(DOCTOR), str(source)],
        env=env,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def test_healthy_system_exits_zero(tmp_path):
    source, _, env = _healthy(tmp_path)
    r = _run(source, env, tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "[fail]" not in r.stdout
    assert "[warn]" not in r.stdout


def test_missing_required_tool_fails(tmp_path):
    source, bindir, env = _healthy(tmp_path)
    (bindir / "uv").unlink()
    r = _run(source, env, tmp_path)
    assert r.returncode == 1
    assert "[fail] uv" in r.stdout


def test_missing_optional_tool_only_warns(tmp_path):
    source, bindir, env = _healthy(tmp_path)
    (bindir / "codebase-memory-mcp").unlink()
    r = _run(source, env, tmp_path)
    assert r.returncode == 0
    assert "[warn] codebase-memory-mcp" in r.stdout


def test_old_node_warns(tmp_path):
    source, bindir, env = _healthy(tmp_path)
    _stub(bindir, "node", "echo v20.0.0")
    r = _run(source, env, tmp_path)
    assert "[warn] node" in r.stdout


def test_aipp_symlink_wrong_target_fails(tmp_path):
    source, _, env = _healthy(tmp_path)
    link = Path(env["HOME"]) / ".local/bin/aipp"
    link.unlink()
    link.symlink_to(tmp_path / "elsewhere.sh")
    r = _run(source, env, tmp_path)
    assert r.returncode == 1
    assert "[fail] aipp symlink" in r.stdout


def test_missing_venv_fails(tmp_path):
    source, _, env = _healthy(tmp_path)
    (source / ".venv").rmdir()
    r = _run(source, env, tmp_path)
    assert r.returncode == 1
    assert "[fail] venv" in r.stdout


def test_env_mismatch_and_missing_plugin_warn(tmp_path):
    source, _, env = _healthy(tmp_path)
    env["AI_PROJECT_ROOT_DIR"] = "/nope"
    (Path(env["HOME"]) / ".claude/plugins/installed_plugins.json").write_text(
        json.dumps({"plugins": {}}), encoding="utf-8"
    )
    r = _run(source, env, tmp_path)
    assert r.returncode == 0
    assert "[warn] AI_PROJECT_ROOT_DIR" in r.stdout
    assert "[warn] plugin caveman@caveman" in r.stdout


def test_broken_symlink_in_project_claude_dir_warns(tmp_path):
    source, _, env = _healthy(tmp_path)
    proj = tmp_path / "proj"
    (proj / ".claude").mkdir(parents=True)
    (proj / ".claude/skills").symlink_to(tmp_path / "gone")
    r = _run(source, env, proj)
    assert r.returncode == 0
    assert "[warn] broken symlink" in r.stdout
