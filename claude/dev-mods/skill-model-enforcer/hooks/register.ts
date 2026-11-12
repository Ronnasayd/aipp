import type { EngineInterface, Register, TurnStepInput } from "claude-code";

// why: the statusline JSON only carries the session's model and effort, so a skill's override is
// invisible there; scripts/statusline-command.sh reads this file by session_id.
const servedFile = (sid: string) => `/tmp/claude-served-${sid}.json`;

const mirror = async (
  $: EngineInterface,
  model: string,
  effort?: TurnStepInput["effort"],
  skill?: string
) =>
  $.fs
    .write(
      servedFile(await $.session.id()),
      JSON.stringify({ skill, model, effort })
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
  model?: string;
  effort?: Level;
  skill?: string;
  refused?: boolean;
};

const MAIN = "";

export const register: Register = (on) => {
  // why: a reload dropping these only loses an override for one turn, so they need no $.state contract
  // invariant: keyed by agentId (MAIN for the main loop) so a subagent's skill never leaks into another loop
  const pins = new Map<string, Pin>();
  // hazard: skill.prompt carries no agentId; the Skill tool's tool.call does, and expands the prompt inside next()
  // ponytail: one slot, so two loops calling Skill at the same instant may swap pins; key by tool_use_id if seen
  let caller = MAIN;

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
    if (context === "fork") return next(e);
    const wanted =
      typeof model === "string" && model !== "inherit" ? model : undefined;
    const level = isLevel(effort) ? effort : undefined;
    if (!wanted && !level) return next(e);
    const loop = caller;
    const change = [wanted && `model ${wanted}`, level && `effort ${level}`]
      .filter(Boolean)
      .join(" and ");
    // why: ask rejects when dismissed and under -p; with no consent the session keeps its own model and effort
    const answer = await $.ui
      .ask(`Skill ${e.skill} requests ${change}. Apply for this turn?`, [
        "Yes",
        "No"
      ])
      .catch(() => undefined);
    const prior = pins.get(loop);
    pins.set(
      loop,
      answer === "Yes"
        ? {
            model: wanted ?? prior?.model,
            effort: level ?? prior?.effort,
            skill: e.skill
          }
        : { refused: true }
    );
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    const loop = e.agentId ?? MAIN;
    const pin = pins.get(loop);
    if (loop !== MAIN) {
      if (!pin?.model && !pin?.effort) return yield* next(e);
      await mirror($, pin.model ?? e.model, pin.effort ?? e.effort, pin.skill);
      return yield* next({
        ...e,
        model: pin.model ?? e.model,
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
    const pin = pins.get(loop);
    pins.delete(loop);
    // why: no step runs between turns, so the file would keep showing the expired override;
    // $.session has no effort getter, so a missing effort means the session's own level
    if (loop === MAIN || pin?.model || pin?.effort) {
      const main = pins.get(MAIN);
      await mirror(
        $,
        main?.model ?? (await $.session.model()),
        main?.effort,
        main?.skill
      );
    }
    return next(e);
  });
};
