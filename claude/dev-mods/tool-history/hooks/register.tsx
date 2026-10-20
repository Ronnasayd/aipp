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

/**
 * Builds a one-line summary of a tool call's arguments for display in the pane.
 * @param e - The tool.call event, carrying `tool` and that tool's own args spread on it.
 * @returns A short string describing the call, or empty string if there is nothing notable to show.
 */
function summarize(e: Record<string, unknown>): string {
  if (typeof e.command === "string") return e.command;
  if (typeof e.file_path === "string") return e.file_path;
  if (typeof e.pattern === "string") return e.pattern;
  if (typeof e.url === "string") return e.url;
  if (typeof e.query === "string") return e.query;
  if (typeof e.description === "string") return e.description;
  return "";
}

const RESULT_LINES_SHOWN = 4;

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
  if (lines.length <= RESULT_LINES_SHOWN) return clean;
  const hidden = lines.length - RESULT_LINES_SHOWN;
  return [...lines.slice(0, RESULT_LINES_SHOWN), `… +${hidden} lines`].join(
    "\n"
  );
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

export const register: Register = (on) => {
  on("session.start", async ($, e, next) => {
    await $.command.register({
      name: "tool-history",
      description: "Toggle the tool calls pane for this session"
    });
    void $.ui.scroll({ to: "end", in: PANE });

    return next(e);
  });

  on("command.run", { command: "tool-history" }, async ($) => {
    const open = await read($, isOpen);
    if (open) {
      await $.ui.close({ id: PANE });
      await update($, isOpen, () => false);
      return { text: "Tool calls pane closed." };
    }

    await $.ui.open({ id: PANE, title: "Tool calls" });
    await update($, isOpen, () => true);
    void $.ui.scroll({ to: "end", in: PANE });
    return { text: "Tool calls pane opened." };
  });

  on("tool.call", async ($, e, next) => {
    const record: ToolCallRecord = {
      id: e.tool_use_id,
      tool: e.tool,
      summary: summarize(e as unknown as Record<string, unknown>),
      isDone: false,
      agentId: e.agentId,
      agentLabel: await resolveAgentLabel($, e.agentId)
    };
    await update($, calls, (list) => [...list, record].slice(-200));
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

    if (await read($, isOpen)) void $.ui.scroll({ to: "end", in: PANE });

    return ran;
  });

  on("prompt.submit", async ($, e, next) => {
    if (!e.isMeta) {
      const record: AgentMessageRecord = {
        id: `user-${Date.now()}-${Math.random().toString(36).slice(2)}`,
        kind: "user",
        text: e.text,
        agentLabel: "Main"
      };
      await update($, messages, (list) => [...list, record].slice(-200));
    }
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    const agentLabel = await resolveAgentLabel($, e.agentId);
    const buffers = new Map<
      number,
      { kind: "text" | "thinking"; text: string }
    >();

    const stream = next(e);
    for await (const chunk of stream) {
      if (chunk.kind === "text" || chunk.kind === "thinking") {
        const buf = buffers.get(chunk.index);
        if (buf && buf.kind === chunk.kind) buf.text += chunk.text;
        else buffers.set(chunk.index, { kind: chunk.kind, text: chunk.text });
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
        agentLabel
      }));

    if (newRecords.length > 0) {
      await update($, messages, (list) => [...list, ...newRecords].slice(-200));
      if (
        (await read($, isOpen)) &&
        (await read($, activeTab)) === "messages"
      ) {
        void $.ui.scroll({ to: "end", in: PANE });
      }
    }
  });

  on("ui.render", { component: "Pane", requestId: PANE }, async ($, e) => {
    const { Box, Text, Button, Markdown } = $.ui.resolve(e);
    const tab = await read($, activeTab);

    const selectTab = (next: ToolHistoryTab) => async () => {
      await update($, activeTab, () => next);
      void $.ui.scroll({ to: "end", in: PANE });
    };

    const header = (
      <Box flexDirection="row" gap={1}>
        <Button
          plain
          hotkey="1"
          variant={tab === "calls" ? "primary" : "secondary"}
          onPress={selectTab("calls")}
        >
          Tool Calls
        </Button>
        <Button
          plain
          hotkey="2"
          variant={tab === "messages" ? "primary" : "secondary"}
          onPress={selectTab("messages")}
        >
          Agent Messages
        </Button>
      </Box>
    );

    if (tab === "messages") {
      const list = await read($, messages);
      const groups: { agentLabel: string; messages: AgentMessageRecord[] }[] =
        [];
      for (const msg of list) {
        const lastGroup = groups[groups.length - 1];
        if (lastGroup && lastGroup.agentLabel === msg.agentLabel) {
          lastGroup.messages.push(msg);
        } else {
          groups.push({ agentLabel: msg.agentLabel, messages: [msg] });
        }
      }
      return (
        <Box flexDirection="column" gap={1}>
          {list.length === 0 && <Text dimColor>No agent messages yet.</Text>}
          {groups.map((group, groupIndex) => (
            <Box
              key={`${group.agentLabel}-${groupIndex}`}
              flexDirection="column"
            >
              <Text bold dimColor>
                ── {group.agentLabel} ──
              </Text>
              {group.messages.map((msg) => (
                <Box
                  key={msg.id}
                  flexDirection="column"
                  borderStyle="round"
                  paddingX={1}
                  borderColor={
                    msg.kind === "user"
                      ? "green"
                      : msg.kind === "thinking"
                        ? "subtle"
                        : "claude"
                  }
                >
                  <Text bold dimColor>
                    {msg.kind === "user" ? "User" : msg.kind}
                  </Text>
                  <Markdown
                    text={msg.text}
                    dimColor={msg.kind === "thinking"}
                  />
                </Box>
              ))}
            </Box>
          ))}
          {header}
        </Box>
      );
    }

    const list = await read($, calls);
    const results = await read($, fullResults);
    const groups: { agentLabel: string; calls: ToolCallRecord[] }[] = [];
    for (const call of list) {
      const lastGroup = groups[groups.length - 1];
      if (lastGroup && lastGroup.agentLabel === call.agentLabel) {
        lastGroup.calls.push(call);
      } else {
        groups.push({ agentLabel: call.agentLabel, calls: [call] });
      }
    }

    return (
      <Box flexDirection="column" gap={1}>
        {list.length === 0 && <Text dimColor>No tool calls yet.</Text>}
        {groups.map((group, groupIndex) => (
          <Box key={`${group.agentLabel}-${groupIndex}`} flexDirection="column">
            <Text bold dimColor>
              ── {group.agentLabel} ──
            </Text>
            {group.calls.map((call) => {
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
                      {icon} {call.tool.toUpperCase()}
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
            })}
          </Box>
        ))}
        {header}
      </Box>
    );
  });
};
