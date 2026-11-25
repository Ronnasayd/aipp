import type { EngineInterface, Register } from "claude-code";

type Option = { label: string; description?: string; preview?: string };
type Question = {
  question: string;
  header?: string;
  multiSelect?: boolean;
  options?: Option[];
};
type Answered = {
  questions: Question[];
  answers: Record<string, string>;
  response?: string;
  annotations?: Record<string, { notes?: string }>;
  afkTimeoutMs?: number;
};
type Decision = Question & {
  answer: string;
  notes?: string;
  timedOut: boolean;
  skill: string;
};

const RECOMMENDED = /\s*\((recommended|recomendad[oa])\)\s*$/i;

const two = (n: number) => String(n).padStart(2, "0");

function stamp(ms: number) {
  const d = new Date(ms);
  const date = `${d.getFullYear()}-${two(d.getMonth() + 1)}-${two(d.getDate())}`;
  return { date, time: `${date} ${two(d.getHours())}:${two(d.getMinutes())}` };
}

const bare = (label: string) => label.replace(RECOMMENDED, "");
const indent = (text: string) => text.replace(/\n(?=.)/g, "\n  ");

// why: a preview may hold a fenced block of its own, so ours must be longer
function fenced(text: string) {
  const runs = text.match(/`+/g)?.map((run) => run.length) ?? [];
  const fence = "`".repeat(Math.max(2, ...runs) + 1);
  return `${fence}\n${text.trimEnd()}\n${fence}`;
}

// why: a multi-select answer arrives comma-joined and a label may hold commas,
// so labels are matched longest first instead of splitting on ", "
function split(answer: string, labels: string[], multi: boolean) {
  if (labels.includes(answer)) return { chosen: [answer], free: "" };
  if (!multi) return { chosen: [], free: answer };
  const byLength = [...labels].sort((a, b) => b.length - a.length);
  const chosen: string[] = [];
  const free: string[] = [];
  for (let rest = answer; rest !== "";) {
    const label = byLength.find((l) => rest === l || rest.startsWith(`${l}, `));
    const piece = label ?? rest.split(", ")[0]!;
    (label ? chosen : free).push(piece);
    rest = rest.slice(piece.length).replace(/^, /, "");
  }
  return { chosen, free: free.join(", ") };
}

function optionLines(o: Option, chosen: boolean) {
  const mark = RECOMMENDED.test(o.label) ? " (recomendada)" : "";
  return [
    `- [${chosen ? "x" : " "}] **${bare(o.label)}**${mark}`,
    ...(o.description ? [`  ${indent(o.description)}`] : []),
    ...(o.preview ? [`\n  ${indent(fenced(o.preview))}\n`] : [])
  ].join("\n");
}

function section(d: Decision, n: number, time: string) {
  const options = d.options ?? [];
  const labels = options.map((o) => o.label);
  const { chosen, free } = split(d.answer, labels, d.multiSelect === true);
  const timedOut = d.timedOut
    ? ", respondida automaticamente por inatividade"
    : "";
  const footer = `${time}, skill: ${d.skill}${timedOut}`;
  return [
    `## D${n} - ${d.header ?? "Pergunta"}`,
    `**Pergunta:** ${d.question}`,
    chosen.length > 0 && `**Resposta:** ${chosen.map(bare).join("; ")}`,
    free && `**Resposta livre:** ${free}`,
    d.notes && `**Nota:** ${d.notes}`,
    options
      .map((o) => optionLines(o, chosen.includes(o.label)))
      .join("\n")
      .trimEnd(),
    `_${footer}_\n`
  ]
    .filter(Boolean)
    .join("\n\n");
}

function isAnswered(result: unknown): result is Answered {
  const { questions, answers } = (result ?? {}) as Partial<Answered>;
  return (
    Array.isArray(questions) && typeof answers === "object" && answers !== null
  );
}

function toDecisions(answered: Answered, skill: string): Decision[] {
  return answered.questions.flatMap((q) => {
    const answer = answered.answers[q.question] || answered.response;
    if (!answer) return [];
    const notes = answered.annotations?.[q.question]?.notes;
    return [{ ...q, answer, notes, timedOut: !!answered.afkTimeoutMs, skill }];
  });
}

async function header(
  $: EngineInterface,
  sid: string,
  root: string,
  time: string
) {
  const git = await $.process
    .run(["git", "branch", "--show-current"])
    .catch(() => undefined);
  const branch = git?.exitCode === 0 ? git.stdout.trim() : "";
  return [
    "# Registro de decisões\n",
    `- Sessão: ${sid}`,
    `- Retomar: \`claude --resume ${sid}\``,
    `- Projeto: ${root.split("/").pop()}`,
    ...(branch ? [`- Branch: ${branch}`] : []),
    `- Início: ${time}\n`
  ].join("\n");
}

async function sessionFile($: EngineInterface, dir: string, sid: string) {
  const suffix = `-${sid.slice(0, 8)}.md`;
  const entries = (await $.fs.exists(dir)) ? await $.fs.list(dir) : [];
  return entries.find((f) => f.name.endsWith(suffix))?.name;
}

const lastNumber = (text: string) =>
  Math.max(0, ...[...text.matchAll(/^## D(\d+)/gm)].map((m) => Number(m[1])));

async function record($: EngineInterface, sid: string, decisions: Decision[]) {
  // why: repo().root is the main working tree, so removing a worktree keeps its log
  const root = (await $.session.repo())?.root ?? (await $.session.root());
  const dir = `${root}/.decisions`;
  const { date, time } = stamp(await $.clock.now());
  const ignore = `${dir}/.gitignore`;
  if (!(await $.fs.exists(ignore))) await $.fs.write(ignore, "*\n");

  // why: looked up by id, not by today's date, so a resumed session keeps its file
  const found = await sessionFile($, dir, sid);
  const path = `${dir}/${found ?? `${date}-${sid.slice(0, 8)}.md`}`;
  const before = found
    ? await $.fs.read(path)
    : await header($, sid, root, time);
  const start = lastNumber(before) + 1;
  const sections = decisions.map((d, i) => section(d, start + i, time));
  await $.fs.write(path, [`${before.trimEnd()}\n`, ...sections].join("\n"));
}

export const register: Register = (on) => {
  // why: each record reads the file and writes it back whole; parallel calls would drop decisions
  let queue: Promise<unknown> = Promise.resolve();
  // why: keyed by session, since /clear changes the id without reloading the module
  const skills = new Map<string, string>();

  on("skill.prompt", async ($, e, next) => {
    skills.set(await $.session.id(), e.skill);
    return next(e);
  });

  on("tool.call", { tool: "AskUserQuestion" }, async ($, e, next) => {
    const ran = await next(e);
    // why: a question another mod asks ($.ui.ask) is not a decision of the session
    if (next.origin.plugin !== "engine") return ran;
    if (ran.deny !== undefined || ran.isError) return ran;
    queue = queue
      .then(async () => {
        const sid = await $.session.id();
        const answered: unknown = ran.result;
        if (!isAnswered(answered))
          throw new Error("formato de resultado desconhecido");
        const decisions = toDecisions(answered, skills.get(sid) ?? "nenhuma");
        if (decisions.length > 0) await record($, sid, decisions);
      })
      .catch((error) =>
        $.ui.log(`decision-log: decisão não gravada: ${String(error)}`)
      );
    await queue;
    return ran;
  });
};
