#!/usr/bin/env python3
"""Mirror a Claude Code .mcp.json into a project-scoped Codex config.

Usage: mcp_json_to_codex.py <path/to/.mcp.json> <project_dir>

Writes a managed block of [mcp_servers.*] tables to <project_dir>/.codex/config.toml,
which Codex loads for trusted projects. Content outside the block is kept.
"""

import json
import os
import re
import sys
from pathlib import Path

BEGIN = "# >>> aipp mcp (generated from .mcp.json; edits are overwritten) >>>"
END = "# <<< aipp mcp <<<"
PLACEHOLDER = "add-value-to-env-vars"
# why: uvx/npx fetch packages on first launch; Codex's default 10s startup timeout kills them.
STDIO_STARTUP_TIMEOUT_SEC = 60
ENV_REF = re.compile(r"\$\{(\w+)(?::-([^}]*))?\}")


def expand(value: str) -> str:
    """Expand ${VAR} and ${VAR:-default} the way Claude Code does for .mcp.json."""
    return ENV_REF.sub(lambda m: os.environ.get(m[1]) or (m[2] or ""), value)


def read_enabled_filter(project: Path) -> tuple[set | None, set]:
    """Return (enabled allowlist or None, disabled set) from the project's Claude settings."""
    enabled, disabled = None, set()
    for name in ("settings.json", "settings.local.json"):
        path = project / ".claude" / name
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("enabledMcpjsonServers"):
            enabled = set(data["enabledMcpjsonServers"])
        disabled |= set(data.get("disabledMcpjsonServers") or [])
    return enabled, disabled


def toml_str(value: str) -> str:
    """TOML basic string; JSON string escapes are valid TOML escapes."""
    return json.dumps(value, ensure_ascii=False)


def toml_map(values: dict) -> str:
    """Inline TOML table of strings."""
    return (
        "{ "
        + ", ".join(f"{toml_str(k)} = {toml_str(v)}" for k, v in values.items())
        + " }"
    )


def render_server(name: str, spec: dict) -> str:
    """Render one Claude server spec as a Codex [mcp_servers.<id>] table."""
    args = [expand(a) for a in spec.get("args", [])]
    env = {k: expand(v) for k, v in spec.get("env", {}).items()}
    headers = {k: expand(v) for k, v in spec.get("headers", {}).items()}
    lines = [f"[mcp_servers.{toml_str(name.replace(':', '_'))}]"]
    if "url" in spec:
        lines.append(f"url = {toml_str(expand(spec['url']))}")
        if headers:
            lines.append(f"http_headers = {toml_map(headers)}")
    else:
        lines.append(f"command = {toml_str(expand(spec['command']))}")
        lines.append(f"args = [{', '.join(toml_str(a) for a in args)}]")
        if env:
            lines.append(f"env = {toml_map(env)}")
        lines.append(f"startup_timeout_sec = {STDIO_STARTUP_TIMEOUT_SEC}")
    if is_unlaunchable(args, headers):
        lines.append("enabled = false")
    return "\n".join(lines)


def is_unlaunchable(args: list, headers: dict) -> bool:
    """True when launch is certain to fail: an unset var in args/headers or a missing file arg.

    invariant: an unset var only in env stays enabled — Claude runs such servers and
    some work degraded (figma-console's desktop bridge needs no token).
    """
    if any(PLACEHOLDER in v for v in [*args, *headers.values()]):
        return True
    return any(a.startswith("/") and not Path(a).exists() for a in args)


def build_block(servers: dict, project: Path) -> str:
    """Render the managed block for every server Claude would load in this project."""
    enabled, disabled = read_enabled_filter(project)
    tables = [
        render_server(name, spec)
        for name, spec in servers.items()
        if name not in disabled and (enabled is None or name in enabled)
    ]
    return "\n\n".join([BEGIN, *tables, END]) + "\n"


def write_config(out: Path, block: str) -> None:
    """Replace the managed block in out (or append it), keeping user content."""
    current = out.read_text(encoding="utf-8") if out.exists() else ""
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", re.DOTALL)
    if pattern.search(current):
        text = pattern.sub(lambda _: block, current)
    else:
        text = (
            current + ("\n" if current and not current.endswith("\n") else "") + block
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    # why: expanded env/headers may carry tokens.
    out.chmod(0o600)


def main() -> None:
    """Convert argv[1] (.mcp.json) into argv[2]/.codex/config.toml."""
    mcp_json, project = Path(sys.argv[1]), Path(sys.argv[2])
    servers = json.loads(mcp_json.read_text(encoding="utf-8")).get("mcpServers", {})
    out = project / ".codex" / "config.toml"
    write_config(out, build_block(servers, project))
    print(f"✓ Codex MCP servers synced to {out}")


if __name__ == "__main__":
    main()
