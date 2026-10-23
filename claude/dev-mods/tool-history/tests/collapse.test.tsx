import { expect, test } from "claude-code/testing";
import { PANE, BAND, setupHooks } from "./helpers";

test("collapse closes the pane and the band reopens it", async ($, on) => {
  const opens: any[] = [];
  const closes: string[] = [];
  setupHooks(on);
  on("ui.open", (_, e: any) => {
    opens.push(e);
    return { value: { isPlaced: true } };
  });
  on("ui.close", (_, e: any) => {
    closes.push(e.id);
    return { value: {} } as never;
  });

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const surface of ["terminal", "desktop"] as const) {
    const band = await $.ui.mount({ ...BAND, surface });
    expect(await band.find({ type: "Button", key: "expand" })).toBeFalsy();

    const pane = await $.ui.mount({ ...PANE, surface });
    // why: the toolbar lives in the band so it stays put while the pane scrolls.
    expect(await pane.find({ type: "Box", key: "toolbar" })).toBeFalsy();
    expect((await band.find({ type: "Button", key: "calls" }))?.text).toBe(
      "🔧"
    );
    expect((await band.find({ type: "Button", key: "messages" }))?.text).toBe(
      "💬"
    );
    expect((await band.find({ type: "Button", key: "collapse" }))?.text).toBe(
      "📋"
    );
    const toolbar = await band.find({ type: "Box", key: "toolbar" });
    expect(toolbar?.props?.borderStyle).toBe("round");
    expect(toolbar?.props?.paddingX).toBe(1);
    expect(await pane.find({ type: "Box", key: "calls-frame" })).toBeFalsy();
    expect((await pane.find({ type: "Box", key: "list" }))?.props?.gap).toBe(1);

    await band.press({ key: "messages" });
    expect(
      (await band.find({ type: "Button", key: "messages" }))?.props?.variant
    ).toBe("primary");
    await band.press({ key: "calls" });

    await band.press({ key: "collapse" });
    await pane.unmount();
    expect(closes.at(-1)).toBe("tool-history");
    expect((await band.find({ type: "Button", key: "expand" }))?.text).toBe(
      "» Tool-History"
    );

    const opensBefore = opens.length;
    await band.press({ key: "expand" });
    expect(opens.length).toBe(opensBefore + 1);
    expect(opens.at(-1)?.id).toBe("tool-history");
    expect(await band.find({ type: "Button", key: "expand" })).toBeFalsy();
    await band.unmount();
  }
});
