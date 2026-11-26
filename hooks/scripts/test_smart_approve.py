"""Regression tests for smart_approve.decide ask handling."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest params need no param docs

from __future__ import annotations

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
from smart_approve import _merge_custom_permissions, decide

SETTINGS = {"permissions": {"ask": ["Bash(curl:*)", "Bash(git push:*)"]}}


@pytest.fixture(autouse=True)
def interactive_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Start every test interactive, whatever the runner's environment holds."""
    monkeypatch.delenv("AIPP_AUTONOMOUS", raising=False)


@pytest.mark.parametrize(
    "command",
    [
        "curl https://x && git push origin feature/x",
        "git push origin feature/x && curl https://x",
    ],
)
def test_immune_ask_wins_over_earlier_ask_in_bypass(command: str) -> None:
    """A bypass-immune ask sub-command must prompt regardless of its position."""
    assert decide(command, SETTINGS, bypass_permissions=True)[0] == "ask"


def test_non_immune_ask_promoted_in_bypass() -> None:
    """Asks that are not bypass-immune still become allow in bypass mode."""
    assert decide("curl https://x", SETTINGS, bypass_permissions=True)[0] == "allow"


def test_immune_ask_promoted_when_autonomous(monkeypatch: pytest.MonkeyPatch) -> None:
    """AIPP_AUTONOMOUS=1 lifts bypass immunity so git push needs no human."""
    monkeypatch.setenv("AIPP_AUTONOMOUS", "1")
    assert (
        decide("git push origin feature/x", SETTINGS, bypass_permissions=True)[0]
        == "allow"
    )


def test_autonomous_still_asks_without_bypass(monkeypatch: pytest.MonkeyPatch) -> None:
    """Autonomous mode only lifts immunity; outside bypass mode asks still prompt."""
    monkeypatch.setenv("AIPP_AUTONOMOUS", "1")
    assert decide("git push origin feature/x", SETTINGS)[0] == "ask"


def test_git_push_asks_from_builtin_permissions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """git push is an ask rule even when no settings file lists it."""
    monkeypatch.delenv("AIPP_AUTONOMOUS", raising=False)
    merged = _merge_custom_permissions({})
    assert (
        decide("git push origin feature/x", merged, bypass_permissions=True)[0] == "ask"
    )


@pytest.mark.parametrize(("env", "expected"), [(None, "deny"), ("1", None)])
def test_git_rebase_denied_only_when_interactive(
    monkeypatch: pytest.MonkeyPatch, env: str | None, expected: str | None
) -> None:
    """git rebase is denied interactively and allowed through in autonomous mode."""
    if env is None:
        monkeypatch.delenv("AIPP_AUTONOMOUS", raising=False)
    else:
        monkeypatch.setenv("AIPP_AUTONOMOUS", env)
    merged = _merge_custom_permissions({})
    assert (
        decide("git rebase origin/master", merged, bypass_permissions=True)[0]
        == expected
    )
