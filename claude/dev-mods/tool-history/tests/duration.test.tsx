import { expect, test } from "claude-code/testing";
import { PANE, setupHooks } from "./helpers";

test("a finished tool call card shows how long it ran", async ($, on) => {
  const clock = setupHooks(on, 1_000);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", async (_: any, e: any) => {
    await clock.advance(e.tool_use_id === "slow" ? 2_300 : 40);
    return { result: { text: "ok" } } as never;
  });
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const surface of ["terminal", "desktop"] as const) {
    const pane = await $.ui.mount({ ...PANE, surface });
    await $.tool.call({ tool: "Bash", command: "ls", tool_use_id: "fast" } as never);
    await $.tool.call({ tool: "Bash", command: "make", tool_use_id: "slow" } as never);

    expect((await pane.find({ type: "Box", key: "fast" }))?.text).toBe("Main - $ BASH40msls");
    expect((await pane.find({ type: "Box", key: "slow" }))?.text).toBe("Main - $ BASH2.3smake");
    await pane.unmount();
  }
});
