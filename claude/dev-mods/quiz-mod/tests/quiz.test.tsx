import { expect, test } from "claude-code/testing";

const PANE = {
  plugin: "quiz-mod",
  component: "Pane",
  requestId: "quiz",
  props: {
    title: "Quiz",
    isFocused: false,
    bodyColumns: 60,
    placement: "dock",
    scroll: { offset: 0, bodyRows: 20 },
    view: {}
  }
} as const;

const QUESTIONS = [
  { question: "Q1", options: ["a", "b"], correctIndex: 0 },
  { question: "Q2", options: ["c", "d"], correctIndex: 1 }
];

function setup(on: any) {
  on("ui.open", () => ({ value: { isPlaced: true } }) as never);
  on("tool.register", () => ({ value: undefined }) as never);
  on("session.start", (_: any, e: any) => ({ cwd: e.cwd }));
}

// why: typing `$.tool.call` against the full tool union trips TS2589.
const start = ($: any, questions: unknown): Promise<any> =>
  $.tool.call({ tool: "mcp__quiz-mod__quiz_start", questions });
const result = ($: any): Promise<any> =>
  $.tool.call({ tool: "mcp__quiz-mod__quiz_result" });

for (const surface of ["terminal", "desktop"] as const) {
  // why: a double click before the redraw used to read the same `current`
  // twice and record two answers for one question.
  test(`concurrent presses record one answer per question (${surface})`, async ($, on) => {
    setup(on);
    await $.session.start({ cwd: "/", surface, isInteractive: true });
    await start($, QUESTIONS);
    const ui = await $.ui.mount({ ...PANE, surface });

    await Promise.all([ui.press({ key: "opt-0" }), ui.press({ key: "opt-0" })]);

    const r = await result($);
    expect(r.result).toBe("Quiz still in progress: 1/2 answered.");
    await ui.unmount();
  });
}

test("quiz_start refuses a correctIndex outside the options", async ($, on) => {
  setup(on);
  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });

  const r = await start($, [
    { question: "Q", options: ["a"], correctIndex: 3 }
  ]);

  expect(r.deny).toMatch(/correctIndex/);
});

test("quiz_start refuses a question with no options", async ($, on) => {
  setup(on);
  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });

  const r = await start($, [{ question: "Q", options: [], correctIndex: 0 }]);

  expect(r.deny).toMatch(/Question 1/);
});
