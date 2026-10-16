# AIPP — AI Pair Programming Workspace

A toolkit that gives AI coding agents specialized roles, reusable skills and structured workflows, linked into any project with one command.

![Python](https://img.shields.io/badge/python-%E2%89%A53.11-blue)
![uv](https://img.shields.io/badge/managed%20with-uv-6c47ff)

## What's included

- [`agents/`](agents/): persona definitions with behavioral instructions.
- [`skills/`](skills/): reusable capabilities (workflows, style guides, analysis patterns).
- [`commands/`](commands/): slash-command templates.
- [`instructions/`](instructions/): domain rules and conventions per language or framework.
- [`hooks/`](hooks/): hook scripts wired into the agent harnesses.
- [`src/`](src/): MCP servers and Python tooling.

## Requirements

- `git`, `curl`, [`uv`](https://docs.astral.sh/uv/), Node.js 24 or newer, and the Claude CLI.
- Tested on Linux. macOS support is partial: one bundled tool download only targets Linux x86_64.
- Everything else the bootstrap downloads is listed in [External tools](docs/external-tools.md).

## Warning: what the installer changes

- It edits your shell startup files (`~/.zshrc` and `~/.bashrc`): `PATH`, `AI_PROJECT_ROOT_DIR`, `CLAUDE_CONFIG_DIR` and the alias file are added.
- Global harness config files become symlinks into this repo (`~/.claude/settings.json`, `~/.gemini/settings.json`, `~/.copilot/mcp-config.json`, `~/.copilot/config.json`). A regular file already at one of these paths is kept beside it as `<path>.bak`; a folder at that path is left untouched and a warning is printed.

## Quickstart

Installation has two stages.

**1. One-time bootstrap**, run inside the clone. It installs dependencies and tools and creates the `aipp` command:

```sh
git clone https://github.com/Ronnasayd/aipp.git ~/aipp
cd ~/aipp
bash install.sh
```

**2. Per project**, run `aipp` from the project root with a backend flag:

```sh
cd ~/my-project
aipp --claude
```

| Flag            | Effect                                             |
| --------------- | -------------------------------------------------- |
| `--all`         | Install every backend (default with no flag)       |
| `--claude`      | Install the Claude backend                         |
| `--copilot`     | Install the Copilot backend                        |
| `--gemini`      | Install the Gemini backend                         |
| `--codex`       | Install the Codex backend                          |
| `--antigravity` | Install the Antigravity backend                    |
| `--taskmaster`  | Install the taskmaster config                      |
| `--gitignore`   | Install the gitignore entries                      |
| `--clean`       | Remove the symlinks created by the install scripts |
| `--help`, `-h`  | Show the help screen                               |

To run the tests, see [CONTRIBUTING.md](CONTRIBUTING.md).

## How it works

`aipp <flag>` symlinks the agents, skills, commands and instructions into the project's harness folder (for example `.claude/`). Which items are linked is a per-project toggle stored in `$CLAUDE_CONFIG_DIR/aipp-settings.json`, seeded from the repo defaults the first time a project is installed. The `mif` alias opens a selection tool that enables or disables items; `mia` runs it and then installs the Claude backend.

## Handy aliases

Defined in [`.aipp.alias.zshrc`](.aipp.alias.zshrc) and sourced from your shell startup files:

| Alias               | What it does                                                        |
| ------------------- | ------------------------------------------------------------------- |
| `mif`               | Toggle skills, agents and instructions for the current project      |
| `mia`               | Run `mif`, then `aipp --claude`                                     |
| `ats`, `ata`, `atr` | Show enabled skills, agents and instructions of the current project |
| `lgh`               | Follow the hooks log                                                |
| `aij`               | Run the `ai-jail` sandbox script                                    |

## Uninstall

```sh
bash uninstall.sh
```

It removes the `aipp` command, runs the harness uninstall, and strips the lines the installer added to `~/.zshrc` and `~/.bashrc` (each edited file is saved as `<rc>.bak`).

It does **not** restore your `.bak` config files; the global config paths stay as symlinks into this repo. To restore one by hand:

```sh
mv ~/.claude/settings.json.bak ~/.claude/settings.json
```

## Directory structure

- `agents/`, `skills/`, `commands/`, `instructions/`, `hooks/`: the shared catalog described above.
- `src/`: MCP servers and Python tooling.
- `scripts/`: install, clean and setup scripts per harness.
- `claude/`, `gemini/`, `github-copilot/`, `antigravity/`: harness-specific configs and settings.
- `taskmaster/`: task tracking config.
- `docs/`: reference and supporting documentation.
- `docker/`: Docker compose configs (for example the LiteLLM proxy).
- `legacy/`: archived configs kept for reference.
- `tlc-harness-toolkit/`: TLC harness tooling and config.
- `install.sh`, `uninstall.sh`: entry-point installer and uninstaller.

## Reference

- [Environment variables](docs/environment.md)
- [External tools](docs/external-tools.md)
- [Contributing](CONTRIBUTING.md)
- [`AGENTS.md`](AGENTS.md): canonical instructions for AI agents working in this repo.
