import type { TestBody } from "claude-code/testing";

type Harness = Parameters<TestBody>;

export const SID = "04fb6267-ee52-4467-a36e-6cc612f41a19";
export const NOON = new Date(2026, 10, 24, 12, 5).getTime();
export const FILE = "/repo/.decisions/2026-11-24-04fb6267.md";

export const ask = (question = "Where to save?", extra: object = {}) => ({
  question,
  header: "Local",
  multiSelect: false,
  options: [
    { label: "Project (Recommended)", description: "Near the code." },
    { label: "Home", description: "Never dirties a repo." }
  ],
  ...extra
});

export function engine($: Harness[0], on: Harness[1]) {
  const files: Record<string, string> = {};
  const logs: string[] = [];
  const world = {
    sid: SID,
    now: NOON,
    repoRoot: "/repo" as string | null,
    branch: "main",
    gitError: undefined as string | undefined,
    readError: undefined as string | undefined,
    writeError: undefined as string | undefined,
    answer: {} as object
  };
  on("session.id", () => ({ value: world.sid }));
  on("session.root", () => ({ value: "/plain" }));
  on("session.repo", () => ({
    value: world.repoRoot
      ? ({ root: world.repoRoot, remote: null, internal: false } as never)
      : null
  }));
  on("clock.now", () => ({ value: world.now }));
  on("process.run", () => {
    if (world.gitError) throw new Error(world.gitError);
    const exitCode = world.repoRoot ? 0 : 128;
    const stdout = world.repoRoot ? `${world.branch}\n` : "";
    return { value: { exitCode, stdout, stderr: "" } as never };
  });
  on("fs.exists", (_, e) => ({
    value: Object.keys(files).some(
      (f) => f === e.path || f.startsWith(`${e.path}/`)
    )
  }));
  on("fs.list", (_, e) => ({
    value: Object.keys(files)
      .filter((f) => f.startsWith(`${e.path}/`))
      .map((f) => ({
        name: f.slice(`${e.path}/`.length),
        kind: "file"
      })) as never
  }));
  on("fs.read", (_, e) => {
    if (world.readError) throw new Error(world.readError);
    return { value: files[e.path]! };
  });
  on("fs.write", (_, e) => {
    if (world.writeError) throw new Error(world.writeError);
    files[e.path] = e.text;
    return { value: undefined };
  });
  on("ui.log", (_, e) => (logs.push(e.text), { value: undefined }));
  on("skill.prompt", (_, e) => ({ text: e.text }));
  on("tool.call", { tool: "AskUserQuestion" }, (_, e) => {
    const fixed = world.answer as { deny?: string; isError?: true };
    if (fixed.deny || fixed.isError) return fixed as never;
    return {
      result: { questions: e.questions, answers: {}, ...world.answer }
    } as never;
  });
  // why: the typed call overloads hit TS2589 on an input built for no one tool
  const call = $.tool.call as unknown as (input: object) => Promise<{
    result?: unknown;
    deny?: string;
  }>;
  const question = (answer: object, ...questions: object[]) => {
    world.answer = answer;
    return call({ tool: "AskUserQuestion", questions });
  };
  return { files, logs, world, question };
}
