#!/usr/bin/env python3
"""Deterministic checks for a spec-to-requirements-table output.

Turns the spec-to-requirements-table skill's step-7 verification and
anti-pattern list into a checkable pass/fail run BEFORE the table is handed
to a reviewer, instead of trusting the model to self-audit. Pure standard
library, zero dependencies. Operates only on the generated requirements.md
markdown artifact - never on spec.md/design.md/tasks.md - so it stays
stack-agnostic and reusable on any project's table.

What it checks (heuristic markdown inspection, not a full parser):
  ERROR  - no data rows found in any requirement table
  ERROR  - a row's Path/id column is not tagged SP or EP
  ERROR  - a row's rationale cell cites a spec code (REQ-03, AC-1.3, FR-07 ...)
           instead of explaining in plain words
  ERROR  - an "Accepted consequences" section is missing
  ERROR  - a consequences row has no "Driven by" row-id back-link
  WARN   - a row's Expression cell contains a bare concrete id/sample value
           (e.g. a standalone number, or a quoted literal) - possible lookup
  WARN   - no Glossary section, or an abbreviation used in the body
           (FR/NR/SP/EP) is not defined in it
  WARN   - a source line is missing: Spec and Design, unless the table names a
           tlc-spec-lean Plan or Checks source

Usage:
  python3 <skill-dir>/scripts/validate_requirements.py [target] [--strict]

  Invoke from the skill directory that ships this script (not the project
  root). target defaults to requirements.md in the current directory.
  --strict  Treat warnings as errors.

Exit codes: 0 pass, 1 errors found (or warnings under --strict), 2 usage error.
"""

import argparse
from collections.abc import Callable, Iterator
import os
import re
import sys

SPEC_CODE_RE = re.compile(r"\b(REQ|AC|FR|NR)-\d+(\.\d+)?\b")
PATH_TAG_RE = re.compile(r"\b(SP|EP)\b")
BARE_NUMBER_RE = re.compile(r"(?<![\w.#-])\d{2,}(?![\w.-])")
QUOTED_LITERAL_RE = re.compile(r'"[^"]{2,}"|\'[^\']{2,}\'')
SOURCE_LINE_RE = re.compile(
    r"^\*\*(Spec|Design|Tasks|BDD|Plan|Checks):\*\*\s*`([^`]+)`", re.MULTILINE
)

Table = tuple[list[str], list[list[str]]]


def split_row(line: str) -> list[str]:
    """Split a markdown table line into its cells.

    Args:
        line: The table line.

    Returns:
        The stripped cell texts.
    """
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_separator(line: str) -> bool:
    """Tell whether a line is a markdown table separator.

    Args:
        line: The line to test.

    Returns:
        True for a separator line such as `| --- | --- |`.
    """
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def find_tables(lines: list[str]) -> Iterator[Table]:
    """Walk every markdown table in the document.

    Args:
        lines: The document's lines.

    Yields:
        A (header_cells, data_rows) pair per table.
    """
    i = 0
    while i < len(lines):
        if (
            lines[i].strip().startswith("|")
            and i + 1 < len(lines)
            and is_separator(lines[i + 1])
        ):
            header = split_row(lines[i])
            j = i + 2
            rows = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def _column(header: list[str], matches: Callable[[str], bool]) -> int | None:
    """Find the first header cell a predicate accepts.

    Args:
        header: The header cells.
        matches: Predicate over a lowercased cell.

    Returns:
        The column index, or None when no cell matches.
    """
    return next((i for i, c in enumerate(header) if matches(c.strip().lower())), None)


def _cell(row: list[str], column: int | None) -> str | None:
    """Read a cell that may not exist.

    Args:
        row: The row's cells.
        column: The column index, or None when the table lacks that column.

    Returns:
        The cell text, or None when the row has no such cell.
    """
    return row[column] if column is not None and column < len(row) else None


def _check_row(
    row: list[str], path: str | None, rationale: str | None, expression: str | None
) -> tuple[list[str], list[str]]:
    """Check one requirement row.

    Args:
        row: The row's cells.
        path: Its Path cell, if any.
        rationale: Its Complement cell, if any.
        expression: Its Expression cell, if any.

    Returns:
        The row's (errors, warnings).
    """
    errors, warnings = [], []
    if path is not None and not PATH_TAG_RE.search(path):
        errors.append(f"row not tagged SP/EP: {row[0][:50]!r}")
    code = SPEC_CODE_RE.search(rationale) if rationale is not None else None
    if code:
        errors.append(
            f"rationale cites spec code {code.group(0)} instead of explaining: "
            f"{row[0][:40]!r}"
        )
    if expression is not None and (
        BARE_NUMBER_RE.search(expression) or QUOTED_LITERAL_RE.search(expression)
    ):
        warnings.append(
            "Expression may embed a concrete id/sample value (forces lookup): "
            f"{row[0][:40]!r}"
        )
    return errors, warnings


def _check_requirements(tables: list[Table]) -> tuple[list[str], list[str]]:
    """Check that rows exist, are tagged, and explain themselves.

    Args:
        tables: The requirement tables.

    Returns:
        The (errors, warnings) of all rows.
    """
    errors, warnings = [], []
    total_rows = 0
    for header, rows in tables:
        path_col = _column(header, lambda c: c in ("path", "sp/ep"))
        expr_col = _column(header, lambda c: "expression" in c)
        comp_col = _column(header, lambda c: "complement" in c)
        total_rows += len(rows)
        for row in rows:
            row_errors, row_warnings = _check_row(
                row, _cell(row, path_col), _cell(row, comp_col), _cell(row, expr_col)
            )
            errors.extend(row_errors)
            warnings.extend(row_warnings)
    if total_rows == 0:
        errors.append("no data rows found in any requirement table")
    return errors, warnings


def _check_consequences(text: str, tables: list[Table]) -> list[str]:
    """Check the Accepted consequences section and its back-links.

    Args:
        text: The document.
        tables: The tables with a Driven by column.

    Returns:
        The errors found.
    """
    if not re.search(r"^#{1,3}\s.*consequence", text, re.IGNORECASE | re.MULTILINE):
        return ["missing 'Accepted consequences' section"]
    if not tables:
        return ["consequences section has no table with a 'Driven by' column"]
    errors: list[str] = []
    for header, rows in tables:
        driven_col = _column(header, lambda c: "driven by" in c)
        errors.extend(
            f"consequence row has empty 'Driven by' back-link: {row[0][:40]!r}"
            for row in rows
            if not (_cell(row, driven_col) or "").strip()
        )
    return errors


def _check_glossary(text: str) -> list[str]:
    """Check that the Glossary covers the abbreviations in use.

    Args:
        text: The document.

    Returns:
        The warnings found.
    """
    body_upper = text.upper()
    used_abbrevs = {
        a for a in ("FR", "NR", "SP", "EP") if re.search(rf"\b{a}\b", body_upper)
    }
    gloss_match = re.search(
        r"^#{1,3}\s*Glossary\s*$", text, re.IGNORECASE | re.MULTILINE
    )
    if not gloss_match:
        if used_abbrevs:
            return [
                f"no Glossary section, but abbreviations used: {sorted(used_abbrevs)}"
            ]
        return []
    gloss_body = text[gloss_match.end() :]
    undefined = [a for a in used_abbrevs if not re.search(rf"\*\*{a}\*\*", gloss_body)]
    if undefined:
        return [f"abbreviations used but not defined in Glossary: {sorted(undefined)}"]
    return []


def _check_sources(text: str) -> list[str]:
    """Check the source lines at the top of the file.

    Args:
        text: The document.

    Returns:
        The warnings found.
    """
    sources = dict(SOURCE_LINE_RE.findall(text))
    # why: a tlc-spec-lean feature has plan.md/checks.md instead of spec.md/design.md.
    required = () if sources.keys() & {"Plan", "Checks"} else ("Spec", "Design")
    return [
        f"no **{label}**: source line at top of file"
        for label in required
        if label not in sources
    ]


def check(path: str | os.PathLike[str]) -> tuple[list[str], list[str]]:
    """Run every check over a requirements.md.

    Args:
        path: The file to check.

    Returns:
        The (errors, warnings) found.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()

    tables = list(find_tables(text.splitlines()))
    cons_tables = [
        t for t in tables if _column(t[0], lambda c: "driven by" in c) is not None
    ]
    req_tables = [t for t in tables if t not in cons_tables]

    errors, warnings = _check_requirements(req_tables)
    errors.extend(_check_consequences(text, cons_tables))
    warnings.extend(_check_glossary(text))
    warnings.extend(_check_sources(text))
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    """Run the command line.

    Args:
        argv: Arguments, or None to read them from the process.

    Returns:
        The exit code: 0 pass, 1 findings, 2 usage error.
    """
    p = argparse.ArgumentParser(
        prog="validate_requirements.py",
        description="Deterministic checks for a spec-to-requirements-table output.",
    )
    p.add_argument("target", nargs="?", default="requirements.md")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)

    path = args.target
    if os.path.isdir(path):
        path = os.path.join(path, "requirements.md")
    if not os.path.isfile(path):
        sys.stderr.write(f"validate_requirements: file not found: {path}\n")
        return 2

    errors, warnings = check(path)
    for w in warnings:
        sys.stdout.write(f"  WARN  {w}\n")
    for e in errors:
        sys.stdout.write(f"  ERROR {e}\n")
    fail = errors or (warnings and args.strict)
    sys.stdout.write(
        f"\nvalidate_requirements: {len(errors)} error(s), "
        f"{len(warnings)} warning(s) in {path}\n"
    )
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
