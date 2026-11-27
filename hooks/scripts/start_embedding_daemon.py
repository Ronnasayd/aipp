#!/usr/bin/python3
"""Pre-warm embedding daemon on hook startup."""

import os
import subprocess
import sys
from pathlib import Path

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import get_hooks_logger, get_project_name  # pylint: disable=wrong-import-position

DAEMON_SCRIPT = Path(__file__).parent / "embedding_daemon.py"

logger = get_hooks_logger("StartEmbedding")


def prewarm_embedding_daemon() -> None:
    """Start embedding daemon if socket doesn't exist."""
    sock_path = f"/tmp/embedding-daemon-{get_project_name()}.sock"
    if Path(sock_path).exists():
        return
    logger.debug("Pre-warming embedding daemon")
    # hazard: no `with` — Popen.__exit__ waits on the daemon, blocking the hook
    # forever; Codex waits on SessionStart hooks, so the first turn never starts.
    subprocess.Popen(  # pylint: disable=consider-using-with
        [sys.executable, str(DAEMON_SCRIPT)],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> None:
    """Invoke embedding daemon pre-warming."""
    prewarm_embedding_daemon()
    sys.exit(0)


if __name__ == "__main__":
    main()
