import { expect, test } from "claude-code/testing";
import { PANE, setupHooks } from "./helpers";

test("a finished tool call card shows its result size", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  const sizes: Record<string, number> = {
    b: 512,
    kb: 2_048,
    mb: 3 * 1024 * 1024
  };
  on(
    "tool.call",
    (_: any, e: any) =>
      ({ result: {}, text: "x".repeat(sizes[e.tool_use_id]) }) as never
  );
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);
  const pane = await $.ui.mount({ ...PANE, surface: "terminal" });
  for (const id of Object.keys(sizes)) {
    await $.tool.call({
      tool: "Bash",
      command: "ls",
      tool_use_id: id
    } as never);
  }

  const header = async (id: string) =>
    (await pane.find({ type: "Box", key: id }))?.text?.split("[")[0];
  expect(await header("b")).toBe("Main - $ BASH0ms512B");
  expect(await header("kb")).toBe("Main - $ BASH0ms2.0KB");
  expect(await header("mb")).toBe("Main - $ BASH0ms3.0MB");
  await pane.unmount();
});
