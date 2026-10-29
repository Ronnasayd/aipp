import { expect, test } from "claude-code/testing";
import { PANE, BAND, setupHooks } from "./helpers";

test("all tab interleaves messages and tool calls in arrival order", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", () => ({ result: { text: "ok" } }) as never);
  on("prompt.submit", (_: any, e: any) => ({ text: e.text }) as never);
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  const pane = await $.ui.mount({ ...PANE, surface: "terminal" });
  await $.prompt.submit({ text: "first ask" } as never);
  await $.tool.call({
    tool: "Bash",
    command: "ls",
    tool_use_id: "c1"
  } as never);
  await $.prompt.submit({ text: "second ask" } as never);
  await $.tool.call({
    tool: "Bash",
    command: "pwd",
    tool_use_id: "c2"
  } as never);

  expect((await band.find({ type: "Button", key: "all" }))?.text).toBe("🔀");
  await band.press({ key: "all" });

  const list = await pane.find({ type: "Box", key: "list" });
  expect(list?.props?.gap).toBe(0);
  const text = list?.text ?? "";
  const order = ["first ask", "BASHls", "second ask", "BASHpwd"].map((s) =>
    text.indexOf(s)
  );
  expect(order.every((i) => i >= 0)).toBe(true);
  expect([...order].sort((a, b) => a - b)).toEqual(order);
});

test("all tab stamps text when it streams, not when the step ends", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", () => ({ result: { text: "ok" } }) as never);
  on("agent.list", () => ({ value: [] }) as never);
  // why: tools may run while the step still streams; the text came first.
  on("turn.step", async function* (_: any, _e: any) {
    yield { kind: "text", index: 0, text: "let me look" };
    await $.tool.call({
      tool: "Bash",
      command: "ls",
      tool_use_id: "mid"
    } as never);
    return {
      turnId: "t1",
      index: 0,
      answer: "let me look",
      toolUses: [],
      stopReason: "end_turn",
      usage: null
    };
  } as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  const pane = await $.ui.mount({ ...PANE, surface: "terminal" });
  for await (const _ of $.turn.step({
    turnId: "t1",
    index: 0,
    model: "m",
    messageCount: 1
  } as never)) {
  }
  await band.press({ key: "all" });

  const text = (await pane.find({ type: "Box", key: "list" }))?.text ?? "";
  expect(text.indexOf("let me look")).toBeGreaterThanOrEqual(0);
  expect(text.indexOf("let me look")).toBeLessThan(text.indexOf("BASHls"));
});
