import { expect, test } from "claude-code/testing";

import { ask, engine, FILE, NOON } from "./helpers";

const home = { answers: { "Where to save?": "Home" } };

test("appends to the session file and keeps manual edits", async ($, on) => {
  const { files, question } = engine($, on);
  await question(home, ask());
  files[FILE] = files[FILE]!.replace("Near the code.", "EDITED");

  await question(home, ask());

  expect(files[FILE]).toContain("EDITED");
  expect(files[FILE]!.match(/^# Registro/gm)).toHaveLength(1);
  expect(files[FILE]!.match(/^## D\d+/gm)).toEqual(["## D1", "## D2"]);
});

test("numbers after the highest decision left in the file", async ($, on) => {
  const { files, question } = engine($, on);
  await question(home, ask());
  await question(home, ask());
  files[FILE] = files[FILE]!.replace(/## D1 [\s\S]*?(?=## D2)/, "");

  await question(home, ask());

  expect(files[FILE]!.match(/^## D\d+/gm)).toEqual(["## D2", "## D3"]);
});

test("separates sections when a manual edit dropped the final newline", async ($, on) => {
  const { files, question } = engine($, on);
  await question(home, ask());
  files[FILE] = files[FILE]!.trimEnd();

  await question(home, ask());

  expect(files[FILE]).toContain("nenhuma_\n\n## D2");
});

test("resumed on another day, keeps writing to the first day's file", async ($, on) => {
  const { files, world, question } = engine($, on);
  await question(home, ask());
  world.now = NOON + 3 * 24 * 3600 * 1000;

  await question(home, ask());

  expect(Object.keys(files).filter((f) => f.endsWith(".md"))).toEqual([FILE]);
  expect(files[FILE]).toContain("_2026-11-27 12:05");
});

test("/clear moves to a new session id, so a new file", async ($, on) => {
  const { files, world, question } = engine($, on);
  await question(home, ask());
  world.sid = "aaaabbbb-0000-0000-0000-000000000000";

  await question(home, ask());

  expect(files["/repo/.decisions/2026-11-24-aaaabbbb.md"]).toContain("## D1");
  expect(files[FILE]).not.toContain("## D2");
});

test("parallel calls keep every decision", async ($, on) => {
  const { files, question } = engine($, on);
  await Promise.all([1, 2, 3].map(() => question(home, ask())));
  expect(files[FILE]!.match(/^## D\d+/gm)).toEqual(["## D1", "## D2", "## D3"]);
});

test("leaves an existing .gitignore alone", async ($, on) => {
  const { files, question } = engine($, on);
  files["/repo/.decisions/.gitignore"] = "mine\n";
  await question(home, ask());
  expect(files["/repo/.decisions/.gitignore"]).toBe("mine\n");
});
