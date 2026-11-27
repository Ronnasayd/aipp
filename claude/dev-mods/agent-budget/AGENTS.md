# agent-budget

Admits each `Agent` tool call by a cost budget instead of a flat count.

- Weight of an agent = price of one call for its model family and effort (opus high = 128).
  Unknown families (fable, new ids) are priced as opus; `xhigh`, `max` and integer efforts as `high`.
- Running weight = sum over `$.agent.list()` entries in `pending`/`running`/`waiting`.
- A call is refused when running weight + its weight > `AGENT_BUDGET_MAX` (default 128),
  or when running agents >= `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`.
- Model/effort resolution: the call's `model`/`effort`, then the agent file frontmatter
  (`<cwd>/.claude/agents`, then `~/.claude/agents`), then `CLAUDE_CODE_SUBAGENT_MODEL` / parent model
  and the session `effortLevel`.

## Environment

| Variable | Default | Effect |
| --- | --- | --- |
| `AGENT_BUDGET_MAX` | `128` | Total weight allowed at once |

## Why it refuses instead of queueing

Measured on Claude Code 2.1.332: a `tool.call` hook on `Agent` gets 10 s of own time
(`next.budget.ms` = 10000), so a queue of minutes cannot be held in the hook. Over budget,
the call is denied at once, with no wait; the deny text tells the model how much is used
so it retries after an agent ends.

## Tests

`claude plugin test claude/dev-mods/agent-budget`
