import type { Register } from "claude-code";

type Counts = { bash: number; read: number; write: number; mcp: number };
const ZERO: Counts = { bash: 0, read: 0, write: 0, mcp: 0 };
const WRITES = new Set(["Write", "Edit", "MultiEdit", "NotebookEdit"]);

// why: $.ui.status has no position and always draws first in the footer; the
// statusline script (scripts/statusline-command.sh) reads this file by session_id.
// One file per session so parallel sessions don't overwrite each other.
export const statusFile = (sid: string) => `/tmp/claude-tool-stats-${sid}.txt`;

export function bucket(tool: string): keyof Counts | undefined {
  if (tool === "Bash") return "bash";
  if (tool === "Read") return "read";
  if (WRITES.has(tool)) return "write";
  if (tool.startsWith("mcp__")) return "mcp";
  return undefined;
}

export function format(c: Counts): string {
  return `Bash ${c.bash} · Read ${c.read} · Write ${c.write} · MCP ${c.mcp}`;
}

export const register: Register = (on) => {
  let sid = "";
  let counts: Counts = { ...ZERO };
  // why: parallel tool calls can finish fs.write out of order; chaining keeps the file at the latest count.
  let queue: Promise<unknown> = Promise.resolve();

  // why: /clear moves to a new session id without firing session.start, so reset is keyed on the id.
  const current = async (id: string) => {
    if (id !== sid) {
      sid = id;
      counts = { ...ZERO };
    }
    return counts;
  };

  on("session.start", async ($, e, next) => {
    const id = await $.session.id();
    await current(id);
    await $.fs.write(statusFile(id), format(counts)).catch(() => {});
    return next(e);
  });

  on("tool.call", async ($, e, next) => {
    const key = bucket(e.tool);
    if (key) {
      const id = await $.session.id();
      const c = await current(id);
      c[key]++;
      queue = queue.then(() => $.fs.write(statusFile(id), format(c))).catch(() => {});
      await queue;
    }
    return next(e);
  });
};
