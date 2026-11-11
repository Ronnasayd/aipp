import { expect, test } from "claude-code/testing";

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

test("invoking /rs-<name> injects SKILL.md as model context", async ($, on) => {
  const calls: any[] = [];
  on("mcp.call", (_, e: any) => {
    calls.push(e);
    return {
      value: {
        isError: false,
        content: [
          {
            type: "text",
            text: JSON.stringify({
              name: "git-guide",
              content: "# Git",
              files: ["a.md"]
            })
          }
        ]
      }
    };
  });

  const out = await $.command.run({
    command: "rs-git-guide",
    args: "rebase my branch"
  });

  expect(calls[0].server).toBe("aipp_skill-loader");
  expect(calls[0].tool).toBe("get_remote_skill");
  expect(calls[0].args).toEqual({ name: "git-guide" });
  expect(out.text).toBe("Skill git-guide carregada.");
  expect(out.context?.[0]).toContain("# Git");
  expect(out.context?.[0]).toContain("a.md");
  expect(out.context?.[0]).toContain("rebase my branch");
});
