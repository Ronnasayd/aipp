"""Tests for the session-start durable pages listing."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
import subprocess

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import start_memory_rules

PROJECT_HIT = {"path": "gotchas/local.md", "title": "Local"}


def run_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    hits: list[dict[str, str]],
) -> tuple[str, list[list[str]]]:
    """Run the hook on a fake CLI; return the context and the commands run."""
    commands: list[list[str]] = []

    def fake_run(cmd: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        commands.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, json.dumps(hits), "")

    monkeypatch.setattr(start_memory_rules.subprocess, "run", fake_run)
    monkeypatch.setattr("sys.stdin", io.StringIO("{}"))
    with pytest.raises(SystemExit):
        start_memory_rules.main()
    payload = json.loads(capsys.readouterr().out)
    return str(payload["hookSpecificOutput"]["additionalContext"]), commands


def test_project_pages_are_listed_with_global_hint(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Project pages are listed; global pages are only pointed at."""
    context, commands = run_main(monkeypatch, capsys, [PROJECT_HIT])
    assert "- `gotchas/local.md` — Local" in context
    assert start_memory_rules.GLOBAL_HINT in context
    assert len(commands) == 1
    assert "_global" not in commands[0]


def test_hint_is_emitted_without_project_pages(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A project without pages still learns where generic memory lives."""
    context, _ = run_main(monkeypatch, capsys, [])
    assert start_memory_rules.GLOBAL_HINT in context
    assert "durable pages in this project" not in context


@pytest.mark.parametrize(
    ("prefix", "terms"),
    [
        ("notes/", ("note", "notes")),
        ("decisions/", ("decision", "decisions")),
        ("preferences/", ("preference", "preferences")),
        ("bugs/", ("bug", "bugs")),
        ("concepts/", ("concept", "concepts")),
        ("reference/", ("reference", "references")),
        ("tools/", ("tool", "tools")),
    ],
)
def test_extra_durable_prefix_is_queried_and_listed(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    prefix: str,
    terms: tuple[str, str],
) -> None:
    """Each prefix is searched by both forms and its pages are listed."""
    hits = [
        {"path": f"{prefix}page.md", "title": "Page"},
        {"path": "sessions/abc.md", "title": "Session"},
    ]
    context, commands = run_main(monkeypatch, capsys, hits)
    assert f"- `{prefix}page.md` — Page" in context
    assert "sessions/abc.md" not in context
    assert set(terms) <= set(commands[0][2].split(" OR "))
