"""Tests for the session-start glossary reference."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import start_context

if TYPE_CHECKING:
    from pathlib import Path

GLOSSARY = """# Ctx

## Language

**Role agent**:
An agent with one job.
_Avoid_: Persona

**Dev-mod**:
An interface extension.
"""


@pytest.fixture(autouse=True)
def payload_cwd_is_project_root(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stop the real session's root from overriding the test's tmp cwd."""
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)


def test_no_glossary_emits_nothing(tmp_path: Path) -> None:
    """A repo without a glossary adds no section."""
    assert start_context.glossary_reference({"cwd": str(tmp_path)}) == ""


def test_glossary_lists_path_and_term_names_only(tmp_path: Path) -> None:
    """The section names the file and its terms, without definitions."""
    (tmp_path / "GLOSSARY.md").write_text(GLOSSARY, encoding="utf-8")

    text = start_context.glossary_reference({"cwd": str(tmp_path)})

    assert "`GLOSSARY.md`" in text
    assert "Role agent, Dev-mod" in text
    assert "An agent with one job" not in text


def test_glossary_map_wins_over_root_glossary(tmp_path: Path) -> None:
    """A multi-context repo points at the map instead of one glossary."""
    (tmp_path / "GLOSSARY.md").write_text(GLOSSARY, encoding="utf-8")
    (tmp_path / "GLOSSARY-MAP.md").write_text("# Glossary Map\n", encoding="utf-8")

    text = start_context.glossary_reference({"cwd": str(tmp_path)})

    assert "`GLOSSARY-MAP.md`" in text
    assert "Role agent" not in text


def test_extra_allowed_unset_emits_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    """No PROTECT_FILES_EXTRA_ALLOWED adds no section."""
    monkeypatch.delenv("PROTECT_FILES_EXTRA_ALLOWED", raising=False)
    assert start_context.extra_allowed_paths() == ""


def test_extra_allowed_blank_emits_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    """A blank value (installer default) adds no section."""
    monkeypatch.setenv("PROTECT_FILES_EXTRA_ALLOWED", " ; , ")
    assert start_context.extra_allowed_paths() == ""


def test_extra_allowed_lists_each_pattern(monkeypatch: pytest.MonkeyPatch) -> None:
    """Each comma/semicolon-separated entry is listed."""
    monkeypatch.setenv("PROTECT_FILES_EXTRA_ALLOWED", "/tmp/a, ~/b/**:r;/c")
    section = start_context.extra_allowed_paths()
    assert "PROTECT_FILES_EXTRA_ALLOWED" in section
    for entry in ("`/tmp/a`", "`~/b/**:r`", "`/c`"):
        assert entry in section


def test_extra_allowed_included_in_optional_sections(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The section reaches the hook's additionalContext."""
    monkeypatch.setenv("PROTECT_FILES_EXTRA_ALLOWED", "/tmp/xyz")
    assert "`/tmp/xyz`" in start_context.optional_sections({"cwd": str(tmp_path)})
