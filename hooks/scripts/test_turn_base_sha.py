"""Tests for turn-base SHA pinning and `--session` changed-file selection."""

# ruff: noqa: F811 - `repo` is a pytest fixture imported from test_lint_changed

from __future__ import annotations

import io
import json
from pathlib import Path
import subprocess
import sys

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

# pylint: disable=protected-access,redefined-outer-name,unused-import

sys.path.insert(0, str(Path(__file__).resolve().parent))

import test_changed
from test_lint_changed import (  # noqa: F401 - pytest fixtures
    FakeRepo,
    _dirty,
    _install_python,
    _isolated_tmp,
    _py_args,
    _run_main,
    repo,
)
import turn_base_sha
import utils

SID = "abcdef12-3456-7890-abcd-ef1234567890"


def _head(repo: FakeRepo) -> str:
    """Return the full SHA of the repo's HEAD.

    Args:
        repo: Repo to inspect.

    Returns:
        str: HEAD's SHA.
    """
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo.root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _tlc_session(repo: FakeRepo, sha: str) -> Path:
    """Write a tlc handoff-session file pinning `sha` for SID.

    Args:
        repo: Repo to write into.
        sha: Turn-base SHA to record.

    Returns:
        Path: The written file.
    """
    body = json.dumps({"slice": {"turn_base_sha": sha}})
    return repo.write(f".tlc/harness/state/handoff-sessions/claude-{SID}.json", body)


def _own_pin(repo: FakeRepo, sha: str) -> None:
    """Write the turn_base_sha.py pin file for SID.

    Args:
        repo: Repo the pin belongs to.
        sha: Turn-base SHA to record.
    """
    pin = utils.tmp_project_dir(str(repo.root), "turn-base-sha")
    (pin / f"{utils.get_session_id_short(SID)}.txt").write_text(sha, encoding="utf-8")


def test_turn_base_sha_prefers_tlc(repo: FakeRepo) -> None:
    _tlc_session(repo, "tlc1234")
    _own_pin(repo, "own5678")

    assert utils.get_turn_base_sha(str(repo.root), SID) == "tlc1234"


def test_turn_base_sha_falls_back_to_own_pin(repo: FakeRepo) -> None:
    _own_pin(repo, "own5678")

    assert utils.get_turn_base_sha(str(repo.root), SID) == "own5678"


def test_turn_base_sha_bad_tlc_falls_back(repo: FakeRepo) -> None:
    repo.write(f".tlc/harness/state/handoff-sessions/claude-{SID}.json", "{bad")
    _own_pin(repo, "own5678")

    assert utils.get_turn_base_sha(str(repo.root), SID) == "own5678"


def test_turn_base_sha_none_without_pins(repo: FakeRepo) -> None:
    assert utils.get_turn_base_sha(str(repo.root), SID) is None


def test_turn_base_sha_none_for_empty_session(repo: FakeRepo) -> None:
    body = json.dumps({"slice": {"turn_base_sha": "x1"}})
    repo.write(utils.tlc_session_path("", "").as_posix(), body)

    assert utils.get_turn_base_sha(str(repo.root), "") is None


def _run_turn_base_hook(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> str:
    """Run turn_base_sha.main() with a UserPromptSubmit payload for SID.

    Args:
        repo: Repo used as the project root.
        monkeypatch: pytest monkeypatch.
        capsys: pytest capture fixture.

    Returns:
        str: The hook's stdout.
    """
    payload = json.dumps({"session_id": SID, "cwd": str(repo.root)})
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    with pytest.raises(SystemExit):
        turn_base_sha.main()
    return capsys.readouterr().out


def test_turn_base_hook_pins_own_sha_without_tlc(
    repo: FakeRepo,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = _run_turn_base_hook(repo, monkeypatch, capsys)

    assert json.loads(out)["session_id"] == SID
    assert utils.get_turn_base_sha(str(repo.root), SID) == _head(repo)


def test_turn_base_hook_skips_own_pin_with_tlc(
    repo: FakeRepo,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _tlc_session(repo, "tlc1234")

    _run_turn_base_hook(repo, monkeypatch, capsys)

    pin = utils.tmp_project_dir(str(repo.root), "turn-base-sha")
    assert not (pin / f"{utils.get_session_id_short(SID)}.txt").exists()


def test_session_lints_files_committed_since_base(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo.write("before.py", "x = 1\n")
    repo.commit("before base")
    _own_pin(repo, _head(repo))
    committed = str(repo.write("committed.py", "x = 1\n").resolve())
    repo.commit("mid-turn commit")
    untracked = str(repo.write("new.py", "x = 1\n").resolve())
    _install_python(repo)
    repo.fake("npx")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setattr(sys, "argv", ["lint_changed.py", "--session"])

    assert _run_main(capsys) == (0, "")
    assert _py_args(repo.calls("ruff")) == [sorted([committed, untracked])]


def test_session_without_base_uses_porcelain(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo.write("committed.py", "x = 1\n")
    repo.commit("no pin")
    dirty = _dirty(repo, "dirty.py")
    _install_python(repo)
    repo.fake("npx")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setattr(sys, "argv", ["lint_changed.py", "--session"])

    assert _run_main(capsys) == (0, "")
    assert _py_args(repo.calls("ruff")) == [dirty]


def test_test_changed_session_runs_files_since_base(
    repo: FakeRepo, monkeypatch: pytest.MonkeyPatch
) -> None:
    _own_pin(repo, _head(repo))
    repo.write("a.ts", "export const a = 1;\n")
    repo.commit("mid-turn commit")
    repo.fake("jest", dest=repo.root / "node_modules" / ".bin")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", SID)
    monkeypatch.setattr(sys, "argv", ["test_changed.py", "--session"])

    assert test_changed.main() == 0
    assert repo.calls("jest") == [[*test_changed._RUNNERS["jest"].split(), "a.ts"]]
