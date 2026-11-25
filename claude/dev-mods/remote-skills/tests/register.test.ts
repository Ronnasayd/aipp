import { expect, mock, test } from "claude-code/testing";

const INDEX = `skills:
- name:
  - git-guide
  description: A guide to Git
    commands and workflows.
- name:
  - skill-advisor
  description: 'Picks the "best" skill —
    it''s handy.'
`;

test("registers /rs-<name> per index.yaml entry with its description", async ($, on) => {
  const registered: { name: string; description: string }[] = [];
  on("fs.exists", () => ({ value: true }));
  on("fs.read", () => ({ value: INDEX }));
  on("command.list", () => ({ value: [] }));
  on("command.register", (_, e: any) => {
    registered.push({ name: e.name, description: e.description });
    return { value: { command: e.name } };
  });
  on("session.start", (_, e) => ({ cwd: e.cwd }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });

  expect(registered).toEqual([
    {
      name: "rs-git-guide",
      description: "A guide to Git commands and workflows."
    },
    {
      name: "rs-skill-advisor",
      description: `Picks the "best" skill — it's handy.`
    }
  ]);
});

const SKILL_DIR = "/proj/.claude/skills/git-guide";
const DOWNLOADED = JSON.stringify({
  name: "git-guide",
  dir: SKILL_DIR,
  saved: [`${SKILL_DIR}/SKILL.md`]
});

// why: every invocation test needs the same host: a project root, the skill-loader answer
// and the SKILL.md the download left on disk.
function mockHost(
  on: any,
  answer: () => { text: string; isError?: boolean },
  skillMd: string | null = "# Git"
) {
  const calls: any[] = [];
  const reads: string[] = [];
  on("session.root", () => ({ value: "/proj" }));
  on("mcp.call", (_: unknown, e: any) => {
    calls.push(e);
    const { text, isError = false } = answer();
    return { value: { isError, content: [{ type: "text", text }] } };
  });
  on("fs.read", (_: unknown, e: any) => {
    reads.push(e.path);
    if (skillMd === null) throw new Error("ENOENT");
    return { value: skillMd };
  });
  return { calls, reads };
}

const run = ($: any, args = "") =>
  $.command.run({ command: "rs-git-guide", args } as never);

test("invoking /rs-<name> submits a prompt so the model starts a turn", async ($, on) => {
  const prompts: any[] = [];
  const clock = mock.clock(on, { now: 0 });
  mockHost(on, () => ({ text: DOWNLOADED }));
  on("prompt.submit", (_, e: any) => {
    prompts.push(e);
    return { text: e.text };
  });

  await run($, "rebase my branch");
  expect(prompts).toHaveLength(0);
  await clock.advance(1);

  expect(prompts).toHaveLength(1);
  expect(prompts[0].text).toContain("git-guide");
  expect(prompts[0].text).toContain("rebase my branch");
});

test("invoking /rs-<name> downloads the skill and injects the SKILL.md saved on disk", async ($, on) => {
  mock.clock(on, { now: 0 });
  const { calls, reads } = mockHost(on, () => ({ text: DOWNLOADED }));

  const out = await run($, "rebase my branch");

  expect(calls).toHaveLength(1);
  expect(calls[0].server).toBe("aipp_skill-loader");
  expect(calls[0].tool).toBe("download_remote_skill");
  expect(calls[0].args).toEqual({
    name: "git-guide",
    dest_dir: "/proj/.claude/skills"
  });
  expect(reads).toEqual([`${SKILL_DIR}/SKILL.md`]);
  expect(out.text).toBe("Skill git-guide carregada.");
  expect(out.context?.[0]).toContain("# Git");
  expect(out.context?.[0]).toContain(SKILL_DIR);
  expect(out.context?.[0]).toContain("rebase my branch");
});

test("loads the skill when a hook replaced the MCP answer with non-JSON text", async ($, on) => {
  mock.clock(on, { now: 0 });
  mockHost(on, () => ({
    text: "mcp__plugin_context-mode_context-mode__ctx_search({queries:[]})"
  }));

  const out = await run($);

  expect(out.text).toBe("Skill git-guide carregada.");
  expect(out.context?.[0]).toContain("# Git");
});

test("reports the files that failed to download", async ($, on) => {
  mock.clock(on, { now: 0 });
  mockHost(on, () => ({
    text: JSON.stringify({ dir: SKILL_DIR, errors: ["a.py: 404"] })
  }));

  const out = await run($);

  expect(out.context?.[0]).toContain("a.py: 404");
});

test("reports a loader error instead of reading a stale copy", async ($, on) => {
  mock.clock(on, { now: 0 });
  const { reads } = mockHost(on, () => ({
    text: JSON.stringify({ error: "not found in manifest" })
  }));

  const out = await run($);

  expect(out.text).toContain("Falha ao carregar skill git-guide");
  expect(out.text).toContain("not found in manifest");
  expect(reads).toEqual([]);
});

test("reports an MCP isError answer", async ($, on) => {
  mock.clock(on, { now: 0 });
  mockHost(on, () => ({ text: "boom", isError: true }));

  expect((await run($)).text).toContain("boom");
});

test("answers with the real reason when the MCP call throws", async ($, on) => {
  mock.clock(on, { now: 0 });
  mockHost(on, () => {
    throw new Error("no connected MCP tool");
  });

  const out = await run($);

  expect(out.text).toContain("Falha ao carregar skill git-guide");
});

test("answers with a failure when SKILL.md is not on disk", async ($, on) => {
  mock.clock(on, { now: 0 });
  mockHost(on, () => ({ text: DOWNLOADED }), null);

  expect((await run($)).text).toContain("Falha ao carregar skill git-guide");
});

test("skips index entries already available as local or plugin commands", async ($, on) => {
  const registered: string[] = [];
  on("fs.exists", () => ({ value: true }));
  on("fs.read", () => ({ value: INDEX }));
  on("command.list", () => ({
    value: [
      { name: "skill-advisor", description: "", source: "skills" },
      { name: "other:git-guide-x", description: "", source: "plugin" }
    ] as never
  }));
  on("command.register", (_, e: any) => {
    registered.push(e.name);
    return { value: { command: e.name } };
  });
  on("session.start", (_, e) => ({ cwd: e.cwd }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });

  expect(registered).toEqual(["rs-git-guide"]);
});

test("skips entries a plugin provides under its namespace", async ($, on) => {
  const registered: string[] = [];
  on("fs.exists", () => ({ value: true }));
  on("fs.read", () => ({ value: INDEX }));
  on("command.list", () => ({
    value: [{ name: "acme:git-guide", description: "", source: "plugin" }]
  }));
  on("command.register", (_, e: any) => {
    registered.push(e.name);
    return { value: { command: e.name } };
  });
  on("session.start", (_, e) => ({ cwd: e.cwd }));

  await $.session.start({ cwd: "/", surface: "terminal", isInteractive: true });

  expect(registered).toEqual(["rs-skill-advisor"]);
});
