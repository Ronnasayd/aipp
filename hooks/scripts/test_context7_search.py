"""Regression suite for the context7 search relevance gate."""

# pylint: disable=missing-param-doc,missing-return-doc
# why: test names and docstrings state intent; pytest fixtures need no param docs

from __future__ import annotations

import io
import json
import sys
from typing import Any

import context7_search as hook
import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error
import utils

PROMPT = "como configurar middleware no Next.js 16?"
LIBRARY = {
    "title": "Next.js",
    "project": "/vercel/next.js",
    "description": "React framework",
    "queryBenchmarkScore": 95,
    "stars": 100000,
}


def run_hook(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    decision: dict[str, Any] | None,
) -> tuple[str, list[str]]:
    """Run main() on a prompt payload with search and embeddings faked.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest stdout capture fixture.
        decision: what decide() returns, or None to run the real backend.

    Returns:
        tuple[str, list[str]]: hook stdout and the queries sent to context7.
    """
    searched: list[str] = []

    def fake_fetch(query: str) -> list[dict]:
        searched.append(query)
        return [dict(LIBRARY)]

    monkeypatch.setattr(hook, "fetch_results", fake_fetch)
    monkeypatch.setattr(hook, "encode_via_daemon", lambda *_: None)
    if decision is not None:
        monkeypatch.setattr(utils, "decide", lambda *_: decision)
    payload = json.dumps({"prompt": PROMPT})
    monkeypatch.setattr(sys, "stdin", io.StringIO(payload))
    with pytest.raises(SystemExit):
        hook.main()
    return capsys.readouterr().out, searched


def answer(noul: float) -> dict[str, Any]:
    """Build a decide() result for the hook's relevance question."""
    return {"answers": {hook.QUESTION_ID: {"type": "noul", "noul": noul}}}


def test_relevant_prompt_searches_context7(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A prompt judged worth searching surfaces libraries."""
    out, searched = run_hook(monkeypatch, capsys, answer(0.9))
    assert searched == [PROMPT]
    assert "/vercel/next.js" in out


def test_irrelevant_prompt_skips_search(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A prompt judged not worth searching costs no context7 request."""
    out, searched = run_hook(monkeypatch, capsys, answer(0.1))
    assert out == ""
    assert not searched


def test_backend_error_keeps_searching(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A failing backend leaves today's unconditional search in place."""
    out, searched = run_hook(monkeypatch, capsys, {"error": "down"})
    assert searched == [PROMPT]
    assert "/vercel/next.js" in out


@pytest.mark.parametrize("var", ["CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"])
def test_unconfigured_clef_keeps_searching_without_request(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], var: str
) -> None:
    """Without credentials Clef gets no request and the search still runs."""

    def forbid(*_: object, **__: object) -> None:
        pytest.fail("Clef must not be called without credentials")

    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "acct")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "token")
    monkeypatch.delenv("DECISION_BACKEND", raising=False)
    monkeypatch.delenv(var)
    monkeypatch.setattr("urllib.request.urlopen", forbid)
    out, searched = run_hook(monkeypatch, capsys, None)
    assert searched == [PROMPT]
    assert "/vercel/next.js" in out


def test_repeated_prompt_decides_once(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Replaying a rejected prompt spends no second backend call."""
    calls: list[str] = []

    def record(state: str, _: dict[str, Any]) -> dict[str, Any]:
        calls.append(state)
        return answer(0.1)

    monkeypatch.setattr(utils, "decide", record)
    for _ in range(2):
        out, searched = run_hook(monkeypatch, capsys, None)
        assert out == ""
        assert not searched
    assert calls == [PROMPT]


def test_question_sent_to_backend_is_typed(monkeypatch: pytest.MonkeyPatch) -> None:
    """The prompt is the state and the relevance question is a noul."""
    seen: list[tuple[Any, dict[str, Any]]] = []

    def record(state: Any, questions: dict[str, Any]) -> dict[str, Any]:
        seen.append((state, questions))
        return answer(0.9)

    monkeypatch.setattr(utils, "decide", record)
    assert hook.worth_searching(PROMPT)
    state, questions = seen[0]
    assert state == PROMPT
    assert questions[hook.QUESTION_ID]["type"] == "noul"


def test_decision_and_counts_are_logged_without_prompt(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Logs explain the gate and the filtering, never the prompt text."""
    run_hook(monkeypatch, capsys, answer(0.9))
    assert f"{hook.QUESTION_ID}: noul=0.9" in caplog.text
    assert "1 results, 1 kept" in caplog.text
    assert PROMPT not in caplog.text


def test_cache_hit_is_logged(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """A cached query says so, explaining why no request happened."""
    monkeypatch.setattr(hook, "_read_cache", lambda _: [dict(LIBRARY)])
    assert hook.fetch_results(PROMPT)
    assert "cache hit: 1 results" in caplog.text
