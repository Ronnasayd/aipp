import { expect, test } from "claude-code/testing";
import { PANE, setupHooks } from "./helpers";

test("tool calls never get the yellow subagent border", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", () => ({ result: { text: "ok" } }) as never);
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const surface of ["terminal", "desktop"] as const) {
    const pane = await $.ui.mount({ ...PANE, surface });
    await $.tool.call({
      tool: "Bash",
      command: "ls",
      tool_use_id: `main-${surface}`
    } as never);
    await $.tool.call({
      tool: "Bash",
      command: "ls",
      tool_use_id: `sub-${surface}`,
      agentId: "a1"
    } as never);

    const sub = await pane.find({ type: "Box", key: `sub-${surface}` });
    const main = await pane.find({ type: "Box", key: `main-${surface}` });
    // why: yellow marks subagents only in the messages tab; call cards keep status colors.
    expect(sub?.props?.borderColor).not.toBe("yellow");
    expect(sub?.props?.borderColor).toBe(main?.props?.borderColor);
    // why: the agent is named inside each card, not in a "── Main ──" divider.
    expect(main?.text).toBe("Main - $ BASHls");
    expect(sub?.text).toBe("a1 - $ BASHls");
    await pane.unmount();
  }
});
