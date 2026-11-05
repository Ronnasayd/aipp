import type { EngineInterface, Register } from "claude-code";

// why: the statusline JSON only carries the session model, so a skill's override is invisible
// there; scripts/statusline-command.sh reads this file by session_id.
const modelFile = (sid: string) => `/tmp/claude-model-${sid}.txt`;

const mirror = async ($: EngineInterface, model: string) =>
  $.fs.write(modelFile(await $.session.id()), model).catch(() => {});

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
    if (e.agentId !== undefined) return yield* next(e);
    const model = pinned ?? e.model;
    await mirror($, model);
    return yield* next({ ...e, model });
  });

  on("turn.complete", async ($, e, next) => {
    if (e.agentId === undefined) {
      pinned = undefined;
      // why: no step runs between turns, so the file would keep showing the expired override
      await mirror($, await $.session.model());
    }
    return next(e);
  });
};
