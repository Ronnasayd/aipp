# Setup and daily operation

Sources of truth: `install.sh`, `uninstall.sh`, `scripts/claude.install.sh`, `scripts/ignores.sh`, `scripts/aipp_settings.py`, `.aipp.alias.zshrc`. User-facing overview: `README.md`.

## Install

There are two stages.

1. **Bootstrap, once per machine.** Run `bash install.sh` inside the clone. It installs dependencies and creates the `aipp` command, a symlink at `~/.local/bin/aipp` pointing to `install.sh`. It edits `~/.zshrc` and `~/.bashrc`, and it turns global harness config files into symlinks into the repo (for example `~/.claude/settings.json`), keeping a regular file that was there as `<path>.bak`.
2. **Link, once per project.** Run `aipp --claude` from the project root, then run it again in a new project (see below). Other flags: `--all`, `--copilot`, `--gemini`, `--codex`, `--antigravity`, `--taskmaster`, `--gitignore`, `--clean`. With no flag it installs every backend.

**Run it twice in a new project.** `install.sh` seeds the project's settings after the backend script has already linked and filtered (`install.sh:238-239`). `scripts/ignores.sh` only removes items marked `false`, so on the first run nothing is removed and every skill stays linked, while no instruction is linked yet. The second run applies the defaults.

Re-run `aipp --claude` whenever the enabled set or the toolkit changes. It rebuilds the links, so it is safe to repeat.

What linking does in the project:

- Symlinks skills, commands, agents and hooks into `.claude/`, then removes the disabled ones.
- Overwrites `CLAUDE.md` and rewrites the auto-generated block of `AGENTS.md` from the enabled instructions. `CLAUDE_INSTALL_SKIP_CLAUDE_MD=1` and `CLAUDE_INSTALL_SKIP_AUTO_CONTEXT=1` skip these.
- Links `.mcp.json` and `lefthook.yml`, or merges into them when the project has its own regular file, then runs `lefthook install`.
- Writes `.tlc/harness/config.json` and `.claude/settings.local.json`.
- Starts rag-rat setup in the background when the project has `rag-rat.toml` (log: `/tmp/rag-rat-setup.log`), and codebase-memory indexing when that tool is installed (log: `/tmp/codebase-memory-mcp-setup.log`).
- Adds the generated paths to `.git/info/exclude`, so they do not appear in `git status`.

Project-local additions go in `<project>/agents/skills/`, `<project>/agents/commands/` and `<project>/agents/agents/`. They get linked too, and a name that collides with a toolkit item stops the install with an error.

## Enable or disable items

State lives in `$CLAUDE_CONFIG_DIR/aipp-settings.json`, under `.projects["<absolute project path>"]`, with `skills`, `agents` and `instructions` maps of name to boolean.

| Command | Effect                                                                 |
| ------- | ---------------------------------------------------------------------- |
| `mif`   | Interactive checkbox menu for the current project. Changes state only. |
| `mia`   | `mif`, then `aipp --claude`, so the change takes effect.               |
| `ats`   | List skills for the current project (`✅` marks enabled).              |
| `ata`   | List agents.                                                           |
| `atr`   | List instructions.                                                     |

Names follow the path under `skills/` with `/` replaced by `:`, for example `tech-leads-club:the-judge`.

Seeding uses `claude/aipp-default-settings.json`. It fills in missing keys for a project and never overrides a value that is already set.

A skill can be used without enabling it: the skill-loader MCP tools `list_remote_skills` and `get_remote_skill(name)` fetch from GitHub through `skills/manifest.json`.

## Aliases

All live in `.aipp.alias.zshrc`. Read that file for the full list, since each alias has a trailing comment. The ones people need most:

| Group        | Aliases                                                                                 |
| ------------ | --------------------------------------------------------------------------------------- |
| Items        | `mif`, `mia`, `ats`, `ata`, `atr`                                                       |
| Hook logs    | `lgh` (all), `lght` (tools), `lghac` (additionalContext only), `lghe` (external)        |
| ai-memory    | `aims` (start container), `aimm` (install MCP), `aimh` (install hooks), `aimw` (web UI) |
| Repo tools   | `rri` (init rag-rat), `sri` (init serena), `lhi` (install lefthook)                     |
| Sandbox      | `aij` (ai-jail), `lca` (Claude in ai-jail), `lcay` (same, no permission prompts)        |
| Claude runs  | `cldyl` (no permission prompts), `cpln` (no Write or Edit tools), `rc` (continue)       |
| Accounts     | `ca`, `cacs` (choose account)                                                           |
| Caveman mode | `scvm` (off), `acvm` (on)                                                               |

## Uninstall

- Remove links from one project: `aipp --clean` (or with a backend flag, such as `aipp --claude --clean`).
- Remove the toolkit from the machine: `bash uninstall.sh`. It deletes the `aipp` command, runs `tlc harness uninstall --purge --yes` and strips the installer's lines from the shell rc files. It does not restore `.bak` files: global config paths stay as symlinks into the repo until restored by hand, for example `mv ~/.claude/settings.json.bak ~/.claude/settings.json`.

## Troubleshooting

| Symptom                                              | Cause                                                                                           | Fix                                                       |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| Every skill is linked in a new project               | First run links before the project is seeded                                                    | Run `aipp --claude` again                                 |
| Skill missing from a project                         | Disabled in `aipp-settings.json`                                                                | `ats` to check, then `mia` to enable it                   |
| New toolkit skill appears, then vanishes on next run | `sync-catalog` runs after linking and registers new items as `false` for every existing project | Enable it with `mia`                                      |
| Toggled an item in `mif`, nothing changed            | `mif` only writes state                                                                         | Run `aipp --claude`, or use `mia`                         |
| Skill linked but not listed in the session           | Skills load at session start                                                                    | Restart the session                                       |
| `aipp: command not found`                            | Bootstrap not run, or shell not reloaded                                                        | Run `bash install.sh` in the clone, then open a new shell |
| `ats` prints `no entry found`                        | Project never linked, or run from another directory (the key is the exact `pwd`)                | Run from the project root; run `aipp --claude` if needed  |
| Install stops with `collides with an existing skill` | A project-local item has the same name as a toolkit item                                        | Rename the local item                                     |
| Need to see what a hook did                          | Hook logs are in `$CLAUDE_CONFIG_DIR/logs/`                                                     | `lgh` in another terminal                                 |
