import type { AgentInfo } from "claude-code";
import { expect, test, type TestBody } from "claude-code/testing";

// why: the test environment has timers, but the hooks lib declares none
declare const setTimeout: (fn: () => void, ms: number) => unknown;

type Harness = Parameters<TestBody>;
type Running = Pick<AgentInfo, "id" | "model" | "status"> & { effort?: string };

const HOME = "/home/u";
const CWD = "/repo";

function engine($: Harness[0], on: Harness[1]) {
  const list: Running[] = [];
  const env: Record<string, string> = { HOME };
  const files: Record<string, string> = {};
  const spawned: string[] = [];
  const limits = { concurrent: 20 };
  const settings: { effortLevel?: string } = { effortLevel: "medium" };
  let clock = 0;
  let slept = 0;
  // why: each sleep is a poll; a test frees agents at a chosen poll to model one finishing
  const onSleep: Array<() => void> = [];
  // why: a foreground Agent call returns only when its agent ends, long after the spawn
  const finish: Record<string, () => void> = {};
  let nextId = 0;

  on("agent.list", () => ({ value: list.map((a) => ({ ...a })) as never }));
  on("agent.limits", () => ({
    value: {
      concurrent: limits.concurrent,
      depth: 1,
      isBackgroundEnabled: true
    }
  }));
  on("session.model", () => ({ value: "claude-opus-5-5" }));
  on("session.cwd", () => ({ value: CWD }));
  on("env.get", (_, e) => ({ value: env[e.name] }));
  on("settings.read", () => ({ value: settings }) as never);
  on("clock.now", () => ({ value: clock }));
  on("clock.sleep", (_, e) => {
    clock += e.ms;
    onSleep[slept++]?.();
    return { value: undefined };
  });
  on("fs.list", (_, e) => {
    const dir = `${e.path ?? ""}/`;
    const names = Object.keys(files)
      .filter((p) => p.startsWith(dir) && !p.slice(dir.length).includes("/"))
      .map((p) => p.slice(dir.length));
    if (names.length === 0) throw new Error("ENOENT");
    return {
      value: names.map((name) => ({
        name,
        kind: "file",
        size: 1,
        mtimeMs: 0,
        isLink: false
      }))
    } as never;
  });
  on("fs.read", (_, e) => {
    const text = files[e.path];
    if (text === undefined) throw new Error("ENOENT");
    return { value: text } as never;
  });
  on("agent.spawn", (_, e) => {
    const id = `a${++nextId}`;
    const model = e.model ?? "claude-opus-5-5";
    list.push({ id, model, status: "running" });
    spawned.push(id);
    return { model, agentId: id };
  });
  on("tool.call", { tool: "Agent" }, async (_, e) => {
    const ran = await $.agent.spawn({
      tool_use_id: e.tool_use_id ?? "",
      prompt: e.prompt,
      description: e.description,
      subagentType: e.subagent_type ?? "general-purpose",
      provider: { plugin: "engine", tier: "core" } as never,
      parentModel: "claude-opus-5-5",
      background: false,
      fork: false,
      ...(e.model ? { model: e.model } : {})
    });
    const id = ran.agentId!;
    // why: the engine records the call's effort on the started agent
    const entry = list.find((a) => a.id === id)!;
    if (e.effort) entry.effort = e.effort;
    await new Promise<void>((done) => (finish[id] = done));
    return { result: { agentId: id } } as never;
  });

  const agent = (input: {
    model?: "opus" | "sonnet" | "haiku";
    effort?: "low" | "medium" | "high" | "xhigh" | "max";
    subagent_type?: string;
  }) => {
    // why: the typed call overloads hit TS2589 on an input built for no one tool
    const call = $.tool.call as unknown as (
      input: object
    ) => Promise<{ deny?: string }>;
    return call({ tool: "Agent", description: "d", prompt: "p", ...input });
  };
  const end = (id: string) => {
    list.splice(
      list.findIndex((a) => a.id === id),
      1
    );
    finish[id]?.();
  };
  // why: lets pending hook chains run up to their next await on the engine
  const settle = () => new Promise<void>((r) => setTimeout(r, 0));
  const until = async (n: number) => {
    for (let i = 0; i < 500 && spawned.length < n; i++) await settle();
  };
  return {
    list,
    env,
    files,
    spawned,
    limits,
    settings,
    onSleep,
    agent,
    end,
    until
  };
}

test("one opus+high fills the budget; a second one is refused", async ($, on) => {
  const { spawned, agent, end, until } = engine($, on);

  void agent({ model: "opus", effort: "high" });
  await until(1);
  expect(spawned).toEqual(["a1"]);

  const second = await agent({ model: "opus", effort: "high" });
  expect(spawned).toEqual(["a1"]);
  expect(second.deny).toMatch(/128/);
  end("a1");
});

test("two sonnet+high fit together; a third is refused without waiting, even with AGENT_BUDGET_WAIT_MS set", async ($, on) => {
  const { spawned, env, onSleep, agent, end, until } = engine($, on);
  env.AGENT_BUDGET_WAIT_MS = "8000";
  let slept = false;
  onSleep[0] = () => (slept = true);

  void agent({ model: "sonnet", effort: "high" });
  void agent({ model: "sonnet", effort: "high" });
  await until(2);
  expect(spawned).toEqual(["a1", "a2"]);

  const third = await agent({ model: "sonnet", effort: "high" });
  expect(third.deny).toMatch(/agent-budget/);
  expect(third.deny).not.toMatch(/Waited/);
  expect(slept).toBe(false);
  expect(spawned).toEqual(["a1", "a2"]);
  end("a1");
  end("a2");
});

test("eight sonnet+low fit, a ninth does not", async ($, on) => {
  const { spawned, agent, until } = engine($, on);

  for (let i = 0; i < 8; i++) void agent({ model: "sonnet", effort: "low" });
  await until(8);
  expect(spawned.length).toBe(8);

  const ninth = await agent({ model: "sonnet", effort: "low" });
  expect(ninth.deny).toBeDefined();
  expect(spawned.length).toBe(8);
});

test("the count cap refuses cheap agents past CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS", async ($, on) => {
  const { spawned, limits, agent, until } = engine($, on);
  limits.concurrent = 3;

  for (let i = 0; i < 3; i++) void agent({ model: "haiku", effort: "low" });
  await until(3);

  const fourth = await agent({ model: "haiku", effort: "low" });
  expect(fourth.deny).toMatch(/3/);
  expect(spawned.length).toBe(3);
});

test("xhigh and max weigh as high", async ($, on) => {
  const { spawned, agent, until } = engine($, on);

  void agent({ model: "sonnet", effort: "xhigh" });
  void agent({ model: "sonnet", effort: "max" });
  await until(2);
  expect(spawned.length).toBe(2);

  const third = await agent({ model: "haiku", effort: "high" });
  expect(third.deny).toBeDefined();
});

test("a type's frontmatter model and effort decide its weight when the call gives none", async ($, on) => {
  const { spawned, files, agent, until } = engine($, on);
  files[`${HOME}/.claude/agents/cheap.md`] =
    "---\nname: cheap-helper\nmodel: haiku\neffort: low\n---\nbody";

  void agent({ model: "opus", effort: "high" });
  await until(1);
  const cheap = await agent({ subagent_type: "cheap-helper" });
  expect(cheap.deny).toBeDefined();
  expect(cheap.deny).toMatch(/haiku/);
  expect(spawned.length).toBe(1);
});

test("with nothing declared a subagent weighs as the parent's model at the session effort", async ($, on) => {
  const { spawned, settings, agent, until } = engine($, on);
  settings.effortLevel = "high";

  void agent({ model: "sonnet", effort: "low" });
  await until(1);
  // why: opus (session model) + high (session effort) = 128, over what remains
  const plain = await agent({});
  expect(plain.deny).toMatch(/opus/);
  expect(spawned.length).toBe(1);
});

test("two parallel opus+high calls never both pass on the same free budget", async ($, on) => {
  const { spawned, agent, until } = engine($, on);

  const answers: Array<{ deny?: string }> = [];
  void agent({ model: "opus", effort: "high" }).then((r) => answers.push(r));
  void agent({ model: "opus", effort: "high" }).then((r) => answers.push(r));
  await until(2);
  expect(spawned).toEqual(["a1"]);
  expect(answers.filter((a) => a.deny).length).toBe(1);
});

test("by default an agent over budget is refused at once, without waiting", async ($, on) => {
  const { spawned, onSleep, agent, until } = engine($, on);
  let slept = false;
  onSleep[0] = () => (slept = true);

  void agent({ model: "opus", effort: "high" });
  await until(1);
  const second = await agent({ model: "haiku", effort: "low" });
  expect(second.deny).toMatch(/agent-budget/);
  expect(slept).toBe(false);
  expect(spawned.length).toBe(1);
});
