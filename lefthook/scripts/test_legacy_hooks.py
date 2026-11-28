"""Tests for lefthook/scripts/legacy_hooks.sh (keep pre-lefthook git hooks running)."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import stat
import subprocess

import pytest
import yaml

SCRIPT = Path(__file__).parent / "legacy_hooks.sh"
ROOT = Path(__file__).resolve().parents[2]
LEFTHOOK_MARKER = "#!/bin/sh\ncall_lefthook()\n{\n  lefthook run x\n}\n"


def _repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path / ".git" / "hooks"


def _hook(hooks: Path, name: str, body: str) -> Path:
    path = hooks / name
    path.write_text(body)
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _sh(tmp_path: Path, *args: str, stdin: str | None = None):
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=tmp_path,
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def test_preserve_moves_foreign_hook_to_numbered_old(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    _hook(hooks, "pre-commit", "#!/bin/sh\necho mine\n")
    assert _sh(tmp_path, "preserve", "pre-commit").returncode == 0
    assert not (hooks / "pre-commit").exists()
    assert (hooks / "pre-commit.old.1").read_text() == "#!/bin/sh\necho mine\n"


def test_preserve_picks_next_free_number(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    _hook(hooks, "pre-commit.old", "a")
    _hook(hooks, "pre-commit.old.1", "b")
    _hook(hooks, "pre-commit.old.2", "c")
    _hook(hooks, "pre-commit", "new")
    assert _sh(tmp_path, "preserve", "pre-commit").returncode == 0
    assert (hooks / "pre-commit.old.3").read_text() == "new"
    assert (hooks / "pre-commit.old.1").read_text() == "b"


def test_preserve_keeps_lefthook_generated_hook(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    _hook(hooks, "pre-commit", LEFTHOOK_MARKER)
    assert _sh(tmp_path, "preserve", "pre-commit").returncode == 0
    assert (hooks / "pre-commit").read_text() == LEFTHOOK_MARKER
    assert not list(hooks.glob("pre-commit.old*"))


def test_preserve_ignores_hooks_not_listed(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    _hook(hooks, "prepare-commit-msg", "x")
    assert _sh(tmp_path, "preserve", "pre-commit").returncode == 0
    assert (hooks / "prepare-commit-msg").exists()


def test_run_without_legacy_hooks_succeeds(tmp_path: Path) -> None:
    _repo(tmp_path)
    assert _sh(tmp_path, "run", "pre-commit").returncode == 0


def test_run_executes_all_in_numeric_order_with_args(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    log = tmp_path / "log"
    for name in ["pre-commit.old", "pre-commit.old.10", "pre-commit.old.2"]:
        _hook(hooks, name, f'#!/bin/sh\necho "{name} $*" >> "{log}"\n')
    assert _sh(tmp_path, "run", "pre-commit", "a1", "a2").returncode == 0
    assert log.read_text().splitlines() == [
        "pre-commit.old a1 a2",
        "pre-commit.old.2 a1 a2",
        "pre-commit.old.10 a1 a2",
    ]


def test_run_skips_non_executable_and_non_numbered(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    (hooks / "pre-commit.old.1").write_text("#!/bin/sh\nexit 1\n")
    _hook(hooks, "pre-commit.old.bak", "#!/bin/sh\nexit 1\n")
    assert _sh(tmp_path, "run", "pre-commit").returncode == 0


def test_run_stops_on_failure_and_propagates_code(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    log = tmp_path / "log"
    _hook(hooks, "pre-commit.old.1", "#!/bin/sh\nexit 3\n")
    _hook(hooks, "pre-commit.old.2", f'#!/bin/sh\necho ran >> "{log}"\n')
    assert _sh(tmp_path, "run", "pre-commit").returncode == 3
    assert not log.exists()


def test_run_forwards_stdin_to_every_hook(tmp_path: Path) -> None:
    hooks = _repo(tmp_path)
    log = tmp_path / "log"
    for name in ["pre-push.old.1", "pre-push.old.2"]:
        _hook(hooks, name, f'#!/bin/sh\ncat >> "{log}"\n')
    assert _sh(tmp_path, "run", "pre-push", stdin="refs\n").returncode == 0
    assert log.read_text() == "refs\nrefs\n"


def test_lefthook_config_runs_legacy_hooks_for_every_event() -> None:
    config = yaml.safe_load((ROOT / "lefthook" / "lefthook.yml").read_text())
    for event, spec in config.items():
        cmd = spec["commands"]["legacy-hooks"]
        assert f"legacy_hooks.sh run {event}" in cmd["run"]
        # hazard: lefthook reads {0} as a file template in pre-commit and skips it
        assert "{0}" not in cmd["run"]
    assert config["pre-push"]["commands"]["legacy-hooks"]["use_stdin"] is True


@pytest.mark.skipif(shutil.which("lefthook") is None, reason="lefthook not installed")
def test_real_commit_runs_preserved_hook_after_reinstall(tmp_path: Path) -> None:
    real = yaml.safe_load((ROOT / "lefthook" / "lefthook.yml").read_text())
    events = ["pre-commit", "commit-msg"]
    config = {
        e: {"commands": {"legacy-hooks": real[e]["commands"]["legacy-hooks"]}}
        for e in events
    }
    (tmp_path / "lefthook.yml").write_text(yaml.safe_dump(config))
    hooks = _repo(tmp_path)
    log = tmp_path / "log"
    env = {**os.environ, "AI_PROJECT_ROOT_DIR": str(ROOT)}

    def install() -> None:
        _sh(tmp_path, "preserve", *events)
        subprocess.run(
            ["lefthook", "install"],
            cwd=tmp_path,
            env=env,
            check=True,
            capture_output=True,
        )

    _hook(hooks, "commit-msg", f'#!/bin/sh\necho "first $1" >> "{log}"\n')
    install()
    _hook(hooks, "commit-msg", f'#!/bin/sh\necho "second $1" >> "{log}"\n')
    install()
    git = [
        "git",
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@t",
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        "m",
    ]
    subprocess.run(["git", "checkout", "-q", "-b", "feat"], cwd=tmp_path, check=True)
    subprocess.run(git, cwd=tmp_path, env=env, check=True, capture_output=True)
    assert log.read_text().splitlines() == [
        "first .git/COMMIT_EDITMSG",
        "second .git/COMMIT_EDITMSG",
    ]

    _hook(hooks, "pre-commit.old.1", "#!/bin/sh\nexit 1\n")
    # invariant: lefthook skips every pre-commit command when nothing is staged
    (tmp_path / "f").write_text("x")
    subprocess.run(["git", "add", "f"], cwd=tmp_path, check=True)
    blocked = subprocess.run(
        git, cwd=tmp_path, env=env, capture_output=True, check=False
    )
    assert blocked.returncode != 0


@pytest.mark.skipif(shutil.which("lefthook") is None, reason="lefthook not installed")
def test_real_push_gives_legacy_hook_args_and_stdin(tmp_path: Path) -> None:
    work, remote = tmp_path / "work", tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    real = yaml.safe_load((ROOT / "lefthook" / "lefthook.yml").read_text())
    hooks = _repo(work)
    (work / "lefthook.yml").write_text(
        yaml.safe_dump(
            {
                "pre-push": {
                    "commands": {
                        "legacy-hooks": real["pre-push"]["commands"]["legacy-hooks"]
                    }
                }
            }
        )
    )
    env = {**os.environ, "AI_PROJECT_ROOT_DIR": str(ROOT)}
    subprocess.run(
        ["lefthook", "install"], cwd=work, env=env, check=True, capture_output=True
    )
    log = tmp_path / "log"
    _hook(
        hooks,
        "pre-push.old.1",
        f'#!/bin/sh\necho "args $1 $2" >> "{log}"\ncat >> "{log}"\n',
    )

    def git(*args: str) -> None:
        subprocess.run(
            ["git", *args], cwd=work, env=env, check=True, capture_output=True
        )

    git("checkout", "-q", "-b", "feat")
    (work / "f").write_text("x")
    git("add", "f")
    git(
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@t",
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        "m",
    )
    git("remote", "add", "origin", str(remote))
    git("push", "-q", "origin", "feat")
    lines = log.read_text().splitlines()
    assert lines[0] == f"args origin {remote}"
    assert lines[1].startswith("refs/heads/feat ")


def test_installer_preserves_hooks_before_lefthook_install() -> None:
    text = (ROOT / "scripts" / "claude.install.sh").read_text()
    preserve = text.index('legacy_hooks.sh" preserve')
    assert preserve < text.index("&& lefthook install)", preserve)
