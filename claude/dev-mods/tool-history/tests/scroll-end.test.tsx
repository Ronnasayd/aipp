import { expect, test } from "claude-code/testing";
import { PANE, BAND, paneScroll, setupHooks } from "./helpers";

test("band shows a jump-to-end button only while scrolled up", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  const pane = await $.ui.mount({
    plugin: "tool-history",
    component: "Pane",
    requestId: "tool-history",
    surface: "terminal",
    props: {
      title: "Tool calls",
      isFocused: false,
      bodyColumns: 60,
      placement: "dock",
      scroll: { offset: 0, bodyRows: 20 },
      view: {}
    }
  });
  const band = await $.ui.mount({ ...BAND, surface: "terminal" });
  expect(await band.find({ type: "Button", key: "to-end" })).toBeFalsy();

  await $.ui.scroll(paneScroll(0));
  const toolbar = await band.find({ type: "Box", key: "toolbar" });
  expect(
    toolbar?.children.some(
      (c) => (c as { props?: { key?: string } }).props?.key === "to-end"
    )
  ).toBe(true);
  expect((await band.find({ type: "Button", key: "to-end" }))?.text).toBe(
    "⬇ fim"
  );

  // why: the kit never resolves `{ to: "end" }` into a window move, so the
  // engine's follow-up scroll to the bottom is raised by hand below.
  await band.press({ key: "to-end" });
  await $.ui.scroll(paneScroll(80));
  expect(await band.find({ type: "Button", key: "to-end" })).toBeFalsy();
  await band.unmount();
  await pane.unmount();
});
