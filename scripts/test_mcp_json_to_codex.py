"""Tests for scripts/mcp_json_to_codex.py (Claude .mcp.json -> Codex config)."""

import json
import subprocess
import sys
import tomllib
from pathlib import Path

SCRIPT = Path(__file__).parent / "mcp_json_to_codex.py"

MCP_JSON = {
    "mcpServers": {
        "aipp:stdio": {
            "command": "uvx",
            "args": ["--config", "${HOME}/x.json"],
            "env": {"TOKEN": "${MY_TOKEN:-add-value-to-env-vars}"},
        },
        "aipp:http": {
            "type": "http",
            "url": "https://example.test/mcp",
            "headers": {"Authorization": "Bearer ${MY_TOKEN:-add-value-to-env-vars}"},
        },
        "aipp:unset": {
            "command": "npx",
            "args": ["--api-key", "${NOT_SET_ANYWHERE:-add-value-to-env-vars}"],
        },
        "aipp:env-only-unset": {
            "command": "npx",
            "env": {"KEY": "${NOT_SET_ANYWHERE:-add-value-to-env-vars}"},
        },
        "aipp:missing-file": {"command": "java", "args": ["-jar", "/nope/proxy.jar"]},
        "aipp:skipped": {"command": "echo"},
    }
}


def _run(tmp_path, enabled=None, existing=""):
    project = tmp_path / "proj"
    (project / ".claude").mkdir(parents=True)
    (tmp_path / "x.json").write_text("{}")
    mcp = project / ".mcp.json"
    mcp.write_text(json.dumps(MCP_JSON))
    if enabled is not None:
        settings = {"enabledMcpjsonServers": enabled}
        (project / ".claude" / "settings.local.json").write_text(json.dumps(settings))
    out = project / ".codex" / "config.toml"
    if existing:
        out.parent.mkdir()
        out.write_text(existing)
    env = {"HOME": str(tmp_path), "MY_TOKEN": "s3cret", "PATH": "/usr/bin:/bin"}
    subprocess.run(
        [sys.executable, str(SCRIPT), str(mcp), str(project)], check=True, env=env
    )
    return out


def test_converts_stdio_and_http_with_env_expansion(tmp_path):
    """Stdio and HTTP specs map to Codex keys with ${VAR} expanded."""
    servers = tomllib.loads(_run(tmp_path).read_text())["mcp_servers"]

    stdio = servers["aipp_stdio"]
    assert stdio["command"] == "uvx"
    assert stdio["args"] == ["--config", f"{tmp_path}/x.json"]
    assert stdio["env"] == {"TOKEN": "s3cret"}
    assert stdio["startup_timeout_sec"] >= 30

    http = servers["aipp_http"]
    assert http["url"] == "https://example.test/mcp"
    assert http["http_headers"] == {"Authorization": "Bearer s3cret"}


def test_unconfigured_placeholder_disables_server(tmp_path):
    """Unset var in args, or a missing file arg, breaks launch: write it disabled.

    An unset var only in env is kept enabled, as Claude runs it (e.g. figma-console
    works through its desktop bridge without a token).
    """
    servers = tomllib.loads(_run(tmp_path).read_text())["mcp_servers"]
    assert servers["aipp_unset"]["enabled"] is False
    assert servers["aipp_missing-file"]["enabled"] is False
    assert "enabled" not in servers["aipp_env-only-unset"]
    assert "enabled" not in servers["aipp_stdio"]


def test_respects_claude_enabled_list(tmp_path):
    """Only servers Claude enabled for the project are synced."""
    out = _run(tmp_path, enabled=["aipp:http"])
    assert set(tomllib.loads(out.read_text())["mcp_servers"]) == {"aipp_http"}


def test_replaces_managed_block_and_keeps_user_content(tmp_path):
    """Re-running is idempotent and user tables survive; file is 0600."""
    user = '[mcp_servers.mine]\ncommand = "mine"\n'
    out = _run(tmp_path, existing=user)
    first = out.read_text()
    env = {"HOME": str(tmp_path), "MY_TOKEN": "s3cret", "PATH": "/usr/bin:/bin"}
    mcp = tmp_path / "proj" / ".mcp.json"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(mcp), str(tmp_path / "proj")],
        check=True,
        env=env,
    )

    assert out.read_text() == first
    servers = tomllib.loads(first)["mcp_servers"]
    assert servers["mine"]["command"] == "mine"
    assert "aipp_stdio" in servers
    assert oct(out.stat().st_mode & 0o777) == "0o600"
