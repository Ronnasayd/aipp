import { expect, test, type Plugin } from "claude-code/testing";

import { ask, engine, FILE } from "./helpers";

const Q = "Where to save?";
const multi = (labels: string[]) =>
  ask(Q, {
    multiSelect: true,
    options: labels.map((label) => ({ label, description: "d" }))
  });

test("free text: no option is checked and the answer says so", async ($, on) => {
  const { files, question } = engine($, on);
  await question({ answers: { [Q]: "neither, use S3" } }, ask());
  expect(files[FILE]).toContain("**Resposta livre:** neither, use S3\n");
  expect(files[FILE]).not.toContain("[x]");
});

test("multi-select checks every chosen label, even one holding a comma", async ($, on) => {
  const { files, question } = engine($, on);
  await question(
    { answers: { [Q]: "A, with comma, C" } },
    multi(["A", "A, with comma", "B", "C (Recommended)", "C"])
  );
  expect(files[FILE]!.match(/^- \[x\].*$/gm)).toEqual([
    "- [x] **A, with comma**",
    "- [x] **C**"
  ]);
  expect(files[FILE]).toContain("**Resposta:** A, with comma; C\n");
});

test("multi-select keeps text typed under Other next to the labels", async ($, on) => {
  const { files, question } = engine($, on);
  await question({ answers: { [Q]: "A, and also, mine" } }, multi(["A", "B"]));
  expect(files[FILE]!.match(/^- \[x\].*$/gm)).toEqual(["- [x] **A**"]);
  expect(files[FILE]).toContain("**Resposta:** A\n");
  expect(files[FILE]).toContain("**Resposta livre:** and also, mine\n");
});

test("notes and previews are kept, the fence outgrowing backticks inside", async ($, on) => {
  const { files, question } = engine($, on);
  await question(
    { answers: { [Q]: "Home" }, annotations: { [Q]: { notes: "for now" } } },
    ask(Q, {
      options: [
        { label: "Home", description: "d", preview: "```sh\nls\n```" },
        { label: "Project", description: "d" }
      ]
    })
  );
  expect(files[FILE]).toContain("**Nota:** for now\n");
  expect(files[FILE]).toContain("  ````\n  ```sh\n  ls\n  ```\n  ````\n");
});

test("multi-line descriptions stay inside their list item", async ($, on) => {
  const { files, question } = engine($, on);
  await question(
    { answers: { [Q]: "Home" } },
    ask(Q, {
      options: [
        { label: "Home", description: "one\n\ntwo" },
        { label: "B", description: "d" }
      ]
    })
  );
  expect(files[FILE]).toContain("- [x] **Home**\n  one\n\n  two\n");
});

test("a reply typed instead of picking is recorded as free text", async ($, on) => {
  const { files, question } = engine($, on);
  await question({ answers: {}, response: "let us talk first" }, ask());
  expect(files[FILE]).toContain("**Resposta livre:** let us talk first\n");
});

test("an answer the idle timeout gave is marked as such", async ($, on) => {
  const { files, question } = engine($, on);
  await question({ answers: { [Q]: "Home" }, afkTimeoutMs: 60000 }, ask());
  expect(files[FILE]).toContain("respondida automaticamente por inatividade");
});

test("unanswered, denied and errored calls write nothing", async ($, on) => {
  const { files, logs, question } = engine($, on);
  await question({ answers: {} }, ask());
  await question({ deny: "dismissed" }, ask());
  await question(
    { isError: true, result: "rejected", text: "rejected" },
    ask()
  );
  expect(files).toEqual({});
  expect(logs).toEqual([]);
});

test("only the answered questions of a call are recorded", async ($, on) => {
  const { files, question } = engine($, on);
  await question({ answers: { "One?": "Home" } }, ask("One?"), ask("Two?"));
  expect(files[FILE]!.match(/^## D\d+/gm)).toEqual(["## D1"]);
});

const asker: Plugin = {
  name: "asker",
  register: (on) => {
    on("turn.complete", async ($, e, next) => {
      await $.ui.ask("Swap model?", ["Home", "Project"]);
      return next(e);
    });
  }
};

test(
  "a question another mod asks is not a session decision",
  { plugins: [asker] },
  async ($, on) => {
    let asked = 0;
    on(
      "tool.call",
      { tool: "AskUserQuestion" },
      (_, e, next) => (asked++, next(e))
    );
    const { files, world } = engine($, on);
    on("turn.complete", () => ({ text: "" }));
    world.answer = { answers: { "Swap model?": "Home" } };
    await $.turn.complete({ turnId: "t1", answer: "ok" } as never);
    expect(asked).toBe(1);
    expect(files).toEqual({});
  }
);
