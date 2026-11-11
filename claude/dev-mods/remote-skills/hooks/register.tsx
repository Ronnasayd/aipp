import type { Register } from "claude-code";

const INDEX = ".claude/skills/index.yaml";
const PREFIX = "rs-";
// why: tool-name spelling of the "aipp:skill-loader" server, accepted by $.mcp.call.
const SERVER = "aipp_skill-loader";

type Entry = { name: string; description: string };

// hazard: ponytail shortcut — parses only the shape build-skill-index.py writes (one name, plain or
// single-quoted description); switch to an index.json if the format grows.
export function parseIndex(text: string): Entry[] {
  return text
    .split(/^- name:\s*$/m)
    .slice(1)
    .flatMap((block) => {
      const name = block.match(/^\s+- (\S+)/m)?.[1];
      const raw = block.split(/^\s+description:/m)[1];
      if (!name || raw === undefined) return [];
      let description = raw.replace(/\s+/g, " ").trim();
      if (description.startsWith("'") && description.endsWith("'"))
        description = description.slice(1, -1).replace(/''/g, "'");
      return [{ name, description: description.slice(0, 200) }];
    })
    .filter((e) => /^[A-Za-z0-9_-]{1,61}$/.test(e.name));
}

export const register: Register = (on) => {
  on("session.start", async ($, e, next) => {
    // invariant: projects without aipp's install have no index symlink; register nothing.
    if (await $.fs.exists(INDEX)) {
      const text = await $.fs.read(INDEX);
      if (typeof text === "string")
        for (const { name, description } of parseIndex(text))
          await $.command.register({
            name: PREFIX + name,
            description,
            argumentHint: "[task]"
          });
    }
    return next(e);
  });

  on("command.run", async ($, e, next) => {
    if (!e.command.startsWith(PREFIX)) return next(e);
    const name = e.command.slice(PREFIX.length);
    const res = await $.mcp.call(SERVER, "get_remote_skill", { name });
    const block = res.content.find((b) => b.type === "text") as
      { text?: string } | undefined;
    const data = (res.structuredContent ?? JSON.parse(block?.text ?? "{}")) as {
      content?: string;
      files?: string[];
      error?: string;
    };
    if (res.isError || !data.content)
      return {
        text: `Falha ao carregar skill ${name}: ${data.error ?? block?.text ?? "sem conteúdo"}`
      };

    const files = data.files?.length
      ? `\n\nAdjacent files (fetch with ${SERVER} get_remote_skill_file): ${data.files.join(", ")}`
      : "";
    const task = e.args.trim() ? `\n\nTask: ${e.args.trim()}` : "";
    return {
      text: `Skill ${name} carregada.`,
      context: [
        `Follow this skill "${name}":\n\n${data.content}${files}${task}`
      ]
    };
  });
};
