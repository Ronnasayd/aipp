import { expect, test } from "claude-code/testing";
import { PANE, BAND, setupHooks } from "./helpers";

test("errors tab lists only the tool calls that failed", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on(
    "tool.call",
    (_: any, e: any) =>
      (e.tool_use_id === "bad"
        ? { result: {}, text: "boom", isError: true }
        : { result: { text: "ok" } }) as never
  );
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const surface of ["terminal", "desktop"] as const) {
    const band = await $.ui.mount({ ...BAND, surface });
    const pane = await $.ui.mount({ ...PANE, surface });
    await $.tool.call({
      tool: "Bash",
      command: "ls",
      tool_use_id: "good"
    } as never);
    await $.tool.call({
      tool: "Bash",
      command: "rm x",
      tool_use_id: "bad"
    } as never);

    expect((await band.find({ type: "Button", key: "errors" }))?.text).toBe(
      "🚨"
    );
    await band.press({ key: "errors" });

    expect(await pane.find({ type: "Box", key: "bad" })).toBeTruthy();
    expect(await pane.find({ type: "Box", key: "good" })).toBeFalsy();
    await band.unmount();
    await pane.unmount();
  }
});

test("errors tab says so when nothing failed", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", () => ({ result: { text: "ok" } }) as never);
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  const pane = await $.ui.mount({ ...PANE, surface: "terminal" });
  await $.tool.call({
    tool: "Bash",
    command: "ls",
    tool_use_id: "good"
  } as never);
  await band.press({ key: "errors" });

  const text = (await pane.find({ type: "Box", key: "list" }))?.text ?? "";
  expect(text).toBe("No failed tool calls.");
});
