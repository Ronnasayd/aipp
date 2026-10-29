import { atom, read, update } from "claude-code";
import type { EngineInterface, Register } from "claude-code";

import type {
  AgentMessageRecord,
  ToolCallRecord,
  ToolHistoryTab
} from "../types";

const PANE = "tool-history";
const OUTPUT_DIR = "/tmp/tool-history";
const calls = atom({ plugin: "tool-history", key: "calls" } as const, []);
const messages = atom({ plugin: "tool-history", key: "messages" } as const, []);
const isOpen = atom({ plugin: "tool-history", key: "isOpen" } as const, false);
// why: the session starts collapsed so the band shows the reopen button
// without the pane taking dock space until it is clicked.
const isCollapsed = atom(
  { plugin: "tool-history", key: "isCollapsed" } as const,
  true
);
const activeTab = atom(
  { plugin: "tool-history", key: "activeTab" } as const,
  "calls" as ToolHistoryTab
);
// why: full, untruncated results keyed by tool_use_id, so the pane can write
// them out on click without re-running the tool or growing `calls` itself.
const fullResults = atom(
  { plugin: "tool-history", key: "fullResults" } as const,
  {} as Record<string, string>
);
// why: passive auto-scroll (new tool call/message) should not yank the
// window back down once the person has scrolled up to read something.
const isAtBottom = atom(
  { plugin: "tool-history", key: "isAtBottom" } as const,
  true
);

/**
 * Builds a one-line summary of a tool call's arguments for display in the pane.
 * @param e - The tool.call event, carrying `tool` and that tool's own args spread on it.
 * @returns A short string describing the call, or empty string if there is nothing notable to show.
 */
const SUMMARY_CHARS_SHOWN = 300;

function summarize(e: Record<string, unknown>): string {
  const raw =
    (typeof e.command === "string" && e.command) ||
    (typeof e.file_path === "string" && e.file_path) ||
    (typeof e.pattern === "string" && e.pattern) ||
    (typeof e.url === "string" && e.url) ||
    (typeof e.query === "string" && e.query) ||
    (typeof e.description === "string" && e.description) ||
    "";
  if (!raw) return raw;
  const oneLine = raw.replace(/\s+/g, " ").trim();
  return oneLine.length <= SUMMARY_CHARS_SHOWN
    ? oneLine
    : `${oneLine.slice(0, SUMMARY_CHARS_SHOWN)}…`;
}

const RESULT_LINES_SHOWN = 4;
// why: engine's ui.render chokes past ~100k chars in one draw (observed crash)
const RESULT_CHARS_SHOWN = 2000;

/**
 * Resolves a human-readable label for the agent loop a tool call ran in.
 * @param $ - The engine interface, used to list known agents.
 * @param agentId - The loop's agent id, or undefined for the main loop.
 * @returns "Main" for the main loop, or the agent's name/type/id.
 */
async function resolveAgentLabel(
  $: EngineInterface,
  agentId: string | undefined
): Promise<string> {
  if (!agentId) return "Main";
  const agents = await $.agent.list();
  const info = agents.find((a) => a.id === agentId);
  if (!info) return agentId;
  return info.name ?? info.type ?? info.description ?? agentId;
}

// why: unfiltered ANSI/control bytes (e.g. from MCP console-log tools) can
// throw while the pane draws, which makes the engine render it empty.
// eslint-disable-next-line no-control-regex
const ANSI_AND_CONTROL = /\x1b\[[0-9;]*[a-zA-Z]|[\x00-\x08\x0b\x0c\x0e-\x1f]/g;

/**
 * Trims a tool result's text down to the first few lines for pane display.
 * @param text - The raw result text, or undefined when the call produced none.
 * @returns The trimmed text, or undefined when there was nothing to show.
 */
function trimResult(text: string | undefined): string | undefined {
  if (!text) return undefined;
  const clean = text.replace(ANSI_AND_CONTROL, "");
  const lines = clean.split("\n");
  const byLines =
    lines.length <= RESULT_LINES_SHOWN
      ? clean
      : [
          ...lines.slice(0, RESULT_LINES_SHOWN),
          `… +${lines.length - RESULT_LINES_SHOWN} lines`
        ].join("\n");
  if (byLines.length <= RESULT_CHARS_SHOWN) return byLines;
  return `${byLines.slice(0, RESULT_CHARS_SHOWN)}… +${byLines.length - RESULT_CHARS_SHOWN} chars`;
}

// invariant: result written to disk first — OS handler opens a file path, not stdin/stdout
async function openFullResult(
  $: EngineInterface,
  call: ToolCallRecord
): Promise<void> {
  const map = await read($, fullResults);
  const text = map[call.id];
  if (!text) return;
  const path = `${OUTPUT_DIR}/${call.id}.md`;
  const doc = [
    `# ${call.tool}`,
    "",
    "## Command",
    "",
    "```",
    call.summary || "(no arguments)",
    "```",
    "",
    "## Result",
    "",
    "```",
    text,
    "```"
  ].join("\n");
  await $.fs.write(path, doc);
  // why: no platform-detection API is exposed to plugins; try both openers.
  await $.process
    .run(["xdg-open", path])
    .catch(() => $.process.run(["open", path]))
    .catch(() => {});
}

// why: fire-and-forget; with no surface attached the scroll rejects, and an
// unhandled rejection there must not fail the hook that asked for it.
function scrollToEnd($: EngineInterface) {
  $.ui.scroll({ to: "end", in: PANE }).catch(() => {});
}

// why: the dock never narrows below 24 columns, so collapsing closes the pane
// outright and leaves the reopen button in the band above the prompt.
async function setCollapsed($: EngineInterface, collapsed: boolean) {
  await update($, isCollapsed, () => collapsed);
  await update($, isOpen, () => !collapsed);
  if (collapsed) {
    await $.ui.close({ id: PANE });
    return;
  }
  await $.ui.open({ id: PANE, title: "Tool calls" });
  scrollToEnd($);
}

export const register: Register = (on) => {
  on("session.start", async ($, e, next) => {
    await $.command.register({
      name: "tool-history",
      description: "Toggle the tool calls pane for this session"
    });
    scrollToEnd($);

    return next(e);
  });

  // why: `/clear` keeps the process (and these atoms) alive and fires no
  // session.start, so the new session would inherit an open pane.
  on("session.end", async ($, e, next) => {
    if (e.reason === "clear") await setCollapsed($, true);
    return next(e);
  });

  on("command.run", { command: "tool-history" }, async ($) => {
    const open = await read($, isOpen);
    await setCollapsed($, open);
    return {
      text: open ? "Tool calls pane closed." : "Tool calls pane opened."
    };
  });

  on(
    "ui.scroll",
    { component: "Pane", requestId: PANE },
    async ($, e, next) => {
      const maxOffset = Math.max(0, e.contentRows - e.bodyRows);
      await update($, isAtBottom, () => e.offset >= maxOffset);
      return next(e);
    }
  );

  on("tool.call", async ($, e, next) => {
    const record: ToolCallRecord = {
      id: e.tool_use_id,
      tool: e.tool,
      summary: summarize(e as unknown as Record<string, unknown>),
      isDone: false,
      agentId: e.agentId,
      agentLabel: await resolveAgentLabel($, e.agentId),
      at: Date.now()
    };
    await update($, calls, (list) => [...list, record].slice(-200));
    const args = e as unknown as Record<string, unknown>;
    if (e.tool === "Agent" && typeof args.prompt === "string") {
      const delegation: AgentMessageRecord = {
        id: `agent-call-${e.tool_use_id}`,
        kind: "agent",
        text: `**${args.subagent_type ?? "agent"}** — ${args.description ?? ""}\n\n${args.prompt}`,
        agentId: e.agentId,
        agentLabel: record.agentLabel,
        at: record.at
      };
      await update($, messages, (list) => [...list, delegation].slice(-200));
    }
    const ran = await next(e);
    const rawText = "text" in ran ? ran.text : undefined;
    const resultText = trimResult(rawText);
    const isError = "isError" in ran ? ran.isError : undefined;
    let trimmed: ToolCallRecord[] = [];
    await update($, calls, (list) => {
      trimmed = list.map((one) =>
        one.id === record.id
          ? { ...one, isDone: true, resultText, isError }
          : one
      );
      return trimmed;
    });
    if (rawText) {
      const liveIds = new Set(trimmed.map((one) => one.id));
      await update($, fullResults, (map) => {
        const nextMap: Record<string, string> = { [record.id]: rawText };
        for (const [id, text] of Object.entries(map)) {
          if (liveIds.has(id)) nextMap[id] = text;
        }
        return nextMap;
      });
    }

    if ((await read($, isOpen)) && (await read($, isAtBottom))) {
      scrollToEnd($);
    }

    return ran;
  });

  on("prompt.submit", async ($, e, next) => {
    if (!e.isMeta) {
      const record: AgentMessageRecord = {
        id: `user-${Date.now()}-${Math.random().toString(36).slice(2)}`,
        kind: "user",
        text: e.text,
        agentLabel: "Main",
        at: Date.now()
      };
      await update($, messages, (list) => [...list, record].slice(-200));
    }
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    const agentLabel = await resolveAgentLabel($, e.agentId);
    const buffers = new Map<
      number,
      { kind: "text" | "thinking"; text: string; at: number }
    >();

    const stream = next(e);
    for await (const chunk of stream) {
      if (chunk.kind === "text" || chunk.kind === "thinking") {
        const buf = buffers.get(chunk.index);
        if (buf && buf.kind === chunk.kind) buf.text += chunk.text;
        // why: tools run mid-stream; stamping at step end would sort the
        // text after the calls it introduced in the all tab.
        else
          buffers.set(chunk.index, {
            kind: chunk.kind,
            text: chunk.text,
            at: Date.now()
          });
      }
      yield chunk;
    }

    const turnId = e.turnId;
    const newRecords: AgentMessageRecord[] = [...buffers.entries()]
      .sort(([a], [b]) => a - b)
      .filter(([, buf]) => buf.text.trim().length > 0)
      .map(([index, buf]) => ({
        id: `${turnId}-${index}`,
        turnId,
        kind: buf.kind,
        text: buf.text,
        agentId: e.agentId,
        agentLabel,
        at: buf.at
      }));

    if (newRecords.length > 0) {
      await update($, messages, (list) => [...list, ...newRecords].slice(-200));
      if (
        (await read($, isOpen)) &&
        (await read($, activeTab)) !== "calls" &&
        (await read($, isAtBottom))
      ) {
        scrollToEnd($);
      }
    }
  });

  on("ui.render", { component: "AbovePrompt" }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e);
    if (await read($, isCollapsed)) {
      const { Button } = $.ui.resolve(e);
      return (
        <Button key="expand" plain onPress={() => setCollapsed($, false)}>
          » Tool-History
        </Button>
      );
    }
    if (!(await read($, isOpen))) return next(e);

    // why: the pane body scrolls; the band is the only spot that stays
    // visible while the person reads further up, so the toolbar lives here.
    const { Box, Button } = $.ui.resolve(e);
    const tab = await read($, activeTab);
    const atBottom = await read($, isAtBottom);
    const selectTab = (target: ToolHistoryTab) => async () => {
      await update($, activeTab, () => target);
      scrollToEnd($);
    };
    return (
      <Box
        key="toolbar"
        flexDirection="row"
        gap={1}
        borderStyle="round"
        borderColor="subtle"
        paddingX={1}
        alignSelf="flex-start"
      >
        <Button
          key="calls"
          plain
          variant={tab === "calls" ? "primary" : "secondary"}
          onPress={selectTab("calls")}
        >
          🔧
        </Button>
        <Button
          key="messages"
          plain
          variant={tab === "messages" ? "primary" : "secondary"}
          onPress={selectTab("messages")}
        >
          💬
        </Button>
        <Button
          key="all"
          plain
          variant={tab === "all" ? "primary" : "secondary"}
          onPress={selectTab("all")}
        >
          🔀
        </Button>
        <Button key="collapse" plain onPress={() => setCollapsed($, true)}>
          📋
        </Button>
        {!atBottom && (
          <Button key="to-end" plain onPress={() => scrollToEnd($)}>
            ⬇ fim
          </Button>
        )}
      </Box>
    );
  });

  on("ui.render", { component: "Pane", requestId: PANE }, async ($, e) => {
    const { Box, Text, Button, Markdown } = $.ui.resolve(e);
    const tab = await read($, activeTab);
    const msgs = tab === "calls" ? [] : await read($, messages);
    const callList = tab === "messages" ? [] : await read($, calls);
    const results = await read($, fullResults);

    const messageCard = (msg: AgentMessageRecord) => (
      <Box
        key={msg.id}
        flexDirection="column"
        borderStyle="round"
        paddingX={1}
        borderColor={
          msg.kind === "user"
            ? "green"
            : msg.agentId
              ? "yellow"
              : msg.kind === "thinking"
                ? "subtle"
                : "claude"
        }
      >
        <Text bold dimColor>
          {msg.kind === "user" ? "User" : `${msg.agentLabel} - ${msg.kind}`}
        </Text>
        <Markdown text={msg.text} dimColor={msg.kind === "thinking"} />
      </Box>
    );

    const callCard = (call: ToolCallRecord) => {
      const isBash = call.tool === "Bash";
      const icon = call.isDone ? (isBash ? "$" : "✓") : "⚙";
      const borderColor = call.isError
        ? "danger"
        : call.isDone
          ? "subtle"
          : "claude";
      return (
        <Box
          key={call.id}
          flexDirection="column"
          borderStyle="round"
          paddingX={1}
          borderColor={borderColor}
        >
          <Box flexDirection="row" gap={1}>
            <Text bold color={borderColor}>
              {`${call.agentLabel} - ${icon} ${call.tool.toUpperCase()}`}
            </Text>
            {results[call.id] && (
              <Button
                key={`open-${call.id}`}
                plain
                onPress={() => openFullResult($, call)}
              >
                [{call.id.slice(-8)}]
              </Button>
            )}
          </Box>
          {call.summary && <Text color="yellow">{call.summary}</Text>}
          {call.resultText && (
            <Text color="cyan" dimColor={call.isDone}>
              {call.resultText}
            </Text>
          )}
        </Box>
      );
    };

    // invariant: stable sort keeps a step's messages ahead of the tool calls
    // it spawned when both carry the same `at`.
    const items = [
      ...msgs.map((msg) => ({ at: msg.at ?? 0, card: () => messageCard(msg) })),
      ...callList.map((call) => ({
        at: call.at ?? 0,
        card: () => callCard(call)
      }))
    ].sort((a, b) => a.at - b.at);

    const empty =
      tab === "calls"
        ? "No tool calls yet."
        : tab === "messages"
          ? "No agent messages yet."
          : "Nothing yet.";

    return (
      <Box key="root" flexDirection="column">
        <Box key="list" flexDirection="column" gap={0}>
          {items.length === 0 && <Text dimColor>{empty}</Text>}
          {items.map((item) => item.card())}
        </Box>
      </Box>
    );
  });
};
