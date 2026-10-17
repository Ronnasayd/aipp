import { atom, read, update } from "claude-code";
import type { EngineInterface, Register } from "claude-code";

import type { ToolCallRecord } from "../types";

const PANE = "tool-history";
const calls = atom({ plugin: "tool-history", key: "calls" } as const, []);
const isOpen = atom({ plugin: "tool-history", key: "isOpen" } as const, false);

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
    const resultText = trimResult("text" in ran ? ran.text : undefined);
    const isError = "isError" in ran ? ran.isError : undefined;
    await update($, calls, (list) =>
      list.map((one) =>
        one.id === record.id
          ? { ...one, isDone: true, resultText, isError }
          : one
      )
    );

    if (await read($, isOpen)) void $.ui.scroll({ to: "end", in: PANE });

    return ran;
  });

  on("ui.render", { component: "Pane", requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e);
    const list = await read($, calls);

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
          <Box key={groupIndex} flexDirection="column">
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
                  <Text bold color={borderColor}>
                    {icon} {call.tool.toUpperCase()}
                  </Text>
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
      </Box>
    );
  });
};
