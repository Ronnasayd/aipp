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

export function setupHooks(on: any) {
  on("command.register", () => ({ value: { command: "tool-history" } }));
  on("ui.render", { component: "AbovePrompt" }, ($: any, e: any) => {
    const { Text } = $.ui.resolve(e);
    return { type: "Text", children: ["engine"] };
  });
  on("ui.scroll", () => ({}));
  on("session.start", (_: any, e: any) => ({ cwd: e.cwd }));
  on("command.run", () => ({ text: "" }));
}
