import type {
  EngineInterface,
  ModelForkResult,
  PluginOptions,
  Register,
  Timer
} from "claude-code";

// why: keeps the prompt cache warm with no band: one short request over the conversation shortly before
// the entry lapses. Its cache read restarts the entry's life. Logic ported from vayaan-labs/cache-maxxer (MIT).

const COMMAND = "cache-warmup";
// why: one word keeps output cost near zero; the request exists only to read the cached prefix
const PROMPT = "Reply with exactly one word: ok. Do not use any tools.";

const HOUR_MS = 3_600_000;
const FIVE_MIN_MS = 300_000;
const TAIL_BYTES = 262_144;
const RECHECK_MS = 10 * 60_000;
const RETRY_MS = 15_000;
const LEADS: Record<string, number> = {
  "1m": 60_000,
  "2m": 120_000,
  "4m": 240_000,
  "8m": 480_000
};
const CAPS: Record<string, number> = {
  "1h": HOUR_MS,
  "3h": 3 * HOUR_MS,
  "8h": 8 * HOUR_MS
};

type Cfg = { ttl: string; lead: string; idleCap: string };

// invariant: module state; a hot reload starts it over and the next main request re-arms it
const rt = {
  isEnabled: true,
  startedAt: 0,
  learnedTtlMs: null as number | null,
  lastActivity: 0,
  // why: only a main request in flight blocks a ping; a turn waiting on tools or a subagent sends none
  isRequesting: false,
  isPinging: false,
  // why: the entry whose ping failed, so a failure is not retried on every tick until expiry
  skippedFor: -1,
  timer: null as Timer | null,
  lookup: { at: -Infinity, isRunning: false, path: "" }
};

const ttlMs = (cfg: Cfg) =>
  cfg.ttl === "5m"
    ? FIVE_MIN_MS
    : cfg.ttl === "1h"
      ? HOUR_MS
      : (rt.learnedTtlMs ?? HOUR_MS);

// why: never more than half the entry's life, so a short lead setting cannot ping right after a request
const leadMs = (cfg: Cfg, ttl: number) =>
  Math.min(LEADS[cfg.lead] ?? (ttl >= 600_000 ? 240_000 : 40_000), ttl / 2);

type Split = {
  ephemeral_1h_input_tokens?: unknown;
  ephemeral_5m_input_tokens?: unknown;
};
const count = (n: unknown) => (typeof n === "number" && n > 0 ? n : 0);

// invariant: the newest cache write's split in a transcript tail: the entry lives as long as the larger part.
export function parseTtl(tail: string): number | null {
  const lines = tail.split("\n");
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i];
    if (!line || !line.includes("cache_creation")) continue;
    try {
      const entry = JSON.parse(line) as {
        message?: { usage?: { cache_creation?: Split } };
        usage?: { cache_creation?: Split };
      };
      const split =
        entry.message?.usage?.cache_creation ?? entry.usage?.cache_creation;
      if (!split) continue;
      const h = count(split.ephemeral_1h_input_tokens);
      const m = count(split.ephemeral_5m_input_tokens);
      if (h + m > 0) return m > h ? FIVE_MIN_MS : HOUR_MS;
    } catch {
      // why: the tail's first line is usually cut mid-JSON
    }
  }
  return null;
}

async function learnTtl($: EngineInterface, cfg: Cfg) {
  if (cfg.ttl !== "auto" || rt.lookup.isRunning) return;
  const now = await $.clock.now();
  if (now - rt.lookup.at < (rt.learnedTtlMs === null ? RETRY_MS : RECHECK_MS))
    return;
  rt.lookup.isRunning = true;
  rt.lookup.at = now;
  try {
    if (rt.lookup.path === "") {
      const id = await $.session.id();
      const root =
        (await $.env.get("CLAUDE_CONFIG_DIR")) ??
        `${(await $.env.get("HOME")) ?? ""}/.claude`;
      const found = await $.process.run(
        [
          "/usr/bin/find",
          `${root}/projects`,
          "-maxdepth",
          "2",
          "-name",
          `${id}.jsonl`
        ],
        { timeoutMs: 15_000 }
      );
      rt.lookup.path =
        found.stdout.split("\n").find((line) => line.trim() !== "") ?? "";
    }
    if (rt.lookup.path === "") return;
    // why: a long session's transcript is large; the newest write is near the end
    const tail = await $.process.run(
      ["/usr/bin/tail", "-c", String(TAIL_BYTES), rt.lookup.path],
      { timeoutMs: 15_000 }
    );
    const ms = tail.exitCode === 0 ? parseTtl(tail.stdout) : null;
    if (ms !== null) rt.learnedTtlMs = ms;
  } catch {
    // why: the length stays assumed (1h) until a later look succeeds
  } finally {
    rt.lookup.isRunning = false;
  }
}

function arm($: EngineInterface, cfg: Cfg) {
  rt.timer ??= $.clock.every(1000, () => void tick($, cfg));
}

function disarm() {
  rt.timer?.cancel();
  rt.timer = null;
}

async function tick($: EngineInterface, cfg: Cfg) {
  if (!rt.isEnabled || rt.startedAt === 0) return disarm();
  if (cfg.ttl === "auto" && rt.learnedTtlMs === null) void learnTtl($, cfg);
  const now = await $.clock.now();
  const ttl = ttlMs(cfg);
  const left = rt.startedAt + ttl - now;
  // why: a ping after expiry rewrites the whole prefix at write price, which is what warming avoids
  if (left <= 0) return disarm();
  if (
    left > leadMs(cfg, ttl) ||
    rt.isRequesting ||
    rt.isPinging ||
    rt.skippedFor === rt.startedAt
  )
    return;
  const cap = CAPS[cfg.idleCap];
  if (cap !== undefined && now - rt.lastActivity > cap) return disarm();
  const r = await ping($, now);
  if (!r.ok) {
    rt.skippedFor = rt.startedAt;
    $.ui.toast(`Cache warmup skipped: ${r.reason}`);
    return;
  }
  try {
    await $.ui.notify(
      `Cache warmed · ${Math.round(r.read / 1000)}K tokens read`,
      { title: "Cache warmup" }
    );
  } catch {
    // why: notify rejects on a hook's deny or a failed write; the cache is warm regardless
  }
}

type PingResult = { ok: true; read: number } | { ok: false; reason: string };

async function ping(
  $: EngineInterface,
  startedAt: number
): Promise<PingResult> {
  rt.isPinging = true;
  try {
    const r: ModelForkResult = await $.model.fork({ prompt: PROMPT });
    if (!r.isAnswered) return { ok: false, reason: failureOf(r) };
    if (r.usage.cache_read_input_tokens === 0)
      return { ok: false, reason: "the request did not read the cache" };
    if (startedAt > rt.startedAt) rt.startedAt = startedAt;
    return { ok: true, read: r.usage.cache_read_input_tokens };
  } catch (error) {
    return {
      ok: false,
      reason: error instanceof Error ? error.message : String(error)
    };
  } finally {
    rt.isPinging = false;
  }
}

function failureOf(r: Exclude<ModelForkResult, { isAnswered: true }>): string {
  if (r.reason === "api-error")
    return `the API answered ${r.status ?? "with an error"} (${r.error.replace(/_/g, " ")})`;
  if (r.reason === "nothing-to-fork") return "nothing to fork yet";
  if (r.reason === "aborted") return "the request was cut short";
  return "the reply was empty";
}

async function statusText($: EngineInterface, cfg: Cfg) {
  if (!rt.isEnabled)
    return "Cache warmup is off. /cache-warmup on to turn it on.";
  if (rt.startedAt === 0 || !rt.timer)
    return "Cache warmup is on; it arms on your next message.";
  const ttl = ttlMs(cfg);
  const left = rt.startedAt + ttl - (await $.clock.now());
  const nextPing = Math.max(0, Math.round((left - leadMs(cfg, ttl)) / 1000));
  return `Cache warmup is on · ${ttl === HOUR_MS ? "1h" : "5m"} cache · next ping in ${Math.floor(nextPing / 60)}m${nextPing % 60}s`;
}

async function setEnabled($: EngineInterface, cfg: Cfg, isEnabled: boolean) {
  rt.isEnabled = isEnabled;
  await $.store.set("enabled", isEnabled);
  if (!isEnabled) return disarm();
  rt.lastActivity = await $.clock.now();
  if (rt.startedAt > 0) arm($, cfg);
}

export const register: Register = (on, options: PluginOptions) => {
  const cfg: Cfg = {
    ttl: String(options.ttl ?? "auto"),
    lead: String(options.lead ?? "auto"),
    idleCap: String(options.idle_cap ?? "3h")
  };

  on("session.start", async ($, e, next) => {
    const started = await next(e);
    rt.isEnabled = (await $.store.get("enabled")) !== false;
    rt.lastActivity = await $.clock.now();
    try {
      await $.command.register({
        name: COMMAND,
        description: "Keep the prompt cache warm: on, off, or show status",
        argumentHint: "[on | off]",
        immediate: true
      });
    } catch {
      // why: another mod may own the name; warming still works without the command
    }
    return started;
  });

  on("session.end", async ($, e, next) => {
    rt.isRequesting = false;
    // why: reset where the old session id ends, so the next session looks up its own transcript
    rt.lookup.path = "";
    if (e.reason === "clear") rt.startedAt = 0;
    return next(e);
  });

  on("turn.start", async ($, e, next) => {
    rt.lastActivity = await $.clock.now();
    return next(e);
  });

  // invariant: only main-conversation requests move the entry; subagents cache prefixes of their own
  on("turn.step", async function* ($, e, next) {
    const startedAt = e.agentId ? 0 : await $.clock.now();
    if (!e.agentId) rt.isRequesting = true;
    let result;
    try {
      result = yield* next(e);
    } finally {
      if (!e.agentId) rt.isRequesting = false;
    }
    const u = result.usage;
    if (
      !e.agentId &&
      u &&
      u.cache_read_input_tokens + u.cache_creation_input_tokens > 0
    ) {
      rt.startedAt = startedAt;
      rt.skippedFor = -1;
      if (rt.isEnabled) arm($, cfg);
      void learnTtl($, cfg);
    }
    return result;
  });

  on("command.run", { command: COMMAND }, async ($, e) => {
    const word = e.args.trim().toLowerCase();
    if (word === "on" || word === "off")
      await setEnabled($, cfg, word === "on");
    return { text: await statusText($, cfg) };
  });
};
