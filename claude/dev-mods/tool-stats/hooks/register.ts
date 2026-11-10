import type { Register } from "claude-code";

type Counts = {
  bash: number;
  read: number;
  write: number;
  search: number;
  web: number;
  mcp: number;
  skill: number;
  tasks: number;
  others: number;
};
const ZERO: Counts = {
  bash: 0,
  read: 0,
  write: 0,
  search: 0,
  web: 0,
  mcp: 0,
  skill: 0,
  tasks: 0,
  others: 0
};
const WRITES = new Set(["Write", "Edit", "MultiEdit", "NotebookEdit"]);
const SEARCHES = new Set(["Grep", "Glob"]);
const WEBS = new Set(["WebFetch", "WebSearch"]);

// why: $.ui.status has no position and always draws first in the footer; the
// statusline script (scripts/statusline-command.sh) reads this file by session_id.
// One file per session so parallel sessions don't overwrite each other.
export const statusFile = (sid: string) => `/tmp/claude-tool-stats-${sid}.txt`;

export function bucket(tool: string): keyof Counts {
  if (tool === "Bash") return "bash";
  if (tool === "Read") return "read";
  if (WRITES.has(tool)) return "write";
  if (SEARCHES.has(tool)) return "search";
  if (WEBS.has(tool)) return "web";
  if (tool.startsWith("mcp__")) return "mcp";
  if (tool === "Skill") return "skill";
  if (tool.startsWith("Task")) return "tasks";
  return "others";
}

export function format(c: Counts): string {
  const total = Object.values(c).reduce((sum, n) => sum + n, 0);
  return `Bash ${c.bash} · Read ${c.read} · Write ${c.write} · Search ${c.search} · Web ${c.web} · MCP ${c.mcp} · Skill ${c.skill} · Tasks ${c.tasks} · Others ${c.others} · Total ${total}`;
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
    const id = await $.session.id();
    const c = await current(id);
    c[key]++;
    queue = queue
      .then(() => $.fs.write(statusFile(id), format(c)))
      .catch(() => {});
    await queue;
    return next(e);
  });
};
