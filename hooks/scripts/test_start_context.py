"""Tests for the session-start glossary reference."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import start_context

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


@pytest.mark.parametrize("value", [None, "0", "true"])
def test_autonomous_section_absent_unless_exactly_one(
    monkeypatch: pytest.MonkeyPatch, value: str | None
) -> None:
    """Only AIPP_AUTONOMOUS=1 reports autonomous mode; anything else is silent."""
    if value is None:
        monkeypatch.delenv("AIPP_AUTONOMOUS", raising=False)
    else:
        monkeypatch.setenv("AIPP_AUTONOMOUS", value)
    assert start_context.autonomous_mode_notice() == ""


def test_autonomous_section_in_optional_sections(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """AIPP_AUTONOMOUS=1 adds the autonomous-mode notice to session context."""
    monkeypatch.setenv("AIPP_AUTONOMOUS", "1")
    sections = start_context.optional_sections({"cwd": str(tmp_path)})
    assert "AUTONOMOUS MODE ACTIVE" in sections


def test_autonomous_section_carries_full_mode_rules(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Autonomous rules live only in the notice, so it must carry all of them."""
    monkeypatch.setenv("AIPP_AUTONOMOUS", "1")
    notice = start_context.autonomous_mode_notice()
    for rule in (
        "Never ask the user",
        "Task request = authorization to change code",
        "auto-approved, autonomous mode",
        "feature branch + pull request",
        "protect_branches.py",
        "BLOCKED / TRIED / NEED",
    ):
        assert rule in notice


def test_agent_instructions_have_no_autonomous_section() -> None:
    """Interactive sessions must not see autonomous-mode rules at all."""
    instructions = Path(__file__).resolve().parents[2] / "instructions"
    text = (instructions / "agent.instructions.md").read_text(encoding="utf-8")
    assert "AIPP_AUTONOMOUS" not in text


def test_strip_frontmatter_drops_leading_frontmatter() -> None:
    """Frontmatter is removed; body keeps its own --- separators."""
    text = "---\ndescription: x\n---\nbody\n\n---\n\nmore"
    assert start_context.strip_frontmatter(text) == "\nbody\n\n---\n\nmore"


@pytest.mark.parametrize(
    "text",
    ["intro\n\n---\n\nrest", "a\n---\nb\n---\nc", "---\nunclosed"],
)
def test_strip_frontmatter_keeps_text_without_frontmatter(text: str) -> None:
    """Horizontal rules or an unclosed block must not cut the text."""
    assert start_context.strip_frontmatter(text) == text


def test_main_emits_instructions_without_frontmatter(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """SessionStart context carries the instruction body, not its frontmatter."""
    instructions = tmp_path / ".claude/instructions"
    instructions.mkdir(parents=True)
    (instructions / "agent.instructions.md").write_text(
        "---\ndescription: hidden-meta\n---\n# Rules\n\nkeep-this-body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(start_context, "optional_sections", lambda _payload: "")
    payload = {"cwd": str(tmp_path), "hook_event_name": "SessionStart"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))

    try:
        start_context.main()
    except SystemExit:
        pass

    output = json.loads(capsys.readouterr().out)
    context = output["hookSpecificOutput"]["additionalContext"]
    assert "keep-this-body" in context
    assert "hidden-meta" not in context


def run_main(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    event: str,
) -> str:
    """Run main() on a tmp project and return its additionalContext."""
    instructions = tmp_path / ".claude/instructions"
    instructions.mkdir(parents=True, exist_ok=True)
    (instructions / "agent.instructions.md").write_text(
        "# Rules\n\nrule-body\n", encoding="utf-8"
    )
    monkeypatch.setattr(start_context, "optional_sections", lambda _payload: "")
    payload = {"cwd": str(tmp_path), "hook_event_name": event, "session_id": "s1"}
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
    try:
        start_context.main()
    except SystemExit:
        pass
    return json.loads(capsys.readouterr().out)["hookSpecificOutput"][
        "additionalContext"
    ]


def test_session_start_puts_precedence_before_rules(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """AGENTS.md precedence is stated before the rules it ranks."""
    context = run_main(monkeypatch, tmp_path, capsys, "SessionStart")
    assert "AGENTS.md" in context
    assert context.index("override") < context.index("rule-body")


def test_prompt_submit_off_cycle_emits_only_precedence(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    """Off-cycle prompts re-assert precedence without repeating the rules."""
    monkeypatch.setattr(start_context, "read_loop_count", lambda *_a: 0)
    monkeypatch.setattr(start_context, "bump_loop_count", lambda *_a: None)
    context = run_main(monkeypatch, tmp_path, capsys, "UserPromptSubmit")
    assert context == start_context.PRECEDENCE_NOTICE
    assert "AGENTS.md rules" in context and "override" in context
