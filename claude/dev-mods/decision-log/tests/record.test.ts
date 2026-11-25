import { expect, test } from "claude-code/testing";

import { ask, engine, FILE, SID } from "./helpers";

test("writes one answered question with header, options and answer", async ($, on) => {
  const { files, question } = engine($, on);

  const ran = await question(
    { answers: { "Where to save?": "Project (Recommended)" } },
    ask()
  );

  expect((ran.result as { answers: object }).answers).toEqual({
    "Where to save?": "Project (Recommended)"
  });
  expect(files[FILE]).toBe(`# Registro de decisões

- Sessão: ${SID}
- Retomar: \`claude --resume ${SID}\`
- Projeto: repo
- Branch: main
- Início: 2026-11-24 12:05

## D1 - Local

**Pergunta:** Where to save?

**Resposta:** Project

- [x] **Project** (recomendada)
  Near the code.
- [ ] **Home**
  Never dirties a repo.

_2026-11-24 12:05, skill: nenhuma_
`);
  expect(files["/repo/.decisions/.gitignore"]).toBe("*\n");
});

test("records each question of one call as its own decision", async ($, on) => {
  const { files, question } = engine($, on);
  await question(
    { answers: { "One?": "Home", "Two?": "Home" } },
    ask("One?"),
    ask("Two?")
  );
  expect(files[FILE]!.match(/^## D\d+/gm)).toEqual(["## D1", "## D2"]);
});
