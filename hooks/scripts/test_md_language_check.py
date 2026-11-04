"""Regression suite for the markdown language check hook."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
import sys
from typing import TYPE_CHECKING

import md_language_check as hook
import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import utils

if TYPE_CHECKING:
    from collections.abc import Callable

PORTUGUESE = (
    "Este documento explica como os dados são salvos para uma pessoa que não "
    "conhece o projeto."
)
ENGLISH = "This document explains how the data is saved for newcomers."


@pytest.fixture(name="run_hook")
def run_hook_fixture(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> Callable[[str, str], str]:
    """Return a runner that feeds main() a Write payload and yields its stdout."""

    def run(file_path: str, content: str) -> str:
        payload = {"tool_input": {"file_path": file_path, "content": content}}
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        monkeypatch.setattr(utils, "is_within_project", lambda *_: True)
        with pytest.raises(SystemExit) as exit_info:
            hook.main()
        assert exit_info.value.code == 0
        return capsys.readouterr().out

    return run


def test_portuguese_in_docs_asks_the_user(run_hook: Callable[[str, str], str]) -> None:
    """Portuguese content in a controlled dir prompts instead of blocking."""
    decision = json.loads(run_hook("/proj/docs/guide.md", PORTUGUESE))[
        "hookSpecificOutput"
    ]

    assert decision["hookEventName"] == "PreToolUse"
    assert decision["permissionDecision"] == "ask"
    assert "guide.md" in decision["permissionDecisionReason"]
    assert "Save anyway?" in decision["permissionDecisionReason"]


def test_english_in_docs_stays_silent(run_hook: Callable[[str, str], str]) -> None:
    """English content in a controlled dir produces no decision."""
    assert run_hook("/proj/docs/guide.md", ENGLISH) == ""


def test_portuguese_outside_controlled_dirs_stays_silent(
    run_hook: Callable[[str, str], str],
) -> None:
    """Portuguese content elsewhere is not the hook's concern."""
    assert run_hook("/proj/notes/guide.md", PORTUGUESE) == ""
