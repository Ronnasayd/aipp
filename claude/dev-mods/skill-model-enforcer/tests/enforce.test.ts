import { expect, test, type TestBody } from "claude-code/testing";

const SESSION_MODEL = "claude-opus-5-5";
const SESSION_EFFORT = "high";

type Harness = Parameters<TestBody>;

function engine($: Harness[0], on: Harness[1]) {
  const served: string[] = [];
  const efforts: unknown[] = [];
  const files: Record<string, string> = {};
  on("session.id", () => ({ value: "s1" }));
  on("session.model", () => ({ value: SESSION_MODEL }));
  on("fs.write", (_, e) => ((files[e.path] = e.text), { value: undefined }));
  on("skill.prompt", (_$, e) => ({ text: e.text }));
  on("turn.complete", () => ({ text: "" }));
  on("turn.step", async function* (_$, e) {
    served.push(e.model);
    efforts.push(e.effort);
    return {
      turnId: e.turnId,
      index: e.index,
      answer: "ok",
      toolUses: [],
      stopReason: "end_turn"
    } as never;
  });
  const skill = (frontmatter: Record<string, string | number>) =>
    $.skill.prompt({ skill: "probe", text: "go", frontmatter });
  const step = async (
    index: number,
    agentId?: string,
    effort: typeof SESSION_EFFORT | number = SESSION_EFFORT
  ) => {
    const stream = $.turn.step({
      turnId: "t1",
      index,
      model: SESSION_MODEL,
      effort,
      messageCount: 1,
      ...(agentId ? { agentId } : {})
    });
    for await (const _ of stream) void _;
  };
  const complete = (agentId?: string) =>
    $.turn.complete({
      turnId: "t1",
      answer: "ok",
      durationMs: 1,
      reason: "answer",
      ...(agentId ? { agentId } : {})
    } as never);
  return { served, efforts, files, skill, step, complete };
}

const SERVED_FILE = "/tmp/claude-served-s1.json";

test("the served file follows the main loop's model and effort", async ($, on) => {
  const { files, skill, step, complete } = engine($, on);
  const served = () => JSON.parse(files[SERVED_FILE]!);

  await step(0);
  expect(served()).toEqual({ model: SESSION_MODEL, effort: SESSION_EFFORT });

  await skill({ model: "haiku", effort: "low" });
  await step(1);
  expect(served()).toEqual({ model: "haiku", effort: "low" });

  await complete();
  expect(served()).toEqual({ model: SESSION_MODEL });
});

test("a subagent's steps and completion leave the served file alone", async ($, on) => {
  const { files, skill, step, complete } = engine($, on);

  await skill({ model: "haiku", effort: "low" });
  await step(0);
  await step(1, "agent-1");
  await complete("agent-1");

  expect(JSON.parse(files[SERVED_FILE]!)).toEqual({
    model: "haiku",
    effort: "low"
  });
});

test("an inline skill's model serves every later step of its turn", async ($, on) => {
  const { served, skill, step } = engine($, on);

  await step(0);
  await skill({ model: "haiku" });
  await step(1);
  await step(2);

  expect(served).toEqual([SESSION_MODEL, "haiku", "haiku"]);
});

test("the session model resumes after the turn completes", async ($, on) => {
  const { served, skill, step, complete } = engine($, on);

  await skill({ model: "haiku" });
  await step(0);
  await complete();
  await step(0);

  expect(served).toEqual(["haiku", SESSION_MODEL]);
});

test("a subagent finishing mid-turn does not end the override", async ($, on) => {
  const { served, skill, step, complete } = engine($, on);

  await skill({ model: "haiku" });
  await complete("agent-1");
  await step(1);

  expect(served).toEqual(["haiku"]);
});

test("a subagent's own steps keep their model", async ($, on) => {
  const { served, skill, step } = engine($, on);

  await skill({ model: "haiku" });
  await step(0, "agent-1");

  expect(served).toEqual([SESSION_MODEL]);
});

test("a forked skill is left to the engine", async ($, on) => {
  const { served, skill, step } = engine($, on);

  await skill({ model: "haiku", context: "fork" });
  await step(0);

  expect(served).toEqual([SESSION_MODEL]);
});

test("inherit and a skill without model change nothing", async ($, on) => {
  const { served, skill, step } = engine($, on);

  await skill({ model: "inherit" });
  await step(0);
  await skill({});
  await step(1);

  expect(served).toEqual([SESSION_MODEL, SESSION_MODEL]);
});

test("an inline skill's effort serves every later step of its turn", async ($, on) => {
  const { efforts, served, skill, step } = engine($, on);

  await step(0);
  await skill({ effort: "low" });
  await step(1);
  await step(2);

  expect(efforts).toEqual([SESSION_EFFORT, "low", "low"]);
  expect(served).toEqual([SESSION_MODEL, SESSION_MODEL, SESSION_MODEL]);
});

test("a numeric frontmatter effort changes nothing and keeps the model override", async ($, on) => {
  const { efforts, served, skill, step } = engine($, on);

  await skill({ model: "haiku", effort: 42 });
  await step(0);

  expect(efforts).toEqual([SESSION_EFFORT]);
  expect(served).toEqual(["haiku"]);
});

test("a numeric session effort does not cost the model override", async ($, on) => {
  const { efforts, served, skill, step } = engine($, on);

  await skill({ model: "haiku" });
  await step(0, undefined, 42);

  expect(efforts).toEqual([42]);
  expect(served).toEqual(["haiku"]);
});

test("the session effort resumes after the turn completes", async ($, on) => {
  const { efforts, skill, step, complete } = engine($, on);

  await skill({ effort: "low" });
  await step(0);
  await complete();
  await step(0);

  expect(efforts).toEqual(["low", SESSION_EFFORT]);
});

test("a subagent finishing mid-turn does not end the effort override", async ($, on) => {
  const { efforts, skill, step, complete } = engine($, on);

  await skill({ effort: "low" });
  await complete("agent-1");
  await step(1);

  expect(efforts).toEqual(["low"]);
});

test("a subagent's own steps keep their effort", async ($, on) => {
  const { efforts, skill, step } = engine($, on);

  await skill({ effort: "low" });
  await step(0, "agent-1");

  expect(efforts).toEqual([SESSION_EFFORT]);
});

test("a forked skill's effort is left to the engine", async ($, on) => {
  const { efforts, skill, step } = engine($, on);

  await skill({ effort: "low", context: "fork" });
  await step(0);

  expect(efforts).toEqual([SESSION_EFFORT]);
});

test("an unknown effort level changes nothing", async ($, on) => {
  const { efforts, skill, step } = engine($, on);

  await skill({ effort: "inherit" });
  await step(0);

  expect(efforts).toEqual([SESSION_EFFORT]);
});
