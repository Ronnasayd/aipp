---
name: sd-interview
description: Research a feature request through iterative codebase investigation and relentless user grilling until shared understanding is reached, then produce an SRS and a verified context map as hand-off artifacts for sd-planning. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', 'walk through planning this feature', or 'interview me about this idea before we spec it'.
model: claude-opus-5-5[1m]
---

# Steps

See [diagram](references/diagram.md) for a visual flow overview.

Add the following steps as tasks using the `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` tools. Update the status as you progress through each step to keep the user informed.

1. Repeat these steps until you have a complete understanding of the problem and how it fits into the current context. When you feel the loop should end because you have sufficient context, ask the user if they wish to finish or continue refining issues before moving on.
   1. Use `sequentialthinking` in `mcp-manager` to break down the feature request into sub-issues (scope, constraints, edge cases, dependencies). Use `/dynamic-programming-analysis` when the breakdown itself is hard (unclear where to start, many interdependent sub-problems).
      1. Treat codebase as absolute source of truth. Navigate file-by-file, following flows that will be modified/adjusted, until you reach limits and have total understanding of current behavior.
      2. Don't trust linear flows alone — search transversally: hunt keywords/terms possibly related but not directly linked, or absent from files already inspected (config, feature flags, error codes, event names, shared constants).
      3. Use every available tool to reach this understanding: semantic search, sub-agents for parallel/deep search, CLI commands, MCP tools, skills, or anything else that helps.
      4. If a knowledge gap remains that the codebase and `context7` (library docs) can't cover — market patterns, RFCs, security advisories, precedent for a novel architectural decision — use `WebSearch` to fill it. Skip this when the codebase/context7 already answer the question.
   2. **Grilling must be conducted by a dedicated, independent sub-agent** — never inline by the main thread. See [grilling](references/grilling.md) for why (hides the downstream goal of writing code/plans, so the sub-agent doesn't rush the interview, and isolates context). Dispatch a fresh sub-agent with: the problem description, the sub-issues and research gathered above, and the instruction below verbatim. Strip code-editing and task-creation tools from its toolset — it may only ask questions and read docs/code to inform them. It is specified as a user-invoked skill (`/grilling`), not model-auto-triggered, so you — not the sub-agent — decide when the session ends.

      > "Interview me relentlessly about every aspect of this idea/plan until we reach a shared understanding. Walk every branch of the decision tree, resolving dependencies one at a time. For each question, provide your recommended default answer. Ask one question at a time. Do not generate final plans or code at this stage."

      The sub-agent runs the `/grilling` skill against the user until no structural ambiguity remains (one question at a time, with a recommended default per question, covering business rules/edge cases, boundaries/architecture, and acceptance criteria/testability — check for unlisted implicit requirements and undefined issues along the way). When it signals the interview complete, it hands back the synthesized Q&A history to the main thread — this feeds step 2 (`/context-map`) and step 3 (SRS generation), not the main thread's own notes.

2. Execute `/context-map` with the sub-issues and grilling-session findings as the task description to get verified anchors, dependents, tests, reference patterns, and risks (it runs `rag-rat`, `codebase-memory-mcp`, `serena` itself). Then use `grep`, `Read`, or any other available tool to go deeper where the map's "Not Checked" or uncertain anchors leave gaps. This map is part of the hand-off to `sd-planning`.
3. Execute the `srs-generator` skill with the problem description, sub-issues, grilling Q&A history, and context map as input to produce the SRS. Follow its own elicitation/generation/validation workflow — do not duplicate it here.
4. Hand off to the user: the saved SRS path (`docs/srs/yyyy-mm-dd-<short-description>.md`) and the context map. State explicitly that `sd-planning` picks up from these two artifacts.
5. At the end of the session, evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md — such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.
