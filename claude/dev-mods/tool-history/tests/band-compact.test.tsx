import { expect, test } from "claude-code/testing";
import { BAND, setupHooks } from "./helpers";

// why: a tall status line (many subagents) shrinks the band's slot; the
// bordered toolbar needs 3 rows, so under that it scrolled and broke apart.
test("toolbar drops its border when the band has under 3 rows", async ($, on) => {
  setupHooks(on);
  on("ui.open", () => ({ value: { isPlaced: true } }));
  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  await $.command.run({ command: "tool-history", args: "" } as never);

  for (const [maxRows, border] of [
    [2, undefined],
    [3, "round"]
  ] as const) {
    const band = await $.ui.mount({
      ...BAND,
      surface: "terminal",
      props: {
        ...BAND.props,
        maxRows,
        scroll: { offset: 0, bodyRows: maxRows }
      }
    });
    const toolbar = await band.find({ type: "Box", key: "toolbar" });
    expect(toolbar?.props?.borderStyle).toBe(border);
    expect((await band.find({ type: "Button", key: "errors" }))?.text).toBe(
      "🚨"
    );
    await band.unmount();
  }
});
