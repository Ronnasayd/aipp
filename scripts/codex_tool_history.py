#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["textual>=0.80"]
# ///
"""Live tool-call history for Codex sessions, shown as a tabbed TUI.

Codex has no UI plugin API, so this runs in a separate terminal split and
follows the rollout JSONL Codex writes under ~/.codex/sessions/.

Usage: codex_tool_history.py [SESSION.jsonl]   (default: newest session)
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import ClassVar

SESSIONS_DIR = Path.home() / ".codex" / "sessions"
CALL_TYPES = {"function_call", "custom_tool_call"}
OUTPUT_TYPES = {"function_call_output", "custom_tool_call_output"}
SHOWN_ROLES = {"user", "assistant"}
SUMMARY_KEYS = ("cmd", "command", "path", "query", "message", "prompt")
# Codex prints the exit status in one of these forms inside the tool output.
ERROR_PATTERN = re.compile(
    r"Process exited with code [1-9]\d*|Exit code: [1-9]\d*|^Script failed", re.MULTILINE
)
POLL_SECONDS = 1.0
SUMMARY_WIDTH = 120


@dataclass
class ToolCall:
    """One tool call, filled in when its output arrives."""

    call_id: str
    name: str
    summary: str
    started: datetime
    ended: datetime | None = None
    output: str = ""
    error: bool = False

    @property
    def done(self) -> bool:
        return self.ended is not None

    @property
    def duration(self) -> float | None:
        if self.ended is None:
            return None
        return round((self.ended - self.started).total_seconds(), 3)


@dataclass
class Message:
    """A user or assistant chat message."""

    role: str
    text: str
    started: datetime


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def flatten_text(value: object) -> str:
    """Codex outputs are either a string or a list of {type, text} parts."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(part.get("text", "") for part in value if isinstance(part, dict))
    return ""


def summarize_args(payload: dict) -> str:
    raw = payload.get("arguments", payload.get("input", ""))
    try:
        args = json.loads(raw) if isinstance(raw, str) else raw
    except json.JSONDecodeError:
        args = raw
    if isinstance(args, dict):
        key = next((k for k in SUMMARY_KEYS if k in args), None)
        raw = args[key] if key else json.dumps(args, ensure_ascii=False)
    return " ".join(str(raw).split())[:SUMMARY_WIDTH]


class History:
    """Accumulates calls and messages from rollout JSONL lines."""

    def __init__(self) -> None:
        self.calls: list[ToolCall] = []
        self.messages: list[Message] = []
        self._by_id: dict[str, ToolCall] = {}

    def feed(self, lines: list[str]) -> None:
        for raw in lines:
            record = parse_record(raw)
            if record:
                self._handle(record)

    def _handle(self, record: dict) -> None:
        payload = record.get("payload") or {}
        kind = payload.get("type")
        at = parse_time(record["timestamp"])
        if kind in CALL_TYPES:
            self._add_call(payload, at)
        elif kind in OUTPUT_TYPES:
            self._finish_call(payload, at)
        elif kind == "message" and payload.get("role") in SHOWN_ROLES:
            text = flatten_text(payload.get("content")).strip()
            if text:
                self.messages.append(Message(payload["role"], text, at))

    def _add_call(self, payload: dict, at: datetime) -> None:
        call = ToolCall(payload["call_id"], payload.get("name", "?"), summarize_args(payload), at)
        self._by_id[call.call_id] = call
        self.calls.append(call)

    def _finish_call(self, payload: dict, at: datetime) -> None:
        call = self._by_id.get(payload.get("call_id", ""))
        if call is None:
            return
        call.ended = at
        call.output = flatten_text(payload.get("output"))
        call.error = bool(ERROR_PATTERN.search(call.output))

    def all(self) -> list[ToolCall | Message]:
        return sorted([*self.calls, *self.messages], key=lambda r: r.started)

    def errors(self) -> list[ToolCall]:
        return [call for call in self.calls if call.error]


def parse_record(raw: str) -> dict | None:
    try:
        record = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return record if isinstance(record, dict) and "timestamp" in record else None


def find_latest_session() -> Path | None:
    sessions = SESSIONS_DIR.glob("*/*/*/*.jsonl")
    return max(sessions, key=lambda p: p.stat().st_mtime, default=None)


def build_app(session: Path):
    """Build the Textual app (imported lazily so the parser needs no deps)."""
    from rich.markup import escape
    from textual.app import App, ComposeResult
    from textual.containers import VerticalScroll
    from textual.widgets import (
        Collapsible,
        Footer,
        Header,
        Static,
        TabbedContent,
        TabPane,
    )

    tabs = {"calls": "🔧 Tools", "messages": "💬 Mensagens", "all": "🔀 Tudo", "errors": "❌ Erros"}

    def call_title(call: ToolCall) -> str:
        status = "…" if not call.done else ("✗" if call.error else "✓")
        took = f"{call.duration:.1f}s" if call.done else "rodando"
        return f"{status} {call.started:%H:%M:%S} {call.name} · {took} · {call.summary}"

    def render_call(call: ToolCall) -> Collapsible:
        body = Static(escape(call.output or "(sem output ainda)"))
        return Collapsible(body, title=call_title(call), classes="error" if call.error else "")

    def update_call(widget: Collapsible, call: ToolCall) -> None:
        widget.title = call_title(call)
        widget.query_one(Static).update(escape(call.output))
        widget.set_class(call.error, "error")

    def render_message(message: Message) -> Static:
        who = "você" if message.role == "user" else "codex"
        return Static(f"[b]{who}[/b] {message.started:%H:%M:%S}\n{escape(message.text)}", classes="msg")

    def render(record: ToolCall | Message):
        return render_call(record) if isinstance(record, ToolCall) else render_message(record)

    class HistoryApp(App):
        CSS = ".error CollapsibleTitle { color: $error; } .msg { border: round $accent; padding: 0 1; }"
        BINDINGS: ClassVar = [("q", "quit", "Sair"), ("r", "refresh", "Recarregar")]
        TITLE = f"codex tool-history · {session.name}"

        def __init__(self) -> None:
            super().__init__()
            self.history = History()
            self.offset = 0
            # Mounted cards per tab; existing ones are updated, never remounted,
            # so expanded cards stay open while new calls stream in.
            self.mounted: dict[str, int] = {key: 0 for key in tabs}
            self.pending: list[tuple[Collapsible, ToolCall]] = []

        def compose(self) -> ComposeResult:
            yield Header()
            with TabbedContent():
                for key, label in tabs.items():
                    with TabPane(label, id=key):
                        yield VerticalScroll(id=f"list-{key}")
            yield Footer()

        def on_mount(self) -> None:
            self.action_refresh()
            self.set_interval(POLL_SECONDS, self.action_refresh)

        def action_refresh(self) -> None:
            with session.open(encoding="utf-8") as handle:
                handle.seek(self.offset)
                chunk = handle.read()
            # Keep a trailing partial line for the next poll.
            complete, _, _ = chunk.rpartition("\n")
            if not complete:
                return
            self.offset += len(complete.encode("utf-8")) + 1
            self.history.feed(complete.split("\n"))
            self.redraw()

        def redraw(self) -> None:
            lists: dict[str, list] = {
                "calls": self.history.calls,
                "messages": self.history.messages,
                "all": self.history.all(),
                "errors": self.history.errors(),
            }
            self.update_finished_calls()
            for key, records in lists.items():
                self.append_new(key, records)
                self.query_one(TabbedContent).get_tab(key).label = f"{tabs[key]} ({len(records)})"

        def update_finished_calls(self) -> None:
            still_pending = []
            for widget, call in self.pending:
                if call.done:
                    update_call(widget, call)
                else:
                    still_pending.append((widget, call))
            self.pending = still_pending

        def append_new(self, key: str, records: list) -> None:
            # ponytail: assumes records only append in time order; a late
            # out-of-order record lands at the end of the "all" tab.
            fresh = records[self.mounted[key]:]
            if not fresh:
                return
            pane = self.query_one(f"#list-{key}", VerticalScroll)
            at_end = pane.scroll_y >= pane.max_scroll_y
            widgets = [render(record) for record in fresh]
            self.pending += [(w, r) for w, r in zip(widgets, fresh) if isinstance(r, ToolCall) and not r.done]
            pane.mount_all(widgets)
            self.mounted[key] = len(records)
            if at_end:
                pane.call_after_refresh(pane.scroll_end, animate=False)

    return HistoryApp()


def main() -> int:
    session = Path(sys.argv[1]) if len(sys.argv) > 1 else find_latest_session()
    if session is None or not session.exists():
        print(f"Nenhuma sessão do Codex encontrada em {SESSIONS_DIR}", file=sys.stderr)
        return 1
    build_app(session).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
