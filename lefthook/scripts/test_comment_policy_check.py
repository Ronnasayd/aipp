"""Tests for comment_policy_check doc-comment handling."""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

from comment_policy_check import find_findings, main

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_jsdoc_block_is_exempt() -> None:
    src = "/**\n * Sum.\n * @param a x\n */\nfunction s(a){}\n"
    assert not find_findings("", src, "a.ts")


def test_python_docstring_is_exempt() -> None:
    src = 'def a():\n    """Docstring."""\n    return 1\n'
    assert not find_findings("", src, "a.py")


def test_plain_block_comment_still_flagged() -> None:
    src = "/* sums */\nfunction s(a){}\n"
    assert len(find_findings("", src, "a.js")) == 1


def test_undeclared_line_comment_still_flagged() -> None:
    src = "// sums\nfunction s(a){}\n"
    assert len(find_findings("", src, "a.js")) == 1


def _repo_with_unstaged_comment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True)

    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (tmp_path / "a.js").write_text("function s(a){}\n")
    git("add", "a.js")
    git("commit", "-qm", "init")
    (tmp_path / "a.js").write_text("// sums\nfunction s(a){}\n")
    (tmp_path / "b.js").write_text("// new file\nfunction t(){}\n")
    monkeypatch.chdir(tmp_path)


def test_worktree_flag_sees_unstaged_and_untracked(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _repo_with_unstaged_comment(tmp_path, monkeypatch)
    assert main(["--worktree"]) == 1
    err = capsys.readouterr().err
    assert "a.js:1" in err
    assert "b.js:1" in err


def test_default_mode_ignores_unstaged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _repo_with_unstaged_comment(tmp_path, monkeypatch)
    assert main([]) == 0
