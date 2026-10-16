# README Improvement + Safe Global Config Linking — Requirements Table

**Spec:** `.specs/features/readme-improvement/spec.md`
**Design:** `.specs/features/readme-improvement/design.md`
**Tasks:** `.specs/features/readme-improvement/tasks.md`
**Status:** Draft
**Created:** 2026-10-16

> Each row is one decision: Expression states the condition and outcome, Complement says why, Path tags success (SP) or error (EP). Every row stands alone.

---

## 1. Linking a global config file to the repo

Applies whenever an installer points a file in the user's home config folder at the repo's copy.

| Requiriment | Scenario                                        | Expression                                                                                                                                                                                                             | Complement                                                                                 | Path |
| ----------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ---- |
| FR-001      | Nothing exists at the destination               | **Given** no file or link at the destination path **When** the link step runs **Then** the destination becomes a link to the repo's copy **And** no backup file is created                                             | Nothing to preserve, so no backup clutter                                                  | SP   |
| FR-002      | Destination is already a link                   | **Given** the destination is a link to anything **When** the link step runs **Then** the link is replaced by one pointing to the repo's copy **And** no backup file is created                                         | A link holds no user data; backing it up would overwrite a real backup on every re-install | SP   |
| FR-003      | Destination is a broken link                    | **Given** the destination is a link whose target no longer exists **When** the link step runs **Then** it is replaced like any other link **And** no backup file is created                                            | Broken links are common after moving the repo; they must not block the install             | SP   |
| FR-004      | Destination is the user's own file              | **Given** the destination is a regular file **When** the link step runs **Then** that file is moved to the same path with a `.bak` suffix, content unchanged **And** the destination becomes a link to the repo's copy | Today this file is deleted; the user's settings must survive the install                   | SP   |
| FR-005      | A backup from an earlier install already exists | **Given** the destination is a regular file **And** a `.bak` file already sits beside it **When** the link step runs **Then** the old `.bak` is replaced by the current file                                           | One backup slot, holding the most recent real file the user had                            | SP   |
| FR-006      | Destination is a folder                         | **Given** the destination path is a folder **When** the link step runs **Then** the folder and its contents are left untouched **And** a warning is printed to the error stream **And** the step reports failure       | Replacing a folder could destroy many files; refusing is the only safe choice              | EP   |
| FR-007      | Parent folder does not exist                    | **Given** the folder that should contain the destination does not exist **When** the link step runs **Then** the folder is created **And** the link is created inside it                                               | On a fresh machine the copilot config folder is absent and linking used to fail            | SP   |
| FR-008      | User is told where the backup went              | **Given** a regular file was moved aside **When** the link step finishes **Then** one line naming the original path and the `.bak` path is printed                                                                     | A silent backup is as good as lost if the user never learns of it                          | SP   |
| FR-009      | Paths contain spaces                            | **Given** the repo path or the home path contains spaces **When** the link step runs **Then** it acts on the exact paths given **And** never on a split fragment of them                                               | Unquoted paths in the old code could delete the wrong file                                 | SP   |
| FR-010      | Installer runs a second time                    | **Given** a previous install already created the link and a `.bak` **When** the installer runs again **Then** the `.bak` keeps its content                                                                             | Re-installs are routine; they must not erase the only copy of the user's original file     | SP   |
| FR-011      | Linking fails after the backup was taken        | **Given** the regular file was already moved to `.bak` **When** creating the link fails **Then** the original content remains in the `.bak` file                                                                       | No failure point leaves the user's settings deleted                                        | EP   |

---

## 2. Installers that touch global config

| Requiriment | Scenario                               | Expression                                                                                                                                                                            | Complement                                                                        | Path |
| ----------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---- |
| FR-012      | Claude installer                       | **Given** the Claude installer runs **When** it links the global Claude settings file **Then** it uses the backup-aware link step **And** it no longer deletes that file directly     | Claude settings are the most customized file users have                           | SP   |
| FR-013      | Gemini installer                       | **Given** the Gemini installer runs **When** it links the global Gemini settings file **Then** it uses the backup-aware link step **And** it no longer deletes that file directly     | Same data-loss risk as Claude                                                     | SP   |
| FR-014      | Copilot MCP config                     | **Given** the Copilot installer runs **When** it links the global Copilot MCP config file **Then** it uses the backup-aware link step **And** it no longer deletes that file directly | Users often hand-edit MCP server lists                                            | SP   |
| FR-015      | Copilot general config                 | **Given** the Copilot installer runs **When** it links the global Copilot config file **Then** it uses the backup-aware link step **And** it no longer deletes that file directly     | Same risk, second file in the same installer                                      | SP   |
| FR-016      | Link step refuses a folder mid-install | **Given** one destination is a folder **When** an installer runs **Then** the warning is printed **And** the installer continues with its remaining steps                             | Installers do not stop on errors; one refused path must not abort the whole setup | EP   |

---

## 3. Documented test command

| Requiriment | Scenario                                  | Expression                                                                                                                                                                                            | Complement                                                       | Path |
| ----------- | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ---- |
| FR-017      | Agent instructions name a working command | **Given** the agent instruction file's "Run tests" block **Then** it shows the command that runs the tests under `scripts/` **And** it no longer shows the command that runs from `src/`              | The old command collects zero tests and exits with an error code | SP   |
| FR-018      | Documented command actually runs tests    | **Given** a checkout of the repo **When** the documented command runs from the repo root **Then** at least one test is collected **And** the run exits successfully                                   | "Tests pass" must mean tests ran                                 | SP   |
| FR-019      | Owner's unrelated edits survive           | **Given** the agent instruction file has uncommitted edits by the owner **When** the test command is changed **Then** those edits stay as they were **And** only the test command change is committed | The owner has pending work in the same file                      | SP   |

---

## 4. Reference documents split out of the README

| Requiriment | Scenario                        | Expression                                                                                                                                                       | Complement                                                                       | Path |
| ----------- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---- |
| FR-020      | Environment variables reference | **Given** the environment-variable table in the current README **Then** a dedicated environment document contains every one of its rows, character for character | Moves bulk out of the README without losing or altering a single entry           | SP   |
| FR-021      | External tools reference        | **Given** the external-tools table in the current README **Then** a dedicated external-tools document contains every one of its rows, character for character    | Moves the tools list out of the README without losing or altering a single entry | SP   |

---

## 5. README content

| Requiriment | Scenario                          | Expression                                                                                                                                                                                                                                         | Complement                                                                         | Path |
| ----------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ---- |
| FR-022      | Section order                     | **Given** the README **Then** it reads, in order: title with one-line pitch and badges, what's included, requirements, a warning block, quickstart, how it works, handy aliases, uninstall, directory structure, reference links                   | Visitors decide in seconds; pitch and setup come before internals                  | SP   |
| FR-023      | Badges                            | **Given** the README header **Then** it shows static badges for the Python version floor and for uv                                                                                                                                                | Signals the toolchain at a glance without a CI service                             | SP   |
| FR-024      | No component counts               | **Given** the README **Then** it describes each component kind and links to its folder or index **And** states no number of skills, agents or other items                                                                                          | Counts change with every added skill and would silently go stale                   | SP   |
| FR-025      | Requirements list                 | **Given** the requirements section **Then** it lists git, curl, uv, Node 24 or newer and the Claude CLI                                                                                                                                            | These are installed or assumed by the bootstrap but never stated today             | SP   |
| FR-026      | Platform support statement        | **Given** the requirements section **Then** it states the project is tested on Linux **And** macOS support is partial                                                                                                                              | One bundled tool download only targets Linux x86_64                                | SP   |
| FR-027      | Warning: shell startup files      | **Given** the warning block **Then** it states that the user's zsh and bash startup files are edited                                                                                                                                               | Silent edits to startup files surprise users                                       | SP   |
| FR-028      | Warning: global config replaced   | **Given** the warning block **Then** it states that global harness config files become links into the repo **And** that a previous regular file is kept beside it with a `.bak` suffix                                                             | Users must know before installing that their config changes hands                  | SP   |
| FR-029      | Two-stage quickstart              | **Given** the quickstart **Then** it shows the one-time bootstrap run inside the clone that installs the `aipp` command **And** the per-project run of `aipp` with a backend flag                                                                  | The real flow has two stages; today the README implies one                         | SP   |
| FR-030      | Flags table matches the installer | **Given** every flag listed in the quickstart flags table **Then** the installer accepts it                                                                                                                                                        | A documented flag that does not exist wastes the reader's first attempt            | SP   |
| FR-031      | How it works                      | **Given** the how-it-works section **Then** it explains that items are linked into the project's harness folder **And** that per-project toggles live in a user settings file seeded from repo defaults **And** that a selection tool toggles them | The per-project selection is the core idea and is undocumented today               | SP   |
| FR-032      | Aliases exist                     | **Given** every alias named in the aliases section **Then** the repo's alias file defines it                                                                                                                                                       | A documented alias that does not exist fails with "command not found" on first try | SP   |
| FR-033      | Links resolve                     | **Given** every relative link in the README **Then** it points to a path that exists in the repo                                                                                                                                                   | Broken links on a public repo erode trust immediately                              | SP   |
| FR-034      | Uninstall and restore             | **Given** the uninstall section **Then** it says what the uninstall script removes **And** that it does not restore `.bak` files **And** how to restore one by hand                                                                                | Uninstall leaves the links in place; users need a manual way back                  | SP   |
| FR-035      | Test command in README            | **Given** the README **Then** it shows the working test command or links to the contributing guide that does                                                                                                                                       | Contributors land on the README first                                              | SP   |

---

## 6. Contributing guide

| Requiriment | Scenario                      | Expression                                                                                                                                                                                                                  | Complement                                                                                                         | Path |
| ----------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---- |
| FR-036      | Adding a skill                | **Given** the contributing guide **Then** it shows where a new skill's file goes and which header fields it needs (name and description required, metadata optional)                                                        | Skills without a name and description do not load or trigger                                                       | SP   |
| FR-037      | Adding an agent               | **Given** the contributing guide **Then** it shows where a new agent's file goes and which header fields it needs (name, description)                                                                                       | Agents without the right header are not listed or selectable                                                       | SP   |
| FR-038      | Regenerating indexes          | **Given** the contributing guide **Then** it names the two scripts that rebuild the skill and agent indexes                                                                                                                 | Indexes are generated; editing them by hand drifts                                                                 | SP   |
| FR-039      | New items start disabled      | **Given** the contributing guide **Then** it states that newly added items enter the catalog disabled **And** that the selection tool enables them                                                                          | Otherwise contributors think their new skill is broken                                                             | SP   |
| FR-040      | Adding a hook                 | **Given** the contributing guide **Then** it says hook scripts go in the hooks scripts folder **And** are wired in the repo's Claude settings file, which is the source of truth **And** are documented in the hooks README | The hooks README still mentions a hooks file that no longer exists; contributors need the one real wiring location | SP   |
| FR-041      | Verifying a hook              | **Given** the contributing guide **Then** it names the hook-verification command for an end-to-end check                                                                                                                    | A hook that is wired but never fires fails silently                                                                | SP   |
| FR-042      | Tests and commit rules        | **Given** the contributing guide **Then** it shows the working test command **And** lists the commit rules: Conventional Commits, no emoji, no AI mentions, English only                                                    | Commits breaking these rules are rejected by git hooks                                                             | SP   |
| FR-043      | Guide links and paths resolve | **Given** every relative link and script path named in the contributing guide **Then** it exists in the repo                                                                                                                | A guide pointing at missing files sends contributors in circles                                                    | SP   |

---

## 7. Accepted consequences (not defects)

Each behavior below is intended per its rows, but costs something in combination.

| #   | Consequence                                                                                                                                                                                                                           | Driven by                      |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| 1   | Only one backup is kept per path: if a user replaces the link with a real file twice, the first real file is lost on the second install.                                                                                              | FR-005, FR-010                 |
| 2   | Uninstall does not restore anything: the four global config paths stay as links into the repo; deleting the clone leaves four broken links until the user restores the `.bak` files by hand.                                          | FR-034                         |
| 3   | A folder at a destination path is never linked: that harness keeps running on the folder's content and the installer only prints a warning, which is easy to miss in long install output.                                             | FR-006, FR-016                 |
| 4   | The Copilot installer now creates the Copilot config folder in the user's home even if Copilot was never installed.                                                                                                                   | FR-007, FR-014, FR-015         |
| 5   | The Claude installer still writes to the fixed home Claude folder, while the bootstrap sets a separate Claude config folder variable; users with a custom config folder get their settings linked in the wrong place. Not fixed here. | FR-012                         |
| 6   | Installer wiring is verified by checking the script text plus one manual smoke run, not by an automated end-to-end install; a later edit that keeps the call but breaks its arguments passes the text check only if it still matches. | FR-012 – FR-015                |
| 7   | The link/flag/alias doc checks are run by hand during this work and not committed; later README edits can reintroduce broken links or stale flags unnoticed.                                                                          | FR-030, FR-032, FR-033, FR-043 |
| 8   | The README flags table lists one flag the installer's own help screen omits, so the two disagree until the help screen is fixed separately.                                                                                           | FR-030                         |
| 9   | Moving the two tables out of the README means old deep links to README anchors for those sections break.                                                                                                                              | FR-020, FR-021                 |

---

## Glossary

- **FR** — functional requirement
- **SP** — success path
- **EP** — error path
- **`.bak`** — backup copy of a user's file, kept beside the original path with a `.bak` suffix
- **Link** — a symbolic link (filesystem pointer to another path)
- **Harness** — an AI coding tool (Claude Code, Gemini CLI, Copilot) whose config this repo manages
