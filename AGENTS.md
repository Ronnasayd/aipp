## Project Architecture

**AI Pair Programming Workspace** — toolkit for enhancing AI-assisted development. Centralizes agent personas, skills, and structured workflows.

### Core Components

- **MCP Servers** (`src/mcps/`): FastMCP-based tools — `skill_loader_mcp.py`, `search_engine.py` (semantic search). Registered proxies (DB, GitHub, Figma, etc.) are routed through `mcp-manager` and configured in `.mcp.json`.
- **Agents** (`agents/`): Persona definitions (developer-specialist, cybersecurity-specialist, etc.) with behavioral instructions.
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

## Mandatory rules that must always be followed

- Every user question → interactive tool, never plain text. Claude:
  `AskUserQuestion`. Multiple questions: `grilling` skill.

- `AskUserQuestion` questions must be fully contextualized, never terse. Each
  question's body must explain _why_ it's being asked (what was found in the
  code, what trade-off is at stake) before stating the choice. Each option's
  `description` must explain what picking it actually does/causes — not just
  restate the label. Never submit a question or option whose text would be
  truncated or cut short; write the full explanation every time.

- When user asks a question → answer only. Do not modify code without user's
  explicit authorization first.

- When task list exists (multi-step work), use `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` to give user feedback. Mark tasks complete as done, don't batch.

- Whenever you modify a component or screen → run tests using Playwright (or a similar E2E tool) before finalizing.

- Whenever lint, type, or test errors are reported in files you have touched, fix them — even if they were not caused by your own changes.

- Never treat documentation (`markdown files`,`memories`) as absolute truth. Only the implemented code should be treated as the truth.

- Never assume the code is correct without tests to validate it.

- TDD mandatory when repo/project already adopts tests (existing test suite/framework present): write failing test first (Red), then minimal code to pass (Green), then refactor. No large unverified code blocks — small loops only. If repo has no test setup, don't impose one unprompted.

- Evidence over trust: before asking human review, provide proof change works — passing test logs, screenshots/recordings of E2E or visual tests. No "should work" claims.

- Vertical slices only: implement thin end-to-end slices (tracer bullets) through all layers, not horizontal layers (all DB, then all API, then all UI). Each slice testable and validated before next.

- Whenever you complete a task (such as testing, execution, or building), immediately terminate all background processes and servers that were started, and delete any temporary directories that were generated.

- In any time evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.

## Mandatory rules for hallucination protection mechanisms

- Allowed to say "I don't know": when uncertain or information is missing, state it explicitly (e.g. "I don't have enough information to confidently assess this"). Never fill gaps with guesses.

- Quote before analyzing: for long documents (>20k tokens), first extract word-for-word quotes relevant to the task, then base the analysis only on those quotes, referencing them by number. If none found, say "No relevant quotes found"

- Cite every factual claim: each claim about code, docs, or external sources must carry its source (`path:line`, command output, URL, or direct quote) so it can be audited.

- Verify after generating: review each claim in the response and find a supporting quote/source. If none can be found, retract the claim (mark removal with `[]` when editing a document).

## Context-Specific Rules

The following rules apply to specific file types:

- [code.instructions](.claude/instructions/code.instructions.md) — applies to: `**/*.ts, **/*.js, **/*.py, **/*.java, **/*.go, **/*.css, **/*.cpp, **/*.c, **/*.vue, **/*.jsx, **/*.tsx`

<!-- END:AUTO-GENERATED-CONTEXT:DO-NOT-MODIFY -->
