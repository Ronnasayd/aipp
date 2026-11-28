#!/usr/bin/python3
"""UserPromptSubmit hook.

Pins the turn's starting commit SHA to a per-session file, so the Stop-time
lint gate can diff against a fixed point even if the agent commits mid-turn
(diffing live HEAD against itself always shows nothing after a commit).
Skipped when the tlc harness already records it for this session; read it
back with utils.get_turn_base_sha.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    get_by_key,
    get_hooks_logger,
    get_session_id_short,
    project_dir,
    run_command_cwd,
    tlc_session_path,
    tmp_project_dir,
)

LOG = get_hooks_logger("TurnBaseSha")


def _pin_head(project_root: str, session_id: str) -> None:
    """Write HEAD's SHA to this session's turn-base-sha pin file."""
    result = run_command_cwd("git rev-parse HEAD", cwd=project_root)
    if not (result["success"] and result["output"]):
        LOG.debug("git rev-parse HEAD failed, skipping SHA pin: %s", result)
        return
    sha_path = (
        tmp_project_dir(project_root, "turn-base-sha")
        / f"{get_session_id_short(session_id)}.txt"
    )
    sha_path.write_text(result["output"], encoding="utf-8")
    LOG.debug("Pinned turn-base SHA %s to %s", result["output"], sha_path)


def main() -> None:
    """Read the hook payload from stdin, pin HEAD's SHA, pass stdin through."""
    stdin_data = sys.stdin.read()

    try:
        payload = json.loads(stdin_data)
    except (json.JSONDecodeError, EOFError) as e:
        LOG.debug("Failed to parse JSON: %s", e)
        sys.stdout.write(stdin_data)
        sys.exit(0)

    project_root = project_dir(payload)
    session_id = get_by_key(payload, "session_id") or ""

    if tlc_session_path(project_root, session_id).exists():
        LOG.debug("tlc session file present, skipping own SHA pin")
    else:
        _pin_head(project_root, session_id)

    loop_count_path = (
        tmp_project_dir(project_root, "stop-loop-count")
        / f"{get_session_id_short(session_id)}.txt"
    )
    loop_count_path.write_text("0", encoding="utf-8")

    sys.stdout.write(stdin_data)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pylint: disable=broad-exception-caught
        LOG.debug("Error: %s", exc)
        sys.exit(0)
