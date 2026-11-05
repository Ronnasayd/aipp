import asyncio
import json

import pytest
from codex_tool_history import History


def line(ts, payload, kind="response_item"):
    return json.dumps({"timestamp": ts, "type": kind, "payload": payload})


CALL = line("2026-09-16T15:08:02.000Z", {
    "type": "function_call", "name": "exec_command", "call_id": "c1",
    "arguments": json.dumps({"cmd": "sed -n 1p AGENTS.md", "workdir": "/x"}),
})
FAIL_OUT = line("2026-09-16T15:08:04.500Z", {
    "type": "function_call_output", "call_id": "c1",
    "output": "Chunk ID: a\nProcess exited with code 1\nOutput:\nsed: no such file\n",
})
CUSTOM = line("2026-09-16T15:08:05.000Z", {
    "type": "custom_tool_call", "name": "exec", "call_id": "c2", "input": "text(1)",
})
CUSTOM_OUT = line("2026-09-16T15:08:05.300Z", {
    "type": "custom_tool_call_output", "call_id": "c2",
    "output": [{"type": "input_text", "text": "Script completed\nWall time 0.3 seconds"}],
})
MSG = line("2026-09-16T15:08:03.000Z", {
    "type": "message", "role": "assistant",
    "content": [{"type": "output_text", "text": "olá"}],
})
DEV_MSG = line("2026-09-16T15:08:01.000Z", {
    "type": "message", "role": "developer",
    "content": [{"type": "input_text", "text": "system stuff"}],
})


def test_pairs_call_with_output_and_flags_error():
    h = History()
    h.feed([CALL, FAIL_OUT])
    (c,) = h.calls
    assert c.name == "exec_command"
    assert c.summary == "sed -n 1p AGENTS.md"
    assert c.duration == 2.5
    assert c.error is True
    assert "no such file" in c.output


def test_custom_call_success_and_pending_until_output():
    h = History()
    h.feed([CUSTOM])
    assert h.calls[0].done is False and h.calls[0].duration is None
    h.feed([CUSTOM_OUT])
    assert h.calls[0].error is False and h.calls[0].duration == 0.3


def test_script_failed_and_exit_code_are_errors():
    for text in ("Script failed\nboom", "Exit code: 2\nOutput:"):
        h = History()
        h.feed([CUSTOM, line("2026-09-16T15:08:06.000Z", {
            "type": "custom_tool_call_output", "call_id": "c2", "output": text})])
        assert h.calls[0].error is True, text


def test_messages_skip_developer_and_all_is_time_sorted():
    h = History()
    h.feed([DEV_MSG, CALL, MSG, FAIL_OUT, "not json", ""])
    assert [m.text for m in h.messages] == ["olá"]
    assert [type(r).__name__ for r in h.all()] == ["ToolCall", "Message"]
    assert [c.call_id for c in h.errors()] == ["c1"]


def test_tui_tabs_count_and_update_pending_call(tmp_path):
    pytest.importorskip("textual")
    from codex_tool_history import build_app
    from textual.widgets import Collapsible, TabbedContent

    session = tmp_path / "rollout.jsonl"
    session.write_text(f"{CALL}\n{MSG}\n")
    asyncio.run(check_tui(build_app(session), session, Collapsible, TabbedContent))


async def check_tui(app, session, Collapsible, TabbedContent):
    async with app.run_test() as pilot:
        tabs = app.query_one(TabbedContent)
        assert "(1)" in str(tabs.get_tab("calls").label)
        card = app.query_one("#list-calls").query_one(Collapsible)
        card.collapsed = False
        assert "rodando" in str(card.title)

        with session.open("a") as handle:
            handle.write(FAIL_OUT + "\n")
        app.action_refresh()
        await pilot.pause()
        same = app.query_one("#list-calls").query_one(Collapsible)
        assert same is card and card.collapsed is False
        assert "✗" in str(card.title) and "2.5s" in str(card.title)
        assert "(1)" in str(tabs.get_tab("errors").label)
        assert "(2)" in str(tabs.get_tab("all").label)
