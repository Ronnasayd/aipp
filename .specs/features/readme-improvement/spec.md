# README Improvement + Safe Global Config Linking Specification

**Source plan**: `docs/plans/grilling-como-melhorar-o-readme.md` (decisions grilled and locked)
**Scope**: Large (10 files, shell + pytest + docs)

## Problem Statement

`README.md` has no title or pitch, contains typos ("Instalation"), and does not explain the real
two-stage install flow, the per-project selection mechanism, or the side effects on the user's
global harness config. Two code defects surfaced while planning: the documented test command
(`cd src && uv run pytest`) collects 0 tests and exits 5, and three installers `rm` the user's
global config files (`scripts/claude.install.sh:123-126`, `scripts/gemini.install.sh:95-98`,
`scripts/copilot.install.sh:6-14`) before symlinking them to the repo, with no backup.

## Goals

- [ ] No installer run destroys a regular-file global config: every replaced regular file survives as `<path>.bak` with identical content.
- [ ] Documented test command runs a non-empty suite and exits 0.
- [ ] A first-time reader can go from clone to a configured project using only `README.md` (two stages + flags), with every relative link resolving.

## Out of Scope

| Feature                                                                            | Reason                                                               |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `LICENSE` file                                                                     | Owner's call                                                         |
| Statusline / Moonlight screenshot                                                  | Deferred                                                             |
| `uninstall.sh` restoring `.bak` or removing global symlinks                        | Documented as manual restore instead                                 |
| `src/pyproject.toml` dead `testpaths` / `asyncio_mode`                             | Separate cleanup                                                     |
| `--antigravity` missing from `install.sh` `show_help`                              | Separate fix                                                         |
| Dangling `hooks/hooks.json` reference in `hooks/README.md` (file no longer exists) | Separate cleanup; CONTRIBUTING.md does not mention it                |
| Backing up directories at the destination path                                     | Current call sites only target files                                 |
| Component counts in README                                                         | Would drift; indexes are generated                                   |
| Other `rm`+`ln -s` blocks (`.geminignore`, project-local links)                    | Not global user config files; grilled scope is the four listed paths |

---

## Assumptions & Open Questions

| Assumption / decision                                         | Chosen default                                                                                                                       | Rationale                                                                                                        | Confirmed? |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------- |
| How the helper is consumed                                    | Sourced shell file `scripts/_link-with-backup.sh` defining `link_with_backup <src> <dst>`, same pattern as `scripts/_git-exclude.sh` | Installers already `source` shared helpers                                                                       | y          |
| Destination is a directory                                    | Helper leaves it unchanged, prints a warning to stderr, returns 1                                                                    | Plan says "leave untouched"; refusing is the only behavior that cannot lose data                                 | n          |
| Parent dir of destination missing (e.g. `~/.copilot/` absent) | Helper runs `mkdir -p "$(dirname dst)"` before linking                                                                               | Current copilot block fails with `ln: No such file or directory`; creating the parent is the minimal correct fix | n          |
| Older `.bak` already present when a regular file is found     | Overwritten by the new backup                                                                                                        | Grilled policy: single `<path>.bak`                                                                              | y          |
| Helper output                                                 | One line per backup on stdout: `backup: <dst> -> <dst>.bak`                                                                          | Installers already echo `[ok]`-style progress; user must learn where the file went                               | n          |
| Test command                                                  | `uv run --with pytest pytest scripts/`                                                                                               | Only suite that actually runs (32 passed at plan time)                                                           | y          |
| Docs language                                                 | English                                                                                                                              | `MD_LANGUAGE=English` (`claude/settings.json:15`)                                                                | y          |
| OS support statement                                          | "Tested on Linux; macOS partial"                                                                                                     | lefthook binary is Linux x86_64; `pkg_install` supports apt and brew                                             | y          |
| `AGENTS.md` pending diff                                      | Preserved; only the "Run tests" block changes                                                                                        | Owner's uncommitted work                                                                                         | y          |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Installers back up global config instead of deleting it ⭐ MVP

**User Story**: As a user running `aipp --claude|--gemini|--copilot`, I want my existing global config file kept as a backup so that installing aipp never silently destroys my settings.

**Why P1**: Data loss on a public tool's install path; the README warning depends on it.

**Acceptance Criteria**:

1. WHEN `link_with_backup <src> <dst>` runs and `<dst>` does not exist THEN the helper SHALL create `<dst>` as a symlink to `<src>` and create no `.bak`. <!-- event-driven -->
2. WHEN `<dst>` is an existing symlink (any target, including dangling) THEN the helper SHALL replace it with a symlink to `<src>` and create no `.bak`. <!-- event-driven -->
3. WHEN `<dst>` is a regular file THEN the helper SHALL move it to `<dst>.bak` (byte-identical content) and create `<dst>` as a symlink to `<src>`. <!-- event-driven -->
4. WHEN `<dst>` is a regular file and `<dst>.bak` already exists THEN the helper SHALL overwrite `<dst>.bak` with the current `<dst>` content. <!-- event-driven -->
5. IF `<dst>` is a directory THEN the helper SHALL leave `<dst>` and its contents unchanged, write a warning to stderr, and return exit code 1. <!-- unwanted-behavior -->
6. WHEN the parent directory of `<dst>` does not exist THEN the helper SHALL create it and then create the symlink. <!-- event-driven -->
7. WHEN the helper backs up a file THEN it SHALL print `backup: <dst> -> <dst>.bak` to stdout. <!-- event-driven -->
8. The installers SHALL route `~/.claude/settings.json` (`scripts/claude.install.sh`), `~/.gemini/settings.json` (`scripts/gemini.install.sh`), `~/.copilot/mcp-config.json` and `~/.copilot/config.json` (`scripts/copilot.install.sh`) through `link_with_backup`, with no remaining `rm` of those paths. <!-- ubiquitous -->

**Independent Test**: `uv run --with pytest pytest scripts/test_link_with_backup.py` green; run `scripts/claude.install.sh` with `HOME` and `LOCAL` pointed at temp dirs holding a regular `settings.json`, then `ls -la` shows the symlink plus `settings.json.bak`.

---

### P1: Documented test command runs a real suite ⭐ MVP

**User Story**: As a contributor, I want the documented test command to run the tracked tests so that "tests pass" means something.

**Why P1**: The current command exits 5 with 0 tests; every doc referencing it misleads.

**Acceptance Criteria**:

1. The `AGENTS.md` "Run tests" block SHALL contain `uv run --with pytest pytest scripts/` and SHALL NOT contain `cd src && uv run pytest`. <!-- ubiquitous -->
2. WHEN `uv run --with pytest pytest scripts/` runs from the repo root THEN it SHALL collect at least 1 test and exit 0. <!-- event-driven -->
3. The `AGENTS.md` edit SHALL leave the owner's pre-existing uncommitted hunks unchanged. <!-- ubiquitous -->

**Independent Test**: run the command and read the summary line; `git diff AGENTS.md` shows the pending hunks plus the one test-command hunk.

---

### P2: Reference tables moved out of README

**User Story**: As a reader, I want the long env-var and external-tool tables in their own docs so that the README stays scannable.

**Why P2**: Readability; README rewrite links these files.

**Acceptance Criteria**:

1. The `docs/environment.md` file SHALL contain every row of the current README "Environment Variables" table, byte-identical. <!-- ubiquitous -->
2. The `docs/external-tools.md` file SHALL contain every row of the current README "External Tools" table, byte-identical. <!-- ubiquitous -->

**Independent Test**: extract the table rows from `git show HEAD:README.md` and diff against each new file's rows; diff is empty.

---

### P2: README rewrite

**User Story**: As a first-time visitor, I want a README with a pitch, requirements, quickstart, and how-it-works so that I can install and use aipp without reading the scripts.

**Why P2**: Main deliverable for third parties; depends on P1 (warning text describes the backup).

**Acceptance Criteria**:

1. The `README.md` SHALL present, in order: title + one-line pitch + badges (Python 3.11+, uv); What's included; Requirements; a `> [!WARNING]` block; Quickstart; How it works; Handy aliases; Uninstall; Directory structure; Reference. <!-- ubiquitous -->
2. The README SHALL NOT state numeric counts of skills, agents, or other components. <!-- ubiquitous -->
3. The Requirements section SHALL list git, curl, `uv`, Node >= 24, `claude` CLI, and state "Tested on Linux; macOS partial". <!-- ubiquitous -->
4. The warning block SHALL state that shell rc files (`~/.zshrc`, `~/.bashrc`) are edited and that global harness config files are replaced by symlinks with the previous regular file saved as `<path>.bak`. <!-- ubiquitous -->
5. The Quickstart SHALL describe stage 1 (`bash install.sh` inside the clone, installing the `aipp` command) and stage 2 (`aipp --<backend>` inside a project), plus a flags table. <!-- ubiquitous -->
6. Every flag in the README flags table SHALL be accepted by `install.sh` argument parsing. <!-- ubiquitous -->
7. Every alias named in the README SHALL be defined in `.aipp.alias.zshrc`. <!-- ubiquitous -->
8. Every relative link in the README SHALL resolve to an existing path in the repo. <!-- ubiquitous -->
9. The Uninstall section SHALL state that `uninstall.sh` does not restore `.bak` files and how to restore one manually. <!-- ubiquitous -->
10. The README SHALL document the test command `uv run --with pytest pytest scripts/` (or link to `CONTRIBUTING.md` which does). <!-- ubiquitous -->

**Independent Test**: scripted link/flag/alias check (see design) exits 0; visual read of section order.

---

### P3: CONTRIBUTING.md

**User Story**: As a contributor, I want a guide for adding skills, agents, and hooks so that my additions follow repo conventions and show up correctly.

**Why P3**: Useful but not needed to install or use aipp.

**Acceptance Criteria**:

1. The `CONTRIBUTING.md` SHALL describe adding a skill (`skills/<name>/SKILL.md` frontmatter `name` and `description` required, `metadata` optional) and an agent (`agents/<name>.agent.md` frontmatter `name`, `description`). <!-- ubiquitous -->
2. The `CONTRIBUTING.md` SHALL name `scripts/list_skills_agents.py` and `scripts/build-skill-index.py` as the index regeneration step and state that new catalog items enter disabled and are enabled with `mif`. <!-- ubiquitous -->
3. The `CONTRIBUTING.md` SHALL describe adding a hook: script in `hooks/scripts/`, wiring in `claude/settings.json` (source of truth), docs in `hooks/README.md`, and the `verify-hook` command. <!-- ubiquitous -->
4. The `CONTRIBUTING.md` SHALL document the test command `uv run --with pytest pytest scripts/` and the commit rules (Conventional Commits, no emoji, no AI mentions, English). <!-- ubiquitous -->
5. Every relative link and every script path named in `CONTRIBUTING.md` SHALL resolve to an existing path. <!-- ubiquitous -->

**Independent Test**: same scripted link check as README, run on `CONTRIBUTING.md`.

---

## Edge Cases

- IF `<dst>` is a dangling symlink THEN the helper SHALL replace it with no `.bak` (covered by P1 AC2).
- IF `<dst>` is a directory THEN the helper SHALL refuse (P1 AC5).
- WHEN an installer runs a second time THEN `<dst>` is a symlink, so the first `.bak` SHALL remain unchanged.
- IF `<src>` or `<dst>` contains spaces THEN the helper SHALL still operate on the exact paths (all expansions quoted).

## Implicit-Requirement Dimensions

| Dimension                        | Resolution                                                                         |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| Input validation & bounds        | Directory dst refused (AC5); quoted paths (edge case)                              |
| Failure / partial-failure states | Backup is `mv` before `ln`; if `ln` fails the original is at `.bak` (documented)   |
| Idempotency / retry              | Second run sees symlink, never touches `.bak` (edge case)                          |
| Auth boundaries & rate limits    | N/A because local shell script, no auth surface                                    |
| Concurrency / ordering           | N/A because installers run interactively, one at a time                            |
| Data lifecycle / expiry          | Single `.bak`, overwritten only when a new regular file appears (AC4)              |
| Observability                    | `backup:` stdout line (AC7)                                                        |
| External-dependency failure      | N/A because only coreutils (`mv`, `ln`, `mkdir`)                                   |
| State-transition integrity       | Missing / symlink / file / directory states each have one defined action (AC1-AC5) |

---

## Requirement Traceability

| Requirement ID | Story                                        | Phase | Status  |
| -------------- | -------------------------------------------- | ----- | ------- |
| LINK-01        | P1: Installers back up (AC1 missing dst)     | Tasks | Pending |
| LINK-02        | P1: Installers back up (AC2 symlink dst)     | Tasks | Pending |
| LINK-03        | P1: Installers back up (AC3 regular file)    | Tasks | Pending |
| LINK-04        | P1: Installers back up (AC4 existing .bak)   | Tasks | Pending |
| LINK-05        | P1: Installers back up (AC5 directory)       | Tasks | Pending |
| LINK-06        | P1: Installers back up (AC6 missing parent)  | Tasks | Pending |
| LINK-07        | P1: Installers back up (AC7 backup message)  | Tasks | Pending |
| LINK-08        | P1: Installers back up (AC8 call sites)      | Tasks | Pending |
| TEST-01        | P1: Test command (AC1 AGENTS.md text)        | Tasks | Pending |
| TEST-02        | P1: Test command (AC2 runs non-empty)        | Tasks | Pending |
| TEST-03        | P1: Test command (AC3 pending diff kept)     | Tasks | Pending |
| REF-01         | P2: Reference tables (AC1 environment.md)    | Tasks | Pending |
| REF-02         | P2: Reference tables (AC2 external-tools.md) | Tasks | Pending |
| README-01      | P2: README (AC1 section order)               | Tasks | Pending |
| README-02      | P2: README (AC2 no counts)                   | Tasks | Pending |
| README-03      | P2: README (AC3 requirements)                | Tasks | Pending |
| README-04      | P2: README (AC4 warning)                     | Tasks | Pending |
| README-05      | P2: README (AC5 quickstart)                  | Tasks | Pending |
| README-06      | P2: README (AC6 flags exist)                 | Tasks | Pending |
| README-07      | P2: README (AC7 aliases exist)               | Tasks | Pending |
| README-08      | P2: README (AC8 links resolve)               | Tasks | Pending |
| README-09      | P2: README (AC9 uninstall restore)           | Tasks | Pending |
| README-10      | P2: README (AC10 test command)               | Tasks | Pending |
| CONTRIB-01     | P3: CONTRIBUTING (AC1 skill/agent)           | Tasks | Pending |
| CONTRIB-02     | P3: CONTRIBUTING (AC2 indexes + mif)         | Tasks | Pending |
| CONTRIB-03     | P3: CONTRIBUTING (AC3 hooks)                 | Tasks | Pending |
| CONTRIB-04     | P3: CONTRIBUTING (AC4 tests + commits)       | Tasks | Pending |
| CONTRIB-05     | P3: CONTRIBUTING (AC5 links resolve)         | Tasks | Pending |

**Coverage:** 28 total, 28 mapped to tasks, 0 unmapped

`requirements.md` is a derived reviewer view of these IDs (rows FR-001..FR-043); each task in `tasks.md` lists both its requirement IDs and its `Review rows`.

---

## Success Criteria

- [ ] `uv run --with pytest pytest scripts/` exits 0 with the new link tests included.
- [ ] Fake-`HOME` installer run leaves `settings.json` as a symlink and `settings.json.bak` byte-identical to the original.
- [ ] Doc check script (links, flags, aliases) exits 0 for `README.md` and `CONTRIBUTING.md`.
