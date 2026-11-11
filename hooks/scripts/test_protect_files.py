"""Regression suite for protect_files.py false positives seen in real session logs."""

# pylint: disable=missing-param-doc,missing-return-doc,redefined-outer-name
# pylint: disable=missing-any-param-doc,missing-type-doc,missing-yield-doc
# pylint: disable=missing-yield-type-doc
# why: test names state intent; pytest fixtures need no param docs

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

HOOK = Path(__file__).with_name("protect_files.py")


@pytest.fixture(scope="module")
def sandbox():
    """Project + fake aipp root + fake config dir, all outside the /tmp allowlist."""
    # why: /tmp/** is allowlisted by the hook, so a pytest tmp_path would make
    # every outside-project assertion pass vacuously.
    cache = Path.home() / ".cache"
    cache.mkdir(exist_ok=True)
    base = Path(tempfile.mkdtemp(prefix="protect-files-test-", dir=cache))
    proj, aipp, cfg = base / "proj", base / "aipp", base / "cfg"
    files = {
        proj / "README.md": "x",
        proj / "sub" / "dir" / "a.txt": "x",
        proj / ".env": "K=v",
        proj / ".env.example": "K=",
        proj / "example.env": "K=",
        proj / ".git" / "hooks" / "pre-commit": "x",
        proj / ".git" / "config": "x",
        aipp / "lefthook" / "lefthook.yml": "x",
        aipp / "skills" / "s" / "x.md": "x",
        aipp / ".env": "K=v",
        cfg / "projects" / "p" / "tool-results" / "a.txt": "x",
        cfg / "skills" / "synced" / "k" / "SKILL.md": "x",
        base / "outside" / "secret.txt": "x",
    }
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    (proj / "lefthook.yml").symlink_to(aipp / "lefthook" / "lefthook.yml")
    (proj / ".claude" / "skills").mkdir(parents=True)
    (proj / ".claude" / "skills" / "s").symlink_to(aipp / "skills" / "s")
    (proj / "escape").symlink_to(base / "outside")
    yield {"base": base, "proj": proj, "aipp": aipp, "cfg": cfg}
    shutil.rmtree(base)


def run_hook(
    sandbox, tool_input: dict, tool_name: str = "Bash"
) -> tuple[int, dict | None]:
    """Feed one tool call to the hook; return (exit code, parsed deny JSON)."""
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("PROTECT_FILES_EXTRA_ALLOWED", "PROTECT_FILES_MCP_ALLOWLIST")
    }
    env |= {
        "CLAUDE_PROJECT_DIR": str(sandbox["proj"]),
        "AI_PROJECT_ROOT_DIR": str(sandbox["aipp"]),
        "CLAUDE_CONFIG_DIR": str(sandbox["cfg"]),
    }
    proc = subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"tool_name": tool_name, "tool_input": tool_input}),
        capture_output=True,
        text=True,
        cwd=sandbox["proj"],
        env=env,
        check=False,
    )
    deny = None
    if proc.returncode == 2:
        deny = json.loads(proc.stderr.strip().splitlines()[-1])
    return proc.returncode, deny


ALLOWED_COMMANDS = [
    # why: sed/awk/grep script or pattern is not a path
    "sed -n '/## /,$p' README.md",
    "sed -n '/^## Checks/,/^## Handoff/p' README.md",
    "awk '/^foo/{f=1} f' README.md",
    "awk -F'/' '{print $1}' README.md",
    "awk -F / '{print $1}' README.md",
    "grep -v '/android/' README.md",
    "grep -n -A 3 '/clear|x' README.md",
    "git log | sed -n '/lint-staged/,/summary/p'",
    # why: read commands honor ":r" allowlist entries
    "cat CFG/projects/p/tool-results/a.txt",
    "sed -n 1,5p CFG/projects/p/tool-results/a.txt",
    "grep x CFG/projects/p/tool-results/a.txt",
    "sed -n 1,5p .claude/skills/s/x.md",
    # why: symlinked toolkit files resolve into the aipp root
    "cat lefthook.yml",
    "head -5 AIPP/lefthook/lefthook.yml",
    "cat CFG/skills/synced/k/SKILL.md",
    # why: a cd earlier in the command shifts the base for relative paths
    "cd sub/dir && cat ../../README.md",
    "cd sub/dir; sed -n 1p ../../README.md",
    # why: env templates and find -name predicates expose no secrets
    "cat .env.example",
    "cat example.env",
    "find . -iname '*.env'",
    "find . -name '.env' -o -name '*.pem'",
    # why: reading hooks is harmless; writing them is the risk
    "cat .git/hooks/pre-commit",
    # why: trailing punctuation from subshell text is not part of a path
    "x=$(ls 2>/dev/null)",
    # why: fd duplication and heredoc delimiters are not files
    "cd BASE/outside && echo hi 2>&1",
    "echo hi >&2",
    "cd BASE/outside && python3 - <<'EOF'\nprint(1)\nEOF",
    # why: process substitution inside a segment is checked as its own command
    "grep -c x <(sed -n '/### T8:/,/### T15:/p' README.md)",
    # why: find/cp only read their sources
    "find .claude/skills/s -type f",
    "cp .claude/skills/s/x.md sub/copy.md",
]

DENIED_COMMANDS = [
    "cat .env",
    "grep K .env",
    "sed -n 1p .env",
    "sed -e '/x/d' .env",
    "grep -e K .env",
    "grep -f .env README.md",
    "sed -f .env README.md",
    "awk -f .env README.md",
    "awk '{print}' .env",
    "cat AIPP/.env",
    "cat .git/config",
    "echo x > .git/hooks/pre-commit",
    "sed -i s/x/y/ CFG/projects/p/tool-results/a.txt",
    "sed -ni s/x/y/ lefthook.yml",
    "echo x >> lefthook.yml",
    "cat BASE/outside/secret.txt",
    "cat escape/secret.txt",
    "cd sub && cat ../../outside/secret.txt",
    "cd BASE/outside && cat secret.txt",
    "find . -name x -exec cat .env \\;",
    "sed 's/a/b/w BASE/outside/out' README.md",
    "echo x >&BASE/outside/out",
    "find .claude/skills/s -delete",
    "cp README.md .claude/skills/s/",
    "cp -t .claude/skills/s README.md",
    "cp .env sub/",
    "grep x <(cat .env)",
]


def _fill(sandbox, cmd: str) -> str:
    for key in ("cfg", "aipp", "base"):
        cmd = cmd.replace(key.upper(), str(sandbox[key]))
    return cmd


@pytest.mark.parametrize("cmd", ALLOWED_COMMANDS)
def test_command_allowed(sandbox, cmd: str) -> None:
    """Commands seen as false positives in session logs must pass."""
    rc, deny = run_hook(sandbox, {"command": _fill(sandbox, cmd)})
    assert rc == 0, deny


@pytest.mark.parametrize("cmd", DENIED_COMMANDS)
def test_command_denied(sandbox, cmd: str) -> None:
    """Real protected/outside access must still be denied."""
    rc, deny = run_hook(sandbox, {"command": _fill(sandbox, cmd)})
    assert rc == 2, deny


def test_read_tool_symlinked_toolkit_file_allowed(sandbox) -> None:
    """Read of a project symlink into the aipp root passes."""
    rc, deny = run_hook(
        sandbox, {"file_path": str(sandbox["proj"] / "lefthook.yml")}, "Read"
    )
    assert rc == 0, deny


def test_write_tool_symlinked_toolkit_file_denied(sandbox) -> None:
    """Writing through a symlink into the aipp root stays denied."""
    rc, _ = run_hook(
        sandbox,
        {"file_path": str(sandbox["proj"] / "lefthook.yml"), "content": "x"},
        "Write",
    )
    assert rc == 2


def test_outside_deny_reason_names_resolved_path_and_fix(sandbox) -> None:
    """Outside-project denial explains where the path resolved and how to allow it."""
    _, deny = run_hook(sandbox, {"command": "cat escape/secret.txt"})
    assert deny is not None
    assert str(sandbox["base"] / "outside" / "secret.txt") in deny["reason"]
    assert "PROTECT_FILES_EXTRA_ALLOWED" in deny["reason"]


def test_write_deny_source_label_is_write(sandbox) -> None:
    """A redirect write is not labeled as a read."""
    _, deny = run_hook(sandbox, {"command": "echo x > .git/hooks/pre-commit"})
    assert deny is not None
    assert deny["source"] == "command_write"
