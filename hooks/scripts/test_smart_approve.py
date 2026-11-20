"""Regression tests for smart_approve.decide ask handling."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest params need no param docs

from __future__ import annotations

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
from smart_approve import decide

SETTINGS = {"permissions": {"ask": ["Bash(curl:*)", "Bash(git push:*)"]}}


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
