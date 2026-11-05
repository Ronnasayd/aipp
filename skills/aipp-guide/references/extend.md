# Extending the toolkit

Sources of truth: `CONTRIBUTING.md`, `scripts/list_skills_agents.py`, `scripts/build-skill-index.py`, `scripts/aipp_settings.py`, `scripts/update-external-tools.sh`, `lefthook/lefthook.yml`.

All of this happens inside the toolkit repo, not in a project that uses it.

## Add a skill

1. Create `skills/<skill-name>/SKILL.md`, or `skills/<category>/<skill-name>/SKILL.md`. The path decides the catalog key: `skills/foo/bar/` becomes `foo:bar`.
2. Start it with YAML frontmatter holding `name` and `description`. A skill without them does not load or trigger. Put trigger phrases in `description`, since both the harness and `hooks/scripts/skill_activation.py` match against it.
3. Use `disable-model-invocation: true` for workflows that only the user may start.
4. Use `context: fork` to run the skill isolated. A forked skill sees no conversation history and cannot ask questions, so required input must arrive through `$ARGUMENTS`. When input is missing it stops and reports back instead of assuming a default.
5. Do not rely on `model:` in the frontmatter to pick the model on the Skill tool path. Read the durable note `gotchas/skill-model-frontmatter-ignored.md` in ai-memory before depending on it.
6. Regenerate the indexes (below), then enable the skill.

Helpers, disabled by default: `skill-description-generator` for the description, `compress-skill` when a `SKILL.md` grows too long.

## Add an agent

Create `agents/<agent-name>.agent.md` with `name` and `description` in the frontmatter, then the instructions. Without that header it is not listed. Regenerate the indexes. The catalog key is the file name, for example `developer-specialist.agent.md`. Helper: `agent-creator`.

## Add an instruction

Create `instructions/<name>.instructions.md` with frontmatter (`description`, `applyTo`). Regenerate the indexes. The catalog key is the file name.

## Add a hook

1. Put the script in `hooks/scripts/`. Helper: `author-claude-hook`.
2. Wire it in `claude/settings.json`, which decides what fires. `.claude/settings.json` is not the source.
3. Document it in `hooks/README.md`.
4. Run `/verify-hook <script path>` to prove it works end to end.

## Add an external skill source

`scripts/update-external-tools.sh` downloads third-party skills and needs `GITHUB_PAT_TOKEN`. It scans each download with SkillSpector and moves anything with findings to `skills/.quarantine/`. Follow an existing `get_skills_*` function, which registers each item as disabled with `aipp_settings.py register-if-absent`. Do not hand-edit downloaded skills, because the next sync overwrites them.

## Regenerate the indexes

Run from the repo root after adding or renaming an item:

```sh
uv run python3 scripts/list_skills_agents.py
uv run python3 scripts/build-skill-index.py
```

| Artifact                                                            | Built by                | Git status |
| ------------------------------------------------------------------- | ----------------------- | ---------- |
| `skills/index.yaml`, `agents/index.yaml`, `instructions/index.yaml` | `list_skills_agents.py` | Tracked    |
| `skills/manifest.json`                                              | `build-skill-index.py`  | Tracked    |
| `skills/skills.db`, `skills/skills.db.sha256`                       | `build-skill-index.py`  | Untracked  |

Never edit these by hand. `skills/manifest.json` has to be committed, because remote loaders read it from GitHub.

## Make an item available

New items enter the catalog as `false`, for new and existing projects alike.

- To enable in one project: `mia` from that project.
- To enable by default in new projects: set the key to `true` in `claude/aipp-default-settings.json`. Existing projects keep the value they already hold, so each of them still needs `mia`.

Each enabled skill costs its description in every session, so default to `false` unless most projects need it.

## Test

- Scripts: `uv run --with pytest pytest scripts/`
- Hooks: `uv run --with pytest pytest hooks/scripts/`
- MCP servers live in `src/`, with their own `uv` project (`cd src && uv sync`).

The repo requires a failing test first where a test suite exists. Run the lint gate before committing:

```sh
git add <files>
uv run lefthook/scripts/comment_policy_check.py
uv run hooks/scripts/lint_changed.py --staged
```

## Commit

- Conventional Commits (`type(scope): description`), English, no emoji, no mention of AI tools. Enforced by lefthook `commit-msg`.
- Work on a branch: commits on `master` are denied. Create the branch in its own command first.
- `post-commit` runs `semantic_version_bump.py`, and `pre-push` pushes pending tags.
