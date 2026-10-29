import { expect, test } from "claude-code/testing";
import { PANE, setupHooks } from "./helpers";

test("subagent tool calls get a yellow border, main ones do not", async ($, on) => {
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
    expect(sub?.props?.borderColor).toBe("yellow");
    expect(main?.props?.borderColor).not.toBe("yellow");
    // why: the agent is named inside each card, not in a "── Main ──" divider.
    expect(main?.text).toBe("Main - $ BASHls");
    expect(sub?.text).toBe("a1 - $ BASHls");
    await pane.unmount();
  }
});
