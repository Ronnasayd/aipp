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

export const register: Register = (on) => {
  // why: a reload dropping this value only loses the override for one turn, so it needs no $.state contract
  let pinned: string | undefined;
  let pinnedEffort: Level | undefined;
  let refused = false;
  let skill: string | undefined;

  on("skill.prompt", async ($, e, next) => {
    const { model, effort, context } = e.frontmatter;
    // invariant: a forked skill's model and effort are applied by the engine to its subagent, never to this loop
    if (context === "fork") return next(e);
    const wanted =
      typeof model === "string" && model !== "inherit" ? model : undefined;
    const level = isLevel(effort) ? effort : undefined;
    if (!wanted && !level) return next(e);
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
    refused = answer !== "Yes";
    if (!refused) {
      pinned = wanted ?? pinned;
      pinnedEffort = level ?? pinnedEffort;
      skill = e.skill;
    }
    return next(e);
  });

  on("turn.step", async function* ($, e, next) {
    if (e.agentId !== undefined) return yield* next(e);
    // hazard: a typed /skill reaches this step with the engine's own override on e, so a refusal must undo it
    const model = pinned ?? (refused ? await $.session.model() : e.model);
    const effort =
      pinnedEffort ?? (refused ? await readSessionEffort($) : undefined);
    await mirror($, model, effort ?? e.effort, skill);
    return yield* next({ ...e, model, ...(effort && { effort }) });
  });

  on("turn.complete", async ($, e, next) => {
    if (e.agentId === undefined) {
      pinned = undefined;
      pinnedEffort = undefined;
      refused = false;
      skill = undefined;
      // why: no step runs between turns, so the file would keep showing the expired override;
      // $.session has no effort getter, so a missing effort means the session's own level
      await mirror($, await $.session.model());
    }
    return next(e);
  });
};
