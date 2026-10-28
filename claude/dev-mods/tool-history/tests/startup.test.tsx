import { expect, test } from "claude-code/testing";
import { BAND, setupHooks } from "./helpers";

test("session starts with the expand button and no pane", async ($, on) => {
  const opens: any[] = [];
  setupHooks(on);
  on("ui.open", (_, e: any) => {
    opens.push(e);
    return { value: { isPlaced: true } };
  });
  on("ui.close", () => ({ value: {} }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  expect(opens.length).toBe(0);

  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  expect((await band.find({ type: "Button", key: "expand" }))?.text).toBe(
    "» Tool-History"
  );

  await band.press({ key: "expand" });
  expect(opens.at(-1)?.id).toBe("tool-history");

  // why: closing via the slash command must leave the reopen button behind,
  // otherwise the band goes empty and the pane is only reachable by typing.
  await $.command.run({ command: "tool-history", args: "" } as never);
  expect((await band.find({ type: "Button", key: "expand" }))?.text).toBe(
    "» Tool-History"
  );
  await band.unmount();
});

test("/clear closes an open pane and leaves the expand button", async ($, on) => {
  const closes: any[] = [];
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }) as never);
  on("ui.close", (_, e: any) => {
    closes.push(e);
    return { value: {} } as never;
  });
  on("session.end", (_, e: any) => ({ sessionId: e.sessionId }) as never);

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  await band.press({ key: "expand" });

  await $.session.end({ reason: "clear", sessionId: "session-1" } as never);
  expect(closes.at(-1)?.id).toBe("tool-history");
  expect((await band.find({ type: "Button", key: "expand" }))?.text).toBe(
    "» Tool-History"
  );
  await band.unmount();
});
