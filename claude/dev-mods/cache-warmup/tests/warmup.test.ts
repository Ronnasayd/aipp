import type { On } from "claude-code";
import { expect, mock, test, type Engine } from "claude-code/testing";

import { parseTtl } from "../hooks/register";

const T0 = Date.parse("2026-10-22T10:00:00Z");
const MINUTE = 60_000;
const SECOND = 1000;

type Body = Parameters<typeof test>[1];
const withOptions =
  (options: Record<string, unknown>) => (name: string, body: Body) =>
    test(name, options as never, body as never);
// why: a 5 minute entry keeps clock-driven tests short (40s lead → ping at 4:20)
const fiveMinute = withOptions({ options: { ttl: "5m" }, timeoutMs: 30_000 });
const auto = withOptions({ options: { ttl: "auto" }, timeoutMs: 30_000 });
const idleCap = withOptions({
  options: { ttl: "5m", idle_cap: "1h" },
  timeoutMs: 60_000
});

const READ = {
  input_tokens: 12,
  output_tokens: 3,
  cache_read_input_tokens: 61_000,
  cache_creation_input_tokens: 0
};

async function boot($: Engine, on: On, transcriptTail = "") {
  const clock = mock.clock(on, { now: T0 });
  mock.store(on, {});
  const toasts: string[] = [];
  on("ui.toast", (_$, e) => {
    toasts.push(e.text);
    return { value: undefined } as never;
  });
  const notices: { text: string; title?: string }[] = [];
  const notify = { fail: false };
  on("ui.notify", (_$, e) => {
    if (notify.fail) throw new Error("write failed");
    notices.push({ text: e.text, title: e.title });
    return { value: { isSent: true, channel: "terminal_bell" } } as never;
  });
  on("turn.step", async function* (_$, e) {
    return {
      turnId: e.turnId,
      index: e.index,
      answer: "ok",
      toolUses: [],
      stopReason: "end_turn",
      usage: {
        input_tokens: 20,
        output_tokens: 100,
        cache_read_input_tokens: 0,
        cache_creation_input_tokens: 60_000,
        model: "claude-opus-5-5"
      }
    } as never;
  });
  on("turn.start", (_$, e) => ({ turnId: e.turnId }));
  on("turn.complete", (_$, e) => ({ text: e.answer }));
  const fork = {
    calls: 0,
    answer: async (): Promise<unknown> => ({
      isAnswered: true,
      text: "ok",
      usage: READ
    })
  };
  on("model.fork", async () => {
    fork.calls += 1;
    return { value: await fork.answer() } as never;
  });
  on("session.id", () => ({ value: "session-1" }) as never);
  on("env.get", () => ({ value: undefined }) as never);
  on("process.run", (_$, e) => {
    const isFind = e.argv[0] === "/usr/bin/find";
    return {
      value: {
        exitCode: 0,
        stdout: isFind
          ? "/home/u/.claude/projects/p/session-1.jsonl"
          : transcriptTail,
        stderr: ""
      }
    } as never;
  });
  on("classic.SessionStart", () => ({}) as never);
  on("session.end", () => ({ sessionId: "session-1" }) as never);
  on("session.start", () => ({ cwd: "/work" }));
  on("command.register", () => ({ value: undefined }) as never);
  await $.session.start({
    surface: "terminal",
    isInteractive: true,
    cwd: "/work"
  });

  const request = async (extra: Record<string, unknown> = {}) => {
    const step = $.turn.step({
      turnId: "t1",
      index: 0,
      model: "claude-opus-5-5",
      messageCount: 1,
      ...extra
    } as never);
    for await (const chunk of step) void chunk;
    await step.result;
  };
  const command = (args: string) =>
    $.command.run({ command: "cache-warmup", args } as never) as Promise<{
      text?: string;
    }>;
  return { clock, toasts, notices, notify, fork, request, command };
}

fiveMinute(
  "pings at the lead time and keeps pinging, each ping restarting the entry",
  async ($, on) => {
    const { clock, fork, request } = await boot($, on);
    await request();
    await clock.advance(250 * SECOND);
    expect(fork.calls).toBe(0);
    await clock.advance(15 * SECOND);
    expect(fork.calls).toBe(1);
    // why: the ping at ~4:20 restarted the 5m entry, so the next lead is ~8:40, not before
    await clock.advance(240 * SECOND);
    expect(fork.calls).toBe(1);
    await clock.advance(30 * SECOND);
    expect(fork.calls).toBe(2);
  }
);

fiveMinute("a subagent request does not arm the warmer", async ($, on) => {
  const { clock, fork, request } = await boot($, on);
  await request({ agentId: "agent-1" });
  await clock.advance(5 * MINUTE);
  expect(fork.calls).toBe(0);
});

fiveMinute(
  "waits for a running turn, then pings once it ends",
  async ($, on) => {
    const { clock, fork, request } = await boot($, on);
    await request();
    await $.turn.start({ text: "go on", turnId: "t2" });
    await clock.advance(280 * SECOND);
    expect(fork.calls).toBe(0);
    await $.turn.complete({
      answer: "done",
      durationMs: 1000,
      isAborted: false,
      turnId: "t2",
      reason: "answer",
      usage: null
    } as never);
    await clock.advance(2 * SECOND);
    expect(fork.calls).toBe(1);
  }
);

fiveMinute(
  "a failed ping is not retried every second, and says why",
  async ($, on) => {
    const { clock, toasts, fork, request } = await boot($, on);
    await request();
    fork.answer = async () => ({
      isAnswered: false,
      reason: "api-error",
      status: 529,
      error: "overloaded",
      usage: { ...READ, cache_read_input_tokens: 0 }
    });
    await clock.advance(265 * SECOND);
    await clock.advance(30 * SECOND);
    expect(fork.calls).toBe(1);
    expect(toasts).toEqual([
      "Cache warmup skipped: the API answered 529 (overloaded)"
    ]);
  }
);

fiveMinute(
  "a ping that did not read the cache is not retried every second either",
  async ($, on) => {
    const { clock, fork, request } = await boot($, on);
    await request();
    fork.answer = async () => ({
      isAnswered: true,
      text: "ok",
      usage: { ...READ, cache_read_input_tokens: 0 }
    });
    await clock.advance(265 * SECOND);
    await clock.advance(30 * SECOND);
    expect(fork.calls).toBe(1);
  }
);

idleCap(
  "stops once the person has been idle past the cap, and resumes on the next message",
  async ($, on) => {
    const { clock, fork, request } = await boot($, on);
    await request();
    await clock.advance(66 * MINUTE);
    const pinged = fork.calls;
    expect(pinged).toBeGreaterThan(5);
    await clock.advance(10 * MINUTE);
    expect(fork.calls).toBe(pinged);

    await $.turn.start({ text: "back", turnId: "t3" });
    await request();
    await $.turn.complete({
      answer: "ok",
      durationMs: 1000,
      isAborted: false,
      turnId: "t3",
      reason: "answer",
      usage: null
    } as never);
    await clock.advance(265 * SECOND);
    expect(fork.calls).toBe(pinged + 1);
  }
);

fiveMinute(
  "/cache-warmup off stops pinging and on brings it back",
  async ($, on) => {
    const { clock, fork, request, command } = await boot($, on);
    expect((await command("off")).text).toContain("off");
    await request();
    await clock.advance(5 * MINUTE);
    expect(fork.calls).toBe(0);

    expect((await command("on")).text).toContain("on");
    await request();
    await clock.advance(265 * SECOND);
    expect(fork.calls).toBe(1);
  }
);

auto("on auto, the cache length is read from the transcript", async ($, on) => {
  const tail = JSON.stringify({
    message: {
      usage: {
        cache_creation: {
          ephemeral_5m_input_tokens: 60_000,
          ephemeral_1h_input_tokens: 0
        }
      }
    }
  });
  const { clock, fork, request } = await boot($, on, tail);
  await request();
  // why: a learned 5m entry pings at ~4:20; an assumed 1h one would wait ~56 min
  await clock.advance(265 * SECOND);
  expect(fork.calls).toBe(1);
});

test("parseTtl reads the newest cache write split", () => {
  const line = (h: number, m: number) =>
    JSON.stringify({
      message: {
        usage: {
          cache_creation: {
            ephemeral_1h_input_tokens: h,
            ephemeral_5m_input_tokens: m
          }
        }
      }
    });
  expect(parseTtl(`${line(100, 0)}\n${line(0, 100)}`)).toBe(5 * MINUTE);
  expect(parseTtl(`${line(0, 100)}\n${line(100, 0)}`)).toBe(60 * MINUTE);
  expect(parseTtl('{"cut line')).toBe(null);
});

fiveMinute(
  "a resumed session with a live cache is kept warm without a new message",
  async ($, on) => {
    const { clock, fork } = await boot($, on);
    await $.classic.SessionStart({
      source: "resume",
      seconds_since_last_response: 100,
      prompt_cache_likely_expired: false
    } as never);
    // why: 100s already elapsed of the 5m entry, so the 40s lead is reached ~160s later
    await clock.advance(165 * SECOND);
    expect(fork.calls).toBe(1);
  }
);

fiveMinute("a successful ping raises a native notification", async ($, on) => {
  const { clock, notices, request } = await boot($, on);
  await request();
  await clock.advance(265 * SECOND);
  expect(notices).toEqual([
    { text: "Cache warmed · 61K tokens read", title: "Cache warmup" }
  ]);
});

fiveMinute(
  "a notification that fails to send does not count the ping as failed",
  async ($, on) => {
    const { clock, toasts, notify, fork, request } = await boot($, on);
    notify.fail = true;
    await request();
    await clock.advance(265 * SECOND);
    expect(toasts).toEqual([]);
    // why: the ping still restarted the entry, so the next one comes a full cycle later
    await clock.advance(270 * SECOND);
    expect(fork.calls).toBe(2);
  }
);
