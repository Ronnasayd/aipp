import type { Register } from "claude-code";

export const register: Register = (on) => {
  // why: a reload dropping this value only loses the override for one turn, so it needs no $.state contract
  let pinned: string | undefined;

  on("skill.prompt", ($, e, next) => {
    const { model, context } = e.frontmatter;
    // invariant: a forked skill's model is applied by the engine to its subagent, never to this loop
    if (
      typeof model === "string" &&
      model !== "inherit" &&
      context !== "fork"
    ) {
      pinned = model;
    }
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    const isOverridden = pinned !== undefined && e.agentId === undefined;
    return yield* next(isOverridden ? { ...e, model: pinned as string } : e);
  });

  on("turn.complete", ($, e, next) => {
    if (e.agentId === undefined) pinned = undefined;
    return next(e);
  });
};
