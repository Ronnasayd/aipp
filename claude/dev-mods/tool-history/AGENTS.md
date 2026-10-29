# tool-history

## Card spacing

- Cards in the pane (tool calls and agent messages) sit flush: the `list` Box
  in `hooks/register.tsx` uses `gap={0}`. No blank line between cards — the
  round border already separates them.
- Do not add `gap`, `marginY`, `marginTop` or `marginBottom` to the `list` Box
  or to individual cards. `tests/collapse.test.tsx` asserts `gap` is `0`.
- Why: when cards were grouped per agent, `gap={1}` only separated groups.
  After the groups were flattened (each card names its agent), the same
  `gap={1}` landed between every card and the pane got sparse.

## Border colors

- Yellow border = subagent, and only in the messages tab (agent message cards).
- Tool call cards (Bash, Read, etc.) never use yellow, even when a subagent
  made the call: `danger` on error, `subtle` when done, `claude` while running.
  `tests/subagent-border.test.tsx` asserts this.

## Agent tool calls in the messages tab

- Each `Agent` tool call also adds a `kind: "agent"` card to the messages tab
  (key `agent-call-<tool_use_id>`): `subagent_type`, `description` and the
  full `prompt`. Border follows the caller (yellow only if a subagent spawned
  it). `tests/agent-call-message.test.tsx` asserts this.
