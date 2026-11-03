import { expect, mock, test } from "claude-code/testing";
import { BAND, setupHooks } from "./helpers";

// why: with router wrapping AbovePrompt, two band renders settle out of order
// and the terminal keeps handles of the stale one ("no Button of tool-history
// is held under handle"); nothing redraws the band mid-turn to heal it.
test("a band press asks for one more redraw once the renders settled", async ($, on) => {
  setupHooks(on);
  const clock = mock.clock(on);
  const invalidated: string[] = [];
  on("ui.open", () => ({ value: { isPlaced: true } }) as never);
  on("ui.invalidate", (_: any, e: any) => {
    invalidated.push(e.event);
    return { value: undefined } as never;
  });

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });
  const band = await $.ui.mount({ ...BAND, surface: "terminal" });

  await band.press({ key: "expand" });
  expect(invalidated).toEqual([]);
  await clock.advance(150);
  expect(invalidated).toEqual(["ui.render"]);

  await band.press({ key: "messages" });
  await clock.advance(150);
  expect(invalidated).toEqual(["ui.render", "ui.render"]);
  await band.unmount();
});
