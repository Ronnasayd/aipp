import type { EngineInterface, Register, TurnStepInput } from "claude-code";

// why: the statusline JSON only carries the session's model and effort, so a skill's override is
// invisible there; scripts/statusline-command.sh reads this file by session_id.
const servedFile = (sid: string) => `/tmp/claude-served-${sid}.json`;

const mirror = async (
  $: EngineInterface,
  model: string,
  effort?: TurnStepInput["effort"]
) =>
  $.fs
    .write(servedFile(await $.session.id()), JSON.stringify({ model, effort }))
    .catch(() => {});

type Level = Exclude<TurnStepInput["effort"], number | undefined>;

const LEVELS: unknown[] = ["low", "medium", "high", "xhigh", "max"];

// hazard: the engine refuses a numeric effort in next() and skips the whole hook, model override included
const isLevel = (v: unknown): v is Level => LEVELS.includes(v);

export const register: Register = (on) => {
  // why: a reload dropping this value only loses the override for one turn, so it needs no $.state contract
  let pinned: string | undefined;
  let pinnedEffort: Level | undefined;

  on("skill.prompt", ($, e, next) => {
    const { model, effort, context } = e.frontmatter;
    // invariant: a forked skill's model and effort are applied by the engine to its subagent, never to this loop
    if (context === "fork") return next(e);
    if (typeof model === "string" && model !== "inherit") pinned = model;
    if (isLevel(effort)) pinnedEffort = effort;
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    if (e.agentId !== undefined) return yield* next(e);
    const model = pinned ?? e.model;
    await mirror($, model, pinnedEffort ?? e.effort);
    return yield* next({
      ...e,
      model,
      ...(pinnedEffort && { effort: pinnedEffort })
    });
  });

  on("turn.complete", async ($, e, next) => {
    if (e.agentId === undefined) {
      pinned = undefined;
      pinnedEffort = undefined;
      // why: no step runs between turns, so the file would keep showing the expired override;
      // $.session has no effort getter, so a missing effort means the session's own level
      await mirror($, await $.session.model());
    }
    return next(e);
  });
};
