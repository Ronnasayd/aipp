import { mock } from "claude-code/testing";

export const PANE = {
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

export const BAND = {
  plugin: "tool-history",
  component: "AbovePrompt",
  requestId: "above-prompt",
  props: {
    hasSurvey: false,
    isCollapsed: false,
    isWorking: false,
    maxRows: 10,
    bodyColumns: 80,
    scroll: { offset: 0, bodyRows: 10 },
    view: {}
  }
} as const;

export const paneScroll = (offset: number) =>
  ({
    component: "Pane",
    requestId: "tool-history",
    offset,
    contentRows: 100,
    bodyRows: 20
  }) as never;

// why: the mod reads $.clock.now() to time each tool call; nothing beneath
// the plugins answers it unless a test mocks the clock, so every test gets one.
export function setupHooks(on: any, now = 0) {
  const clock = mock.clock(on, { now });
  on("command.register", () => ({ value: { command: "tool-history" } }));
  on("ui.render", { component: "AbovePrompt" }, ($: any, e: any) => {
    const { Text } = $.ui.resolve(e);
    return { type: "Text", children: ["engine"] };
  });
  on("ui.scroll", () => ({}));
  on("session.start", (_: any, e: any) => ({ cwd: e.cwd }));
  on("command.run", () => ({ text: "" }));
  return clock;
}
