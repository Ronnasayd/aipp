import { expect, test, type TestBody } from "claude-code/testing";

const SESSION_MODEL = "claude-opus-5-5";
const SESSION_EFFORT = "high";

type Harness = Parameters<TestBody>;

function engine($: Harness[0], on: Harness[1]) {
  const served: string[] = [];
  const efforts: unknown[] = [];
  const files: Record<string, string> = {};
  const asks: string[] = [];
  const dialog = { reply: "Yes" as string | undefined };
  // why: a typed /skill arrives with the engine's own override already on the step
  const applied: { model: string; effort: typeof SESSION_EFFORT | "low" } = {
    model: SESSION_MODEL,
    effort: SESSION_EFFORT
  };
  const stored: { effortLevel?: string } = { effortLevel: SESSION_EFFORT };
  on("settings.read", () => ({ value: stored }) as never);
  on("tool.call", { tool: "AskUserQuestion" }, (_$, e) => {
    const { question } = e.questions[0]!;
    asks.push(question);
    if (dialog.reply === undefined) return { deny: "dismissed" };
    return {
      result: {
        questions: e.questions,
        answers: { [question]: dialog.reply }
      }
    } as never;
  });
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
    effort: typeof applied.effort | number = applied.effort
  ) => {
    const stream = $.turn.step({
      turnId: "t1",
      index,
      model: applied.model,
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
  return {
    served,
    efforts,
    files,
    asks,
    dialog,
    applied,
    stored,
    skill,
    step,
    complete
  };
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

test("the override asks first and names what it would change", async ($, on) => {
  const { asks, served, efforts, skill, step } = engine($, on);

  await skill({ model: "haiku", effort: "low" });
  await step(0);

  expect(asks).toEqual([
    "Skill probe requests model haiku and effort low. Apply for this turn?"
  ]);
  expect(served).toEqual(["haiku"]);
  expect(efforts).toEqual(["low"]);
});

test("a refusal keeps the session's model and effort", async ($, on) => {
  const { dialog, served, efforts, skill, step } = engine($, on);

  dialog.reply = "No";
  await skill({ model: "haiku", effort: "low" });
  await step(0);

  expect(served).toEqual([SESSION_MODEL]);
  expect(efforts).toEqual([SESSION_EFFORT]);
});

test("free text under Other counts as a refusal", async ($, on) => {
  const { dialog, served, skill, step } = engine($, on);

  dialog.reply = "maybe later";
  await skill({ model: "haiku" });
  await step(0);

  expect(served).toEqual([SESSION_MODEL]);
});

test("a dismissed dialog keeps the session's model and still runs the skill", async ($, on) => {
  const { dialog, served, skill, step } = engine($, on);

  dialog.reply = undefined;
  const { text } = await skill({ model: "haiku" });
  await step(0);

  expect(text).toBe("go");
  expect(served).toEqual([SESSION_MODEL]);
});

test("nothing to override asks nothing", async ($, on) => {
  const { asks, skill } = engine($, on);

  await skill({});
  await skill({ model: "inherit", effort: "inherit" });
  await skill({ effort: 42 });
  await skill({ model: "haiku", context: "fork" });

  expect(asks).toEqual([]);
});

test("a refusal undoes the override the engine applied to a typed skill", async ($, on) => {
  const { applied, dialog, served, efforts, files, skill, step } = engine(
    $,
    on
  );

  dialog.reply = "No";
  await skill({ model: "haiku", effort: "low" });
  applied.model = "claude-haiku-5-5";
  applied.effort = "low";
  await step(0);
  await step(1);

  expect(served).toEqual([SESSION_MODEL, SESSION_MODEL]);
  expect(efforts).toEqual([SESSION_EFFORT, SESSION_EFFORT]);
  expect(JSON.parse(files[SERVED_FILE]!)).toEqual({
    model: SESSION_MODEL,
    effort: SESSION_EFFORT
  });
});

test("a refusal with no stored effort still restores the model", async ($, on) => {
  const { applied, dialog, stored, served, efforts, skill, step } = engine(
    $,
    on
  );

  dialog.reply = "No";
  delete stored.effortLevel;
  await skill({ model: "haiku", effort: "low" });
  applied.model = "claude-haiku-5-5";
  applied.effort = "low";
  await step(0);

  expect(served).toEqual([SESSION_MODEL]);
  expect(efforts).toEqual(["low"]);
});

test("a refusal lasts one turn", async ($, on) => {
  const { applied, dialog, served, skill, step, complete } = engine($, on);

  dialog.reply = "No";
  await skill({ model: "haiku" });
  await step(0);
  await complete();
  applied.model = "claude-sonnet-5-5";
  await step(0);

  expect(served).toEqual([SESSION_MODEL, "claude-sonnet-5-5"]);
});
