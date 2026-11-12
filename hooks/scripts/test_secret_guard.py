"""Regression suite for the UserPromptSubmit secret guard hook."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
import sys
from typing import TYPE_CHECKING

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import secret_guard as hook

if TYPE_CHECKING:
    from collections.abc import Callable

# why: fake credentials only; the pragma keeps the repo's own secret scan
# (protect_files.py) from blocking this fixture file.
LEAKING_PROMPTS = [
    "user:34jh321 pass:7r7161a",  # pragma: allowlist secret
    "usar user:a@b.com; pass=ronnas2022 para testar step3",  # pragma: allowlist secret
    "senha: Hunter2Forte!",  # pragma: allowlist secret
    'export API_KEY="abc123def456ghi789jkl"',  # pragma: allowlist secret
    "mongodb+srv://bob:realPassw0rd@x.mongodb.net/db",  # pragma: allowlist secret
    "token=ghp_abcdefghijklmnopqrstuvwxyz0123456789",  # pragma: allowlist secret
]

SAFE_PROMPTS = [
    "como criar uma migration no prisma ?",
    "verifique se mongodb mcp esta funcionando",
    "mongodb+srv://<user>:<pass>@bb-prd.x.mongodb.net/admin",
    'export APY_KEY="[secret]"',
    "password=$DB_PASSWORD",
    "pass=${PASS}",
    "a senha esta no .env",
    "token: ***",
    "pass:7r7161a  # pragma: allowlist secret",
]


@pytest.fixture(name="run_hook")
def run_hook_fixture(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> Callable[[str], dict | None]:
    """Return a runner that feeds main() a prompt and yields its parsed stdout."""

    def run(prompt: str) -> dict | None:
        payload = {"hook_event_name": "UserPromptSubmit", "prompt": prompt}
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
        with pytest.raises(SystemExit) as exit_info:
            hook.main()
        assert exit_info.value.code == 0
        out = capsys.readouterr().out
        return json.loads(out) if out.strip() else None

    return run


@pytest.mark.parametrize("prompt", LEAKING_PROMPTS)
def test_blocks_prompt_with_credential(
    run_hook: Callable[[str], dict | None], prompt: str
) -> None:
    """Credentials typed in plain text block the prompt before it is sent.

    Args:
        run_hook: runner from run_hook_fixture.
        prompt: prompt text under test.
    """
    out = run_hook(prompt)
    assert out is not None
    assert out["decision"] == "block"
    assert "line 1" in out["reason"]


def test_reason_never_echoes_the_secret(run_hook: Callable[[str], dict | None]) -> None:
    """The block reason names the finding but never repeats the raw value.

    Args:
        run_hook: runner from run_hook_fixture.
    """
    out = run_hook(LEAKING_PROMPTS[1])
    assert out is not None
    assert "ronnas2022" not in out["reason"]


@pytest.mark.parametrize("prompt", SAFE_PROMPTS)
def test_allows_prompt_without_credential(
    run_hook: Callable[[str], dict | None], prompt: str
) -> None:
    """Placeholders, env references, prose and allowlisted lines pass through.

    Args:
        run_hook: runner from run_hook_fixture.
        prompt: prompt text under test.
    """
    assert run_hook(prompt) is None


def test_reports_line_of_multiline_finding(
    run_hook: Callable[[str], dict | None],
) -> None:
    """The reason points at the offending line so the user can edit it.

    Args:
        run_hook: runner from run_hook_fixture.
    """
    out = run_hook("contexto do bug\nlogin com\n" + LEAKING_PROMPTS[2])
    assert out is not None
    assert "line 3" in out["reason"]


def test_invalid_json_is_ignored(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Malformed stdin never blocks the user.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest stdout capture fixture.
    """
    monkeypatch.setattr(sys, "stdin", io.StringIO("not json"))
    with pytest.raises(SystemExit) as exit_info:
        hook.main()
    assert exit_info.value.code == 0
    assert capsys.readouterr().out == ""
