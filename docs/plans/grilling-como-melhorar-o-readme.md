# README Improvement + Safe Global Config Linking

## Context

`README.md` (87 lines) has no title or pitch, typos ("Instalation"), and does not
explain the real install flow, the per-project selection mechanism, or the
side effects on the user's global harness config. Half the file is two wide
reference tables. While grilling, two code-level problems surfaced that the
new docs would otherwise have to document as-is:

1. The documented test command runs nothing.
2. Three installers delete the user's global config files without backup.

## Findings (evidence)

| #   | Finding                                                                                                                                                                                                                                          | Evidence                                                                                                                                                                                                                   |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| F1  | Two-stage install: first `bash install.sh` inside the repo bootstraps tools + global `aipp` command; afterwards `aipp --<backend>` per project                                                                                                   | `install.sh:12-95` (bootstrap branch), `install.sh:150-210` (flags)                                                                                                                                                        |
| F2  | Backend flags: `--all` (default), `--claude`, `--copilot`, `--gemini`, `--codex`, `--antigravity`, `--taskmaster`, `--gitignore`, `--clean`, `--help`. `--antigravity` missing from `show_help`                                                  | `install.sh:150-210`                                                                                                                                                                                                       |
| F3  | Hidden prerequisites: Node >= 24 for harness-toolkit, `uv`, `claude` CLI; lefthook download hardcoded to Linux x86_64; `pkg_install` supports apt and brew                                                                                       | `install.sh:84,87-92`, `scripts/installs/_generic.install.sh:5-12`                                                                                                                                                         |
| F4  | Bootstrap appends to `~/.zshrc` / `~/.bashrc` (`PATH`, `AI_PROJECT_ROOT_DIR`, `CLAUDE_CONFIG_DIR`, alias source) and moves `~/.claude.json`                                                                                                      | `install.sh:26-64`                                                                                                                                                                                                         |
| F5  | Installers `rm` a **regular file** at the global config path, then symlink it to the repo — user config lost, no backup                                                                                                                          | `scripts/claude.install.sh:123-126` (`~/.claude/settings.json`), `scripts/gemini.install.sh:95-98` (`~/.gemini/settings.json`), `scripts/copilot.install.sh:6-14` (`~/.copilot/mcp-config.json`, `~/.copilot/config.json`) |
| F6  | `uninstall.sh` removes the `aipp` symlink, tlc harness and rc-file lines only; global config symlinks are left in place                                                                                                                          | `uninstall.sh`                                                                                                                                                                                                             |
| F7  | Per-project selection: installers link every skill/agent, then `scripts/ignores.sh` removes entries set to `false` in `~/.claude/aipp-settings.json`; defaults seeded from `claude/aipp-default-settings.json`; new catalog items enter disabled | `scripts/claude.install.sh:150-163,210,294`, `scripts/ignores.sh`, `scripts/aipp_settings.py::sync_catalog`                                                                                                                |
| F8  | Selection UI: `mif` (curses checkboxes, `scripts/manage-ignore-files.py`); `mia` = `mif && aipp --claude`; `ats`/`ata`/`atr` show current state                                                                                                  | `.aipp.alias.zshrc:31-34,40,66`                                                                                                                                                                                            |
| F9  | `cd src && uv run pytest` collects 0 tests (`src/tests/` absent) → exit 5. Only tracked test suite is `scripts/test_aipp_settings.py` → 32 passed                                                                                                | `/tmp/readme-src-pytest.log`, `/tmp/readme-scripts-pytest.log`                                                                                                                                                             |
| F10 | Skill/agent indexes are generated (`scripts/list_skills_agents.py`, `scripts/build-skill-index.py`); README is not — hardcoded counts would drift                                                                                                | `scripts/list_skills_agents.py:1-4`                                                                                                                                                                                        |
| F11 | `MD_LANGUAGE=English`; `docs/` and `CONTRIBUTING.md` are allowed `.md` locations                                                                                                                                                                 | `claude/settings.json:15`, `hooks/scripts/md_location_check.py:17-34`                                                                                                                                                      |
| F12 | Commit gates: Conventional Commits, no emoji, no AI mentions, English only                                                                                                                                                                       | `lefthook/lefthook.yml:20-36`                                                                                                                                                                                              |

## Design Decisions (grilled)

| Decision                               | Choice                                                                                    |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| Audience                               | Owner + third parties (public repo): short pitch, clear quickstart, details via links     |
| Language                               | English (README, new docs, CONTRIBUTING)                                                  |
| Long tables (env vars, external tools) | Move verbatim to `docs/environment.md` and `docs/external-tools.md`; README links them    |
| New README sections                    | What's included, Requirements, Quickstart (2 stages + flags), How it works, Handy aliases |
| Component counts                       | No numbers — describe each component and link its `index.yaml` / dir                      |
| Aliases                                | Top ~10, grouped, plus link to `.aipp.alias.zshrc`                                        |
| OS support                             | "Tested on Linux; macOS partial" (apt/brew supported, lefthook binary is Linux x86_64)    |
| Badges                                 | Static shields.io: Python 3.11+, uv                                                       |
| Screenshot                             | Not now                                                                                   |
| License                                | Out of scope (no `LICENSE` exists; owner's call)                                          |
| Contribution docs                      | Separate `CONTRIBUTING.md`: adding a skill/agent, adding a hook                           |
| Test command documented                | `uv run --with pytest pytest scripts/` (the one that actually runs)                       |
| `AGENTS.md`                            | Fix the dead test command only; preserve the owner's pending uncommitted diff             |
| Global config overwrite                | Warning in README **and** backup in the installers                                        |
| Backup scope                           | Shared helper used by claude, gemini and copilot installers                               |
| Backup policy                          | Regular file → single `<path>.bak`; existing symlink → replaced, no backup                |
| Helper test                            | pytest in `scripts/`, helper run via `subprocess` against `tmp_path` (TDD red → green)    |
| Uninstall restore                      | No — document where the `.bak` lives for manual restore                                   |

### Backup edge cases

| Destination state    | Action                                                                        |
| -------------------- | ----------------------------------------------------------------------------- |
| Missing              | Create symlink                                                                |
| Symlink (any target) | Replace symlink, no backup                                                    |
| Regular file         | `mv` to `<path>.bak` (overwrites an older `.bak`), then symlink               |
| Directory            | Out of scope — current call sites only target files; leave untouched behavior |

A second install finds a symlink, so it never overwrites the first `.bak`.
The `.bak` is only replaced if the user swaps the symlink for a real file again.

## Plan (vertical slices)

Each slice is independently verifiable before the next.

### Slice 1 — Safe linking helper (TDD)

1. Red: `scripts/test_link_with_backup.py` — cases: missing dst, existing
   symlink, regular file (asserts `.bak` content == original and dst is a
   symlink to src), regular file with pre-existing `.bak` (overwritten).
   Run → fails (helper absent).
2. Green: `scripts/_link-with-backup.sh` exposing `link_with_backup <src> <dst>`.
3. Wire call sites, replacing the `if … rm …; fi; ln -s` blocks:
   - `scripts/claude.install.sh:123-126`
   - `scripts/gemini.install.sh:95-98`
   - `scripts/copilot.install.sh:6-14` (both files)
4. Verify: `uv run --with pytest pytest scripts/` all green; run one installer
   against a fake `HOME` and show `ls -la` of the result.

### Slice 2 — Fix the dead test command

- `AGENTS.md` "Run tests": replace `cd src && uv run pytest` with
  `uv run --with pytest pytest scripts/`. Edit only that block; keep the
  owner's pending diff intact.
- Verify: `git diff AGENTS.md` shows the pending hunks plus this one only.

### Slice 3 — Reference docs split

- Create `docs/environment.md` (env-var table, verbatim) and
  `docs/external-tools.md` (tools table, verbatim).
- Verify: tables byte-identical to the current README rows (diff check).

### Slice 4 — README rewrite

Section order:

1. Title, one-line pitch, badges (Python 3.11+, uv)
2. **What's included** — agents, skills, instructions, hooks, commands, MCP
   servers; each with a link, no counts
3. **Requirements** — git, curl, `uv`, Node >= 24, `claude` CLI; tested on
   Linux, macOS partial
4. `> [!WARNING]` — rc files edited; global harness config replaced by a
   symlink, previous regular file saved as `<path>.bak`
5. **Quickstart** — stage 1 bootstrap (`bash install.sh` inside the clone →
   `aipp` command), stage 2 per project (`aipp --claude`), flags table
6. **How it works** — symlinks into `.claude/`; per-project toggles in
   `~/.claude/aipp-settings.json`; defaults from
   `claude/aipp-default-settings.json`; `mif` to toggle, `ats`/`ata`/`atr` to view
7. **Handy aliases** — ai-memory (`aims`, `aimm`, `aimh`, `aimw`), sandbox
   (`aij`, `lca`), repo intel (`rri`, `sri`), selection (`mif`, `mia`), logs
   (`lgh`); link to `.aipp.alias.zshrc`
8. **Uninstall** — `bash uninstall.sh`; what it removes; restore `.bak` manually
9. **Directory structure** — trimmed current list
10. **Reference** — `docs/environment.md`, `docs/external-tools.md`,
    `hooks/README.md`, `hooks/ENVIRONMENTS.md`, `CONTRIBUTING.md`

- Verify: every relative link resolves (scripted check over README links);
  every flag listed exists in `install.sh`; every alias listed exists in
  `.aipp.alias.zshrc`.

### Slice 5 — CONTRIBUTING.md

- **Adding a skill or agent** — `skills/<name>/SKILL.md` frontmatter
  (`name`, `description`, `metadata`), `agents/<name>.agent.md` frontmatter
  (`name`, `description`); regenerate indexes with
  `scripts/list_skills_agents.py` + `scripts/build-skill-index.py`; new items
  enter the catalog disabled — enable with `mif`; `skill-description-generator`
  skill for reliable triggering.
- **Adding a hook** — script in `hooks/scripts/`, wiring in
  `claude/settings.json` (source of truth; `hooks/hooks.json` is stale),
  document in `hooks/README.md`; `verify-hook` command for end-to-end check.
- **Tests** — `uv run --with pytest pytest scripts/`.
- Verify: same link/command checks as Slice 4.

## Files to Create/Modify

| File                               | Action                          |
| ---------------------------------- | ------------------------------- |
| `scripts/_link-with-backup.sh`     | Create                          |
| `scripts/test_link_with_backup.py` | Create                          |
| `scripts/claude.install.sh`        | Modify (lines 123-126)          |
| `scripts/gemini.install.sh`        | Modify (lines 95-98)            |
| `scripts/copilot.install.sh`       | Modify (lines 6-14)             |
| `AGENTS.md`                        | Modify ("Run tests" block only) |
| `docs/environment.md`              | Create                          |
| `docs/external-tools.md`           | Create                          |
| `README.md`                        | Rewrite                         |
| `CONTRIBUTING.md`                  | Create                          |

## Out of Scope / Follow-ups

- `LICENSE` file.
- Screenshot of statusline / Moonlight theme.
- `uninstall.sh` restoring `.bak` files or removing global symlinks.
- `src/pyproject.toml` dead `testpaths = ["tests"]` / `asyncio_mode` options.
- `--antigravity` missing from `install.sh` `show_help`.
- `hooks/hooks.json` stale template.
