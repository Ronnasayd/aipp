"""Installers must run cleanly in a fresh project: no AGENTS.md, no git repo."""

from pathlib import Path
import re
import subprocess

import pytest

SCRIPTS = Path(__file__).parent
INSTALLERS = ["claude.install.sh", "gemini.install.sh", "antigravity.install.sh"]


def _function(script: str, name: str) -> str:
    text = (SCRIPTS / script).read_text(encoding="utf-8")
    match = re.search(rf"^{name}\(\) \{{\n.*?^\}}\n", text, re.M | re.S)
    assert match, f"{name} not found in {script}"
    return match.group(0)


@pytest.mark.parametrize("script", INSTALLERS)
def test_replace_between_creates_missing_file(tmp_path, script):
    target = tmp_path / "AGENTS.md"
    code = _function(script, "replace_between")
    code += 'replace_between "<A>" "<B>" "body" "$1"'
    result = subprocess.run(
        ["bash", "-c", code, "_", str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stderr == ""
    assert target.read_text(encoding="utf-8") == "\n<A>\nbody\n<B>\n"


def _lefthook_block() -> str:
    text = (SCRIPTS / "claude.install.sh").read_text(encoding="utf-8")
    start = text.index('if ! git -C "$LOCAL" rev-parse')
    return text[start : text.index('git_exclude "lefthook.yml"')]


def test_lefthook_install_skipped_outside_git(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "lefthook"
    fake.write_text("#!/bin/sh\necho CALLED\nexit 128\n", encoding="utf-8")
    fake.chmod(0o755)
    local = tmp_path / "proj"
    local.mkdir()
    result = subprocess.run(
        ["bash", "-c", _lefthook_block()],
        env={"PATH": f"{bin_dir}:/usr/bin:/bin", "LOCAL": str(local)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert "CALLED" not in result.stdout
    assert result.returncode == 0
