import type { EngineInterface, Register, TurnStepInput } from "claude-code";

// why: the statusline JSON only carries the session's model and effort, so a skill's override is
// invisible there; scripts/statusline-command.sh reads this file by session_id.
const servedFile = (sid: string) => `/tmp/claude-served-${sid}.json`;

const mirror = async (
  $: EngineInterface,
  model: string,
  effort?: TurnStepInput["effort"],
  skill?: string,
  fork?: true
) =>
  $.fs
    .write(
      servedFile(await $.session.id()),
      JSON.stringify({ skill, model, effort, fork })
    )
    .catch(() => {});

type Level = Exclude<TurnStepInput["effort"], number | undefined>;

const LEVELS: unknown[] = ["low", "medium", "high", "xhigh", "max"];

// hazard: the engine refuses a numeric effort in next() and skips the whole hook, model override included
const isLevel = (v: unknown): v is Level => LEVELS.includes(v);

// why: $.session has no effort getter; the stored level misses a --effort flag or env override
const readSessionEffort = async ($: EngineInterface) => {
  const stored = await $.settings.read({ key: "effortLevel" });
  return isLevel(stored) ? stored : undefined;
};

type Pin = {
  loop: string;
  model?: string;
  effort?: Level;
  skill?: string;
  refused?: boolean;
};

const MAIN = "";

// hazard: an alias (opus) matches the session's id by family only, so a pinned older version reads as the same
const sameModel = (wanted: string, current?: string) =>
  wanted === current || !!current?.startsWith(`claude-${wanted}-`);

export const register: Register = (on) => {
  // why: a reload dropping these only loses an override for one turn, so they need no $.state contract
  // invariant: each entry names its loop (MAIN for the main loop) so a subagent's skill never leaks into another loop
  // why: the engine has no skill-end event; an inline skill lasts until its loop's turn completes, which pops it
  const stack: Pin[] = [];
  const top = (loop: string) => stack.findLast((p) => p.loop === loop);
  // why: a subagent's model and effort are only visible on its steps; the main loop reads the session instead
  const seen = new Map<string, { model: string; effort?: Level }>();
  // hazard: skill.prompt carries no agentId; the Skill tool's tool.call does, and expands the prompt inside next()
  // ponytail: one slot, so two loops calling Skill at the same instant may swap pins; key by tool_use_id if seen
  let caller = MAIN;
  // why: skill.prompt never learns the forked subagent's agentId, so the next loop that has not stepped yet claims it
  // ponytail: one slot, so two forks started together may swap names; read agent.spawn if it proves to fire for them
  let pendingFork: string | undefined;
  const forks = new Map<string, string>();

  on("tool.call", { tool: "Skill" }, async ($, e, next) => {
    caller = e.agentId ?? MAIN;
    try {
      return await next(e);
    } finally {
      caller = MAIN;
    }
  });

  on("skill.prompt", async ($, e, next) => {
    const { model, effort, context } = e.frontmatter;
    // invariant: a forked skill's model and effort are applied by the engine to its subagent, never to this loop
    if (context === "fork") {
      pendingFork = e.skill;
      return next(e);
    }
    const wanted =
      typeof model === "string" && model !== "inherit" ? model : undefined;
    const level = isLevel(effort) ? effort : undefined;
    if (!wanted && !level) return next(e);
    const loop = caller;
    const below = top(loop);
    const current =
      loop === MAIN
        ? {
            model: await $.session.model(),
            effort: await readSessionEffort($)
          }
        : seen.get(loop);
    const nowModel = below?.model ?? current?.model;
    const nowEffort = below?.effort ?? current?.effort;
    const change = [
      wanted && !sameModel(wanted, nowModel) && `model ${wanted}`,
      level && level !== nowEffort && `effort ${level}`
    ]
      .filter(Boolean)
      .join(" and ");
    const inherited = { loop, model: below?.model, effort: below?.effort };
    if (!change) {
      stack.push({ ...inherited, refused: below?.refused, skill: e.skill });
      return next(e);
    }
    // why: ask rejects when dismissed and under -p; with no consent the loop keeps what it was serving
    const answer = await $.ui
      .ask(`Skill ${e.skill} requests ${change}. Apply for this turn?`, [
        "Yes",
        "No"
      ])
      .catch(() => undefined);
    stack.push(
      answer === "Yes"
        ? {
            loop,
            model: wanted ?? below?.model,
            effort: level ?? below?.effort,
            skill: e.skill
          }
        : { ...inherited, skill: below?.skill, refused: true }
    );
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    const loop = e.agentId ?? MAIN;
    const pin = top(loop);
    if (loop !== MAIN) {
      if (pendingFork && !seen.has(loop) && !forks.has(loop)) {
        forks.set(loop, pendingFork);
        pendingFork = undefined;
      }
      const model = pin?.model ?? e.model;
      const effort = pin?.effort ?? (isLevel(e.effort) ? e.effort : undefined);
      seen.set(loop, { model, effort });
      const fork = forks.get(loop);
      if (fork) await mirror($, model, effort, pin?.skill ?? fork, true);
      if (!pin) return yield* next(e);
      if (!fork) await mirror($, model, pin.effort ?? e.effort, pin.skill);
      return yield* next({
        ...e,
        model,
        ...(pin.effort && { effort: pin.effort })
      });
    }
    // hazard: a typed /skill reaches this step with the engine's own override on e, so a refusal must undo it
    const model =
      pin?.model ?? (pin?.refused ? await $.session.model() : e.model);
    const effort =
      pin?.effort ?? (pin?.refused ? await readSessionEffort($) : undefined);
    await mirror($, model, effort ?? e.effort, pin?.skill);
    return yield* next({ ...e, model, ...(effort && { effort }) });
  });

  on("turn.complete", async ($, e, next) => {
    const loop = e.agentId ?? MAIN;
    const wasFork = forks.delete(loop);
    const had = wasFork || stack.some((p) => p.loop === loop);
    for (let i = stack.length; i--;)
      if (stack[i]!.loop === loop) stack.splice(i, 1);
    if (loop !== MAIN) seen.delete(loop);
    // why: no step runs between turns, so the file would keep showing the popped skill;
    // $.session has no effort getter, so a missing effort means the session's own level
    if (loop === MAIN || had) {
      const shown = top(MAIN);
      await mirror(
        $,
        shown?.model ?? (await $.session.model()),
        shown?.effort,
        shown?.skill
      );
    }
    return next(e);
  });
};
