# AIPP

AI Pair Programming Workspace: a toolkit of agents, skills, instructions, hooks and MCP servers that shapes how AI coding agents work in a project.

## Language

### Agents

**Role agent**:
An agent definition in `agents/` with one fixed job, a tool allowlist and a model limit.
_Avoid_: Persona, specialist, subagent

**Retired persona**:
A former agent definition kept in `legacy/agents/` and no longer installed.
_Avoid_: Legacy agent, old specialist

### Skills and instructions

**Skill**:
A packaged set of instructions (a `SKILL.md` plus adjacent files) that an agent loads to perform one kind of task.
_Avoid_: Command, workflow, prompt

**Forked skill**:
A Skill declared with `context: fork`, which runs in a separate agent context instead of the caller's conversation.
_Avoid_: Background skill, subagent skill

**Remote skill**:
A Skill served from the AIPP repository by the skill-loader MCP server rather than installed locally.
_Avoid_: Downloaded skill, cloud skill

**Instruction**:
A domain-specific rule file in `instructions/` that applies to files matching its `applyTo` pattern.
_Avoid_: Rule, guideline, convention file

### MCP

**Backend server**:
An MCP server reached only through the `mcp-manager` proxy, not registered directly with the agent.
_Avoid_: Proxied MCP, MCP tool

### Claude mods

**Dev-mod**:
A Claude Code interface or behaviour extension that lives in `claude/dev-mods/`.
_Avoid_: Plugin, extension, mod

**Band**:
A strip of interactive UI that a Dev-mod renders inside the Claude Code interface.
_Avoid_: Panel, bar, widget

**Statusline badge**:
A short label that a Dev-mod adds to the Claude Code status line.
_Avoid_: Indicator, tag

**Decision log**:
The per-session record of the questions an agent asked the user, the options offered and the answers chosen.
_Avoid_: Question history, grilling log, decision history

### Harness

**Harness**:
The set of gates (in `tlc-harness-toolkit/`) that decide whether an agent's turn may stop.
_Avoid_: Guardrails, gate system

**Grind**:
The Harness mode that runs the lint and test gates at stop and sends the agent back to work when they fail, up to a loop limit.
_Avoid_: Auto-fix loop, retry loop

**Ship claim**:
An explicit `HARNESS_SHIP_CLAIM:` line in which the agent declares the work done; it is the only signal the ship gate reacts to.
_Avoid_: Done message, completion claim

**Evidence dir**:
The directory where verification proof (test logs, verdicts) must exist before a Ship claim is accepted.
_Avoid_: Proof folder, artifacts dir

**Lesson**:
A ranked, reusable rule the Harness learned from a past failure and injects at session start.
_Avoid_: Tip, hint

### Memory

**Durable page**:
A permanent ai-memory page that holds a rule, gotcha, procedure or decision.
_Avoid_: Note, memory, wiki entry

**Handoff**:
A single-use ai-memory record that carries open work from one session to the next.
_Avoid_: Resume note, session summary

**Observation**:
A bounded record of a prompt or tool event that lifecycle hooks capture into ai-memory automatically.
_Avoid_: Log entry, event

### Process

**Vertical slice**:
A thin end-to-end piece of a feature that crosses every layer and is tested before the next one starts.
_Avoid_: Tracer bullet, feature slice, horizontal layer
