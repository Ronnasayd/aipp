import type { Register } from "claude-code";

const INDEX = ".claude/skills/index.yaml";
const PREFIX = "rs-";
// why: tool-name spelling of the "aipp:skill-loader" server, accepted by $.mcp.call.
const SERVER = "aipp_skill-loader";

type Entry = { name: string; description: string };
type Download = { errors?: string[]; error?: string };

// hazard: PostToolUse hooks (context-mode) replace answers over 4096 B with a non-JSON excerpt,
// so an unparsable answer says nothing about whether the download worked; the disk does.
function parseDownload(text: string): Download {
  try {
    return (JSON.parse(text) as Download | null) ?? {};
  } catch {
    return {};
  }
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
    let content: string;
    let files: string;
    // why: a throwing command.run hook is skipped and the user only sees the host's misleading
    // "no command.run hook answered", so every failure becomes an answer.
    try {
      // why: the MCP server's own cwd is not guaranteed to be the project.
      const skills = `${await $.session.root()}/.claude/skills`;
      const res = await $.mcp.call(SERVER, "download_remote_skill", {
        name,
        dest_dir: skills
      });
      const raw = res.content
        .map((b) => (b as { text?: string }).text ?? "")
        .join("");
      const { error, errors } = parseDownload(raw);
      if (res.isError || error) throw new Error(error ?? raw);

      const dir = `${skills}/${name}`;
      const skillMd = await $.fs.read(`${dir}/SKILL.md`);
      if (typeof skillMd !== "string" || !skillMd)
        throw new Error(`SKILL.md vazio ou ilegível em ${dir}`);
      content = skillMd;
      files =
        `\n\nSkill files saved to ${dir}; resolve relative paths in the skill from that directory.` +
        (errors?.length ? ` Failed: ${errors.join("; ")}` : "");
    } catch (err) {
      return {
        text: `Falha ao carregar skill ${name}: ${err instanceof Error ? err.message : String(err)}`
      };
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
      context: [`Follow this skill "${name}":\n\n${content}${files}${task}`]
    };
  });
};
