import type { Register } from "claude-code";

const INDEX = ".claude/skills/index.yaml";
const PREFIX = "rs-";
// why: tool-name spelling of the "aipp:skill-loader" server, accepted by $.mcp.call.
const SERVER = "aipp_skill-loader";

type Entry = { name: string; description: string };
type McpResult = { content: { type: string }[]; structuredContent?: unknown };

// why: skill-loader tools return a JSON dict either as structuredContent or as a text block.
function parseResult<T>(res: McpResult): { data: T; text?: string } {
  const text = (
    res.content.find((b) => b.type === "text") as { text?: string } | undefined
  )?.text;
  return {
    data: (res.structuredContent ?? JSON.parse(text ?? "{}")) as T,
    text
  };
}

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
      // why: a skill installed locally or by a plugin (`plugin:name`) already has a
      // command; registering rs-<name> too would duplicate it.
      const local = new Set(
        (await $.command.list()).map((c) => c.name.split(":").pop())
      );
      if (typeof text === "string")
        for (const { name, description } of parseIndex(text))
          if (!local.has(name))
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
    const { data, text: raw } = parseResult<{
      content?: string;
      files?: string[];
      error?: string;
    }>(res);
    if (res.isError || !data.content)
      return {
        text: `Falha ao carregar skill ${name}: ${data.error ?? raw ?? "sem conteúdo"}`
      };

    let files = "";
    if (data.files?.length) {
      // why: scripts the SKILL.md runs by relative path must exist on disk; the MCP
      // server's own cwd is not guaranteed to be the project, so pass an absolute dir.
      const saved = await $.mcp.call(SERVER, "download_remote_skill", {
        name,
        dest_dir: `${await $.session.root()}/.claude/skills`
      });
      const { data: out, text } = parseResult<{
        dir?: string;
        errors?: string[];
        error?: string;
      }>(saved);
      files = out.dir
        ? `\n\nSkill files saved to ${out.dir} (${data.files.join(", ")}); resolve relative paths in the skill from that directory.` +
          (out.errors?.length ? ` Failed: ${out.errors.join("; ")}` : "")
        : `\n\nAdjacent files (download failed: ${out.error ?? text}; fetch with ${SERVER} get_remote_skill_file): ${data.files.join(", ")}`;
    }
    const task = e.args.trim() ? `\n\nTask: ${e.args.trim()}` : "";
    // why: a command.run answer only records context and never starts a model turn.
    // hazard: the host refuses prompt.submit from inside a command.run hook (it would wait
    // on the turn the hook holds), so a timer submits it once this hook has returned.
    $.clock.after(0, () =>
      $.prompt.submit({
        text: `Follow the "${name}" skill loaded above.${task}`,
        asUser: true
      })
    );
    return {
      text: `Skill ${name} carregada.`,
      context: [
        `Follow this skill "${name}":\n\n${data.content}${files}${task}`
      ]
    };
  });
};
