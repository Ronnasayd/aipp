"""Shared pytest fixtures for the hook scripts."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import utils

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(autouse=True)
def isolated_decision_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Keep decisions from leaking between tests or into the user's real cache.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        tmp_path: per-test temporary directory.

    Returns:
        Path: the directory decisions are cached in during the test.
    """
    cache_dir = tmp_path / "decisions"
    monkeypatch.setattr(utils, "DECISION_CACHE_DIR", cache_dir)
    return cache_dir
