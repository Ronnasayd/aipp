import type { PaneOpenArgs } from "claude-code";
import { expect, test } from "claude-code/testing";

const PANE = {
  plugin: "tool-history",
  component: "Pane",
  requestId: "tool-history",
  props: {
    title: "Tool calls",
    isFocused: false,
    bodyColumns: 60,
    placement: "dock",
    scroll: { offset: 0, bodyRows: 20 },
    view: {}
  }
} as const;

const BAND = {
  plugin: "tool-history",
  component: "AbovePrompt",
  requestId: "above-prompt",
  props: {
    hasSurvey: false,
    isWorking: false,
    maxRows: 10,
    bodyColumns: 80,
    scroll: { offset: 0, bodyRows: 10 },
    view: {}
  }
} as const;

test("collapse closes the pane and the band reopens it", async ($, on) => {
  const opens: PaneOpenArgs[] = [];
  const closes: string[] = [];
  on("command.register", () => ({ value: { command: "tool-history" } }));
  on("ui.open", (_, e) => {
    opens.push(e as PaneOpenArgs);
    return { value: { isPlaced: true } };
  });
  on("ui.close", (_, e) => {
    closes.push(e.id);
    return { value: {} } as never;
  });
  on("ui.render", { component: "AbovePrompt" }, ($, e) => {
    const { Text } = $.ui.resolve(e);
    return <Text>engine</Text>;
  });
  on("ui.scroll", () => ({}));
  on("session.start", (_, e) => ({ cwd: e.cwd }));
  on("command.run", () => ({ text: "" }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const surface of ["terminal", "desktop"] as const) {
    const band = await $.ui.mount({ ...BAND, surface });
    expect(await band.find({ type: "Button", key: "expand" })).toBeFalsy();

    const pane = await $.ui.mount({ ...PANE, surface });
    expect((await pane.find({ type: "Button", key: "calls" }))?.text).toBe(
      "🔧"
    );
    expect((await pane.find({ type: "Button", key: "messages" }))?.text).toBe(
      "💬"
    );
    expect((await pane.find({ type: "Button", key: "collapse" }))?.text).toBe(
      "📋"
    );
    const toolbar = await pane.find({ type: "Box", key: "toolbar" });
    expect(toolbar?.props?.borderStyle).toBe("round");
    expect(toolbar?.props?.paddingX).toBe(1);
    expect(await pane.find({ type: "Box", key: "calls-frame" })).toBeFalsy();
    // why: the cards keep their 1-row gap; the toolbar sits flush under them.
    expect((await pane.find({ type: "Box", key: "list" }))?.props?.gap).toBe(1);
    expect(
      (await pane.find({ type: "Box", key: "root" }))?.props?.gap
    ).toBeUndefined();
    await pane.press({ key: "collapse" });
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
