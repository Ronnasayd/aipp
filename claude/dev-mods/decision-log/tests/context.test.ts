import { expect, test } from "claude-code/testing";

import { ask, engine, FILE } from "./helpers";

const home = { answers: { "Where to save?": "Home" } };

test("each decision names the latest skill of its own session", async ($, on) => {
  const { files, world, question } = engine($, on);
  const skill = (name: string) =>
    $.skill.prompt({ skill: name, text: "go", frontmatter: {} });

  await skill("sd-grilling");
  await question(home, ask());
  await skill("grilling");
  await question(home, ask());
  expect(files[FILE]!.match(/skill: \S+(?=_)/g)).toEqual([
    "skill: sd-grilling",
    "skill: grilling"
  ]);

  world.sid = "aaaabbbb-0000-0000-0000-000000000000";
  await question(home, ask());
  expect(files["/repo/.decisions/2026-11-24-aaaabbbb.md"]).toContain(
    "skill: nenhuma_"
  );
});

test("passes the skill prompt through unchanged", async ($, on) => {
  engine($, on);
  const out = await $.skill.prompt({ skill: "a", text: "go", frontmatter: {} });
  expect(out.text).toBe("go");
});

test("outside git, writes under the session root with no branch line", async ($, on) => {
  const { files, world, question } = engine($, on);
  world.repoRoot = null;
  await question(home, ask());
  const text = files["/plain/.decisions/2026-11-24-04fb6267.md"];
  expect(text).toContain("- Projeto: plain\n- Início:");
});

test("detached HEAD leaves the branch line out", async ($, on) => {
  const { files, world, question } = engine($, on);
  world.branch = "";
  await question(home, ask());
  expect(files[FILE]).not.toContain("- Branch:");
});

test("a git that cannot start still records the decision", async ($, on) => {
  const { files, world, question } = engine($, on);
  world.gitError = "ENOENT git";
  await question(home, ask());
  expect(files[FILE]).toContain("## D1");
});

test("a failed write warns, keeps the answer and the next call still records", async ($, on) => {
  const { files, logs, world, question } = engine($, on);
  world.writeError = "EACCES";
  const ran = await question(home, ask());
  expect((ran.result as { answers: object }).answers).toEqual(home.answers);
  expect(logs).toHaveLength(1);
  expect(logs[0]).toContain("decision-log");

  world.writeError = undefined;
  await question(home, ask());
  expect(files[FILE]).toContain("## D1");
});

test("an unreadable session file is never overwritten", async ($, on) => {
  const { files, logs, world, question } = engine($, on);
  await question(home, ask());
  const before = files[FILE];
  world.readError = "EIO";
  await question(home, ask());
  expect(files[FILE]).toBe(before!);
  expect(logs).toHaveLength(1);
});

test("a result shape this build does not know warns and keeps the answer", async ($, on) => {
  const { files, logs, question } = engine($, on);
  const ran = await question({ answers: null, questions: "?" }, ask());
  expect(ran.result).toEqual({ answers: null, questions: "?" });
  expect(files).toEqual({});
  expect(logs).toHaveLength(1);
});
