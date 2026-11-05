"""Behaviour of validate_requirements.py over spec-driven and lean tables."""

from pathlib import Path

from validate_requirements import check, main

SPEC_WARNING = "no **Spec**: source line at top of file"
DESIGN_WARNING = "no **Design**: source line at top of file"
REQUIREMENTS = """| Requirement | Expression | Complement | Path |
| --- | --- | --- | --- |
| FR-001 | a rule | a reason | SP |
"""
CONSEQUENCES = """## Accepted consequences

| # | Consequence | Driven by |
| --- | --- | --- |
| 1 | a cost | FR-001 |
"""
GLOSSARY = """## Glossary

- **FR** - functional requirement
- **SP** - success path
"""
SOURCES = "**Spec:** `f/spec.md`\n**Design:** `f/design.md`\n"


def write(tmp_path: Path, *parts: str) -> Path:
    """Write a requirements.md made of the given parts.

    Args:
        tmp_path: Directory to write into.
        *parts: Markdown blocks, joined by a blank line.

    Returns:
        The path of the written file.
    """
    path = tmp_path / "requirements.md"
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def warnings_for(header: str, tmp_path: Path) -> list[str]:
    """Run the checks over a file holding only a header line.

    Args:
        header: Line placed under the title.
        tmp_path: Directory to write into.

    Returns:
        The warnings reported for that file.
    """
    return check(write(tmp_path, "# Feature", header))[1]


def test_lean_plan_source_needs_no_spec_or_design(tmp_path):
    warnings = warnings_for("**Plan:** `f/plan.md`", tmp_path)
    assert SPEC_WARNING not in warnings
    assert DESIGN_WARNING not in warnings


def test_lean_checks_only_source_needs_no_spec_or_design(tmp_path):
    warnings = warnings_for("**Checks:** `f/checks.md`", tmp_path)
    assert SPEC_WARNING not in warnings
    assert DESIGN_WARNING not in warnings


def test_missing_sources_still_warn(tmp_path):
    warnings = warnings_for("no sources here", tmp_path)
    assert SPEC_WARNING in warnings
    assert DESIGN_WARNING in warnings


def test_complete_table_has_no_findings(tmp_path):
    path = write(tmp_path, SOURCES, REQUIREMENTS, CONSEQUENCES, GLOSSARY)
    assert check(path) == ([], [])


def test_no_rows_is_an_error(tmp_path):
    errors, _ = check(write(tmp_path, SOURCES, CONSEQUENCES, GLOSSARY))
    assert errors == ["no data rows found in any requirement table"]


def test_untagged_row_is_an_error(tmp_path):
    table = REQUIREMENTS.replace("| SP |", "| ?? |")
    errors, _ = check(write(tmp_path, SOURCES, table, CONSEQUENCES, GLOSSARY))
    assert errors == ["row not tagged SP/EP: 'FR-001'"]


def test_rationale_citing_a_spec_code_is_an_error(tmp_path):
    table = REQUIREMENTS.replace("a reason", "see AC-1.3")
    errors, _ = check(write(tmp_path, SOURCES, table, CONSEQUENCES, GLOSSARY))
    assert errors == [
        "rationale cites spec code AC-1.3 instead of explaining: 'FR-001'"
    ]


def test_concrete_value_in_expression_warns(tmp_path):
    table = REQUIREMENTS.replace("a rule", "record 4071 loads")
    _, warnings = check(write(tmp_path, SOURCES, table, CONSEQUENCES, GLOSSARY))
    assert warnings == [
        "Expression may embed a concrete id/sample value (forces lookup): 'FR-001'"
    ]


def test_missing_consequences_section_is_an_error(tmp_path):
    errors, _ = check(write(tmp_path, SOURCES, REQUIREMENTS, GLOSSARY))
    assert errors == ["missing 'Accepted consequences' section"]


def test_consequences_without_driven_by_table_is_an_error(tmp_path):
    section = "## Accepted consequences\n\nnone\n"
    errors, _ = check(write(tmp_path, SOURCES, REQUIREMENTS, section, GLOSSARY))
    assert errors == ["consequences section has no table with a 'Driven by' column"]


def test_empty_driven_by_is_an_error(tmp_path):
    section = CONSEQUENCES.replace("| FR-001 |", "|  |")
    errors, _ = check(write(tmp_path, SOURCES, REQUIREMENTS, section, GLOSSARY))
    assert errors == ["consequence row has empty 'Driven by' back-link: '1'"]


def test_no_glossary_warns(tmp_path):
    _, warnings = check(write(tmp_path, SOURCES, REQUIREMENTS, CONSEQUENCES))
    assert warnings == ["no Glossary section, but abbreviations used: ['FR', 'SP']"]


def test_undefined_abbreviation_warns(tmp_path):
    glossary = GLOSSARY.replace("- **SP** - success path\n", "")
    path = write(tmp_path, SOURCES, REQUIREMENTS, CONSEQUENCES, glossary)
    assert check(path)[1] == ["abbreviations used but not defined in Glossary: ['SP']"]


def test_main_exit_codes(tmp_path, capsys):
    clean = write(tmp_path, SOURCES, REQUIREMENTS, CONSEQUENCES, GLOSSARY)
    assert main([str(clean)]) == 0
    assert main([str(tmp_path)]) == 0
    assert "0 error(s), 0 warning(s)" in capsys.readouterr().out

    warned = write(tmp_path, REQUIREMENTS, CONSEQUENCES, GLOSSARY)
    assert main([str(warned)]) == 0
    assert main([str(warned), "--strict"]) == 1

    broken = write(tmp_path, SOURCES, GLOSSARY)
    assert main([str(broken)]) == 1
    assert "  ERROR " in capsys.readouterr().out

    assert main([str(tmp_path / "missing.md")]) == 2
    assert "file not found" in capsys.readouterr().err
