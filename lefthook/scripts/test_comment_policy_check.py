"""Tests for comment_policy_check doc-comment handling."""

from __future__ import annotations

from comment_policy_check import find_findings


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
