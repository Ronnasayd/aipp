# Contributing

## Adding a skill

Create `skills/<category>/<skill-name>/SKILL.md`. The file starts with a YAML header:

```markdown
---
name: my-skill
description: One or two sentences on what it does and when to use it.
---
```

`name` and `description` are required: without them the skill does not load or trigger. `metadata` is optional.

## Adding an agent

Create `agents/<agent-name>.agent.md` with a YAML header holding `name` and `description` (both required), followed by the agent's instructions. Agents without this header are not listed or selectable.

## Regenerating the indexes

The skill and agent indexes are generated; do not edit them by hand. After adding or renaming an item, run from the repo root:

```sh
uv run python3 scripts/list_skills_agents.py
uv run python3 scripts/build-skill-index.py
```

New items enter the catalog disabled. Enable them per project with the `mif` alias (see [README](README.md#how-it-works)).

## Adding a hook

1. Put the script in [`hooks/scripts/`](hooks/scripts).
2. Wire it in [`claude/settings.json`](claude/settings.json). That file is the source of truth for which script fires on which event.
3. Document it in [`hooks/README.md`](hooks/README.md).

To verify that a hook works end to end, run the `/verify-hook` command with the hook's script path.

## Running tests

```sh
uv run --with pytest pytest scripts/
```

## Commit rules

Commits are checked by git hooks ([`lefthook/lefthook.yml`](lefthook/lefthook.yml)) and rejected unless they follow these rules:

- Conventional Commits format (`type(scope): description`).
- No emoji.
- No mentions of AI tools or assistants.
- English only.
