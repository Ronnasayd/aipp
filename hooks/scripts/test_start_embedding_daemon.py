"""Regression: the SessionStart pre-warm hook must not wait on the daemon."""

from __future__ import annotations

import time
from pathlib import Path

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import start_embedding_daemon as hook


def test_returns_without_waiting_for_long_lived_daemon(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A daemon that never exits must not block the hook (Codex hung on it)."""
    sleeper = tmp_path / "daemon.py"
    sleeper.write_text("import time\ntime.sleep(10)\n")
    monkeypatch.setattr(hook, "DAEMON_SCRIPT", sleeper)
    monkeypatch.chdir(tmp_path)

    start = time.monotonic()
    hook.prewarm_embedding_daemon()
    elapsed = time.monotonic() - start

    assert elapsed < 5, f"hook blocked {elapsed:.1f}s waiting on the daemon"


def test_skips_spawn_when_socket_exists(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """An existing socket means a daemon is already up: spawn nothing."""
    monkeypatch.chdir(tmp_path)
    sock = Path(f"/tmp/embedding-daemon-{tmp_path.name}.sock")
    sock.touch()
    spawned: list[object] = []
    monkeypatch.setattr(hook.subprocess, "Popen", lambda *a, **k: spawned.append(a))
    try:
        hook.prewarm_embedding_daemon()
    finally:
        sock.unlink()
    assert not spawned
