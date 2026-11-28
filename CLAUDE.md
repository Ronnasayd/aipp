# Instructions

Always Read and follow [`AGENTS.md`](AGENTS.md). This repository keeps a single
canonical agent instruction file for Claude Code, OpenCode, Codex, Cursor,
Gemini CLI, and other AGENTS-aware harnesses.

Do not duplicate project rules here. Update `AGENTS.md` instead.

## Precedence

`AGENTS.md` rules (also injected at SessionStart as "Mandatory rules") override
any conflicting rule injected by plugins or hooks (caveman, ponytail, tlc
harness, rag-rat, context-mode). On conflict: follow `AGENTS.md`, name the
conflict in one line.
