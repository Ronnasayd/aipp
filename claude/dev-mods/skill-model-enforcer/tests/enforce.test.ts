import { expect, test, type TestBody } from "claude-code/testing";

const SESSION_MODEL = "claude-opus-5-5";

type Harness = Parameters<TestBody>;

function engine($: Harness[0], on: Harness[1]) {
  const served: string[] = [];
  const files: Record<string, string> = {};
  on("session.id", () => ({ value: "s1" }));
  on("session.model", () => ({ value: SESSION_MODEL }));
  on("fs.write", (_, e) => ((files[e.path] = e.text), { value: undefined }));
  on("skill.prompt", (_$, e) => ({ text: e.text }));
  on("turn.complete", () => ({ text: "" }));
  on("turn.step", async function* (_$, e) {
    served.push(e.model);
    return {
      turnId: e.turnId,
      index: e.index,
      answer: "ok",
      toolUses: [],
      stopReason: "end_turn"
    } as never;
  });
  const skill = (frontmatter: Record<string, string>) =>
    $.skill.prompt({ skill: "probe", text: "go", frontmatter });
  const step = async (index: number, agentId?: string) => {
    const stream = $.turn.step({
      turnId: "t1",
      index,
      model: SESSION_MODEL,
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
  return { served, files, skill, step, complete };
}

const MODEL_FILE = "/tmp/claude-model-s1.txt";

test("the model file follows the main loop's served model", async ($, on) => {
  const { files, skill, step, complete } = engine($, on);

  await step(0);
  expect(files[MODEL_FILE]).toBe(SESSION_MODEL);

  await skill({ model: "haiku" });
  await step(1);
  expect(files[MODEL_FILE]).toBe("haiku");

  await complete();
  expect(files[MODEL_FILE]).toBe(SESSION_MODEL);
});

test("a subagent's steps and completion leave the model file alone", async ($, on) => {
  const { files, skill, step, complete } = engine($, on);

  await skill({ model: "haiku" });
  await step(0);
  await step(1, "agent-1");
  await complete("agent-1");

  expect(files[MODEL_FILE]).toBe("haiku");
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
