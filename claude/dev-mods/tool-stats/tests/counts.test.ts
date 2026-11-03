import { expect, test } from "claude-code/testing";

test("counts tools per session, resets on new session id, mirrors to per-session statusline file", async ($, on) => {
  let sid = "s1";
  on("session.id", () => ({ value: sid }));
  const files: Record<string, string> = {};
  let statusCalls = 0;
  on("ui.status", () => (statusCalls++, { value: undefined }));
  on("fs.write", (_, e) => ((files[e.path] = e.text), { value: undefined }));
  on("session.start", (_, e) => ({ cwd: e.cwd }));
  on("tool.call", () => ({ result: {} }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  expect(files["/tmp/claude-tool-stats-s1.txt"]).toBe(
    "Bash 0 · Read 0 · Write 0 · MCP 0 · Skill 0 · Others 0"
  );

  await Promise.all([
    $.tool.call({ tool: "Bash", command: "ls" }),
    $.tool.call({ tool: "Bash", command: "pwd" }),
    $.tool.call({ tool: "Read", file_path: "/a" }),
    $.tool.call({
      tool: "Edit",
      file_path: "/a",
      old_string: "x",
      new_string: "y"
    }),
    $.tool.call({ tool: "Glob", pattern: "*" } as never),
    $.tool.call({ tool: "mcp__x__y" } as never),
    $.tool.call({ tool: "Skill" } as never)
  ]);
  expect(files["/tmp/claude-tool-stats-s1.txt"]).toBe(
    "Bash 2 · Read 1 · Write 1 · MCP 1 · Skill 1 · Others 1"
  );

  // why: /clear switches session id without firing session.start; counts must still restart.
  sid = "s2";
  await $.tool.call({ tool: "Bash", command: "ls" });
  expect(files["/tmp/claude-tool-stats-s2.txt"]).toBe(
    "Bash 1 · Read 0 · Write 0 · MCP 0 · Skill 0 · Others 0"
  );
  expect(files["/tmp/claude-tool-stats-s1.txt"]).toBe(
    "Bash 2 · Read 1 · Write 1 · MCP 1 · Skill 1 · Others 1"
  );
  expect(statusCalls).toBe(0);
});
