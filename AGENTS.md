## Project Architecture

**AI Pair Programming Workspace** — toolkit for enhancing AI-assisted development. Centralizes agent personas, skills, and structured workflows.

### Core Components

- **MCP Servers** (`src/mcps/`): FastMCP-based tools — `skill_loader_mcp.py`, `search_engine.py` (semantic search). Registered proxies (DB, GitHub, Figma, etc.) are routed through `mcp-manager` and configured in `.mcp.json`.
- **Agents** (`agents/`): Role agents (developer, planner, reviewer, qa, explorer specialists) with tool and model limits. Retired persona agents are in `legacy/agents/`.
- **Skills** (`skills/`): Reusable capabilities (workflows, guides, analysis patterns).
- **Instructions** (`instructions/`): Domain-specific rules (code style, testing, React patterns, etc.).

### Directory Reference

```
src/            MCP servers, utilities, copilot proxy
agents/         Agent persona YAML/markdown definitions
skills/         Skill files (workflows, style guides)
instructions/   Domain-specific rules and conventions
scripts/        Installation and environment setup
commands/       CLI command definitions
hooks/          Event-driven automation (Claude Code hooks)
lefthook/       Git hooks (managed by lefthook)
docs/           Project documentation
```

## Key Technologies

- **Python 3.11+** with `uv` for dependency management (`uv.lock` at root; `src/` builds with setuptools)
- **FastMCP** (`fastmcp>=2.0`): Model Context Protocol server framework
- **pytest**: Test framework (`asyncio_mode = "auto"`)
- **Node.js/TypeScript**: Supported for various project types
- **Bash**: Installation and environment scripts

## Quick Start Commands

Install and setup:

```bash
uv sync                         # Install root Python deps (hook scripts)
cd src && uv sync               # Install MCP server deps
./install.sh [--all|--claude]   # Set up symlinks, lefthook, and configurations
```

Run tests:

```bash
uv run --with pytest pytest scripts/  # Run script tests
```

Run MCP servers:

```bash
cd src && uv run skill-loader-mcp    # skill-loader MCP server
```

<!-- INIT:AUTO-GENERATED-CONTEXT:DO-NOT-MODIFY -->


## Mandatory rules — always follow

- User question → interactive tool, never plain text. Claude: `AskUserQuestion`. Many questions: `grilling` skill. Rule = HOW to ask; WHEN to ask = harness posture. Every needed question (incl. a BLOCKED `NEED` requiring user decision) → `AskUserQuestion`.

- `AskUserQuestion` must be fully contextualized, never terse. Question body: explain _why_ asked (what found in code, what trade-off) before choice. Option `description`: what picking it does/causes — not label restated. No truncated question/option text; full explanation every time.

- User asks question → answer only. No code change without explicit user authorization.

- Multi-step work → use `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` for feedback. Mark each task complete when done, no batching.

- Modify component/screen → run Playwright (or similar E2E) tests before finalizing.

- Lint/type/test errors in touched files → fix, even if not caused by you.

- Docs (`markdown files`, `memories`) not absolute truth. Only implemented code = truth.

- No code assumed correct without tests validating it.

- TDD mandatory when repo already has tests (suite/framework present): failing test first (Red), minimal code to pass (Green), then refactor. Small loops only, no big unverified blocks. No test setup in repo → don't impose one unprompted.

- Mutation testing mandatory when repo already has tests and code modified: mutate only changed lines/hunks, run suite, surviving mutant → add/strengthen test until killed. Repo has mutation lib/framework → use it. None → mutate independently (manual edits or ad-hoc tool), revert every mutant after. Report killed/survived counts as evidence.

- Impact analysis on every file change: map inbound deps (inputs, params, consumed contracts) + outbound (outputs, returns, events, side effects, exposed contracts). Search project-wide (text + semantic) for every reference to changed file/functions/classes/interfaces/behaviors. Verify dependents keep contract/behavior compat; contract changed on purpose → fix every impacted site. Relevant change (esp. feat/fix) → find + update docs referencing changed file/feature/module; docs must match code. Goal: no inconsistency, regression, broken contract, stale reference, divergent docs.

- Evidence over trust: before human review, give proof change works — passing test logs, screenshots/recordings of E2E or visual tests. No "should work" claims.

- Vertical slices only: thin end-to-end slices (tracer bullets) through all layers, not horizontal layers (all DB, then all API, then all UI). Each slice tested and validated before next.

- Simplicity proportional to problem: minimum abstractions, deps, components, rules that solve the need. No accidental complexity, premature generalization, duplication, unneeded mechanisms. Never oversimplify problems that need structure: keep essential complexity, organize it clear, cohesive, consistent. Every architectural decision/abstraction needs concrete justification. Prioritize readability, maintainability, low coupling, high cohesion, existing contracts/behaviors. Goal not smallest code: clearest, most robust, efficient solution, complexity strictly justified by problem.

- Task done (testing, execution, build) → kill all background processes/servers started, delete temp dirs generated.

- Anytime: evaluate what worth saving as permanent memory. Save only what next session needs and can't rediscover from code, Git, or CLAUDE.md — _reason_ behind decision, non-obvious invariant, user preference. Already in repo or only relevant to this conversation → don't save. Persist via `ai-memory-durable-pages` skill.

- Permanent memory scope: generic info → save in `_global` (`memory_write_page` with `scope: "global"`). Project pages hold only what is specific to that project. Mixed content → split: generic part in `_global`, specific part in project. Before writing, search `_global` and update the existing page, never duplicate per project.

- Domain vocabulary: `GLOSSARY.md` (or `GLOSSARY-MAP.md`) exists → read before naming things, use its terms exactly. Term resolved/changed with user, or term conflicts with glossary → update via `domain-modeling` skill. No glossary yet → create it only once first term agreed with user, never from agent inference alone. Glossary holds terms only.

- Self-contained task (no dependency on history, clear input, concise output, intermediate work not required in the main conversation) → use a sub-agent. Standing user authorization to spawn, only when these criteria met; goal: keep main context small.

- Output style by consumer. Consumer = agent (prompts, skills, instructions, agent-facing files, sub-agent briefs, reasoning) → maximally compact, ultracave style: keep core idea, cut everything else. Consumer = human/user → maximally descriptive and clear, technical language per STE100 (`ste` skill).

- Plugin scope: caveman → agent-facing text only, never user replies. ponytail → production code size only; never reduces TDD, mutation testing, or mandatory lint fixes.

## Mandatory rules — hallucination protection

- "I don't know" allowed: uncertain or info missing → say so explicitly (e.g. "I don't have enough information to confidently assess this"). Never fill gaps with guesses.

- Quote before analyzing: long docs (>20k tokens) → first extract word-for-word quotes relevant to task, base analysis only on them, reference by number. None found → say "No relevant quotes found".

- Cite every factual claim: each claim about code, docs, external sources carries source (`path:line`, command output, URL, direct quote) for audit.

- Verify after generating: check each claim in response has supporting quote/source. None → retract claim (mark removal with `[]` when editing document).

## Context-Specific Rules

The following rules apply to specific file types:
- [code.instructions](.claude/instructions/code.instructions.md) — applies to: `**/*.ts, **/*.js, **/*.py, **/*.java, **/*.go, **/*.css, **/*.cpp, **/*.c, **/*.vue, **/*.jsx, **/*.tsx`
<!-- END:AUTO-GENERATED-CONTEXT:DO-NOT-MODIFY -->
