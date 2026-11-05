"""Tests for scripts/md2toml.py codex agent output."""

from pathlib import Path
import subprocess
import sys
import tomllib

SCRIPT = Path(__file__).parent / "md2toml.py"

AGENT_MD = '''---
name: demo-specialist
description: Does "demo" things
tools_disabled: [Bash]
---
Body with """triple""" quotes.
'''


def _run(tmp_path, *flags):
    src = tmp_path / "src"
    out = tmp_path / "out"
    src.mkdir()
    (src / "demo-specialist.agent.md").write_text(AGENT_MD, encoding="utf-8")
    subprocess.run(
        [sys.executable, str(SCRIPT), str(src), str(out), *flags], check=True
    )
    return tomllib.loads((out / "demo-specialist.agent.toml").read_text())


def test_codex_flag_emits_top_level_codex_agent_fields_only(tmp_path):
    data = _run(tmp_path, "--codex")
    # invariant: Codex agent loader rejects unknown fields (e.g. `metadata`)
    assert set(data) == {"name", "description", "developer_instructions"}
    assert data["name"] == "demo-specialist"
    assert data["description"] == 'Does "demo" things'
    assert data["developer_instructions"].strip() == 'Body with """triple""" quotes.'


def test_default_keeps_prompt_key(tmp_path):
    data = _run(tmp_path)
    assert data["prompt"].strip() == 'Body with """triple""" quotes.'
