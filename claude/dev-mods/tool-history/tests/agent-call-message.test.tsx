import { expect, test } from "claude-code/testing";
import { PANE, BAND, setupHooks } from "./helpers";

test("an Agent tool call shows its prompt in the messages tab", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  on("tool.call", () => ({ result: { text: "done" } }) as never);
  on("agent.list", () => ({ value: [] }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  const pane = await $.ui.mount({ ...PANE, surface: "terminal" });
  await $.tool.call({
    tool: "Agent",
    description: "Simple check",
    prompt: "List the files",
    subagent_type: "general-purpose",
    tool_use_id: "agent-1"
  } as never);
  await band.press({ key: "messages" });

  const card = await pane.find({ type: "Box", key: "agent-call-agent-1" });
  expect(card?.text).toContain("Main - agent");
  expect(card?.text).toContain("general-purpose");
  expect(card?.text).toContain("Simple check");
  expect(card?.text).toContain("List the files");
  expect(card?.props?.borderColor).not.toBe("yellow");
});
