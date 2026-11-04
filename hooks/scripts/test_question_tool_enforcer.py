"""Regression suite for typed decisions and the question tool enforcer."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
import sys
from typing import TYPE_CHECKING, Any
import urllib.error

import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import question_tool_enforcer as enforcer
import utils

if TYPE_CHECKING:
    from urllib.request import Request

TOKEN = "secret-token"
QUESTION = "Quer que eu faça commit agora?"


def clef_reply(noul: float) -> bytes:
    """Build a successful Clef envelope for the enforcer's question.

    Args:
        noul: probability to report.

    Returns:
        bytes: the JSON body Cloudflare would send.
    """
    answer = {"type": "noul", "noul": noul}
    result = {"answers": {enforcer.QUESTION_ID: answer}, "model": "clef"}
    return json.dumps({"success": True, "result": result}).encode()


def serve(monkeypatch: pytest.MonkeyPatch, body: bytes) -> list[Request]:
    """Replace urlopen with a fake that records requests and returns body.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        body: response bytes.

    Returns:
        list[Request]: requests received, filled as the code under test runs.
    """
    seen: list[Request] = []

    def fake_urlopen(request: Request, timeout: float) -> io.BytesIO:
        assert timeout == utils.DECISION_TIMEOUT_SECONDS
        seen.append(request)
        return io.BytesIO(body)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    return seen


def run_hook(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    message: str,
) -> str:
    """Run the hook's main() on a Stop payload.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest stdout capture fixture.
        message: last assistant message.

    Returns:
        str: what the hook printed to stdout.
    """
    payload = {"hook_event_name": "Stop", "last_assistant_message": message}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with pytest.raises(SystemExit):
        enforcer.main()
    return capsys.readouterr().out


@pytest.fixture(autouse=True)
def clef_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Give every test fake credentials and the default backend and model.

    Args:
        monkeypatch: pytest monkeypatch fixture.
    """
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "acct")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", TOKEN)
    monkeypatch.delenv("DECISION_BACKEND", raising=False)
    monkeypatch.delenv("CLEF_MODEL", raising=False)


def test_real_question_injects_rule(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A message the backend judges as asking the user gets the reminder."""
    serve(monkeypatch, clef_reply(0.98))
    out = run_hook(monkeypatch, capsys, QUESTION)
    assert json.loads(out)["hookSpecificOutput"]["additionalContext"]


def test_rhetorical_question_injects_nothing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A '?' that does not ask the user anything stays silent."""
    serve(monkeypatch, clef_reply(0.01))
    assert run_hook(monkeypatch, capsys, "Por que falha? Regex corta cedo.") == ""


def test_message_without_question_mark_skips_backend(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The free '?' check runs first, so plain messages cost no request."""
    seen = serve(monkeypatch, clef_reply(0.98))
    assert run_hook(monkeypatch, capsys, "Tudo pronto.") == ""
    assert not seen


def test_network_failure_keeps_reminder(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unreachable backend falls back to the plain '?' behavior."""

    def refuse(request: Request, timeout: float) -> io.BytesIO:
        raise urllib.error.URLError(f"down: {request.full_url} {timeout}")

    monkeypatch.setattr("urllib.request.urlopen", refuse)
    assert run_hook(monkeypatch, capsys, QUESTION)


@pytest.mark.parametrize("var", ["CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"])
def test_missing_credential_keeps_reminder_without_request(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], var: str
) -> None:
    """Without credentials nothing is sent and the reminder still fires."""
    seen = serve(monkeypatch, clef_reply(0.01))
    monkeypatch.delenv(var)
    assert run_hook(monkeypatch, capsys, QUESTION)
    assert not seen


def test_malformed_answer_keeps_reminder(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A success envelope with no usable answer counts as a failure."""
    serve(monkeypatch, json.dumps({"success": True, "result": {}}).encode())
    assert run_hook(monkeypatch, capsys, QUESTION)


def test_clef_request_follows_api(monkeypatch: pytest.MonkeyPatch) -> None:
    """decide() posts state and questions with the bearer token."""
    seen = serve(monkeypatch, clef_reply(0.5))
    monkeypatch.setenv("CLEF_MODEL", "clef-flash")
    questions = {"q": {"type": "noul", "instructions": "x"}}
    assert "answers" in utils.decide("estado", questions)
    assert seen[0].full_url.endswith("/accounts/acct/ai/run/@cf/cloudflare/clef-flash")
    assert seen[0].get_header("Authorization") == f"Bearer {TOKEN}"
    assert json.loads(seen[0].data) == {  # type: ignore[arg-type]
        "model": "clef-flash",
        "state": "estado",
        "questions": questions,
    }


def test_clef_failure_is_error_without_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """API-reported failures become an error that never leaks the token."""
    errors = [{"message": f"bad token {TOKEN}"}]
    serve(monkeypatch, json.dumps({"success": False, "errors": errors}).encode())
    error = utils.decide("s", {}).get("error", "")
    assert "bad token" in error
    assert TOKEN not in error


def test_long_message_sends_only_the_tail(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Very long messages are clipped to the end, where questions live."""
    seen = serve(monkeypatch, clef_reply(0.98))
    run_hook(monkeypatch, capsys, "x" * enforcer.MAX_STATE_CHARS + QUESTION)
    state = json.loads(seen[0].data)["state"]  # type: ignore[arg-type]
    assert len(state) == enforcer.MAX_STATE_CHARS
    assert state.endswith(QUESTION)


def test_backend_is_swappable(monkeypatch: pytest.MonkeyPatch) -> None:
    """A registered backend serves the same contract with no other change."""

    def local_model(state: Any, questions: dict[str, Any]) -> dict[str, Any]:
        return {"answers": dict.fromkeys(questions, state)}

    monkeypatch.setitem(utils.DECISION_BACKENDS, "local", local_model)
    monkeypatch.setenv("DECISION_BACKEND", "local")
    assert utils.decide("s", {"q": {}}) == {"answers": {"q": "s"}}


def test_unknown_backend_is_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """A misconfigured backend name is reported, not raised."""
    monkeypatch.setenv("DECISION_BACKEND", "nope")
    assert "nope" in utils.decide("s", {}).get("error", "")


def test_raising_backend_becomes_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """decide() contains any backend crash, so hooks never die on it."""
    serve(monkeypatch, b"[]")
    assert "error" in utils.decide("s", {})


@pytest.mark.parametrize(
    ("payload", "reason"),
    [
        ({"stop_hook_active": True}, "stop_hook_active"),
        ({"last_assistant_message": ""}, "no assistant message"),
        ({"last_assistant_message": "Tudo pronto."}, "no '?'"),
        ({"last_assistant_message": "Por que falha?"}, "does not ask the user"),
    ],
)
def test_skip_reason_is_logged(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    payload: dict[str, Any],
    reason: str,
) -> None:
    """Every silent exit leaves its reason in the log."""
    serve(monkeypatch, clef_reply(0.01))
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    with pytest.raises(SystemExit):
        enforcer.main()
    assert reason in caplog.text


def test_unavailable_decision_is_logged(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A fail-open decision names the question and the backend's error."""
    monkeypatch.delenv("CLOUDFLARE_API_TOKEN")
    run_hook(monkeypatch, capsys, QUESTION)
    assert f"{enforcer.QUESTION_ID}: unavailable" in caplog.text
    assert "Missing CLOUDFLARE_ACCOUNT_ID" in caplog.text
