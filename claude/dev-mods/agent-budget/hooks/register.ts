import type { AgentInfo, EngineInterface, Register } from "claude-code";

type Family = "opus" | "sonnet" | "haiku";
type Level = "low" | "medium" | "high";

// why: cost of one call per model+effort (USD x1000) from the owner's price table; opus+high is the ceiling
const WEIGHTS: Record<Family, Record<Level, number>> = {
  opus: { low: 31.04, medium: 71.64, high: 128 },
  sonnet: { low: 15.52, medium: 35.82, high: 64 },
  haiku: { low: 0.78, medium: 1.79, high: 3.2 }
};
const DEFAULT_BUDGET = 128;
// why: measured on 2.1.332, an Agent tool.call hook gets 10 s of own time, so no queue can be held here;
// refuse at once and let the model retry after an agent ends
const LIVE: ReadonlySet<AgentInfo["status"]> = new Set([
  "pending",
  "running",
  "waiting"
]);

// why: an unknown family (fable, a full id of a new line) is priced as the most expensive, never as free
const family = (model: string): Family =>
  /haiku/i.test(model) ? "haiku" : /sonnet/i.test(model) ? "sonnet" : "opus";

// why: the table stops at high; the owner chose to price xhigh, max and integer budgets as high
const level = (effort: unknown): Level =>
  effort === "low" || effort === "medium" ? effort : "high";

const weigh = (model: string, effort: unknown) =>
  WEIGHTS[family(model)][level(effort)];

const num = (raw: string | undefined, fallback: number) => {
  const n = Number(raw);
  return raw !== undefined && raw !== "" && Number.isFinite(n) && n >= 0
    ? n
    : fallback;
};

const sessionEffort = async ($: EngineInterface): Promise<unknown> => {
  const stored: unknown = await $.settings
    .read({ key: "effortLevel" })
    .catch(() => undefined);
  if (typeof stored === "string") return stored;
  return (
    (stored as { effortLevel?: unknown } | undefined)?.effortLevel ?? "high"
  );
};

type Frontmatter = { model?: string; effort?: string };

const parseFrontmatter = (text: string): Frontmatter & { name?: string } => {
  const block = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text)?.[1] ?? "";
  const field = (key: string) =>
    new RegExp(`^${key}:\\s*["']?([^"'\\r\\n#]+?)["']?\\s*$`, "m").exec(
      block
    )?.[1];
  return {
    name: field("name"),
    model: field("model"),
    effort: field("effort")
  };
};

// invariant: same lookup order as Claude Code: project agents shadow user agents
const definition = async (
  $: EngineInterface,
  type: string
): Promise<Frontmatter> => {
  const dirs = [
    `${await $.session.cwd()}/.claude/agents`,
    `${await $.env.get("HOME")}/.claude/agents`
  ];
  for (const dir of dirs) {
    const entries = await $.fs.list(dir).catch(() => []);
    for (const entry of entries) {
      if (!entry.name.endsWith(".md")) continue;
      const text = await $.fs.read(`${dir}/${entry.name}`).catch(() => "");
      const fm = parseFrontmatter(typeof text === "string" ? text : "");
      if ((fm.name ?? entry.name.slice(0, -3)) === type) return fm;
    }
  }
  return {};
};

type Ask = {
  model?: string;
  effort?: string;
  subagent_type?: string;
  agentId?: string;
};

const resolve = async ($: EngineInterface, ask: Ask, agents: AgentInfo[]) => {
  const type = ask.subagent_type ?? "general-purpose";
  const fork = type === "fork";
  const def = fork ? {} : await definition($, type);
  const parentModel =
    agents.find((a) => a.id === ask.agentId)?.model ??
    (await $.session.model());
  const declared = fork ? undefined : (ask.model ?? def.model);
  const model =
    declared && declared !== "inherit"
      ? declared
      : ((await $.env.get("CLAUDE_CODE_SUBAGENT_MODEL")) ?? parentModel);
  const effort =
    (fork ? undefined : (ask.effort ?? def.effort)) ?? (await sessionEffort($));
  return { model, effort: level(effort), weight: weigh(model, effort) };
};

const usage = async ($: EngineInterface, agents: AgentInfo[]) => {
  const live = agents.filter((a) => LIVE.has(a.status));
  const fallbackEffort = await sessionEffort($);
  const fallbackModel = await $.session.model();
  const used = live.reduce(
    (sum, a) =>
      sum + weigh(a.model ?? fallbackModel, a.effort ?? fallbackEffort),
    0
  );
  return { used, count: live.length };
};

export const register: Register = (on) => {
  // invariant: one admission at a time, held until its agent is in $.agent.list (spawned) or its call ended,
  // so two parallel Agent calls never both count the same free budget
  let gate: Promise<void> = Promise.resolve();
  let admitting: { toolUseId?: string; release: () => void } | undefined;

  on("tool.call", { tool: "Agent" }, async ($, e, next) => {
    let release!: () => void;
    const turn = new Promise<void>((done) => (release = done));
    const before = gate;
    gate = before.then(() => turn);
    let released = false;
    const free = () => {
      if (released) return;
      released = true;
      if (admitting?.release === free) admitting = undefined;
      release();
    };
    try {
      await before;
      const budget = num(await $.env.get("AGENT_BUDGET_MAX"), DEFAULT_BUDGET);
      const { concurrent } = await $.agent.limits();
      const agents = await $.agent.list();
      const want = await resolve($, e, agents);
      const { used, count } = await usage($, agents);
      if (used + want.weight > budget + 1e-9 || count >= concurrent) {
        return {
          deny:
            `agent-budget: ${want.model} + ${want.effort} costs ${want.weight} of a ${budget} budget; ` +
            `${used.toFixed(2)} used by ${count}/${concurrent} running agents. ` +
            `Retry after an agent ends, or use a cheaper model or effort.`
        };
      }
      admitting = { toolUseId: e.tool_use_id, release: free };
      return await next(e);
    } finally {
      free();
    }
  }).catch((_$, _e, next) =>
    // why: a guard that fails or overruns its budget must refuse, not let the engine admit the agent
    next.called
      ? next(_e)
      : {
          deny: "agent-budget: admission check failed or ran out of time; retry the Agent call."
        }
  );

  on("agent.spawn", async (_$, e, next) => {
    const started = await next(e);
    const pending = admitting;
    if (
      pending &&
      (!pending.toolUseId ||
        !e.tool_use_id ||
        pending.toolUseId === e.tool_use_id)
    ) {
      pending.release();
    }
    return started;
  });
};
