# Changelog

## v2026.11.04 (Unreleased - based on v0.55.0)

### **2026-11-04**

- **[🧹 Chores]** Enable egm plugin and fork readonly command ([caa8d0b](https://github.com/Ronnasayd/aipp/commit/caa8d0b))

## v0.55.0 (2026-11-04)

### **2026-11-04**

- **[✨ Features]** Show effort level as segmented bar ([6915d60c](https://github.com/Ronnasayd/aipp/commit/6915d60c))

## v0.54.0 (2026-11-04)

### **2026-11-04**

- **[✨ Features]** Add total tool call count to stats line ([cc296fa](https://github.com/Ronnasayd/aipp/commit/cc296fa))

## v0.53.0 (2026-11-04)

### **2026-11-04**

- **[✨ Features]** Run context-map and spec skills as forked subagents ([661ff87](https://github.com/Ronnasayd/aipp/commit/661ff87))

## v0.52.0 (2026-11-04)

### **2026-11-04**

- **[✨ Features]** Enforce skill model frontmatter for rest of turn ([604968b](https://github.com/Ronnasayd/aipp/commit/604968b))

### **2026-11-03**

- **[🧹 Chores]** Wire log_hooks to more lifecycle events and pin model ([e706bf9](https://github.com/Ronnasayd/aipp/commit/e706bf9))
- **[✨ Features]** Show next pending task per taskmaster tag ([a52ce49](https://github.com/Ronnasayd/aipp/commit/a52ce49))
- **[🚧 Other Changes]** Cover a single failing root among several ([555388e](https://github.com/Ronnasayd/aipp/commit/555388e))
- **[🚧 Other Changes]** Lint changed files in per-root batches ([f24e7a8](https://github.com/Ronnasayd/aipp/commit/f24e7a8))
- **[🚧 Other Changes]** Batch go vet, golangci-lint and gofmt ([a8db28f](https://github.com/Ronnasayd/aipp/commit/a8db28f))
- **[🚧 Other Changes]** Batch phpstan over all files ([e951b31](https://github.com/Ronnasayd/aipp/commit/e951b31))
- **[🚧 Other Changes]** Batch tsc-files and eslint over all files ([1fe2b73](https://github.com/Ronnasayd/aipp/commit/1fe2b73))
- **[🚧 Other Changes]** Batch mypy, ruff and pylint over all files ([5beb89e](https://github.com/Ronnasayd/aipp/commit/5beb89e))
- **[♻️ Refactoring]** Take a file list in lint dispatchers ([14d7179](https://github.com/Ronnasayd/aipp/commit/14d7179))
- **[♻️ Refactoring]** Make run_jscpd filter by a set of files ([0545c59](https://github.com/Ronnasayd/aipp/commit/0545c59))
- **[🧹 Chores]** Use model aliases in frontmatter ([186f7bd](https://github.com/Ronnasayd/aipp/commit/186f7bd))

## v0.51.0 (2026-11-03)

### **2026-11-03**

- **[✨ Features]** Count skill and other tool calls in tool-stats ([fa25fb2](https://github.com/Ronnasayd/aipp/commit/fa25fb2))

## v0.50.1 (2026-11-03)

### **2026-11-03**

- **[🐛 Bug Fixes]** Keep tool-history band clickable with router plugin ([224a30c](https://github.com/Ronnasayd/aipp/commit/224a30c))

## v0.50.0 (2026-11-03)

### **2026-11-03**

- **[✨ Features]** Add tool-stats mod with per-session tool counts ([51c5454](https://github.com/Ronnasayd/aipp/commit/51c5454))

## v0.49.0 (2026-11-03)

### **2026-11-03**

- **[✨ Features]** Enable claude-router plugin ([5451961](https://github.com/Ronnasayd/aipp/commit/5451961))

### **2026-10-31**

- **[♻️ Refactoring]** Add .tlc on clean ([1bb9126](https://github.com/Ronnasayd/aipp/commit/1bb9126))

## v0.48.0 (2026-10-30)

### **2026-10-30**

- **[✨ Features]** Add reverse-engineer-anything skill from rea ([2046a81](https://github.com/Ronnasayd/aipp/commit/2046a81))
- **[📚 Documentation]** Add yes pipe example; format json files and fix uninstall cleanup ([c3f9a9d](https://github.com/Ronnasayd/aipp/commit/c3f9a9d))

## v0.47.0 (2026-10-30)

### **2026-10-30**

- **[✨ Features]** Add skip_mcp_merge env var to preserve existing .mcp.json ([97c336a](https://github.com/Ronnasayd/aipp/commit/97c336a))
- **[♻️ Refactoring]** Compress mandatory rules to caveman format ([cb02696](https://github.com/Ronnasayd/aipp/commit/cb02696))
- **[📚 Documentation]** Add mandatory rules for task cleanup and permanent memory ([6c843b7](https://github.com/Ronnasayd/aipp/commit/6c843b7))

## v0.46.0 (2026-10-30)

### **2026-10-30**

- **[✨ Features]** Add skip_lint and skip_tests environment variables ([76b388f](https://github.com/Ronnasayd/aipp/commit/76b388f))

## v0.45.0 (2026-10-30)

### **2026-10-30**

- **[✨ Features]** Enable live output for hook commands with follow option ([9e0d792](https://github.com/Ronnasayd/aipp/commit/9e0d792))

### **2026-10-29**

- **[♻️ Refactoring]** Move documentation language rule to start_context hook ([2b80aa1](https://github.com/Ronnasayd/aipp/commit/2b80aa1))

## v0.44.0 (2026-10-29)

### **2026-10-29**

- **[✨ Features]** Expand readonly mode to block write-capable commands and serena tools ([823c122](https://github.com/Ronnasayd/aipp/commit/823c122))

## v0.43.0 (2026-10-29)

### **2026-10-29**

- **[✨ Features]** Add all tab mixing messages and tool calls by arrival order ([fde17f9](https://github.com/Ronnasayd/aipp/commit/fde17f9))
- **[♻️ Refactoring]** Adjust mcp tool name ([a8d4923](https://github.com/Ronnasayd/aipp/commit/a8d4923))

## v0.42.0 (2026-10-29)

### **2026-10-29**

- **[✨ Features]** Add readonly mode toggle command ([f93af99](https://github.com/Ronnasayd/aipp/commit/f93af99))

## v0.41.0 (2026-10-29)

### **2026-10-29**

- **[✨ Features]** Add agent tool calls to messages tab and fix card spacing ([2e3b9b1](https://github.com/Ronnasayd/aipp/commit/2e3b9b1))

## v0.40.0 (2026-10-29)

### **2026-10-29**

- **[✨ Features]** Show agent name in card header, remove section dividers - replace separator dividers ( main ) with inline agent labels in each message/call card - flatten grouped render loops to iterate directly over items - add border colors to message cards: yellow for subagent, green for user, blue for assistant text - add border colors to tool call cards: yellow for subagent calls, red for errors - show "main" or subagent name in card header (e.g., "main - text" or "general-purpose - $ bash") - add test: verify subagent calls/messages render with yellow borders and agent label in title ([bb4b3c3](https://github.com/Ronnasayd/aipp/commit/bb4b3c3))

## v0.39.0 (2026-10-28)

### **2026-10-28**

- **[✨ Features]** Add 5h window burn-rate multiplier ([0a193f6](https://github.com/Ronnasayd/aipp/commit/0a193f6))
- **[♻️ Refactoring]** Collapse tool-history pane by default and consolidate toggle logic ([d5405d8](https://github.com/Ronnasayd/aipp/commit/d5405d8))
- **[📚 Documentation]** Consolidate hallucination protection rules and remove skill duplicates ([afeb093](https://github.com/Ronnasayd/aipp/commit/afeb093))

## v0.38.3 (2026-10-27)

### **2026-10-27**

- **[🐛 Bug Fixes]** Ping while main turn waits on subagent ([411c8e3](https://github.com/Ronnasayd/aipp/commit/411c8e3))

## v0.38.2 (2026-10-27)

### **2026-10-27**

- **[🐛 Bug Fixes]** Remove classic.sessionstart hook bypassed by security plugin ([c6662b8](https://github.com/Ronnasayd/aipp/commit/c6662b8))

## v0.38.1 (2026-10-27)

### **2026-10-27**

- **[🐛 Bug Fixes]** Reset transcript lookup path on session end ([852104b](https://github.com/Ronnasayd/aipp/commit/852104b))
- **[♻️ Refactoring]** Update agents.md formatting and expand rag-rat tlc skill indexing ([f153fb1](https://github.com/Ronnasayd/aipp/commit/f153fb1))

## v0.38.0 (2026-10-27)

### **2026-10-27**

- **[✨ Features]** Add request count with down arrow indicator to cost display ([18f1c29](https://github.com/Ronnasayd/aipp/commit/18f1c29))
- **[♻️ Refactoring]** Update external skills ([315f0f5](https://github.com/Ronnasayd/aipp/commit/315f0f5))

## v0.37.2 (2026-10-26)

### **2026-10-26**

- **[🐛 Bug Fixes]** Standardize duration display format to hh:mm:ss ([26f4b22](https://github.com/Ronnasayd/aipp/commit/26f4b22))

## v0.37.1 (2026-10-26)

### **2026-10-26**

- **[🐛 Bug Fixes]** Improve cost delta display format and baseline initialization ([a25df14](https://github.com/Ronnasayd/aipp/commit/a25df14))

## v0.37.0 (2026-10-26)

### **2026-10-26**

- **[✨ Features]** Add average cost per request to cost display ([c50bb77](https://github.com/Ronnasayd/aipp/commit/c50bb77))

## v0.36.0 (2026-10-23)

### **2026-10-23**

- **[✨ Features]** Move toolbar to band and add jump-to-end button ([a13d2d3](https://github.com/Ronnasayd/aipp/commit/a13d2d3))
- **[♻️ Refactoring]** Update ui controls—emoji buttons, structural keys, gap management ([51124a2](https://github.com/Ronnasayd/aipp/commit/51124a2))

## v0.35.0 (2026-10-23)

### **2026-10-23**

- **[✨ Features]** Add collapse/expand toggle for pane ([713799b](https://github.com/Ronnasayd/aipp/commit/713799b))

## v0.34.0 (2026-10-22)

### **2026-10-22**

- **[✨ Features]** Add session-specific rate-limit tracking ([1129c4b](https://github.com/Ronnasayd/aipp/commit/1129c4b))
- **[♻️ Refactoring]** Consolidate dev server patterns with generator expression ([8189657](https://github.com/Ronnasayd/aipp/commit/8189657))

## v0.33.0 (2026-10-22)

### **2026-10-22**

- **[✨ Features]** Add prompt cache warmer plugin with tests ([2fdc0c0](https://github.com/Ronnasayd/aipp/commit/2fdc0c0))
- **[♻️ Refactoring]** Adjust statusline positions ([c4cd9a1](https://github.com/Ronnasayd/aipp/commit/c4cd9a1))

## v0.32.0 (2026-10-22)

### **2026-10-22**

- **[✨ Features]** Add cost delta display between api calls ([f7a1a77](https://github.com/Ronnasayd/aipp/commit/f7a1a77))

## v0.31.0 (2026-10-22)

### **2026-10-22**

- **[✨ Features]** Add prompt cache ttl countdown display ([04a4d4c](https://github.com/Ronnasayd/aipp/commit/04a4d4c))

## v0.30.0 (2026-10-21)

### **2026-10-21**

- **[✨ Features]** Add sticky-bottom auto-scroll when user scrolls freely ([aedeec9](https://github.com/Ronnasayd/aipp/commit/aedeec9))

## v0.29.0 (2026-10-21)

### **2026-10-21**

- **[✨ Features]** Add high-severity re-verification loop (step 5.5) ([d52c367](https://github.com/Ronnasayd/aipp/commit/d52c367))

## v0.28.7 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Add granular mode flags and glued-syntax detection ([919b6fe](https://github.com/Ronnasayd/aipp/commit/919b6fe))
- **[♻️ Refactoring]** Add new mandatory rules ([3377e09](https://github.com/Ronnasayd/aipp/commit/3377e09))

## v0.28.6 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Skip go-bindata generated files ([049a204](https://github.com/Ronnasayd/aipp/commit/049a204))

## v0.28.5 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Skip go-bindata generated files ([f5cafd6](https://github.com/Ronnasayd/aipp/commit/f5cafd6))

## v0.28.4 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Use dynamic uv project detection instead of hardcoded toplevel ([02fed47](https://github.com/Ronnasayd/aipp/commit/02fed47))

## v0.28.3 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Run linters on package dir to preserve sibling symbols, filter output to edited file only ([a9e5b64](https://github.com/Ronnasayd/aipp/commit/a9e5b64))

## v0.28.2 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Skip linting go-bindata generated files ([81fc95d](https://github.com/Ronnasayd/aipp/commit/81fc95d))

## v0.28.1 (2026-10-21)

### **2026-10-21**

- **[🐛 Bug Fixes]** Update golangci-lint output flag to new syntax ([6951f9c](https://github.com/Ronnasayd/aipp/commit/6951f9c))

## v0.28.0 (2026-10-20)

### **2026-10-20**

- **[✨ Features]** Add :r/:rw mode suffix to allowlist patterns, restrict writes to readonly paths ([4036f0b](https://github.com/Ronnasayd/aipp/commit/4036f0b))

## v0.27.2 (2026-10-20)

### **2026-10-20**

- **[🐛 Bug Fixes]** Cap bash summary and result text to prevent render crash ([ada784f](https://github.com/Ronnasayd/aipp/commit/ada784f))
- **[📚 Documentation]** Clarify askuserquestion contextualization requirements ([256aaac](https://github.com/Ronnasayd/aipp/commit/256aaac))

## v0.27.1 (2026-10-20)

### **2026-10-20**

- **[🐛 Bug Fixes]** Cap bash result text at 2000 chars to prevent render crash ([01a29f5](https://github.com/Ronnasayd/aipp/commit/01a29f5))

## v0.27.0 (2026-10-20)

### **2026-10-20**

- **[✨ Features]** Render agent messages as markdown ([1dbc6bd](https://github.com/Ronnasayd/aipp/commit/1dbc6bd))

## v0.26.0 (2026-10-20)

### **2026-10-20**

- **[✨ Features]** Add clickable links to full tool results and figma-console mcp ([f733890](https://github.com/Ronnasayd/aipp/commit/f733890))

## v0.25.0 (2026-10-20)

### **2026-10-20**

- **[✨ Features]** Add user prompts to agent messages pane and move buttons to bottom ([041afb5](https://github.com/Ronnasayd/aipp/commit/041afb5))

## v0.24.0 (2026-10-16)

### **2026-10-16**

- **[✨ Features]** Add agent message recording and tabbed message/calls view ([3b3105e](https://github.com/Ronnasayd/aipp/commit/3b3105e))

## v0.23.5 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Sanitize ansi escapes in result text to prevent render crash ([2f22889](https://github.com/Ronnasayd/aipp/commit/2f22889))

## v0.23.4 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Add protect_files_extra_allowed to settings.local.json ([2c26026](https://github.com/Ronnasayd/aipp/commit/2c26026))

## v0.23.3 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Use agent_type to guard against subagent hook false positives ([0b7fbf7](https://github.com/Ronnasayd/aipp/commit/0b7fbf7))

## v0.23.2 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Guard subagent format hook against claude code stop event bug ([d43338e](https://github.com/Ronnasayd/aipp/commit/d43338e))
- **[🧹 Chores]** Register tool-history plugin and update indexing ([5e8bb73](https://github.com/Ronnasayd/aipp/commit/5e8bb73))
- **[♻️ Refactoring]** Migrate from per-file accounts to centralized secrets storage ([341df2b](https://github.com/Ronnasayd/aipp/commit/341df2b))
- **[📚 Documentation]** Add readme improvement feature plan and taskmaster config ([4b04242](https://github.com/Ronnasayd/aipp/commit/4b04242))
- **[📚 Documentation]** Show the install warning as a warning block ([815e71f](https://github.com/Ronnasayd/aipp/commit/815e71f))
- **[📚 Documentation]** Add a contributing guide for skills, hooks and commits ([d2a7aff](https://github.com/Ronnasayd/aipp/commit/d2a7aff))
- **[📚 Documentation]** Rewrite with quickstart and install side effects ([068b950](https://github.com/Ronnasayd/aipp/commit/068b950))
- **[📚 Documentation]** Move the external tools reference into docs ([c1f31ea](https://github.com/Ronnasayd/aipp/commit/c1f31ea))
- **[📚 Documentation]** Move the environment variables reference into docs ([e4f1bee](https://github.com/Ronnasayd/aipp/commit/e4f1bee))
- **[📚 Documentation]** Point documented test command at the script tests ([16e8de7](https://github.com/Ronnasayd/aipp/commit/16e8de7))
- **[🐛 Bug Fixes]** Back up remaining global configs before linking ([8b8ebe7](https://github.com/Ronnasayd/aipp/commit/8b8ebe7))
- **[🐛 Bug Fixes]** Back up second global settings file before linking ([c8e50f6](https://github.com/Ronnasayd/aipp/commit/c8e50f6))
- **[🐛 Bug Fixes]** Back up global settings before linking ([262c7f8](https://github.com/Ronnasayd/aipp/commit/262c7f8))
- **[✨ Features]** Add link_with_backup helper ([4436e63](https://github.com/Ronnasayd/aipp/commit/4436e63))

## v0.23.1 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Reorder colors and adjust separator styling ([89212f7](https://github.com/Ronnasayd/aipp/commit/89212f7))

## v0.23.0 (2026-10-16)

### **2026-10-16**

- **[✨ Features]** Add oauth token refresh script and improve logging ([0c9a20b](https://github.com/Ronnasayd/aipp/commit/0c9a20b))

## v0.22.0 (2026-10-16)

### **2026-10-16**

- **[✨ Features]** Add 1s refresh interval to command-based statuslines ([886525e](https://github.com/Ronnasayd/aipp/commit/886525e))

## v0.21.1 (2026-10-16)

### **2026-10-16**

- **[🐛 Bug Fixes]** Use resets_at instead of utilization to detect 5h window state ([c20c3cf](https://github.com/Ronnasayd/aipp/commit/c20c3cf))

## v0.21.0 (2026-10-16)

### **2026-10-16**

- **[✨ Features]** Add custom moonlight theme and refactor statusline palette ([af551cd](https://github.com/Ronnasayd/aipp/commit/af551cd))
- **[🚧 Other Changes]** Run rag-rat maintenance asynchronously in background ([ff2a5e6](https://github.com/Ronnasayd/aipp/commit/ff2a5e6))

## v0.20.0 (2026-10-16)

### **2026-10-16**

- **[✨ Features]** Expand dev server detection to cover more languages and frameworks ([da89424](https://github.com/Ronnasayd/aipp/commit/da89424))

## v0.19.1 (2026-10-15)

### **2026-10-15**

- **[🐛 Bug Fixes]** Fix claude.warmup.sh to properly activate 5h session window ([91cdae6](https://github.com/Ronnasayd/aipp/commit/91cdae6))

## v0.19.0 (2026-10-15)

### **2026-10-15**

- **[✨ Features]** Add sd-grilling skill for enhanced planning support ([ec1240f](https://github.com/Ronnasayd/aipp/commit/ec1240f))

## v0.18.0 (2026-10-15)

### **2026-10-15**

- **[✨ Features]** Extract grilling phase into dedicated sd-grilling skill ([0008454](https://github.com/Ronnasayd/aipp/commit/0008454))

## v0.17.4 (2026-10-15)

### **2026-10-15**

- **[🐛 Bug Fixes]** Emit correct hookeventname for userpromptsubmit events ([ba42dbd](https://github.com/Ronnasayd/aipp/commit/ba42dbd))

## v0.17.3 (2026-10-15)

### **2026-10-15**

- **[🐛 Bug Fixes]** Source save_current_account in warmup before checking account tokens ([754ae7b](https://github.com/Ronnasayd/aipp/commit/754ae7b))

## v0.17.2 (2026-10-15)

### **2026-10-15**

- **[🐛 Bug Fixes]** Accept comma/semicolon separators in protect_files_extra_allowed ([891542f](https://github.com/Ronnasayd/aipp/commit/891542f))
- **[🧹 Chores]** Refactor claude.warmup.sh to use oauth endpoint directly instead of cli ([8b851ce](https://github.com/Ronnasayd/aipp/commit/8b851ce))
- **[📚 Documentation]** Add tdd, evidence-first, and vertical-slice requirements to agent rules ([4e5f467](https://github.com/Ronnasayd/aipp/commit/4e5f467))

## v0.17.1 (2026-10-15)

### **2026-10-15**

- **[🐛 Bug Fixes]** Resolve uv venv to repo-local instead of global ai_project_root_dir ([5ffe855](https://github.com/Ronnasayd/aipp/commit/5ffe855))

## v0.17.0 (2026-10-15)

### **2026-10-15**

- **[✨ Features]** Add p10k-style git working tree status indicators ([b9da2fa](https://github.com/Ronnasayd/aipp/commit/b9da2fa))
- **[🧹 Chores]** Add ai-memory session observations and sendfeedback tools to extended permissions ([0feb066](https://github.com/Ronnasayd/aipp/commit/0feb066))
- **[🧹 Chores]** Add ai-memory tools to extended permissions and clean up agents.md ([a40cb26](https://github.com/Ronnasayd/aipp/commit/a40cb26))
- **[🧹 Chores]** Enable interview-specialist agent and disable rag-rat plugin ([2812882](https://github.com/Ronnasayd/aipp/commit/2812882))
- **[🧹 Chores]** Disable bundled skills and add extended permissions ([ec897af](https://github.com/Ronnasayd/aipp/commit/ec897af))

## v0.16.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Throttle userpromptsubmit context emission to every 5th call ([ca296d5](https://github.com/Ronnasayd/aipp/commit/ca296d5))
- **[♻️ Refactoring]** Extract shared md write-target loader, enforce project-scoped deny ([7a4f9e5](https://github.com/Ronnasayd/aipp/commit/7a4f9e5))

## v0.15.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Add available cli binaries discovery to sessionstart context ([0950d4b](https://github.com/Ronnasayd/aipp/commit/0950d4b))
- **[🚧 Other Changes]** Hide inactive tool indicators instead of showing red ([8e102a7](https://github.com/Ronnasayd/aipp/commit/8e102a7))
- **[🧹 Chores]** Remove codebase-memory and serena from mcp.json, format arrays ([788fade](https://github.com/Ronnasayd/aipp/commit/788fade))

## v0.14.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Add comment policy pre-commit hook ([a7ec3fb](https://github.com/Ronnasayd/aipp/commit/a7ec3fb))
- **[🚧 Other Changes]** Replace context bar characters with rounded block glyphs ([d34aad3](https://github.com/Ronnasayd/aipp/commit/d34aad3))
- **[🧹 Chores]** Update model references and add omnirouter model configs ([111ee68](https://github.com/Ronnasayd/aipp/commit/111ee68))
- **[♻️ Refactoring]** Rename 9router models to omnirouter models and update env vars ([1d034df](https://github.com/Ronnasayd/aipp/commit/1d034df))

## v0.13.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Add omniroute service to litellm stack ([d0f450d](https://github.com/Ronnasayd/aipp/commit/d0f450d))

## v0.12.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Add pace indicator showing progress vs time estimate ([f694fe4](https://github.com/Ronnasayd/aipp/commit/f694fe4))

## v0.11.0 (2026-10-14)

### **2026-10-14**

- **[✨ Features]** Add interview-specialist with ping-pong sub-agent protocol ([f03de22](https://github.com/Ronnasayd/aipp/commit/f03de22))
- **[🧹 Chores]** Simplify claude.warmup.sh to use token-based auth ([5d7961b](https://github.com/Ronnasayd/aipp/commit/5d7961b))

### **2026-10-13**

- **[🧹 Chores]** Refine grilling scope and frontier format ([7f11aed](https://github.com/Ronnasayd/aipp/commit/7f11aed))
- **[🧹 Chores]** Revert to ffd4505 state ([dcbb89b](https://github.com/Ronnasayd/aipp/commit/dcbb89b))

## v0.10.0 (2026-10-13)

### **2026-10-13**

- **[✨ Features]** Split sd-planning into sd-interview + sd-planning ([d1dd2f3](https://github.com/Ronnasayd/aipp/commit/d1dd2f3))

## v0.9.0 (2026-10-13)

### **2026-10-13**

- **[✨ Features]** Add interview-specialist for grilling without write tools ([2b9346b](https://github.com/Ronnasayd/aipp/commit/2b9346b))

## v0.8.0 (2026-10-13)

### **2026-10-13**

- **[✨ Features]** Move grilling to dedicated sub-agent, reorder steps ([ed8d7ce](https://github.com/Ronnasayd/aipp/commit/ed8d7ce))

## v0.7.0 (2026-10-13)

### **2026-10-13**

- **[✨ Features]** Add verifier pass for spec audit ([ffd4505](https://github.com/Ronnasayd/aipp/commit/ffd4505))
- **[♻️ Refactoring]** Add command to fetch mcp-manager context ([5c3a0e0](https://github.com/Ronnasayd/aipp/commit/5c3a0e0))
- **[🧹 Chores]** Integrate rag-rat maintenance into lefthook ([94428ce](https://github.com/Ronnasayd/aipp/commit/94428ce))

## v0.6.0 (2026-10-13)

### **2026-10-13**

- **[✨ Features]** Add english-only commit message gate ([a93357d](https://github.com/Ronnasayd/aipp/commit/a93357d))

### **2026-10-10**

- **[🧹 Chores]** Gate harness-toolkit install on node >= 24 ([4c2f9b1](https://github.com/Ronnasayd/aipp/commit/4c2f9b1))
- **[♻️ Refactoring]** Replace hardcoded paths with $ai_project_root_dir environment variable ([f0b3b39](https://github.com/Ronnasayd/aipp/commit/f0b3b39))
- **[📚 Documentation]** Update directory structure in readme to match current repo layout ([b600e29](https://github.com/Ronnasayd/aipp/commit/b600e29))
- **[📚 Documentation]** Update repository clone urls to reflect new name ([70a80e7](https://github.com/Ronnasayd/aipp/commit/70a80e7))
- **[🧹 Chores]** Exclude cache files from tracking ([e512209](https://github.com/Ronnasayd/aipp/commit/e512209))
- **[♻️ Refactoring]** Rename repository from ai-pair-programming to aipp ([9c6532f](https://github.com/Ronnasayd/aipp/commit/9c6532f))

## v0.5.0 (2026-10-10)

### **2026-10-10**

- **[✨ Features]** Add hash-based change detection and improve caching ([e2ece50](https://github.com/Ronnasayd/aipp/commit/e2ece50))
- **[♻️ Refactoring]** Update install script to use local bin and remove sudo usage ([55b46a4](https://github.com/Ronnasayd/aipp/commit/55b46a4))
- **[🧹 Chores]** Consolidate path configuration and use user-local bin directory ([aeaee71](https://github.com/Ronnasayd/aipp/commit/aeaee71))
- **[🧹 Chores]** Consolidate path configuration and use user-local bin directory ([ee6fd25](https://github.com/Ronnasayd/aipp/commit/ee6fd25))
- **[🧹 Chores]** Cross-platform package manager support for pkg/apt/brew/pacman/dnf ([25ec161](https://github.com/Ronnasayd/aipp/commit/25ec161))

### **2026-10-09**

- **[🐛 Bug Fixes]** Add --no-verify to prevent pre-push hook recursion ([285161f](https://github.com/Ronnasayd/aipp/commit/285161f))
- **[🐛 Bug Fixes]** Restore 30s push timeout accidentally reverted to 15s ([4605cef](https://github.com/Ronnasayd/aipp/commit/4605cef))

### **2026-10-08**

- **[🧹 Chores]** Bump fastmcp from 2.14.7 to 3.2.0 in /src ([5632d57](https://github.com/Ronnasayd/aipp/commit/5632d57))

### **2026-10-01**

- **[🧹 Chores]** Bump urllib3 from 2.7.0 to 2.8.0 ([1c5d2bf](https://github.com/Ronnasayd/aipp/commit/1c5d2bf))

## v0.4.0 (2026-10-09)

### **2026-10-09**

- **[✨ Features]** Add alias for initial semantic-version tag creation ([2a5a3fe](https://github.com/Ronnasayd/aipp/commit/2a5a3fe))
- **[🧹 Chores]** Remove timing instrumentation from push-pending-tags ([62d8c4b](https://github.com/Ronnasayd/aipp/commit/62d8c4b))
- **[🧹 Chores]** Add timing instrumentation to push-pending-tags ([36a5b6e](https://github.com/Ronnasayd/aipp/commit/36a5b6e))
- **[♻️ Refactoring]** Testing ([899a8fd](https://github.com/Ronnasayd/aipp/commit/899a8fd))

## v0.3.2 (2026-10-09)

### **2026-10-09**

- **[🐛 Bug Fixes]** Increase timeout for git push from 15s to 30s ([07d16f3](https://github.com/Ronnasayd/aipp/commit/07d16f3))

## v0.3.1 (2026-10-09)

### **2026-10-09**

- **[🐛 Bug Fixes]** Add timeout to network calls to prevent hook hangs ([e3b6133](https://github.com/Ronnasayd/aipp/commit/e3b6133))

## v0.3.0 (2026-10-09)

### **2026-10-09**

- **[✨ Features]** Migrate semantic versioning from file to git tags ([da7a6d4](https://github.com/Ronnasayd/aipp/commit/da7a6d4))

## v0.2.0 (2026-10-09)

### **2026-10-09**

- **[🧹 Chores]** Bump version to 0.2.0 ([0420dc9](https://github.com/Ronnasayd/aipp/commit/0420dc9))
- **[✨ Features]** Add semantic versioning via post-commit hook ([dfdedbc](https://github.com/Ronnasayd/aipp/commit/dfdedbc))
- **[✨ Features]** Refactor commit-msg hooks to support breaking changes and reduce duplication ([3c90baa](https://github.com/Ronnasayd/aipp/commit/3c90baa))
- **[✨ Features]** Add conventional commits validation hook to lefthook ([7001b9b](https://github.com/Ronnasayd/aipp/commit/7001b9b))
- **[✨ Features]** Add 30-day query cache to context7 search hook ([00b40bd](https://github.com/Ronnasayd/aipp/commit/00b40bd))
- **[🐛 Bug Fixes]** Truncate query text to 250 chars in extract_query_text ([763d84d](https://github.com/Ronnasayd/aipp/commit/763d84d))
- **[✨ Features]** Add codebase-memory-mcp health check to statusline tools indicator ([2100d34](https://github.com/Ronnasayd/aipp/commit/2100d34))
- **[🐛 Bug Fixes]** Resolve claude.warmup.sh project root from script location, not env var ([f70a717](https://github.com/Ronnasayd/aipp/commit/f70a717))
- **[♻️ Refactoring]** Expand tools group to include ponytail, rtk, and tlc harness ([03bbf55](https://github.com/Ronnasayd/aipp/commit/03bbf55))
- **[♻️ Refactoring]** Collapse tool status indicators into single group with detailed log ([c784ac1](https://github.com/Ronnasayd/aipp/commit/c784ac1))
- **[🐛 Bug Fixes]** Isolate account warmup in temporary config directories to avoid session conflicts ([9ed3571](https://github.com/Ronnasayd/aipp/commit/9ed3571))
- **[🐛 Bug Fixes]** Guard claude_project_dir commands in hooks to prevent spawn errors ([c27ab2a](https://github.com/Ronnasayd/aipp/commit/c27ab2a))
- **[♻️ Refactoring]** Adjust default disabledmcpservers list and update .mcp.json configuration ([26488d4](https://github.com/Ronnasayd/aipp/commit/26488d4))
- **[♻️ Refactoring]** Centralize config paths to $claude_config_dir ([3af1692](https://github.com/Ronnasayd/aipp/commit/3af1692))
- **[♻️ Refactoring]** Add alias to copy claude_config_dir to /tmp/.claude for testing ([ee770fe](https://github.com/Ronnasayd/aipp/commit/ee770fe))
- **[♻️ Refactoring]** Update all references to ~/.claude to use $claude_config_dir for config paths ([025117f](https://github.com/Ronnasayd/aipp/commit/025117f))
- **[♻️ Refactoring]** Update all references to ~/.claude to use $claude_config_dir for config paths ([79ca3ff](https://github.com/Ronnasayd/aipp/commit/79ca3ff))
- **[♻️ Refactoring]** Update all references to ~/.claude to use $claude_config_dir for config paths ([c888233](https://github.com/Ronnasayd/aipp/commit/c888233))

### **2026-10-08**

- **[♻️ Refactoring]** Update claude warmup script to use choose mode for account selection ([0004f48](https://github.com/Ronnasayd/aipp/commit/0004f48))
- **[♻️ Refactoring]** Update directory patterns for language check ([45384c4](https://github.com/Ronnasayd/aipp/commit/45384c4))
- **[📚 Documentation]** Generalize sd-review-spec skill for stack-agnostic verification ([1bd9f57](https://github.com/Ronnasayd/aipp/commit/1bd9f57))
- **[✨ Features]** Add sd-review-spec skill and update claude code configuration ([01b9f46](https://github.com/Ronnasayd/aipp/commit/01b9f46))
- **[♻️ Refactoring]** Update interactive question guidelines for clarity and conciseness ([ef83a64](https://github.com/Ronnasayd/aipp/commit/ef83a64))
- **[♻️ Refactoring]** Add language selection via question_tool_lang environment variable ([f88d4e2](https://github.com/Ronnasayd/aipp/commit/f88d4e2))
- **[♻️ Refactoring]** Update uninstall script to remove backend symlinks and configs via tlc harness uninstall command. update install script to install harness-toolkit and run tlc harness install in a single command. ([60f9105](https://github.com/Ronnasayd/aipp/commit/60f9105))
- **[♻️ Refactoring]** Adjust file paths in evals to use /home/ronnas instead of hardcoded user path ([96d2ac6](https://github.com/Ronnasayd/aipp/commit/96d2ac6))

### **2026-10-07**

- **[♻️ Refactoring]** Update install script to include harness installation and fix formatting in agents.md ([8bddb26](https://github.com/Ronnasayd/aipp/commit/8bddb26))
- **[♻️ Refactoring]** Remove redundant harness install command ([a19e6ed](https://github.com/Ronnasayd/aipp/commit/a19e6ed))
- **[♻️ Refactoring]** Update default sonnet model to claude-sonnet-5 ([b929386](https://github.com/Ronnasayd/aipp/commit/b929386))
- **[🧹 Chores]** Update settings, install script, and documentation ([0537320](https://github.com/Ronnasayd/aipp/commit/0537320))

### **2026-10-06**

- **[♻️ Refactoring]** Update ai memory volume path to use home directory ([463e4ba](https://github.com/Ronnasayd/aipp/commit/463e4ba))
- **[✨ Features]** Add test_changed hook to run related jest/vitest tests ([9f0920a](https://github.com/Ronnasayd/aipp/commit/9f0920a))
- **[♻️ Refactoring]** Inject context-refs once per session and widen checklist bucket ([787154c](https://github.com/Ronnasayd/aipp/commit/787154c))
- **[♻️ Refactoring]** Gate md checks and inject subagent guidelines once ([6b0398e](https://github.com/Ronnasayd/aipp/commit/6b0398e))
- **[♻️ Refactoring]** Remove jest_coverage_session_end hook from settings.json ([58b3ffa](https://github.com/Ronnasayd/aipp/commit/58b3ffa))
- **[♻️ Refactoring]** Remove mcps/vscode.mcp.json and related symlink creation ([ed177f0](https://github.com/Ronnasayd/aipp/commit/ed177f0))
- **[♻️ Refactoring]** Remove skill-rules ([00b3604](https://github.com/Ronnasayd/aipp/commit/00b3604))
- **[♻️ Refactoring]** Move legacy code to new module legacy ([f3f3f7e](https://github.com/Ronnasayd/aipp/commit/f3f3f7e))
- **[♻️ Refactoring]** Remove caveman mode hooks from settings.json ([af0c7ff](https://github.com/Ronnasayd/aipp/commit/af0c7ff))
- **[♻️ Refactoring]** Settings.json: remove deprecated hooks and commands ([6e0fab7](https://github.com/Ronnasayd/aipp/commit/6e0fab7))

### **2026-10-05**

- **[♻️ Refactoring]** Move unused hooks to legacy and add ignore globs to lint_changed ([8f9ea1e](https://github.com/Ronnasayd/aipp/commit/8f9ea1e))

### **2026-10-03**

- **[♻️ Refactoring]** Update krita mcp server configuration and disable it by default ([bd73483](https://github.com/Ronnasayd/aipp/commit/bd73483))
- **[♻️ Refactoring]** Update mcp server configuration for krita integration ([f236cc7](https://github.com/Ronnasayd/aipp/commit/f236cc7))
- **[♻️ Refactoring]** Add rules.md to harness-toolkit for operator rules and triggers ([4afd114](https://github.com/Ronnasayd/aipp/commit/4afd114))
- **[🧹 Chores]** Add lint-staged command to lefthook pre-commit ([f30bb54](https://github.com/Ronnasayd/aipp/commit/f30bb54))
- **[✨ Features]** Lint only staged files on pre-commit via lint_changed --staged ([aaa7c41](https://github.com/Ronnasayd/aipp/commit/aaa7c41))
- **[♻️ Refactoring]** Add laya mcp server to disabled list and config ([b7c20d8](https://github.com/Ronnasayd/aipp/commit/b7c20d8))
- **[♻️ Refactoring]** Add vrep mcp server configuration and disable it by default ([1eb9846](https://github.com/Ronnasayd/aipp/commit/1eb9846))

### **2026-10-02**

- **[♻️ Refactoring]** Update config.json and agents.md with new settings and rules ([8e55b0c](https://github.com/Ronnasayd/aipp/commit/8e55b0c))
- **[🐛 Bug Fixes]** Run harness lint command under toolkit uv project on install ([c6ca79e](https://github.com/Ronnasayd/aipp/commit/c6ca79e))
- **[✨ Features]** Prefix external hook log lines with timestamp, session and hook name ([198c905](https://github.com/Ronnasayd/aipp/commit/198c905))
- **[✨ Features]** Log external hook output via tlc-exec-log wrapper ([c4a62e6](https://github.com/Ronnasayd/aipp/commit/c4a62e6))

### **2026-10-01**

- **[♻️ Refactoring]** Remove unused project root directory from lint command ([1409128](https://github.com/Ronnasayd/aipp/commit/1409128))
- **[♻️ Refactoring]** Update lint command to include project directory for better context ([519335f](https://github.com/Ronnasayd/aipp/commit/519335f))
- **[♻️ Refactoring]** Remove harness config symlink and add install script logic ([87593e4](https://github.com/Ronnasayd/aipp/commit/87593e4))
- **[♻️ Refactoring]** Update harness config to use symlink and relative paths ([9de8730](https://github.com/Ronnasayd/aipp/commit/9de8730))
- **[♻️ Refactoring]** Add node_version to settings.json and update install.sh to install harness-toolkit ([a444d6e](https://github.com/Ronnasayd/aipp/commit/a444d6e))
- **[♻️ Refactoring]** Add harness-toolkit installation to install.sh ([35f97e6](https://github.com/Ronnasayd/aipp/commit/35f97e6))
- **[♻️ Refactoring]** Update harness config to use symlink and relative paths ([e640df1](https://github.com/Ronnasayd/aipp/commit/e640df1))
- **[♻️ Refactoring]** Update tlc harness ([88d8bcf](https://github.com/Ronnasayd/aipp/commit/88d8bcf))
- **[🧹 Chores]** Bump pyjwt from 2.13.0 to 2.15.0 in /src ([55f0eb5](https://github.com/Ronnasayd/aipp/commit/55f0eb5))
- **[♻️ Refactoring]** Replace stop lint and comment hooks with harness-toolkit ([7e8ef70](https://github.com/Ronnasayd/aipp/commit/7e8ef70))
- **[✨ Features]** Add consolidate-markdown skill to merge and organize markdown files ([e339814](https://github.com/Ronnasayd/aipp/commit/e339814))
- **[♻️ Refactoring]** Remove manage-ignore-files symlink and add alias for it ([56bb516](https://github.com/Ronnasayd/aipp/commit/56bb516))
- **[♻️ Refactoring]** Update agent instructions for clarity and conciseness ([75ddb5c](https://github.com/Ronnasayd/aipp/commit/75ddb5c))
- **[♻️ Refactoring]** Update agent instructions for clarity and conciseness ([207a5ca](https://github.com/Ronnasayd/aipp/commit/207a5ca))
- **[♻️ Refactoring]** Add uv project to aipp_settings.py commands ([662f991](https://github.com/Ronnasayd/aipp/commit/662f991))

### **2026-09-30**

- **[♻️ Refactoring]** Remove commit ask ([960cc54](https://github.com/Ronnasayd/aipp/commit/960cc54))
- **[✨ Features]** Rewrite skill with phased workflow and validator ([f9c8bd2](https://github.com/Ronnasayd/aipp/commit/f9c8bd2))
- **[♻️ Refactoring]** Update models ([e6dfdd2](https://github.com/Ronnasayd/aipp/commit/e6dfdd2))
- **[📚 Documentation]** Mention codebase-memory-mcp alongside rag-rat across docs ([ec504e9](https://github.com/Ronnasayd/aipp/commit/ec504e9))
- **[✨ Features]** Add codebase-memory-mcp as language fallback alongside rag-rat ([c6ff481](https://github.com/Ronnasayd/aipp/commit/c6ff481))
- **[♻️ Refactoring]** Rename iai binary and alias file to aipp ([44c822d](https://github.com/Ronnasayd/aipp/commit/44c822d))

### **2026-09-29**

- **[♻️ Refactoring]** Remove docs.instructions.md ([3636523](https://github.com/Ronnasayd/aipp/commit/3636523))
- **[♻️ Refactoring]** Adjust applyto ([79536e6](https://github.com/Ronnasayd/aipp/commit/79536e6))
- **[♻️ Refactoring]** Increase repeat every ([afe7bd4](https://github.com/Ronnasayd/aipp/commit/afe7bd4))
- **[✨ Features]** Support exclude globs in per-file instruction rules ([c2281f5](https://github.com/Ronnasayd/aipp/commit/c2281f5))
- **[♻️ Refactoring]** Adjust at texts ([656bee6](https://github.com/Ronnasayd/aipp/commit/656bee6))
- **[🚧 Other Changes]** Batch settings i/o in sync_catalog to avoid per-item disk writes ([328d02f](https://github.com/Ronnasayd/aipp/commit/328d02f))

### **2026-09-28**

- **[✨ Features]** Add deterministic validation script for srs output ([69d2b86](https://github.com/Ronnasayd/aipp/commit/69d2b86))
- **[♻️ Refactoring]** Update manifest ([78a6e0c](https://github.com/Ronnasayd/aipp/commit/78a6e0c))
- **[♻️ Refactoring]** Compress srs-generator and add skill-description-generator ([0b716b0](https://github.com/Ronnasayd/aipp/commit/0b716b0))
- **[♻️ Refactoring]** Generalize protect_files allowlist paths via env var ([4005f4f](https://github.com/Ronnasayd/aipp/commit/4005f4f))
- **[🧹 Chores]** Add model directive to sd-execute skill ([b7ed248](https://github.com/Ronnasayd/aipp/commit/b7ed248))
- **[🧹 Chores]** Update model directives and add session transcript link to statusline ([4d95bc0](https://github.com/Ronnasayd/aipp/commit/4d95bc0))
- **[♻️ Refactoring]** Put actives first in order ([4e3b9a4](https://github.com/Ronnasayd/aipp/commit/4e3b9a4))

### **2026-09-27**

- **[♻️ Refactoring]** Adjust order ([b8540ec](https://github.com/Ronnasayd/aipp/commit/b8540ec))
- **[📚 Documentation]** Add property-based testing rules with fast-check ([f79e4ab](https://github.com/Ronnasayd/aipp/commit/f79e4ab))
- **[🧹 Chores]** Remove cache metrics from status line output ([09df973](https://github.com/Ronnasayd/aipp/commit/09df973))
- **[🐛 Bug Fixes]** Address coderabbit review on new-item sync ([b28aa0f](https://github.com/Ronnasayd/aipp/commit/b28aa0f))
- **[✨ Features]** Auto-propagate new items to catalog and projects ([3cd9534](https://github.com/Ronnasayd/aipp/commit/3cd9534))
- **[📚 Documentation]** Add adr ([18bb0cf](https://github.com/Ronnasayd/aipp/commit/18bb0cf))
- **[♻️ Refactoring]** Put alphabetical order ([60307f4](https://github.com/Ronnasayd/aipp/commit/60307f4))
- **[🐛 Bug Fixes]** Replace live .ignore catalog with static json ([dd5c365](https://github.com/Ronnasayd/aipp/commit/dd5c365))
- **[🐛 Bug Fixes]** Read instructions state from json in installers ([9f498ca](https://github.com/Ronnasayd/aipp/commit/9f498ca))
- **[♻️ Refactoring]** Read enablement status from aipp-settings.json in ats/atr/ata ([eb419b4](https://github.com/Ronnasayd/aipp/commit/eb419b4))
- **[♻️ Refactoring]** Wire aipp_settings migration into install.sh, drop legacy concat block ([9531676](https://github.com/Ronnasayd/aipp/commit/9531676))
- **[♻️ Refactoring]** Rewrite ignores.sh to read enablement from aipp-settings.json ([c56c133](https://github.com/Ronnasayd/aipp/commit/c56c133))
- **[🧹 Chores]** Pin subprocess.run check=false in aipp_settings cli test helper ([792ba81](https://github.com/Ronnasayd/aipp/commit/792ba81))
- **[🧹 Chores]** Fix lint findings in manage-ignore-files.py ([8c947cc](https://github.com/Ronnasayd/aipp/commit/8c947cc))
- **[📚 Documentation]** Add pylint-required param/return docstrings to aipp_settings ([d449234](https://github.com/Ronnasayd/aipp/commit/d449234))
- **[♻️ Refactoring]** Use aipp_settings for new-skill registration in update-external-tools.sh ([fafcfd2](https://github.com/Ronnasayd/aipp/commit/fafcfd2))
- **[♻️ Refactoring]** Rewrite manage-ignore-files.py to use aipp_settings json backend ([a829f35](https://github.com/Ronnasayd/aipp/commit/a829f35))
- **[✨ Features]** Add cli subcommands to aipp_settings for bash consumers ([04fedb0](https://github.com/Ronnasayd/aipp/commit/04fedb0))
- **[✨ Features]** Add register_if_absent and set_item to aipp_settings ([4b7c520](https://github.com/Ronnasayd/aipp/commit/4b7c520))
- **[✨ Features]** Add source-default seeding and ensure_migrated to aipp_settings ([9d1de81](https://github.com/Ronnasayd/aipp/commit/9d1de81))
- **[✨ Features]** Add legacy .ignore file migration to aipp_settings ([befa1dd](https://github.com/Ronnasayd/aipp/commit/befa1dd))
- **[✨ Features]** Add aipp_settings module for load/save/get_project ([e64c28f](https://github.com/Ronnasayd/aipp/commit/e64c28f))
- **[📚 Documentation]** Document undocumented hook env vars and scripts ([c9abbe6](https://github.com/Ronnasayd/aipp/commit/c9abbe6))
- **[♻️ Refactoring]** Wire ui test gate and implicit-requirements check into planning/execution flow ([86c6fd8](https://github.com/Ronnasayd/aipp/commit/86c6fd8))
- **[📚 Documentation]** Require deep codebase traversal and transversal search before planning ([ab35d22](https://github.com/Ronnasayd/aipp/commit/ab35d22))

### **2026-09-26**

- **[♻️ Refactoring]** Register skill-inspector and symlink manifest.json in installer ([ff7024e](https://github.com/Ronnasayd/aipp/commit/ff7024e))
- **[♻️ Refactoring]** Namespace external skill symlinks and skillignore entries by group ([1ccb405](https://github.com/Ronnasayd/aipp/commit/1ccb405))
- **[♻️ Refactoring]** Add complete path ([be3f9c5](https://github.com/Ronnasayd/aipp/commit/be3f9c5))
- **[♻️ Refactoring]** Just move to quarantine ([fa39687](https://github.com/Ronnasayd/aipp/commit/fa39687))
- **[♻️ Refactoring]** Update skillspector to add quarentine ([aec4d67](https://github.com/Ronnasayd/aipp/commit/aec4d67))
- **[♻️ Refactoring]** Update skills ([0cb2534](https://github.com/Ronnasayd/aipp/commit/0cb2534))
- **[✨ Features]** Add session id to shared logger output ([3ff197e](https://github.com/Ronnasayd/aipp/commit/3ff197e))
- **[♻️ Refactoring]** Eslint must run with --quiet ([b410e79](https://github.com/Ronnasayd/aipp/commit/b410e79))
- **[✨ Features]** Self-collect metrics with zero-config paths ([c8a71f3](https://github.com/Ronnasayd/aipp/commit/c8a71f3))
- **[♻️ Refactoring]** Resolve lint findings and dedupe embedding-daemon client code ([b7d37ab](https://github.com/Ronnasayd/aipp/commit/b7d37ab))
- **[🐛 Bug Fixes]** Prevent embedding daemon race with singleton file lock ([889a083](https://github.com/Ronnasayd/aipp/commit/889a083))
- **[✨ Features]** Enforce mandatory subagent response format via subagentstop gate ([ed30183](https://github.com/Ronnasayd/aipp/commit/ed30183))
- **[♻️ Refactoring]** Split into markdowns ([1ee5ab6](https://github.com/Ronnasayd/aipp/commit/1ee5ab6))

### **2026-09-25**

- **[🐛 Bug Fixes]** Resolve ruff and pylint findings across 18 hook scripts ([5922b1e](https://github.com/Ronnasayd/aipp/commit/5922b1e))
- **[🐛 Bug Fixes]** Resolve ruff and pylint findings in utils.py ([58b24c6](https://github.com/Ronnasayd/aipp/commit/58b24c6))
- **[🐛 Bug Fixes]** Prevent rag-rat helper hooks from blocking on nonzero exit ([9a3274c](https://github.com/Ronnasayd/aipp/commit/9a3274c))
- **[✨ Features]** Block write/edit content containing secrets ([4130a9c](https://github.com/Ronnasayd/aipp/commit/4130a9c))

### **2026-09-24**

- **[♻️ Refactoring]** Split log hooks in colorized and default ([59ffba3](https://github.com/Ronnasayd/aipp/commit/59ffba3))
- **[♻️ Refactoring]** Activate and stop caveman by command ([c7426b8](https://github.com/Ronnasayd/aipp/commit/c7426b8))
- **[♻️ Refactoring]** Adjust timeout order ([bf0e11b](https://github.com/Ronnasayd/aipp/commit/bf0e11b))
- **[♻️ Refactoring]** Add pyproject.toml in python lint ([c12b900](https://github.com/Ronnasayd/aipp/commit/c12b900))
- **[🐛 Bug Fixes]** Resolve venv-local mypy/pylint binaries before falling back to global ([5a0d37f](https://github.com/Ronnasayd/aipp/commit/5a0d37f))

### **2026-09-23**

- **[♻️ Refactoring]** Update agents.md ([6aede42](https://github.com/Ronnasayd/aipp/commit/6aede42))
- **[♻️ Refactoring]** Extract secret scanning from protect_files.py into dedicated scripts ([39a8858](https://github.com/Ronnasayd/aipp/commit/39a8858))
- **[♻️ Refactoring]** Adjust order of hooks ([be6b4d0](https://github.com/Ronnasayd/aipp/commit/be6b4d0))
- **[✨ Features]** Throttle context-refs pointer re-injection with repeat_every ([9f47b04](https://github.com/Ronnasayd/aipp/commit/9f47b04))
- **[♻️ Refactoring]** Solve lint errors ([3f397ed](https://github.com/Ronnasayd/aipp/commit/3f397ed))

### **2026-09-22**

- **[♻️ Refactoring]** Adjust lint errors ([75fc6af](https://github.com/Ronnasayd/aipp/commit/75fc6af))
- **[♻️ Refactoring]** Dedupe rag-rat mcp call in impact_surface_hint ([b23ec11](https://github.com/Ronnasayd/aipp/commit/b23ec11))
- **[🐛 Bug Fixes]** Remove stop_hook_active early-exit sabotaging lint retry ([bc29bbe](https://github.com/Ronnasayd/aipp/commit/bc29bbe))
- **[✨ Features]** Cap stop_lint_gate retries with a maxloops counter ([c549abd](https://github.com/Ronnasayd/aipp/commit/c549abd))
- **[♻️ Refactoring]** Add logs ([349c668](https://github.com/Ronnasayd/aipp/commit/349c668))
- **[♻️ Refactoring]** Add to subagent stop ([2f7bfa9](https://github.com/Ronnasayd/aipp/commit/2f7bfa9))
- **[🐛 Bug Fixes]** Dispatch php lint in stop-time gate ([d63260d](https://github.com/Ronnasayd/aipp/commit/d63260d))
- **[✨ Features]** Wire turn-start sha pin and stop-lint gate hooks ([a958113](https://github.com/Ronnasayd/aipp/commit/a958113))
- **[✨ Features]** Add stop-time lint gate hook ([655867f](https://github.com/Ronnasayd/aipp/commit/655867f))
- **[✨ Features]** Add turn-start sha pin hook ([69ea77d](https://github.com/Ronnasayd/aipp/commit/69ea77d))

### **2026-09-21**

- **[🐛 Bug Fixes]** Resolve lint errors in golang_lint.py ([50968c4](https://github.com/Ronnasayd/aipp/commit/50968c4))
- **[✨ Features]** Add docker containers section to start_context ([b86c0a9](https://github.com/Ronnasayd/aipp/commit/b86c0a9))
- **[🐛 Bug Fixes]** Use project_dir helper consistently in start_context ([5c15484](https://github.com/Ronnasayd/aipp/commit/5c15484))
- **[🐛 Bug Fixes]** Resolve project root from claude_project_dir, not payload cwd ([9c9098b](https://github.com/Ronnasayd/aipp/commit/9c9098b))
- **[✨ Features]** Allow md_language override in md_language_check ([d818e05](https://github.com/Ronnasayd/aipp/commit/d818e05))
- **[✨ Features]** Add question_tool_lang override and fix lint in question_tool_enforcer ([d3b0b22](https://github.com/Ronnasayd/aipp/commit/d3b0b22))
- **[✨ Features]** Add question_tool_lang env override for question_tool_enforcer ([0875197](https://github.com/Ronnasayd/aipp/commit/0875197))
- **[📚 Documentation]** Sync skills table and allow gh command in smart_approve ([f0526bf](https://github.com/Ronnasayd/aipp/commit/f0526bf))
- **[🧹 Chores]** Standardize hook timeouts to 10s and fix daemon runtime dir ([b419cbc](https://github.com/Ronnasayd/aipp/commit/b419cbc))
- **[🚧 Other Changes]** Fix ruff/pylint findings in embedding_daemon ([27e4b23](https://github.com/Ronnasayd/aipp/commit/27e4b23))

### **2026-09-19**

- **[🚧 Other Changes]** Fix ruff/pylint findings in start_context ([5874552](https://github.com/Ronnasayd/aipp/commit/5874552))
- **[♻️ Refactoring]** Drop agents.md injection, load via claude.md import instead ([ef9a503](https://github.com/Ronnasayd/aipp/commit/ef9a503))

### **2026-09-18**

- **[♻️ Refactoring]** Rename mcps ([c69a251](https://github.com/Ronnasayd/aipp/commit/c69a251))
- **[✨ Features]** Merge local lefthook.yml instead of overwriting via symlink ([8b87dd1](https://github.com/Ronnasayd/aipp/commit/8b87dd1))
- **[✨ Features]** Merge local configs instead of overwriting via symlink ([410d664](https://github.com/Ronnasayd/aipp/commit/410d664))
- **[♻️ Refactoring]** Swap php lint from pint to phpstan ([4e95bc0](https://github.com/Ronnasayd/aipp/commit/4e95bc0))
- **[✨ Features]** Add php lint hook using laravel pint ([2cc2bb3](https://github.com/Ronnasayd/aipp/commit/2cc2bb3))
- **[📚 Documentation]** Expand comment-policy hint with marker format and line limit ([85bb4ed](https://github.com/Ronnasayd/aipp/commit/85bb4ed))
- **[✨ Features]** Add comment-policy posttooluse hint hook ([11386fe](https://github.com/Ronnasayd/aipp/commit/11386fe))
- **[♻️ Refactoring]** Solving lint errors ([56a43ca](https://github.com/Ronnasayd/aipp/commit/56a43ca))
- **[🧹 Chores]** Add pylint check to python lint hook ([134eba6](https://github.com/Ronnasayd/aipp/commit/134eba6))
- **[🧹 Chores]** Dedupe hook log stream and cleanup dead aliases ([d9b6eaf](https://github.com/Ronnasayd/aipp/commit/d9b6eaf))
- **[♻️ Refactoring]** Trim jscpd duplicate output to file:line pairs ([110c85c](https://github.com/Ronnasayd/aipp/commit/110c85c))
- **[🐛 Bug Fixes]** Scope jscpd scan to $claude_project_dir and filter to edited file ([c20f2d8](https://github.com/Ronnasayd/aipp/commit/c20f2d8))
- **[🐛 Bug Fixes]** Exclude doc extensions from config file glob match ([d4c060d](https://github.com/Ronnasayd/aipp/commit/d4c060d))
- **[♻️ Refactoring]** Update agents.md ([399edeb](https://github.com/Ronnasayd/aipp/commit/399edeb))
- **[♻️ Refactoring]** Update instructions descriptions ([59e60a3](https://github.com/Ronnasayd/aipp/commit/59e60a3))
- **[♻️ Refactoring]** Detect dockerfile and docker-compose recursively in start_context ([e7bacfb](https://github.com/Ronnasayd/aipp/commit/e7bacfb))

### **2026-09-17**

- **[♻️ Refactoring]** Make config-file scan respect .gitignore ([f8dd556](https://github.com/Ronnasayd/aipp/commit/f8dd556))
- **[♻️ Refactoring]** Uodate quality-gate skill ([36922bf](https://github.com/Ronnasayd/aipp/commit/36922bf))
- **[♻️ Refactoring]** Update manifest.json ([cf2c3b1](https://github.com/Ronnasayd/aipp/commit/cf2c3b1))
- **[♻️ Refactoring]** Add scripts to quality-gate skill ([bb66bd4](https://github.com/Ronnasayd/aipp/commit/bb66bd4))
- **[♻️ Refactoring]** Add quality-gate skill ([c302b2a](https://github.com/Ronnasayd/aipp/commit/c302b2a))
- **[📚 Documentation]** Add usage skill ([60e1209](https://github.com/Ronnasayd/aipp/commit/60e1209))
- **[🚧 Other Changes]** Isolate duplicationpercent regression direction ([e532d2a](https://github.com/Ronnasayd/aipp/commit/e532d2a))
- **[✨ Features]** Wire cli flags and non-interactive execution ([11571f6](https://github.com/Ronnasayd/aipp/commit/11571f6))
- **[✨ Features]** Generate markdown report ([fbaaf25](https://github.com/Ronnasayd/aipp/commit/fbaaf25))
- **[✨ Features]** Add ratchet comparison against baseline ([08abf19](https://github.com/Ronnasayd/aipp/commit/08abf19))
- **[✨ Features]** Bootstrap and guard baseline file ([72d165e](https://github.com/Ronnasayd/aipp/commit/72d165e))
- **[✨ Features]** Collect lint/duplication/coverage/file-size metrics ([424863d](https://github.com/Ronnasayd/aipp/commit/424863d))
- **[♻️ Refactoring]** Add rag-rat installer ([6706cb6](https://github.com/Ronnasayd/aipp/commit/6706cb6))
- **[♻️ Refactoring]** Remove caveman init. already in plugins ([19e30ad](https://github.com/Ronnasayd/aipp/commit/19e30ad))
- **[♻️ Refactoring]** Add plugins ([4ba1b20](https://github.com/Ronnasayd/aipp/commit/4ba1b20))
- **[♻️ Refactoring]** Add macos support ([9a35f63](https://github.com/Ronnasayd/aipp/commit/9a35f63))
- **[♻️ Refactoring]** Update to source ([edb8864](https://github.com/Ronnasayd/aipp/commit/edb8864))
- **[♻️ Refactoring]** Update rag-rat install ([b1221c9](https://github.com/Ronnasayd/aipp/commit/b1221c9))
- **[♻️ Refactoring]** Add home env ([3b1e375](https://github.com/Ronnasayd/aipp/commit/3b1e375))

### **2026-09-16**

- **[♻️ Refactoring]** Split rag-rat code-ref hooks into semantic and structural clone detection ([c0fe1e6](https://github.com/Ronnasayd/aipp/commit/c0fe1e6))
- **[✨ Features]** Minify json and markdown in additionalcontext output ([2f56268](https://github.com/Ronnasayd/aipp/commit/2f56268))
- **[✨ Features]** Add deterministic validation scripts for docs output ([ed0a7d3](https://github.com/Ronnasayd/aipp/commit/ed0a7d3))
- **[✨ Features]** Add notion mcp ([73404e9](https://github.com/Ronnasayd/aipp/commit/73404e9))
- **[♻️ Refactoring]** Remove context-refs hook feature and related files ([5ee6b8d](https://github.com/Ronnasayd/aipp/commit/5ee6b8d))
- **[✨ Features]** Add pre-push jest and typecheck hooks ([a8044cf](https://github.com/Ronnasayd/aipp/commit/a8044cf))
- **[📚 Documentation]** Add uninstall.sh reference to readme ([a67c2fb](https://github.com/Ronnasayd/aipp/commit/a67c2fb))
- **[♻️ Refactoring]** Update install script to use generic installer and improve output messages ([f6da985](https://github.com/Ronnasayd/aipp/commit/f6da985))
- **[♻️ Refactoring]** Update install script to use generic installer and improve output messages ([f9325a8](https://github.com/Ronnasayd/aipp/commit/f9325a8))
- **[♻️ Refactoring]** Add lefthook installation and improve install script readability ([101d3e4](https://github.com/Ronnasayd/aipp/commit/101d3e4))
- **[♻️ Refactoring]** Update uv installation to use generic install script ([4990b82](https://github.com/Ronnasayd/aipp/commit/4990b82))
- **[📚 Documentation]** Update changelog for new release ([9808e84](https://github.com/Ronnasayd/aipp/commit/9808e84))
- **[♻️ Refactoring]** Update descriptions in skill.md and instructions files ([78baf5c](https://github.com/Ronnasayd/aipp/commit/78baf5c))
- **[♻️ Refactoring]** Rewrite skill descriptions to english-only triggers and drop negative clauses ([946dec3](https://github.com/Ronnasayd/aipp/commit/946dec3))
- **[♻️ Refactoring]** Update skill-description-generator to enforce english-only trigger phrases ([be99208](https://github.com/Ronnasayd/aipp/commit/be99208))
- **[♻️ Refactoring]** Trim descriptions and drop non-english trigger phrases ([93e6b80](https://github.com/Ronnasayd/aipp/commit/93e6b80))
- **[♻️ Refactoring]** Drop negative-trigger clauses from generated descriptions ([175a831](https://github.com/Ronnasayd/aipp/commit/175a831))
- **[✨ Features]** Resolve /command prompts to body text for embedding ([bda45d5](https://github.com/Ronnasayd/aipp/commit/bda45d5))
- **[♻️ Refactoring]** Separate dedup and referenced-skill skip logging ([5c9858f](https://github.com/Ronnasayd/aipp/commit/5c9858f))

### **2026-09-15**

- **[♻️ Refactoring]** Update skills ([6d9bbb2](https://github.com/Ronnasayd/aipp/commit/6d9bbb2))
- **[♻️ Refactoring]** Use sudo for package installations in install.sh ([982cbf3](https://github.com/Ronnasayd/aipp/commit/982cbf3))
- **[♻️ Refactoring]** Move to installs directory and update source path ([939e030](https://github.com/Ronnasayd/aipp/commit/939e030))
- **[♻️ Refactoring]** Update install and project dir references to project_dir ([73cfef3](https://github.com/Ronnasayd/aipp/commit/73cfef3))
- **[♻️ Refactoring]** Add the-judge skill to manifest and index files ([8ef4d9a](https://github.com/Ronnasayd/aipp/commit/8ef4d9a))
- **[♻️ Refactoring]** Update pr review skill and related tools ([4de4ffc](https://github.com/Ronnasayd/aipp/commit/4de4ffc))
- **[✨ Features]** Add the judge skill ([01d43ae](https://github.com/Ronnasayd/aipp/commit/01d43ae))

### **2026-09-14**

- **[🧹 Chores]** Sync tech-leads-club skills, add spec-driven-eval ([781ce4a](https://github.com/Ronnasayd/aipp/commit/781ce4a))
- **[🐛 Bug Fixes]** Remove existing skill symlink/dir before recreating in claude.install.sh ([c0da771](https://github.com/Ronnasayd/aipp/commit/c0da771))
- **[✨ Features]** Scan mcp tool_input string leaves for protected paths ([677c314](https://github.com/Ronnasayd/aipp/commit/677c314))
- **[✨ Features]** Support pragma allowlist for secret scan false positives ([db635cf](https://github.com/Ronnasayd/aipp/commit/db635cf))
- **[♻️ Refactoring]** Add tlc skills to .skillsignore and update skill_loader_mcp.py ([0a92d86](https://github.com/Ronnasayd/aipp/commit/0a92d86))
- **[✨ Features]** Add download_remote_skill tool for bulk skill fetch add tool to download a skill (skill.md + all auxiliary files) from the remote repo in one call and save to <dest_dir>/<name>/, defaulting to .claude/skills. avoids per-file mcp round trips for skills with many auxiliary files. ([77660d4](https://github.com/Ronnasayd/aipp/commit/77660d4))
- **[♻️ Refactoring]** Update skills and commands for new features ([eeaaa05](https://github.com/Ronnasayd/aipp/commit/eeaaa05))
- **[✨ Features]** Add new tlc skills for confluence, harness eval, spec-driven eval, discover, implement, plan, and spec-lean ([03d3246](https://github.com/Ronnasayd/aipp/commit/03d3246))
- **[✨ Features]** Add claude_install_skip_claude_md env var to skip claude.md write ([3fefbd9](https://github.com/Ronnasayd/aipp/commit/3fefbd9))
- **[✨ Features]** Add claude_install_skip_auto_context env var and document env vars in readme ([6956f9d](https://github.com/Ronnasayd/aipp/commit/6956f9d))
- **[♻️ Refactoring]** Update lefthook script paths to use absolute paths ([8ee5214](https://github.com/Ronnasayd/aipp/commit/8ee5214))
- **[✨ Features]** Add commit-msg hook to reject emoji in commit messages ([b6d72a1](https://github.com/Ronnasayd/aipp/commit/b6d72a1))
- **[♻️ Refactoring]** Remove leftover git-hooks references after lefthook migration ([8ee2884](https://github.com/Ronnasayd/aipp/commit/8ee2884))
- **[♻️ Refactoring]** Migrate git-hooks scripts to lefthook ([27b77b8](https://github.com/Ronnasayd/aipp/commit/27b77b8))
- **[✨ Features]** Inject agents.md content into sessionstart context ([d57af33](https://github.com/Ronnasayd/aipp/commit/d57af33))
- **[📚 Documentation]** Trim agents.md/agent.instructions.md conventions, add skills table ([1c63ed2](https://github.com/Ronnasayd/aipp/commit/1c63ed2))
- **[✨ Features]** Add skill-judge fetch and refactor tool downloader into functions ([14ca634](https://github.com/Ronnasayd/aipp/commit/14ca634))
- **[♻️ Refactoring]** Update .mcp.json to include rag-rat and serena configurations ([40a2957](https://github.com/Ronnasayd/aipp/commit/40a2957))

### **2026-09-12**

- **[📚 Documentation]** Add readme documenting active hook wiring ([0b0a51a](https://github.com/Ronnasayd/aipp/commit/0b0a51a))
- **[♻️ Refactoring]** Move to correct location in spec-to-requirements-table skill ([34c5c41](https://github.com/Ronnasayd/aipp/commit/34c5c41))
- **[✨ Features]** Add deterministic requirements table validator ([1d870ca](https://github.com/Ronnasayd/aipp/commit/1d870ca))
- **[✨ Features]** Add deterministic pr description validator ([e36516c](https://github.com/Ronnasayd/aipp/commit/e36516c))
- **[♻️ Refactoring]** Update external skills ([2993090](https://github.com/Ronnasayd/aipp/commit/2993090))
- **[♻️ Refactoring]** Update .skillsignore to reorder and add new entries ([86e9ff8](https://github.com/Ronnasayd/aipp/commit/86e9ff8))
- **[📚 Documentation]** Add mermaid execution flow diagram ([32682c0](https://github.com/Ronnasayd/aipp/commit/32682c0))
- **[📚 Documentation]** Add mermaid flow diagram and refine web-search step ([7fb93b3](https://github.com/Ronnasayd/aipp/commit/7fb93b3))

### **2026-09-11**

- **[✨ Features]** Add mcp server allowlist to protect_files hook ([4d052e9](https://github.com/Ronnasayd/aipp/commit/4d052e9))

### **2026-09-10**

- **[♻️ Refactoring]** Replace cfie alias with function to open git exclude file in editor ([aaf1bef](https://github.com/Ronnasayd/aipp/commit/aaf1bef))
- **[✨ Features]** Also emit **/-prefixed git exclude patterns for nested dirs ([8f2637b](https://github.com/Ronnasayd/aipp/commit/8f2637b))
- **[♻️ Refactoring]** Centralize git exclude logic in shared helper ([8f03d95](https://github.com/Ronnasayd/aipp/commit/8f03d95))
- **[♻️ Refactoring]** Tighten context7 search result filtering ([b2aecf9](https://github.com/Ronnasayd/aipp/commit/b2aecf9))
- **[♻️ Refactoring]** Add session duration display to status line ([501757c](https://github.com/Ronnasayd/aipp/commit/501757c))

### **2026-09-09**

- **[♻️ Refactoring]** Add ssh-mcp to disabled mcp servers list ([436869e](https://github.com/Ronnasayd/aipp/commit/436869e))

### **2026-09-08**

- **[♻️ Refactoring]** Update permanent memory guidelines in start.md ([a10a9c4](https://github.com/Ronnasayd/aipp/commit/a10a9c4))

### **2026-09-06**

- **[🧹 Chores]** Mount .serena rw and pass through context7/npm cache config ([a1b4832](https://github.com/Ronnasayd/aipp/commit/a1b4832))
- **[♻️ Refactoring]** Rename dontask to bypasspermissions and centralize ask permissions ([6aaf25c](https://github.com/Ronnasayd/aipp/commit/6aaf25c))
- **[♻️ Refactoring]** Update agent creation and task handling guidelines ([797e8c7](https://github.com/Ronnasayd/aipp/commit/797e8c7))
- **[♻️ Refactoring]** Update agent creation and task handling guidelines ([a31e37c](https://github.com/Ronnasayd/aipp/commit/a31e37c))
- **[♻️ Refactoring]** Update project_ports output formatting and command display ([bef4efc](https://github.com/Ronnasayd/aipp/commit/bef4efc))
- **[✨ Features]** Report project apps listening on ports in start context ([c3d78a3](https://github.com/Ronnasayd/aipp/commit/c3d78a3))

### **2026-09-05**

- **[♻️ Refactoring]** Add omniroute to disabled mcp servers list ([65f88b8](https://github.com/Ronnasayd/aipp/commit/65f88b8))
- **[♻️ Refactoring]** Remove ignored entries from disabled mcp servers list ([7772d01](https://github.com/Ronnasayd/aipp/commit/7772d01))
- **[♻️ Refactoring]** Apply disabled mcp servers to all projects ([acce19d](https://github.com/Ronnasayd/aipp/commit/acce19d))
- **[🚧 Other Changes]** Git add src/pyproject.toml src/uv.lock git commit -m "fix(mcp): pin fastmcp<3 to avoid broken v4.0.3 resolution" ([feaf1a1](https://github.com/Ronnasayd/aipp/commit/feaf1a1))
- **[♻️ Refactoring]** Moved to mcp-manager ([2ad0b14](https://github.com/Ronnasayd/aipp/commit/2ad0b14))
- **[✨ Features]** Add guide for generating images with omniroute ([a5db1c1](https://github.com/Ronnasayd/aipp/commit/a5db1c1))

### **2026-09-04**

- **[🧹 Chores]** Add blender mcp server and swap session-memory command ([92297c7](https://github.com/Ronnasayd/aipp/commit/92297c7))

### **2026-09-03**

- **[🐛 Bug Fixes]** Match durable memory pages by path with plural query forms ([d8a4dff](https://github.com/Ronnasayd/aipp/commit/d8a4dff))
- **[🧹 Chores]** Gate ai-memory auto-improve behind manual approval ([20f160f](https://github.com/Ronnasayd/aipp/commit/20f160f))
- **[📚 Documentation]** Add end-of-session permanent-memory step to sd-planning and sd-execute ([26ad590](https://github.com/Ronnasayd/aipp/commit/26ad590))
- **[✨ Features]** Add hook authoring skill and conventions ([becb918](https://github.com/Ronnasayd/aipp/commit/becb918))
- **[✨ Features]** Add sessionstart hook to surface durable ai-memory pages ([965cbb4](https://github.com/Ronnasayd/aipp/commit/965cbb4))
- **[♻️ Refactoring]** Add ai_memory_project_strategy=repo-root to all hook commands and update aliases to include project strategy for consistent repo-root behavior. ([847d330](https://github.com/Ronnasayd/aipp/commit/847d330))
- **[♻️ Refactoring]** Split ai-memory install into separate mcp and hooks aliases ([f253eaf](https://github.com/Ronnasayd/aipp/commit/f253eaf))
- **[✨ Features]** Enforce interactive question tools on subagentstop ([cfe8ec9](https://github.com/Ronnasayd/aipp/commit/cfe8ec9))
- **[🚧 Other Changes]** Add hooks for subagent start and stop commands ([8ee9f65](https://github.com/Ronnasayd/aipp/commit/8ee9f65))

### **2026-09-02**

- **[♻️ Refactoring]** Move ai-memory install-skills to the end of the install process ([66fadec](https://github.com/Ronnasayd/aipp/commit/66fadec))
- **[♻️ Refactoring]** Remove ai_memory_consolidate_on_session_end environment variable from aimsllm alias ([e1ab964](https://github.com/Ronnasayd/aipp/commit/e1ab964))
- **[🧹 Chores]** Harden ai-memory setup and refresh agents.md docs ([baf1379](https://github.com/Ronnasayd/aipp/commit/baf1379))
- **[♻️ Refactoring]** Update permission mode handling to use 'dontask' instead of 'bypasspermissions' ([d712e89](https://github.com/Ronnasayd/aipp/commit/d712e89))
- **[♻️ Refactoring]** Update settings to limit concurrent subagents and disable explore plan agents ([72e60e9](https://github.com/Ronnasayd/aipp/commit/72e60e9))

### **2026-09-01**

- **[♻️ Refactoring]** Update import path for fastmcp and change default model to sonnet ([878e6df](https://github.com/Ronnasayd/aipp/commit/878e6df))
- **[♻️ Refactoring]** Update settings to enable auto-compaction and switch model to haiku ([f10e12f](https://github.com/Ronnasayd/aipp/commit/f10e12f))
- **[✨ Features]** Truncate large lint outputs to /tmp with reference path ([c6f99a6](https://github.com/Ronnasayd/aipp/commit/c6f99a6))

### **2026-08-31**

- **[✨ Features]** Surface disabled mcp servers in session context ([1626fda](https://github.com/Ronnasayd/aipp/commit/1626fda))
- **[♻️ Refactoring]** Add language rule ([38e81c6](https://github.com/Ronnasayd/aipp/commit/38e81c6))
- **[✨ Features]** Add generate-design-md skill ([14e9ccb](https://github.com/Ronnasayd/aipp/commit/14e9ccb))

### **2026-08-30**

- **[✨ Features]** Promote ask to allow in bypasspermissions mode ([482ebeb](https://github.com/Ronnasayd/aipp/commit/482ebeb))

### **2026-08-29**

- **[♻️ Refactoring]** Add label and status ([211d4ea](https://github.com/Ronnasayd/aipp/commit/211d4ea))
- **[♻️ Refactoring]** Add log ([3c86e36](https://github.com/Ronnasayd/aipp/commit/3c86e36))
- **[🐛 Bug Fixes]** Serialize concurrent jest coverage merges and show stale coverage ([ab7df49](https://github.com/Ronnasayd/aipp/commit/ab7df49))
- **[✨ Features]** Add per-subagent status line ([876a3fe](https://github.com/Ronnasayd/aipp/commit/876a3fe))
- **[🐛 Bug Fixes]** Resolve rag-rat.toml check against ai_project_dir ([0a668b5](https://github.com/Ronnasayd/aipp/commit/0a668b5))
- **[🧹 Chores]** Block commit messages that mention ai code assistants ([3da5b80](https://github.com/Ronnasayd/aipp/commit/3da5b80))
- **[♻️ Refactoring]** Compress specialist agent instruction files ([1628b39](https://github.com/Ronnasayd/aipp/commit/1628b39))
- **[✨ Features]** Match rtk-proxied commands against plain permission patterns ([d46f488](https://github.com/Ronnasayd/aipp/commit/d46f488))

### **2026-08-28**

- **[♻️ Refactoring]** Add block any claude info in commits ([3bdb66c](https://github.com/Ronnasayd/aipp/commit/3bdb66c))
- **[♻️ Refactoring]** Remove subagent commit block ([f007296](https://github.com/Ronnasayd/aipp/commit/f007296))
- **[🧹 Chores]** Mount mcp-manager dir read-only and add skip-permissions shortcut ([88cd40c](https://github.com/Ronnasayd/aipp/commit/88cd40c))
- **[♻️ Refactoring]** Expand service labels and use colored dot indicators ([9d8c98a](https://github.com/Ronnasayd/aipp/commit/9d8c98a))
- **[♻️ Refactoring]** Double context bar resolution to 5% per segment ([841aee3](https://github.com/Ronnasayd/aipp/commit/841aee3))
- **[♻️ Refactoring]** Extract field separator into sep variable ([ac8f918](https://github.com/Ronnasayd/aipp/commit/ac8f918))
- **[✨ Features]** Add osc 8 hyperlinks and catppuccin color vars ([675bb84](https://github.com/Ronnasayd/aipp/commit/675bb84))
- **[♻️ Refactoring]** Use catppuccin color vars and k-format token counts ([0d867a7](https://github.com/Ronnasayd/aipp/commit/0d867a7))
- **[✨ Features]** Add nerd font icons, catppuccin colors, and context bar ([2bdbdfb](https://github.com/Ronnasayd/aipp/commit/2bdbdfb))
- **[🧹 Chores]** Retire md_json_lint hook and add requirements-table step to sd-planning ([7e3de8f](https://github.com/Ronnasayd/aipp/commit/7e3de8f))
- **[♻️ Refactoring]** Add omniroute ([fa0c6a8](https://github.com/Ronnasayd/aipp/commit/fa0c6a8))
- **[📚 Documentation]** Align spec-to-requirements-table output with example format ([d53f27e](https://github.com/Ronnasayd/aipp/commit/d53f27e))
- **[✨ Features]** Add spec-to-requirements-table skill ([29ae34c](https://github.com/Ronnasayd/aipp/commit/29ae34c))

### **2026-08-27**

- **[✨ Features]** Play alert sound on user questions and permission prompts ([2de97ca](https://github.com/Ronnasayd/aipp/commit/2de97ca))
- **[🐛 Bug Fixes]** Reconstruct last assistant message from transcript in question enforcer ([b89cfef](https://github.com/Ronnasayd/aipp/commit/b89cfef))
- **[🧹 Chores]** Move scripts unused by settings.json to unused/ ([e82ba29](https://github.com/Ronnasayd/aipp/commit/e82ba29))
- **[♻️ Refactoring]** Rename tlc-* skills to sd-* naming scheme ([674df32](https://github.com/Ronnasayd/aipp/commit/674df32))
- **[♻️ Refactoring]** Add new term for question tool enforce ([a03c8fb](https://github.com/Ronnasayd/aipp/commit/a03c8fb))
- **[✨ Features]** Replace sessionend formatter with git pre-commit hook ([0644045](https://github.com/Ronnasayd/aipp/commit/0644045))
- **[🐛 Bug Fixes]** Only report jscpd duplication above threshold ([57b013b](https://github.com/Ronnasayd/aipp/commit/57b013b))
- **[🐛 Bug Fixes]** Only report jscpd duplication above threshold ([06e47d6](https://github.com/Ronnasayd/aipp/commit/06e47d6))

### **2026-08-26**

- **[🐛 Bug Fixes]** Adjust script location ([53682ee](https://github.com/Ronnasayd/aipp/commit/53682ee))
- **[✨ Features]** Warn agent to write markdown in english for docs/spec dirs ([c93972d](https://github.com/Ronnasayd/aipp/commit/c93972d))
- **[✨ Features]** Add spacy stopword removal deps and model install ([64111d3](https://github.com/Ronnasayd/aipp/commit/64111d3))

### **2026-08-25**

- **[📚 Documentation]** Update env var name in environments.md table ([4df0573](https://github.com/Ronnasayd/aipp/commit/4df0573))
- **[♻️ Refactoring]** Rename claude_project_dir to ai_project_dir, allow memory md writes ([d7301e8](https://github.com/Ronnasayd/aipp/commit/d7301e8))
- **[🐛 Bug Fixes]** Resolve tsconfig path aliases in jest related-files import scan ([145e453](https://github.com/Ronnasayd/aipp/commit/145e453))
- **[✨ Features]** Add jest related-files report hook ([2588e5d](https://github.com/Ronnasayd/aipp/commit/2588e5d))
- **[♻️ Refactoring]** Move jest coverage-summary build out of background merge ([084deda](https://github.com/Ronnasayd/aipp/commit/084deda))
- **[🐛 Bug Fixes]** Write coverage json atomically to avoid partial reads ([37f2143](https://github.com/Ronnasayd/aipp/commit/37f2143))
- **[♻️ Refactoring]** Write jest coverage-summary.json under coverage/summary/ ([a558723](https://github.com/Ronnasayd/aipp/commit/a558723))
- **[🧹 Chores]** Sync dev tooling and hooks config ([c91b696](https://github.com/Ronnasayd/aipp/commit/c91b696))

### **2026-08-24**

- **[✨ Features]** Surface uncovered line numbers in jest coverage report ([5781f16](https://github.com/Ronnasayd/aipp/commit/5781f16))
- **[♻️ Refactoring]** Add position ([27b8ab6](https://github.com/Ronnasayd/aipp/commit/27b8ab6))
- **[🐛 Bug Fixes]** Always append findrelatedtests and coverage flags in incremental jest run ([8ba9783](https://github.com/Ronnasayd/aipp/commit/8ba9783))
- **[✨ Features]** Add custom jest coverage command overrides ([120b40b](https://github.com/Ronnasayd/aipp/commit/120b40b))
- **[🐛 Bug Fixes]** Set node_env=test for jest coverage runs and wire session-end hook ([552eb45](https://github.com/Ronnasayd/aipp/commit/552eb45))
- **[♻️ Refactoring]** Change to runinband ([8d4bfc4](https://github.com/Ronnasayd/aipp/commit/8d4bfc4))
- **[🚧 Other Changes]** Cap jest workers at 25% in coverage hooks ([c283991](https://github.com/Ronnasayd/aipp/commit/c283991))
- **[♻️ Refactoring]** Replace embedding daemon with rag-rat semantic_search in similar_code_ref ([3cac89a](https://github.com/Ronnasayd/aipp/commit/3cac89a))
- **[♻️ Refactoring]** Replace regex symbol/import extraction with tree-sitter ast ([5040eca](https://github.com/Ronnasayd/aipp/commit/5040eca))
- **[📚 Documentation]** Compress skill.md into scannable core ([61f3d97](https://github.com/Ronnasayd/aipp/commit/61f3d97))
- **[✨ Features]** Add dynamic programming ([8934cb5](https://github.com/Ronnasayd/aipp/commit/8934cb5))
- **[📚 Documentation]** Move adr template reference to local skill directory ([c9f441e](https://github.com/Ronnasayd/aipp/commit/c9f441e))
- **[📚 Documentation]** Restructure step loop and sync checklist ([8fcaf89](https://github.com/Ronnasayd/aipp/commit/8fcaf89))
- **[🚧 Other Changes]** Add eval cases for impact_surface_hint hook ([d1cfe40](https://github.com/Ronnasayd/aipp/commit/d1cfe40))
- **[🐛 Bug Fixes]** Resolve symbol from post-edit file content, not stale old_string ([acb31a3](https://github.com/Ronnasayd/aipp/commit/acb31a3))
- **[🐛 Bug Fixes]** Read changed symbols from payload instead of git diff hunks ([b99c5ca](https://github.com/Ronnasayd/aipp/commit/b99c5ca))
- **[✨ Features]** Add impact_surface_hint posttooluse hook ([5155781](https://github.com/Ronnasayd/aipp/commit/5155781))

### **2026-08-23**

- **[✨ Features]** Add taskmaster_next_task sessionstart hook ([3bd2998](https://github.com/Ronnasayd/aipp/commit/3bd2998))

### **2026-08-22**

- **[🐛 Bug Fixes]** Correct ai_project_dir to ai_project_root_dir in hook paths ([e799bb9](https://github.com/Ronnasayd/aipp/commit/e799bb9))

### **2026-08-21**

- **[🐛 Bug Fixes]** Python call ([5bc2f6a](https://github.com/Ronnasayd/aipp/commit/5bc2f6a))
- **[🐛 Bug Fixes]** Add missing pyyaml dependency to pyproject.toml ([9c33734](https://github.com/Ronnasayd/aipp/commit/9c33734))
- **[🧹 Chores]** Migrate src package from poetry to uv/setuptools ([8715ddd](https://github.com/Ronnasayd/aipp/commit/8715ddd))
- **[🧹 Chores]** Install hook-script deps via uv sync ([ba645fb](https://github.com/Ronnasayd/aipp/commit/ba645fb))
- **[🧹 Chores]** Run hook scripts through isolated uv venv ([6ad9c2c](https://github.com/Ronnasayd/aipp/commit/6ad9c2c))
- **[🧹 Chores]** Lock hook-script dependencies (numpy, fastembed) ([aace4f8](https://github.com/Ronnasayd/aipp/commit/aace4f8))
- **[🧹 Chores]** Add root pyproject.toml for hook-script deps ([0cda182](https://github.com/Ronnasayd/aipp/commit/0cda182))
- **[🧹 Chores]** Update styles ([a70840a](https://github.com/Ronnasayd/aipp/commit/a70840a))

### **2026-08-20**

- **[🚧 Other Changes]** Add eval cases for previously untested pretooluse hooks ([63a1923](https://github.com/Ronnasayd/aipp/commit/63a1923))
- **[♻️ Refactoring]** Consolidate hook eval runners into a single generic script ([8e1b7ce](https://github.com/Ronnasayd/aipp/commit/8e1b7ce))
- **[🧹 Chores]** Lower default model/effort and skip commits on protected branches ([b521514](https://github.com/Ronnasayd/aipp/commit/b521514))
- **[🚧 Other Changes]** Git commit -m "refactor: dedupe split_on_operators/strip_heredocs across hook scripts ([34afc2f](https://github.com/Ronnasayd/aipp/commit/34afc2f))
- **[♻️ Refactoring]** Remove rag-rat ([b27dd8f](https://github.com/Ronnasayd/aipp/commit/b27dd8f))
- **[♻️ Refactoring]** Add .serena to exclude ([d067623](https://github.com/Ronnasayd/aipp/commit/d067623))
- **[🧹 Chores]** Create backup ([505c085](https://github.com/Ronnasayd/aipp/commit/505c085))
- **[♻️ Refactoring]** Fix python ([1b0b71a](https://github.com/Ronnasayd/aipp/commit/1b0b71a))
- **[✨ Features]** Re-add claude.warmup.sh ([c35c04d](https://github.com/Ronnasayd/aipp/commit/c35c04d))

### **2026-08-19**

- **[✨ Features]** Allow user-controlled allowed_patterns extension via env var ([698843a](https://github.com/Ronnasayd/aipp/commit/698843a))
- **[🧹 Chores]** Remove rag-rat from settings ([e74c4d0](https://github.com/Ronnasayd/aipp/commit/e74c4d0))
- **[📚 Documentation]** Require taskcreate/taskupdate tracking in grilling and taskmaster skills ([2434f0b](https://github.com/Ronnasayd/aipp/commit/2434f0b))
- **[✨ Features]** Add protect_branches hook for main/master/develop/homolog ([fa6fcf9](https://github.com/Ronnasayd/aipp/commit/fa6fcf9))

### **2026-08-18**

- **[✨ Features]** Add gghget_file for single-file github downloads ([8de4ef0](https://github.com/Ronnasayd/aipp/commit/8de4ef0))
- **[🧹 Chores]** Update skills ([f6bc9e4](https://github.com/Ronnasayd/aipp/commit/f6bc9e4))
- **[🐛 Bug Fixes]** Gate bm25 skill matches on cosine results ([e11af16](https://github.com/Ronnasayd/aipp/commit/e11af16))
- **[✨ Features]** Add regex fallback secret scanner ([0cedc6b](https://github.com/Ronnasayd/aipp/commit/0cedc6b))
- **[🐛 Bug Fixes]** Raise bm25 term overlap threshold to reduce false positives ([4dea762](https://github.com/Ronnasayd/aipp/commit/4dea762))
- **[✨ Features]** Warn on markdown files created outside doc directories ([f8a78c4](https://github.com/Ronnasayd/aipp/commit/f8a78c4))
- **[✨ Features]** Add tmux/screen guard for dev server commands ([53e1853](https://github.com/Ronnasayd/aipp/commit/53e1853))
- **[♻️ Refactoring]** Harden protect_files splitter and add smart_approve hook ([4a21923](https://github.com/Ronnasayd/aipp/commit/4a21923))
- **[🐛 Bug Fixes]** Mount ai_project_root_dir so hooks/skills symlinks resolve ([2339245](https://github.com/Ronnasayd/aipp/commit/2339245))
- **[🐛 Bug Fixes]** Include scores in skill activation debug logs ([37d4c90](https://github.com/Ronnasayd/aipp/commit/37d4c90))
- **[♻️ Refactoring]** Increase min score ([0e5f9ec](https://github.com/Ronnasayd/aipp/commit/0e5f9ec))
- **[🐛 Bug Fixes]** Tighten bm25 skill matching to reduce false positives ([c80ff1e](https://github.com/Ronnasayd/aipp/commit/c80ff1e))
- **[♻️ Refactoring]** Compress technical-decision-helper skill.md ([0992e8a](https://github.com/Ronnasayd/aipp/commit/0992e8a))
- **[✨ Features]** Add bm25 lexical search fused with vector similarity for skill activation ([7987a7b](https://github.com/Ronnasayd/aipp/commit/7987a7b))
- **[✨ Features]** Surface config files in start_context additionalcontext ([663e185](https://github.com/Ronnasayd/aipp/commit/663e185))

### **2026-08-15**

- **[✨ Features]** Add rag-rat search hook for userpromptsubmit and askuserquestion ([cb5cee2](https://github.com/Ronnasayd/aipp/commit/cb5cee2))
- **[♻️ Refactoring]** Remove headroom integration ([e2fc024](https://github.com/Ronnasayd/aipp/commit/e2fc024))

### **2026-08-14**

- **[♻️ Refactoring]** Simplify lhwc alias and disable headroom mcp by default ([1dfad10](https://github.com/Ronnasayd/aipp/commit/1dfad10))
- **[♻️ Refactoring]** Remove claude.warmup ([8f2d4e7](https://github.com/Ronnasayd/aipp/commit/8f2d4e7))
- **[♻️ Refactoring]** Add tee logs ([27eb54a](https://github.com/Ronnasayd/aipp/commit/27eb54a))
- **[✨ Features]** Inject live mcp-manager context via pretooluse hook ([1795cd4](https://github.com/Ronnasayd/aipp/commit/1795cd4))
- **[🐛 Bug Fixes]** Add ~/.local/bin to path in warmup script ([2c2d2ec](https://github.com/Ronnasayd/aipp/commit/2c2d2ec))
- **[♻️ Refactoring]** Persist current account on choose, drop timestamped backups ([f9f31d9](https://github.com/Ronnasayd/aipp/commit/f9f31d9))

### **2026-08-13**

- **[✨ Features]** Add cron warmup script for multi-account session tracking ([b28c10c](https://github.com/Ronnasayd/aipp/commit/b28c10c))
- **[🧹 Chores]** Disable tool search, add ponytail plugin, enable auto mode ([2bc07c8](https://github.com/Ronnasayd/aipp/commit/2bc07c8))
- **[✨ Features]** Detect skill invocation via /skill-name prompts too ([14e47e6](https://github.com/Ronnasayd/aipp/commit/14e47e6))
- **[🐛 Bug Fixes]** Run session-end formatters detached via nohup ([964f6c0](https://github.com/Ronnasayd/aipp/commit/964f6c0))
- **[✨ Features]** Return golangci-lint, ruff, mypy, eslint output as json ([554e769](https://github.com/Ronnasayd/aipp/commit/554e769))
- **[✨ Features]** Return jscpd output as structured json ([0ea3d4b](https://github.com/Ronnasayd/aipp/commit/0ea3d4b))
- **[✨ Features]** Run skill/context7 search on askuserquestion answers ([18c224c](https://github.com/Ronnasayd/aipp/commit/18c224c))
- **[✨ Features]** Log userpromptexpansion events ([40e425f](https://github.com/Ronnasayd/aipp/commit/40e425f))
- **[🐛 Bug Fixes]** Only skip suggesting referenced skill when it exists locally ([7f4740d](https://github.com/Ronnasayd/aipp/commit/7f4740d))
- **[✨ Features]** Detect referenced skill via /skill-name and skip suggesting it ([c839a7c](https://github.com/Ronnasayd/aipp/commit/c839a7c))

### **2026-08-12**

- **[♻️ Refactoring]** Change percentage to 5 ([2ce4fac](https://github.com/Ronnasayd/aipp/commit/2ce4fac))
- **[♻️ Refactoring]** Add cat-ca ([48aa9b5](https://github.com/Ronnasayd/aipp/commit/48aa9b5))
- **[♻️ Refactoring]** Standardize debug log tag for additionalcontext output ([82d9624](https://github.com/Ronnasayd/aipp/commit/82d9624))
- **[🧹 Chores]** Register tlc-semantic-grilling in manifest and ignore list ([6c87c77](https://github.com/Ronnasayd/aipp/commit/6c87c77))
- **[♻️ Refactoring]** Migrate prompt content into skill ([e8d3918](https://github.com/Ronnasayd/aipp/commit/e8d3918))
- **[📚 Documentation]** Restructure into numbered workflow steps ([8b18944](https://github.com/Ronnasayd/aipp/commit/8b18944))
- **[🧹 Chores]** Enable auto permission mode and disable background tasks ([db8b294](https://github.com/Ronnasayd/aipp/commit/db8b294))
- **[📚 Documentation]** Add sequentialthinking pre-step ([11de667](https://github.com/Ronnasayd/aipp/commit/11de667))

### **2026-08-11**

- **[✨ Features]** Add claude account switcher script and aliases ([24bc027](https://github.com/Ronnasayd/aipp/commit/24bc027))
- **[♻️ Refactoring]** Drop metadata.json generation ([e0db8bd](https://github.com/Ronnasayd/aipp/commit/e0db8bd))
- **[♻️ Refactoring]** Extract bucket size constant in checklist_context_watch ([0adb6d1](https://github.com/Ronnasayd/aipp/commit/0adb6d1))
- **[♻️ Refactoring]** Improve readability of skills_root assignment with multi-line formatting ([065db94](https://github.com/Ronnasayd/aipp/commit/065db94))
- **[🐛 Bug Fixes]** Resolve skills root under .claude when ai_project_dir is set ([c54de6e](https://github.com/Ronnasayd/aipp/commit/c54de6e))

### **2026-08-10**

- **[✨ Features]** Protect .claude-l directory from edits ([c48a412](https://github.com/Ronnasayd/aipp/commit/c48a412))
- **[♻️ Refactoring]** Split quality_gate.py into check-only + session-end formatting ([854fd04](https://github.com/Ronnasayd/aipp/commit/854fd04))
- **[♻️ Refactoring]** Change context usage bucket threshold to 5% ([862a98b](https://github.com/Ronnasayd/aipp/commit/862a98b))
- **[🐛 Bug Fixes]** Correct skills root default and add debug logging ([bd1ec11](https://github.com/Ronnasayd/aipp/commit/bd1ec11))
- **[✨ Features]** Resurface skill checklist.md on context growth ([05e0e72](https://github.com/Ronnasayd/aipp/commit/05e0e72))
- **[🐛 Bug Fixes]** Write context debug log to ~/.claude/logs ([4cf480d](https://github.com/Ronnasayd/aipp/commit/4cf480d))
- **[📚 Documentation]** Sync docs via generate-docs after execute ([4de7263](https://github.com/Ronnasayd/aipp/commit/4de7263))
- **[✨ Features]** Add adr template and criteria for offering adrs ([c3e35ce](https://github.com/Ronnasayd/aipp/commit/c3e35ce))

### **2026-08-08**

- **[🐛 Bug Fixes]** Bind systemd-resolved stub for dns resolution in sandbox ([bcf0f47](https://github.com/Ronnasayd/aipp/commit/bcf0f47))
- **[♻️ Refactoring]** Move hook logs from /tmp to ~/.claude/logs ([442858f](https://github.com/Ronnasayd/aipp/commit/442858f))
- **[🐛 Bug Fixes]** Bind real /tmp and passthrough env vars to fix claude auto-update in sandbox ([32192ae](https://github.com/Ronnasayd/aipp/commit/32192ae))

### **2026-08-07**

- **[🧹 Chores]** Enable 1m context and auto tool-search for sonnet/opus ([1726f7c](https://github.com/Ronnasayd/aipp/commit/1726f7c))
- **[✨ Features]** Add phase 3.5 test-file mining ([ddc5cb0](https://github.com/Ronnasayd/aipp/commit/ddc5cb0))
- **[📚 Documentation]** Include grep and read as fallback search tools ([673067b](https://github.com/Ronnasayd/aipp/commit/673067b))

### **2026-08-06**

- **[✨ Features]** Add pretooluse hook to surface dir-level context files ([ad79e71](https://github.com/Ronnasayd/aipp/commit/ad79e71))
- **[✨ Features]** Accept broader change sources and add semantic search ([2fa68d5](https://github.com/Ronnasayd/aipp/commit/2fa68d5))
- **[♻️ Refactoring]** Update skills manifest and index for generate-docs skill ([74a20cd](https://github.com/Ronnasayd/aipp/commit/74a20cd))
- **[🧹 Chores]** Remove superseded generate-docs-init and generate-docs-update skills ([ba34dab](https://github.com/Ronnasayd/aipp/commit/ba34dab))
- **[✨ Features]** Add dispatcher skill.md with auto-detect mode selection ([a3c6ffe](https://github.com/Ronnasayd/aipp/commit/a3c6ffe))
- **[✨ Features]** Port templates for create mode ([23f9c6f](https://github.com/Ronnasayd/aipp/commit/23f9c6f))
- **[✨ Features]** Add update mode reference ([ff9bdc7](https://github.com/Ronnasayd/aipp/commit/ff9bdc7))
- **[✨ Features]** Add create mode reference ([93dae16](https://github.com/Ronnasayd/aipp/commit/93dae16))
- **[✨ Features]** Add shared reference for writing standards and anti-patterns ([119d40b](https://github.com/Ronnasayd/aipp/commit/119d40b))
- **[🚧 Other Changes]** Refactor `/tlc-semantic-grilling` prompt to include taskmaster registration option ([b29a46d](https://github.com/Ronnasayd/aipp/commit/b29a46d))
- **[♻️ Refactoring]** Adjust name ([1725765](https://github.com/Ronnasayd/aipp/commit/1725765))
- **[♻️ Refactoring]** Rename tlc-execute-tasks to tlc-spec-driven-taskmaster, drop adversarial variant ([a5e7644](https://github.com/Ronnasayd/aipp/commit/a5e7644))
- **[♻️ Refactoring]** Fold tlc-execute-tasks-adversarial into tlc-execute-tasks as thin taskmaster wrapper ([b476bc3](https://github.com/Ronnasayd/aipp/commit/b476bc3))
- **[🧹 Chores]** Tune similarity threshold and effort level, silence probe warning ([014da85](https://github.com/Ronnasayd/aipp/commit/014da85))

### **2026-08-05**

- **[♻️ Refactoring]** Update skills ([7cd699a](https://github.com/Ronnasayd/aipp/commit/7cd699a))
- **[✨ Features]** Strip stopwords/lemma via spacy before embedding ([828e61b](https://github.com/Ronnasayd/aipp/commit/828e61b))
- **[♻️ Refactoring]** Replace oauth account switcher with config-dir cloning ([c61f462](https://github.com/Ronnasayd/aipp/commit/c61f462))
- **[♻️ Refactoring]** Route tlc-execute-tasks through orchestrator context-map ([a7dabd4](https://github.com/Ronnasayd/aipp/commit/a7dabd4))
- **[✨ Features]** Add jira-to-todo skill for exporting pending jira issues ([39e87ff](https://github.com/Ronnasayd/aipp/commit/39e87ff))

### **2026-08-04**

- **[📚 Documentation]** Add descriptive comments to remaining aliases ([c29b993](https://github.com/Ronnasayd/aipp/commit/c29b993))
- **[✨ Features]** Add agent-flow hooks to all lifecycle events ([2eb7a75](https://github.com/Ronnasayd/aipp/commit/2eb7a75))
- **[🧹 Chores]** Add osd shortcut for opencode-supervisor dashboard ([43d869e](https://github.com/Ronnasayd/aipp/commit/43d869e))
- **[🧹 Chores]** Rename create-commit prompt to .md and tweak aliases ([0296baa](https://github.com/Ronnasayd/aipp/commit/0296baa))

### **2026-08-03**

- **[✨ Features]** Isolate task execution in worktrees with run-branch merge and post-merge verify ([72d1602](https://github.com/Ronnasayd/aipp/commit/72d1602))

### **2026-07-31**

- **[♻️ Refactoring]** Use .git/info/exclude instead of .gitignore for local ignores ([5123c11](https://github.com/Ronnasayd/aipp/commit/5123c11))
- **[📚 Documentation]** Add semantic-grilling prompt command ([ac531cc](https://github.com/Ronnasayd/aipp/commit/ac531cc))

### **2026-07-30**

- **[📚 Documentation]** Fix run-branch naming and pending-task filter in tlc-execute-tasks-adversarial ([e0127f3](https://github.com/Ronnasayd/aipp/commit/e0127f3))
- **[♻️ Refactoring]** Add log ([1ded8d0](https://github.com/Ronnasayd/aipp/commit/1ded8d0))
- **[🐛 Bug Fixes]** Skip session-end jest coverage if already running ([72ea992](https://github.com/Ronnasayd/aipp/commit/72ea992))
- **[♻️ Refactoring]** Trigger worktree init from enterworktree posttooluse ([189d6f8](https://github.com/Ronnasayd/aipp/commit/189d6f8))
- **[🐛 Bug Fixes]** Prefer explicit worktree path fields over cwd ([c6507d8](https://github.com/Ronnasayd/aipp/commit/c6507d8))
- **[🐛 Bug Fixes]** Echo worktree path from worktreecreate hook ([e677b85](https://github.com/Ronnasayd/aipp/commit/e677b85))
- **[✨ Features]** Symlink node_modules into new worktrees ([c73d910](https://github.com/Ronnasayd/aipp/commit/c73d910))
- **[📚 Documentation]** Add run-branch isolation and review-merge step ([bd20c1b](https://github.com/Ronnasayd/aipp/commit/bd20c1b))
- **[♻️ Refactoring]** Pass full payload to rule match predicates ([6e95e98](https://github.com/Ronnasayd/aipp/commit/6e95e98))
- **[♻️ Refactoring]** Rename context-rules hook to support posttooluse ([6bcc236](https://github.com/Ronnasayd/aipp/commit/6bcc236))
- **[📚 Documentation]** Replace skill's requirements-doc structure with domain-table format ([d87ca7b](https://github.com/Ronnasayd/aipp/commit/d87ca7b))
- **[🐛 Bug Fixes]** Raise context7 match thresholds, expand debug log fields ([96a68d3](https://github.com/Ronnasayd/aipp/commit/96a68d3))
- **[✨ Features]** Inject package.json scripts into sessionstart context ([ea509cd](https://github.com/Ronnasayd/aipp/commit/ea509cd))
- **[📚 Documentation]** Drop mcp suffix from tool names in start.md rules ([104d1d9](https://github.com/Ronnasayd/aipp/commit/104d1d9))
- **[📚 Documentation]** Add mcp-manager tools table to start.md hook ([dff65ff](https://github.com/Ronnasayd/aipp/commit/dff65ff))
- **[🐛 Bug Fixes]** Match tlc-execute-tasks-adversarial in context rule regex ([96f772a](https://github.com/Ronnasayd/aipp/commit/96f772a))

### **2026-07-29**

- **[✨ Features]** Compress extract-software-requirements skill, add last-n extraction ([62feb37](https://github.com/Ronnasayd/aipp/commit/62feb37))
- **[♻️ Refactoring]** Replace start prompt with sessionstart hook injecting rules ([8bbe98c](https://github.com/Ronnasayd/aipp/commit/8bbe98c))
- **[♻️ Refactoring]** Replace start prompt with sessionstart hook injecting rules ([b9a6187](https://github.com/Ronnasayd/aipp/commit/b9a6187))
- **[♻️ Refactoring]** Rebuild manifest ([bfec766](https://github.com/Ronnasayd/aipp/commit/bfec766))
- **[♻️ Refactoring]** Rename simplified-technical-english skill to ste, add ste-pt ([27c5d7b](https://github.com/Ronnasayd/aipp/commit/27c5d7b))
- **[🧹 Chores]** Change style ([e7fa39a](https://github.com/Ronnasayd/aipp/commit/e7fa39a))
- **[♻️ Refactoring]** Derive ai_project_root_dir at install time instead of hardcoding ([49b01bd](https://github.com/Ronnasayd/aipp/commit/49b01bd))
- **[♻️ Refactoring]** Verifi *rc files before insert ([751f81d](https://github.com/Ronnasayd/aipp/commit/751f81d))
- **[♻️ Refactoring]** Adjust names ([d0b091c](https://github.com/Ronnasayd/aipp/commit/d0b091c))
- **[♻️ Refactoring]** Auto install alias ([3638409](https://github.com/Ronnasayd/aipp/commit/3638409))
- **[🐛 Bug Fixes]** Split commands ([087909e](https://github.com/Ronnasayd/aipp/commit/087909e))
- **[🐛 Bug Fixes]** Adjust path ([3241c59](https://github.com/Ronnasayd/aipp/commit/3241c59))
- **[✨ Features]** Add build.sh helper install script and reference it in install.sh ([2ee6c62](https://github.com/Ronnasayd/aipp/commit/2ee6c62))
- **[🐛 Bug Fixes]** Adjust icon ([63e1611](https://github.com/Ronnasayd/aipp/commit/63e1611))
- **[✨ Features]** Add serena status indicator to statusline and alias ([cc364a0](https://github.com/Ronnasayd/aipp/commit/cc364a0))

### **2026-07-28**

- **[🐛 Bug Fixes]** Use $ai_project_root_dir in statusline command path ([c501272](https://github.com/Ronnasayd/aipp/commit/c501272))
- **[♻️ Refactoring]** Rename ai_project_dir to ai_project_root_dir ([3241788](https://github.com/Ronnasayd/aipp/commit/3241788))
- **[♻️ Refactoring]** Adjsut text ([e1858da](https://github.com/Ronnasayd/aipp/commit/e1858da))
- **[🐛 Bug Fixes]** Add rtk install command ([d9ec25b](https://github.com/Ronnasayd/aipp/commit/d9ec25b))
- **[🐛 Bug Fixes]** Add more verbose messages ([0424b68](https://github.com/Ronnasayd/aipp/commit/0424b68))
- **[🐛 Bug Fixes]** Add install fastembed ([661db4f](https://github.com/Ronnasayd/aipp/commit/661db4f))
- **[✨ Features]** Allow read-only mcp tools in permission allow list ([cbf1a6a](https://github.com/Ronnasayd/aipp/commit/cbf1a6a))
- **[✨ Features]** Add per-file lockfile to jest coverage hooks to prevent races ([6f591ae](https://github.com/Ronnasayd/aipp/commit/6f591ae))
- **[✨ Features]** Colorize account email in statusline output ([3de681d](https://github.com/Ronnasayd/aipp/commit/3de681d))
- **[✨ Features]** Add debug logging and empty-data guard to embedding daemon ([b0c9bb2](https://github.com/Ronnasayd/aipp/commit/b0c9bb2))

### **2026-07-27**

- **[✨ Features]** Add config path arg and account email to statusline/dmsl scripts ([e8377d8](https://github.com/Ronnasayd/aipp/commit/e8377d8))
- **[✨ Features]** Add jest coverage reporting hook with additionalcontext ([86f3e09](https://github.com/Ronnasayd/aipp/commit/86f3e09))
- **[✨ Features]** Add jest coverage session end hook and utilities ([bb857b6](https://github.com/Ronnasayd/aipp/commit/bb857b6))
- **[✨ Features]** Improve html report file handling in coverage merge ([f948369](https://github.com/Ronnasayd/aipp/commit/f948369))
- **[✨ Features]** Enhance coverage merging and reporting functionality ([a606221](https://github.com/Ronnasayd/aipp/commit/a606221))
- **[✨ Features]** Implement coverage merging functionality ([cc0b11b](https://github.com/Ronnasayd/aipp/commit/cc0b11b))
- **[🐛 Bug Fixes]** Correct coverage file handling in incremental hook ([86938e1](https://github.com/Ronnasayd/aipp/commit/86938e1))
- **[✨ Features]** Enhance incremental coverage merging process ([093c843](https://github.com/Ronnasayd/aipp/commit/093c843))
- **[✨ Features]** Add coverage report generation to incremental hook ([d89942e](https://github.com/Ronnasayd/aipp/commit/d89942e))
- **[✨ Features]** Update jest command to use --findrelatedtests option ([7d87d02](https://github.com/Ronnasayd/aipp/commit/7d87d02))
- **[✨ Features]** Add incremental jest coverage hook and update models ([fcbd433](https://github.com/Ronnasayd/aipp/commit/fcbd433))

### **2026-07-25**

- **[✨ Features]** Add 9router-medium model and update environment variables ([e1e236a](https://github.com/Ronnasayd/aipp/commit/e1e236a))
- **[✨ Features]** Add start_embedding_daemon.py script for pre-warming daemon ([6366ba1](https://github.com/Ronnasayd/aipp/commit/6366ba1))
- **[✨ Features]** Add rag-rat status to status line output ([dba7f9f](https://github.com/Ronnasayd/aipp/commit/dba7f9f))
- **[🧹 Chores]** Add debug logging to external hooks and rag-rat init alias ([c424c8b](https://github.com/Ronnasayd/aipp/commit/c424c8b))
- **[🐛 Bug Fixes]** Update .gitignore and settings for rag-rat plugin ([5069cf1](https://github.com/Ronnasayd/aipp/commit/5069cf1))
- **[🐛 Bug Fixes]** Disable tool search in headroom wrap command ([dc0ad1f](https://github.com/Ronnasayd/aipp/commit/dc0ad1f))
- **[🐛 Bug Fixes]** Replace session_start.py with start_embedding_daemon.py ([2910181](https://github.com/Ronnasayd/aipp/commit/2910181))

### **2026-07-24**

- **[🐛 Bug Fixes]** Update headroom alias and script for cleanup ([a9ffe43](https://github.com/Ronnasayd/aipp/commit/a9ffe43))
- **[✨ Features]** Add headroom start script and new alias for it ([7088aeb](https://github.com/Ronnasayd/aipp/commit/7088aeb))
- **[🐛 Bug Fixes]** Add completion message to install script ([4453f2a](https://github.com/Ronnasayd/aipp/commit/4453f2a))
- **[🐛 Bug Fixes]** Update command usage in install script for clarity ([4719d56](https://github.com/Ronnasayd/aipp/commit/4719d56))
- **[🐛 Bug Fixes]** Ensure context-refs.json symlink creation and add directory checks ([3c0f69a](https://github.com/Ronnasayd/aipp/commit/3c0f69a))
- **[🐛 Bug Fixes]** Add github_pat_token check in update-external-tools.sh ([a499916](https://github.com/Ronnasayd/aipp/commit/a499916))
- **[📚 Documentation]** Update readme.md for clarity and structure improvements ([6a53dea](https://github.com/Ronnasayd/aipp/commit/6a53dea))
- **[📚 Documentation]** Remove outdated sections from readme.md for clarity ([8317031](https://github.com/Ronnasayd/aipp/commit/8317031))
- **[🐛 Bug Fixes]** Update alias for ai context generator to 'iai' ([66762e2](https://github.com/Ronnasayd/aipp/commit/66762e2))
- **[🐛 Bug Fixes]** Add support for 'path' in file access checks ([add9637](https://github.com/Ronnasayd/aipp/commit/add9637))
- **[✨ Features]** Enhance scoring mechanism in topresults function ([937e3e2](https://github.com/Ronnasayd/aipp/commit/937e3e2))
- **[🐛 Bug Fixes]** Remove context from debug messages in hooks scripts ([b1d19cd](https://github.com/Ronnasayd/aipp/commit/b1d19cd))
- **[✨ Features]** Enhance context7 search with daemon integration ([07a9d4d](https://github.com/Ronnasayd/aipp/commit/07a9d4d))
- **[🐛 Bug Fixes]** Prevent execution if stop hook is active added a check to exit early if the 'stop_hook_active' key is present in the payload, ensuring that the script does not proceed when the hook is disabled. ([b1c6bbc](https://github.com/Ronnasayd/aipp/commit/b1c6bbc))
- **[🐛 Bug Fixes]** Remove 'context7' from disabled mcp servers list ([4c1a8bf](https://github.com/Ronnasayd/aipp/commit/4c1a8bf))
- **[✨ Features]** Add context7 search command and script ([7225269](https://github.com/Ronnasayd/aipp/commit/7225269))
- **[🐛 Bug Fixes]** Add debug logging for output in hooks scripts ([65a4206](https://github.com/Ronnasayd/aipp/commit/65a4206))
- **[✨ Features]** Add hooks for subagent guidelines and question tool enforcement ([5e94196](https://github.com/Ronnasayd/aipp/commit/5e94196))
- **[🐛 Bug Fixes]** Improve instructions for file editing rules updated the instructions to clarify the process of finding and following rules for matching file types before editing or creating files. this enhances user understanding and compliance with file handling protocols. ([7b03ee3](https://github.com/Ronnasayd/aipp/commit/7b03ee3))
- **[🐛 Bug Fixes]** Update ref path to use /tmp for non-absolute paths ([fcf783f](https://github.com/Ronnasayd/aipp/commit/fcf783f))
- **[✨ Features]** Add command to remove orphaned containers in env script ([39989ff](https://github.com/Ronnasayd/aipp/commit/39989ff))

### **2026-07-23**

- **[✨ Features]** Configure 9router models as defaults in env script ([70dfb5a](https://github.com/Ronnasayd/aipp/commit/70dfb5a))
- **[✨ Features]** Add 9router models and update environment setup ([1dd4d3a](https://github.com/Ronnasayd/aipp/commit/1dd4d3a))

### **2026-07-22**

- **[✨ Features]** Restructure figma capture skills and templates ([c9afc0f](https://github.com/Ronnasayd/aipp/commit/c9afc0f))
- **[✨ Features]** Add large file read warning hook ([697ec0c](https://github.com/Ronnasayd/aipp/commit/697ec0c))
- **[🐛 Bug Fixes]** Reduce refresh interval from 20 to 10 seconds ([c5c4189](https://github.com/Ronnasayd/aipp/commit/c5c4189))
- **[✨ Features]** Enhance context refs hook for file editing ([879eab3](https://github.com/Ronnasayd/aipp/commit/879eab3))
- **[✨ Features]** Enhance description extraction from ref files ([0a26247](https://github.com/Ronnasayd/aipp/commit/0a26247))
- **[✨ Features]** Update context refs hook to point to file locations ([d944bbd](https://github.com/Ronnasayd/aipp/commit/d944bbd))
- **[✨ Features]** Add scripts for checking and extracting ste dictionary ([c7b52e0](https://github.com/Ronnasayd/aipp/commit/c7b52e0))

### **2026-07-21**

- **[✨ Features]** Add instructions loaded hook for log processing ([a4b5fcd](https://github.com/Ronnasayd/aipp/commit/a4b5fcd))
- **[✨ Features]** Update scripts and add disable-mcps-default.py ([0d58d8d](https://github.com/Ronnasayd/aipp/commit/0d58d8d))
- **[✨ Features]** Update execution steps and tracking instructions ([3e88b0f](https://github.com/Ronnasayd/aipp/commit/3e88b0f))

### **2026-07-20**

- **[✨ Features]** Update task execution description and wave dispatch logic ([e8c9702](https://github.com/Ronnasayd/aipp/commit/e8c9702))
- **[✨ Features]** Add mutation-testing instructions for stryker analysis ([86305fe](https://github.com/Ronnasayd/aipp/commit/86305fe))
- **[✨ Features]** Update headroom proxy status icons in status line script ([5940579](https://github.com/Ronnasayd/aipp/commit/5940579))
- **[✨ Features]** Add headroom proxy status to status line script ([ec55d6b](https://github.com/Ronnasayd/aipp/commit/ec55d6b))
- **[✨ Features]** Add mutation-survivor-triage skill for stryker analysis ([9dec98a](https://github.com/Ronnasayd/aipp/commit/9dec98a))
- **[✨ Features]** Add coverage-gap-audit skill for jest test coverage analysis ([e0e6345](https://github.com/Ronnasayd/aipp/commit/e0e6345))
- **[✨ Features]** Add litellm docker setup and configuration files ([5defe1d](https://github.com/Ronnasayd/aipp/commit/5defe1d))
- **[✨ Features]** Add new aliases for headroom and token saving ([1e20ae5](https://github.com/Ronnasayd/aipp/commit/1e20ae5))
- **[✨ Features]** Add usage instructions for task tracking in skill.md added instructions on using taskcreate, taskget, tasklist, and taskupdate to track wave/task progress alongside taskmaster mcp updates. ([35df102](https://github.com/Ronnasayd/aipp/commit/35df102))

### **2026-07-18**

- **[✨ Features]** Update image-mockup-recreator skill and add overlay diff script ([af57a0d](https://github.com/Ronnasayd/aipp/commit/af57a0d))
- **[✨ Features]** Add color comparison script and update ssim thresholds ([706bc3c](https://github.com/Ronnasayd/aipp/commit/706bc3c))

### **2026-07-17**

- **[✨ Features]** Enhance logging for hooks with customizable log file ([ff57ecf](https://github.com/Ronnasayd/aipp/commit/ff57ecf))
- **[✨ Features]** Update pr review skill documentation and add examples ([ca8142c](https://github.com/Ronnasayd/aipp/commit/ca8142c))
- **[✨ Features]** Add guidelines for creating subagents in start.prompt.md ([3422241](https://github.com/Ronnasayd/aipp/commit/3422241))

### **2026-07-16**

- **[✨ Features]** Update figma-capture skill to version 1.5.0 ([91b303a](https://github.com/Ronnasayd/aipp/commit/91b303a))
- **[✨ Features]** Update figma-capture skill version to 1.4.0 ([ca4e903](https://github.com/Ronnasayd/aipp/commit/ca4e903))
- **[✨ Features]** Update figma-capture skill and add new scripts ([019e60d](https://github.com/Ronnasayd/aipp/commit/019e60d))
- **[✨ Features]** Update image-mockup-recreator skill and add examples ([8549576](https://github.com/Ronnasayd/aipp/commit/8549576))
- **[✨ Features]** Update figma-capture skill documentation and examples ([86c5f2d](https://github.com/Ronnasayd/aipp/commit/86c5f2d))
- **[✨ Features]** Update skill documentation and examples ([a7abc3a](https://github.com/Ronnasayd/aipp/commit/a7abc3a))
- **[📚 Documentation]** Update test and vue coding standards ([a588fe4](https://github.com/Ronnasayd/aipp/commit/a588fe4))

### **2026-07-15**

- **[✨ Features]** Improve instructions for file creation ([a9b5cb8](https://github.com/Ronnasayd/aipp/commit/a9b5cb8))
- **[✨ Features]** Enhance skill with references and examples ([512de81](https://github.com/Ronnasayd/aipp/commit/512de81))
- **[✨ Features]** Add compress-skill and update related documentation ([d69e438](https://github.com/Ronnasayd/aipp/commit/d69e438))
- **[🧹 Chores]** Remove obsolete rules document ([f3891b8](https://github.com/Ronnasayd/aipp/commit/f3891b8))
- **[✨ Features]** Add rules for editing and large sessions ([76a3759](https://github.com/Ronnasayd/aipp/commit/76a3759))
- **[🐛 Bug Fixes]** Remove redundant traceability footer section ([fa3ee27](https://github.com/Ronnasayd/aipp/commit/fa3ee27))
- **[✨ Features]** Add extract-automation-candidates skill ([e43b437](https://github.com/Ronnasayd/aipp/commit/e43b437))
- **[✨ Features]** Add skill and scripts for automation extraction ([bb2ae0f](https://github.com/Ronnasayd/aipp/commit/bb2ae0f))
- **[🐛 Bug Fixes]** Update applyto pattern for markdown files ([8088cb2](https://github.com/Ronnasayd/aipp/commit/8088cb2))
- **[🐛 Bug Fixes]** Correct awk condition in extract_body function ([b67cba4](https://github.com/Ronnasayd/aipp/commit/b67cba4))
- **[🐛 Bug Fixes]** Update model to haiku in settings.json ([9316f4d](https://github.com/Ronnasayd/aipp/commit/9316f4d))
- **[✨ Features]** Enhance instruction and skill linking for agents ([c1404d4](https://github.com/Ronnasayd/aipp/commit/c1404d4))

### **2026-07-14**

- **[✨ Features]** Enhance context usage reporting in status line script ([01aa8c9](https://github.com/Ronnasayd/aipp/commit/01aa8c9))
- **[🧹 Chores]** Remove disabled mcp servers from settings.json ([625c0e2](https://github.com/Ronnasayd/aipp/commit/625c0e2))
- **[✨ Features]** Enable auto compact and ensure always thinking is disabled ([687a578](https://github.com/Ronnasayd/aipp/commit/687a578))
- **[✨ Features]** Update lintfix alias to use uv run with claude-agent-sdk feat(mcp): change mcp-manager command to use uvx with git source chore(uv.lock): add uv.lock file with version and python requirements ([0c92460](https://github.com/Ronnasayd/aipp/commit/0c92460))
- **[🐛 Bug Fixes]** Update model from haiku to sonnet in settings.json docs(skill): refine description for tlc-execute-tasks-adversarial skill ([b682881](https://github.com/Ronnasayd/aipp/commit/b682881))
- **[✨ Features]** Add additional allowed file patterns for image files ([a5c3432](https://github.com/Ronnasayd/aipp/commit/a5c3432))
- **[✨ Features]** Add tlc-execute-tasks-adversarial skill and update manifest ([045da39](https://github.com/Ronnasayd/aipp/commit/045da39))
- **[✨ Features]** Remove old tlc-execute-tasks references and add adversarial execution skill ([1d9ad60](https://github.com/Ronnasayd/aipp/commit/1d9ad60))
- **[✨ Features]** Add environment variable expansion for command targets ([c5b0912](https://github.com/Ronnasayd/aipp/commit/c5b0912))
- **[♻️ Refactoring]** Enhance path normalization and pattern matching for security ([947e632](https://github.com/Ronnasayd/aipp/commit/947e632))
- **[✨ Features]** Add content-based secret scanning functionality ([57122e1](https://github.com/Ronnasayd/aipp/commit/57122e1))

### **2026-07-13**

- **[♻️ Refactoring]** Bound token cost and disable subagent commits in adversarial-dev/tlc-execute-tasks ([fc2e556](https://github.com/Ronnasayd/aipp/commit/fc2e556))
- **[♻️ Refactoring]** Reorder cross-source precedence to commits > specs > transcripts ([d380589](https://github.com/Ronnasayd/aipp/commit/d380589))
- **[✨ Features]** Add extract-software-requirements skill ([86fbe9e](https://github.com/Ronnasayd/aipp/commit/86fbe9e))
- **[♻️ Refactoring]** Add home_dir ([75f6acd](https://github.com/Ronnasayd/aipp/commit/75f6acd))
- **[✨ Features]** Add per-task executor model selection to tlc-execute-tasks ([9f62b71](https://github.com/Ronnasayd/aipp/commit/9f62b71))
- **[♻️ Refactoring]** Route tlc-execute-tasks execution through adversarial-dev ([b2e0bb4](https://github.com/Ronnasayd/aipp/commit/b2e0bb4))
- **[✨ Features]** Add adversarial-dev skill ([1482cec](https://github.com/Ronnasayd/aipp/commit/1482cec))
- **[✨ Features]** Add adversarial-dev skill for dual-agent generator/evaluator loops ([d66905a](https://github.com/Ronnasayd/aipp/commit/d66905a))

### **2026-07-12**

- **[🧹 Chores]** Register index and manifest ([7ab3707](https://github.com/Ronnasayd/aipp/commit/7ab3707))
- **[✨ Features]** Add image mockup recreator skill ([6fe8b6e](https://github.com/Ronnasayd/aipp/commit/6fe8b6e))
- **[✨ Features]** Add script to overlay pixel grid on images ([c42ab33](https://github.com/Ronnasayd/aipp/commit/c42ab33))

### **2026-07-11**

- **[♻️ Refactoring]** Add sync agents summary ([4aeb391](https://github.com/Ronnasayd/aipp/commit/4aeb391))
- **[♻️ Refactoring]** Update skills ([354a0ec](https://github.com/Ronnasayd/aipp/commit/354a0ec))
- **[♻️ Refactoring]** Change names to avoid colision ([7b6fe85](https://github.com/Ronnasayd/aipp/commit/7b6fe85))
- **[✨ Features]** Add relavant skills ([49410d9](https://github.com/Ronnasayd/aipp/commit/49410d9))
- **[♻️ Refactoring]** Update skills ignore ([56eabdb](https://github.com/Ronnasayd/aipp/commit/56eabdb))
- **[✨ Features]** Add new skills ([2886deb](https://github.com/Ronnasayd/aipp/commit/2886deb))
- **[🚧 Other Changes]** Feat:add new skills ([e6b553e](https://github.com/Ronnasayd/aipp/commit/e6b553e))
- **[🐛 Bug Fixes]** Resolve skills.db path via ai_project_dir env var ([daa3dbf](https://github.com/Ronnasayd/aipp/commit/daa3dbf))
- **[🐛 Bug Fixes]** Use absolute $ai_project_dir path for hook scripts ([623774e](https://github.com/Ronnasayd/aipp/commit/623774e))
- **[🐛 Bug Fixes]** Handle manifest entries as plain path strings ([7136b68](https://github.com/Ronnasayd/aipp/commit/7136b68))
- **[✨ Features]** Support fetching adjacent skill files ([3055bf2](https://github.com/Ronnasayd/aipp/commit/3055bf2))
- **[♻️ Refactoring]** Drop stale .agents skills path and prune index entries ([a96a128](https://github.com/Ronnasayd/aipp/commit/a96a128))

### **2026-07-10**

- **[♻️ Refactoring]** Sync external skills and improve tool script error handling ([c4b42e8](https://github.com/Ronnasayd/aipp/commit/c4b42e8))
- **[♻️ Refactoring]** Update external skills ([3c0ba5e](https://github.com/Ronnasayd/aipp/commit/3c0ba5e))
- **[🐛 Bug Fixes]** Use relative hook paths instead of $claude_project_dir ([19c9166](https://github.com/Ronnasayd/aipp/commit/19c9166))
- **[🐛 Bug Fixes]** Scope rtk permission rules by subcommand ([d9984ad](https://github.com/Ronnasayd/aipp/commit/d9984ad))
- **[🐛 Bug Fixes]** Use project root as cwd for lint-fix subagents so hooks resolve ([21cf0ef](https://github.com/Ronnasayd/aipp/commit/21cf0ef))
- **[🐛 Bug Fixes]** Use $claude_project_dir for hook script paths ([c96b3f7](https://github.com/Ronnasayd/aipp/commit/c96b3f7))
- **[✨ Features]** Load global claude settings for lint-fix subagents ([4565037](https://github.com/Ronnasayd/aipp/commit/4565037))
- **[✨ Features]** Add concurrent eslint auto-fix agent script ([e24e813](https://github.com/Ronnasayd/aipp/commit/e24e813))

### **2026-07-08**

- **[✨ Features]** Add context7 mcp server config ([945ba5d](https://github.com/Ronnasayd/aipp/commit/945ba5d))
- **[✨ Features]** Fall back to git mirror for missing context refs ([a19411d](https://github.com/Ronnasayd/aipp/commit/a19411d))
- **[♻️ Refactoring]** Move colorize_json to utils, drop regex-based coloring ([bc9c051](https://github.com/Ronnasayd/aipp/commit/bc9c051))
- **[📚 Documentation]** Rewrite frontmatter descriptions for all instruction files ([74526b8](https://github.com/Ronnasayd/aipp/commit/74526b8))

### **2026-07-07**

- **[🐛 Bug Fixes]** Scope viewer css to avoid class/tag collisions ([103f9a7](https://github.com/Ronnasayd/aipp/commit/103f9a7))
- **[✨ Features]** Add html viewer for captured figma nodes ([c149d51](https://github.com/Ronnasayd/aipp/commit/c149d51))
- **[🚧 Other Changes]** Add similar_code_ref eval suite ([b51263d](https://github.com/Ronnasayd/aipp/commit/b51263d))
- **[🚧 Other Changes]** Add context_refs eval suite ([db9bd2d](https://github.com/Ronnasayd/aipp/commit/db9bd2d))
- **[✨ Features]** Add ai-memory hooks instalation ([007e7c5](https://github.com/Ronnasayd/aipp/commit/007e7c5))
- **[🧹 Chores]** Update model preference and secure secret handling ([77f6073](https://github.com/Ronnasayd/aipp/commit/77f6073))
- **[🐛 Bug Fixes]** Harden protect_files exec/getfacl handling, tune permissions, add skill_activation evals ([11ef5d9](https://github.com/Ronnasayd/aipp/commit/11ef5d9))

### **2026-07-06**

- **[🧹 Chores]** Add eval and xargs to ask list for interactive confirmation ([d03851f](https://github.com/Ronnasayd/aipp/commit/d03851f))
- **[🧹 Chores]** Add curl and wget to ask permissions ([5b360dd](https://github.com/Ronnasayd/aipp/commit/5b360dd))
- **[🐛 Bug Fixes]** Harden protect_files with process-substitution detection ([f0bb562](https://github.com/Ronnasayd/aipp/commit/f0bb562))
- **[🐛 Bug Fixes]** Harden protect_files and deny with missing checks ([71f7e5c](https://github.com/Ronnasayd/aipp/commit/71f7e5c))
- **[✨ Features]** Add command classification and opaque-command detection ([88db1f6](https://github.com/Ronnasayd/aipp/commit/88db1f6))
- **[✨ Features]** Harden protect_files with exfil detection and interpreter sandboxing ([ae51148](https://github.com/Ronnasayd/aipp/commit/ae51148))
- **[✨ Features]** Harden protect_files with chaining, substitution, and exfil detection ([8d2bee5](https://github.com/Ronnasayd/aipp/commit/8d2bee5))
- **[✨ Features]** Add qa-specialist agent for functional testing and release qa ([4619cde](https://github.com/Ronnasayd/aipp/commit/4619cde))
- **[🧹 Chores]** Simplify hook log aliases from tail -f to cat ([8648b38](https://github.com/Ronnasayd/aipp/commit/8648b38))
- **[🧹 Chores]** Disable unused mcp servers and add hook debug aliases ([336952b](https://github.com/Ronnasayd/aipp/commit/336952b))
- **[🧹 Chores]** Remove mcp-manager instructions from agent guide ([2d4ad23](https://github.com/Ronnasayd/aipp/commit/2d4ad23))
- **[✨ Features]** Add golang lint hook ([e49de7b](https://github.com/Ronnasayd/aipp/commit/e49de7b))

### **2026-07-05**

- **[🧹 Chores]** Increase context-refs refresh interval to 20 ([65d3c93](https://github.com/Ronnasayd/aipp/commit/65d3c93))
- **[📚 Documentation]** Add python docstring instructions ([44484f7](https://github.com/Ronnasayd/aipp/commit/44484f7))
- **[🐛 Bug Fixes]** Add go support and improve multi-import extraction in similar-code-ref ([c612221](https://github.com/Ronnasayd/aipp/commit/c612221))
- **[🧹 Chores]** Add comprehensive debug logging to similar-code-ref hook ([97a7121](https://github.com/Ronnasayd/aipp/commit/97a7121))
- **[✨ Features]** Add similar-code-ref pretooluse hook ([421ed90](https://github.com/Ronnasayd/aipp/commit/421ed90))

### **2026-07-04**

- **[🧹 Chores]** Remove docker run, exec, stop from deny list ([4c963da](https://github.com/Ronnasayd/aipp/commit/4c963da))
- **[📚 Documentation]** Add mcp-manager documentation to agents.md and clarify prompt instructions ([7fb0682](https://github.com/Ronnasayd/aipp/commit/7fb0682))
- **[🧹 Chores]** Negative ([f5ebf8a](https://github.com/Ronnasayd/aipp/commit/f5ebf8a))
- **[📚 Documentation]** Add mcp-manager documentation and update code examples ([4e4b81e](https://github.com/Ronnasayd/aipp/commit/4e4b81e))
- **[🐛 Bug Fixes]** Use fixed-string grep and add missing mcp.json gitignore entry ([af32e27](https://github.com/Ronnasayd/aipp/commit/af32e27))
- **[🧹 Chores]** Add json colorization to logging and enable remote control startup ([d579742](https://github.com/Ronnasayd/aipp/commit/d579742))

### **2026-07-03**

- **[♻️ Refactoring]** Split skill doc into references ([747bcc7](https://github.com/Ronnasayd/aipp/commit/747bcc7))
- **[🧹 Chores]** Change default model to haiku and add notification settings ([9b28c16](https://github.com/Ronnasayd/aipp/commit/9b28c16))
- **[✨ Features]** Add python code standards guide ([782ceb7](https://github.com/Ronnasayd/aipp/commit/782ceb7))
- **[♻️ Refactoring]** Consolidate lint hook logic into shared utils ([0e9a6f3](https://github.com/Ronnasayd/aipp/commit/0e9a6f3))
- **[🐛 Bug Fixes]** Enable exit code signaling for jscpd duplicate detection ([4d19560](https://github.com/Ronnasayd/aipp/commit/4d19560))
- **[✨ Features]** Add jscpd duplicate code detection to lint hooks ([58078ed](https://github.com/Ronnasayd/aipp/commit/58078ed))
- **[✨ Features]** Add remote skill-loader mcp and manifest for cross-project skill activation ([c3e4b2c](https://github.com/Ronnasayd/aipp/commit/c3e4b2c))
- **[🧹 Chores]** Add scan-codebase-rules-ai-memory skill and ai memory service setup ([7a022d0](https://github.com/Ronnasayd/aipp/commit/7a022d0))
- **[📚 Documentation]** Regenerate full history through 2026-07-03 ([e0c69e6](https://github.com/Ronnasayd/aipp/commit/e0c69e6))
- **[🧹 Chores]** Pin model per prompt file ([c7b2ca5](https://github.com/Ronnasayd/aipp/commit/c7b2ca5))
- **[🐛 Bug Fixes]** Switch database mcp servers to git-hosted uvx packages ([c93821d](https://github.com/Ronnasayd/aipp/commit/c93821d))
- **[🐛 Bug Fixes]** Fix keycloak spelling and add admin credential env vars ([95f94b3](https://github.com/Ronnasayd/aipp/commit/95f94b3))
- **[🧹 Chores]** Reorganize ignore rules and add claude.md pointer ([4719102](https://github.com/Ronnasayd/aipp/commit/4719102))
- **[🐛 Bug Fixes]** Switch keycloak server to git-hosted uvx package, add gcloud server ([cf59979](https://github.com/Ronnasayd/aipp/commit/cf59979))

### **2026-07-01**

- **[🐛 Bug Fixes]** Resolve embedding daemon socket never created on cold start ([4448002](https://github.com/Ronnasayd/aipp/commit/4448002))
- **[🧹 Chores]** Update skillsignore entries and protect skill/instruction dirs ([2d76431](https://github.com/Ronnasayd/aipp/commit/2d76431))
- **[🐛 Bug Fixes]** Emit structured json suggestions instead of joined string ([3c2770c](https://github.com/Ronnasayd/aipp/commit/3c2770c))
- **[🐛 Bug Fixes]** Preserve non-ascii chars in json output ([6912d21](https://github.com/Ronnasayd/aipp/commit/6912d21))
- **[♻️ Refactoring]** Use full description as hint, activate skill-description-generator ([5059590](https://github.com/Ronnasayd/aipp/commit/5059590))
- **[📚 Documentation]** Require task* tools for multi-step progress feedback ([8487c2e](https://github.com/Ronnasayd/aipp/commit/8487c2e))
- **[📚 Documentation]** Require task* tools for multi-step progress feedback ([4bf4ef1](https://github.com/Ronnasayd/aipp/commit/4bf4ef1))
- **[✨ Features]** Copy kanban board viewer to .taskmaster on generation ([fdbeb00](https://github.com/Ronnasayd/aipp/commit/fdbeb00))
- **[✨ Features]** Add standalone kanban board viewer for tasks.json ([478a945](https://github.com/Ronnasayd/aipp/commit/478a945))
- **[🧹 Chores]** Activate general-use skills in .skillsignore ([ece83ed](https://github.com/Ronnasayd/aipp/commit/ece83ed))
- **[🐛 Bug Fixes]** Preserve unicode in generated skill/agent index.yaml files ([978eaa4](https://github.com/Ronnasayd/aipp/commit/978eaa4))
- **[🐛 Bug Fixes]** Tune skill suggestion threshold and strengthen prompt ([e903e57](https://github.com/Ronnasayd/aipp/commit/e903e57))

### **2026-06-30**

- **[✨ Features]** Add keycloak mcp server config and revert default model to sonnet ([265f690](https://github.com/Ronnasayd/aipp/commit/265f690))
- **[♻️ Refactoring]** Emphasize agents.md instructions and clean up whitespace ([3d6a567](https://github.com/Ronnasayd/aipp/commit/3d6a567))
- **[🧹 Chores]** Switch default model to haiku and begin ai-memory consolidation ([0399b9d](https://github.com/Ronnasayd/aipp/commit/0399b9d))
- **[♻️ Refactoring]** Use agents.md for instructions in install scripts ([42bb5e6](https://github.com/Ronnasayd/aipp/commit/42bb5e6))
- **[♻️ Refactoring]** Change shebangs to use /usr/bin/python3 for consistency across scripts ([845a629](https://github.com/Ronnasayd/aipp/commit/845a629))

### **2026-06-29**

- **[🧹 Chores]** Add debug logging to skill scoring and remove unused permission setting ([af2cc2e](https://github.com/Ronnasayd/aipp/commit/af2cc2e))
- **[🐛 Bug Fixes]** Ensure embeddings use float32 dtype and set default model to haiku ([eb73b4f](https://github.com/Ronnasayd/aipp/commit/eb73b4f))
- **[♻️ Refactoring]** Replace sentence_transformers with fastembed ([6563f44](https://github.com/Ronnasayd/aipp/commit/6563f44))

### **2026-06-27**

- **[🐛 Bug Fixes]** Update session start script path in settings.json ([9b6e67d](https://github.com/Ronnasayd/aipp/commit/9b6e67d))
- **[🧹 Chores]** Switch default model to haiku and adjust skill similarity threshold ([8ff3fab](https://github.com/Ronnasayd/aipp/commit/8ff3fab))
- **[♻️ Refactoring]** Split agent and docs conventions into separate files ([2f6de52](https://github.com/Ronnasayd/aipp/commit/2f6de52))

### **2026-06-26**

- **[✨ Features]** Enable parallel execution within waves via orchestrate skill ([59e0490](https://github.com/Ronnasayd/aipp/commit/59e0490))
- **[✨ Features]** Switch to multilingual sentence transformer model ([9a4b685](https://github.com/Ronnasayd/aipp/commit/9a4b685))
- **[✨ Features]** Introduce daemon for persistent model serving ([716f1ca](https://github.com/Ronnasayd/aipp/commit/716f1ca))
- **[🐛 Bug Fixes]** Tighten similarity threshold and fix gitignore path ([357f683](https://github.com/Ronnasayd/aipp/commit/357f683))
- **[✨ Features]** Expand debug logging for vector search pipeline ([2b19aa2](https://github.com/Ronnasayd/aipp/commit/2b19aa2))
- **[✨ Features]** Expand debug logging for vector search pipeline ([f28667f](https://github.com/Ronnasayd/aipp/commit/f28667f))
- **[✨ Features]** Replace keyword/regex matching with vector search ([62a6996](https://github.com/Ronnasayd/aipp/commit/62a6996))

### **2026-06-25**

- **[♻️ Refactoring]** Complete hint descriptions and simplify sync script ([c62c2a6](https://github.com/Ronnasayd/aipp/commit/c62c2a6))
- **[🧹 Chores]** Refine keywords and intent patterns for precision ([6068d57](https://github.com/Ronnasayd/aipp/commit/6068d57))
- **[✨ Features]** Add sync script to map index.yaml to skill-rules ([31f2cff](https://github.com/Ronnasayd/aipp/commit/31f2cff))
- **[🐛 Bug Fixes]** Ensure hooks.log exists before tailing in lgh alias ([9c7cfec](https://github.com/Ronnasayd/aipp/commit/9c7cfec))
- **[✨ Features]** Enhance skill activation observability ([3bfed00](https://github.com/Ronnasayd/aipp/commit/3bfed00))
- **[✨ Features]** Add skill activation hook to suggest relevant skills ([3638120](https://github.com/Ronnasayd/aipp/commit/3638120))
- **[🐛 Bug Fixes]** Date command compatibility and display formatting ([93666c1](https://github.com/Ronnasayd/aipp/commit/93666c1))

### **2026-06-24**

- **[🚧 Other Changes]** Simplify statusline display with nerd font icons and cleaner formatting ([b7fb2fb](https://github.com/Ronnasayd/aipp/commit/b7fb2fb))
- **[🐛 Bug Fixes]** Adjust context-refs.json symlink check to handle existing files ([ffc2612](https://github.com/Ronnasayd/aipp/commit/ffc2612))
- **[✨ Features]** Add codebase-linguistic-analysis skill and extend context references for test and vue files ([b1f2ae4](https://github.com/Ronnasayd/aipp/commit/b1f2ae4))
- **[✨ Features]** Add type-specific context references for js, openapi, react, and test files ([383b672](https://github.com/Ronnasayd/aipp/commit/383b672))
- **[♻️ Refactoring]** Adjust context-refs.json and update install script to symlink it ([d6ae37e](https://github.com/Ronnasayd/aipp/commit/d6ae37e))
- **[♻️ Refactoring]** Update .gitignore and context-refs.json for new rules ([f902101](https://github.com/Ronnasayd/aipp/commit/f902101))
- **[✨ Features]** Add support for multiple glob patterns in context_refs.py ([c0ecfe0](https://github.com/Ronnasayd/aipp/commit/c0ecfe0))
- **[♻️ Refactoring]** Simplify glob matching in context_refs.py ([d5260d4](https://github.com/Ronnasayd/aipp/commit/d5260d4))
- **[✨ Features]** Add context-refs hook and reorganize skills ([4c10626](https://github.com/Ronnasayd/aipp/commit/4c10626))
- **[✨ Features]** Add mattpocock engineering skills for diagnosing-bugs and domain-modeling ([071aef4](https://github.com/Ronnasayd/aipp/commit/071aef4))
- **[✨ Features]** Add grilling skill for stress-testing plans ([aae0e83](https://github.com/Ronnasayd/aipp/commit/aae0e83))
- **[♻️ Refactoring]** Add mattpocock skills and remove ignored skills ([e12435d](https://github.com/Ronnasayd/aipp/commit/e12435d))

### **2026-06-23**

- **[✨ Features]** Add analyze-comfyui-workflow-json skill ([d62c1d5](https://github.com/Ronnasayd/aipp/commit/d62c1d5))
- **[♻️ Refactoring]** Update prompts ([e6f644e](https://github.com/Ronnasayd/aipp/commit/e6f644e))
- **[♻️ Refactoring]** Update skill descriptions to use single quotes for consistency and escape apostrophes. ([b415cc4](https://github.com/Ronnasayd/aipp/commit/b415cc4))

### **2026-06-22**

- **[♻️ Refactoring]** Test coverage review skill and update settings ([9e4a8ea](https://github.com/Ronnasayd/aipp/commit/9e4a8ea))
- **[✨ Features]** Add permissions for git merge and git commit commands ([d460f6d](https://github.com/Ronnasayd/aipp/commit/d460f6d))
- **[♻️ Refactoring]** Adjust type hints and handle missing file_path in lint scripts ([d944a64](https://github.com/Ronnasayd/aipp/commit/d944a64))
- **[♻️ Refactoring]** Add logs for mypy and ruff execution results in python_lint.py ([b737f0b](https://github.com/Ronnasayd/aipp/commit/b737f0b))
- **[✨ Features]** Add python linting hook with mypy and ruff support ([bf3c2f6](https://github.com/Ronnasayd/aipp/commit/bf3c2f6))
- **[♻️ Refactoring]** Update typescript linting to use tsc-files for better performance and support for project references ([ccd3f6a](https://github.com/Ronnasayd/aipp/commit/ccd3f6a))

### **2026-06-21**

- **[♻️ Refactoring]** Use local tsc and eslint binaries in typescript lint hook ([917d922](https://github.com/Ronnasayd/aipp/commit/917d922))
- **[♻️ Refactoring]** Add --quiet flag to eslint command and simplify output data construction ([0410490](https://github.com/Ronnasayd/aipp/commit/0410490))
- **[♻️ Refactoring]** Remove .js and .jsx from linting extensions ([f530c66](https://github.com/Ronnasayd/aipp/commit/f530c66))
- **[♻️ Refactoring]** Enhance typescript and eslint hooks with detailed results and logging ([728ecfd](https://github.com/Ronnasayd/aipp/commit/728ecfd))
- **[♻️ Refactoring]** Update post-tool-use hooks and matchers in settings.json ([faadef6](https://github.com/Ronnasayd/aipp/commit/faadef6))
- **[🧹 Chores]** Updates ([89fd43e](https://github.com/Ronnasayd/aipp/commit/89fd43e))
- **[✨ Features]** Allow .claude directory access in protect_files hook ([a73d9b9](https://github.com/Ronnasayd/aipp/commit/a73d9b9))
- **[♻️ Refactoring]** Update quality gate to remove 'strict' mode and related logging ([f28eb2e](https://github.com/Ronnasayd/aipp/commit/f28eb2e))
- **[♻️ Refactoring]** Add logging hooks for subagent events ([c59ee15](https://github.com/Ronnasayd/aipp/commit/c59ee15))
- **[✨ Features]** Add logging hook for all hooks to debug and monitor their payloads ([4176ca9](https://github.com/Ronnasayd/aipp/commit/4176ca9))

### **2026-06-19**

- **[✨ Features]** Add prd-get-implicit-requirements skill for analyzing prds and identifying gaps ([f4e48d3](https://github.com/Ronnasayd/aipp/commit/f4e48d3))
- **[✨ Features]** Add clc alias for conventional commit message generation ([de198db](https://github.com/Ronnasayd/aipp/commit/de198db))
- **[♻️ Refactoring]** Improve alias comment clarity and conciseness in .ai.alias.zshrc ([7995c96](https://github.com/Ronnasayd/aipp/commit/7995c96))
- **[♻️ Refactoring]** Improve ignore file management and ai memory container handling in .ai.alias.zshrc ([caf29bb](https://github.com/Ronnasayd/aipp/commit/caf29bb))
- **[♻️ Refactoring]** Shorten alias names for better usability ([7213a04](https://github.com/Ronnasayd/aipp/commit/7213a04))
- **[✨ Features]** Add pr-review skill for systematic github pr analysis and feedback generation ([cf45a5d](https://github.com/Ronnasayd/aipp/commit/cf45a5d))

### **2026-06-18**

- **[♻️ Refactoring]** Update mcp environment variable defaults and model setting ([cfea33d](https://github.com/Ronnasayd/aipp/commit/cfea33d))

### **2026-06-17**

- **[🐛 Bug Fixes]** Handle large get_diff output in pr-review skill ([5b573fd](https://github.com/Ronnasayd/aipp/commit/5b573fd))
- **[✨ Features]** Add pr-review skill for systematic github pr evaluation ([86f3a47](https://github.com/Ronnasayd/aipp/commit/86f3a47))
- **[♻️ Refactoring]** Remove claude.md and .mcp.json from .gitignore in installation script ([4905bd0](https://github.com/Ronnasayd/aipp/commit/4905bd0))
- **[🐛 Bug Fixes]** Update taskmaster mcp calls to use set_task_status with tag parameter ([f83b61e](https://github.com/Ronnasayd/aipp/commit/f83b61e))

### **2026-06-16**

- **[🧹 Chores]** Update claude ([44ede0e](https://github.com/Ronnasayd/aipp/commit/44ede0e))
- **[🧹 Chores]** Add .mcp.json configuration for multiple mcp servers ([3daff41](https://github.com/Ronnasayd/aipp/commit/3daff41))
- **[✨ Features]** Add git command restrictions to settings.json ([a99c27b](https://github.com/Ronnasayd/aipp/commit/a99c27b))
- **[🧹 Chores]** Add attribution fields to settings.json ([8996855](https://github.com/Ronnasayd/aipp/commit/8996855))
- **[🧹 Chores]** Update .skillsignore to exclude tlc-execute-tasks skill ([5b0013e](https://github.com/Ronnasayd/aipp/commit/5b0013e))
- **[✨ Features]** Add tlc-execute-tasks skill with tag validation and task execution flow ([964ddd3](https://github.com/Ronnasayd/aipp/commit/964ddd3))
- **[✨ Features]** Add active skills, rules, and agents aliases ([23be834](https://github.com/Ronnasayd/aipp/commit/23be834))
- **[♻️ Refactoring]** Update agent context search order and formatting in docs/agent.instructions.md ([5ea3359](https://github.com/Ronnasayd/aipp/commit/5ea3359))
- **[♻️ Refactoring]** Format cost to three decimal places in status line ([fa1c379](https://github.com/Ronnasayd/aipp/commit/fa1c379))
- **[✨ Features]** Add total session cost to status line ([1400f26](https://github.com/Ronnasayd/aipp/commit/1400f26))
- **[✨ Features]** Add sort when saving ([2a9e9ec](https://github.com/Ronnasayd/aipp/commit/2a9e9ec))
- **[✨ Features]** Add search filter to ignore file manager ui ([c71f1cf](https://github.com/Ronnasayd/aipp/commit/c71f1cf))
- **[✨ Features]** Update taskmaster conversion scripts and tests ([2b3fba1](https://github.com/Ronnasayd/aipp/commit/2b3fba1))

### **2026-06-15**

- **[🧹 Chores]** Refactor gemini installation ([1878c8f](https://github.com/Ronnasayd/aipp/commit/1878c8f))
- **[🧹 Chores]** Add script to list mcp manager servers and update instructions ([97f9e99](https://github.com/Ronnasayd/aipp/commit/97f9e99))
- **[🧹 Chores]** Adjust mkdir claude instructions to avoid potential issues with symlinks and directories ([4321dc0](https://github.com/Ronnasayd/aipp/commit/4321dc0))
- **[🧹 Chores]** Update generation claude.md and gemini.md to support context-specific rules ([816db31](https://github.com/Ronnasayd/aipp/commit/816db31))
- **[✨ Features]** Process all frontmatter fields in converters ([ab8d484](https://github.com/Ronnasayd/aipp/commit/ab8d484))
- **[🧹 Chores]** Update agent instructions and node.js/typescript guidelines ([834b223](https://github.com/Ronnasayd/aipp/commit/834b223))
- **[🧹 Chores]** Add alias for claude with code execution capabilities ([4cd363c](https://github.com/Ronnasayd/aipp/commit/4cd363c))
- **[🧹 Chores]** Add plansdirectory setting to settings.json ([951e909](https://github.com/Ronnasayd/aipp/commit/951e909))
- **[✨ Features]** Add caveman mode status to status line ([40b9ee8](https://github.com/Ronnasayd/aipp/commit/40b9ee8))
- **[🧹 Chores]** Update status line script location in settings.json ([219180f](https://github.com/Ronnasayd/aipp/commit/219180f))
- **[✨ Features]** Add skill-description-generator skill with description and frontmatter, update tlc-tasks-to-taskmaster description for better trigger accuracy, and add skill-description-generator to index.yaml and .skillsignore. ([a57a4c5](https://github.com/Ronnasayd/aipp/commit/a57a4c5))
- **[✨ Features]** Add tlc-tasks-to-taskmaster skill for converting tasks.md to taskmaster format with execution metadata ([bd9f143](https://github.com/Ronnasayd/aipp/commit/bd9f143))
- **[🧹 Chores]** Update status line script with enhanced context and rate limit info ([ed2d764](https://github.com/Ronnasayd/aipp/commit/ed2d764))

### **2026-06-13**

- **[🧹 Chores]** Update .skillsignore to include prd-generator ([ce86d1a](https://github.com/Ronnasayd/aipp/commit/ce86d1a))
- **[✨ Features]** Add prd generator skill with 5-battery framework and project type patterns reference guide ([dc5fe7d](https://github.com/Ronnasayd/aipp/commit/dc5fe7d))
- **[🧹 Chores]** Update settings.json ([a0008f1](https://github.com/Ronnasayd/aipp/commit/a0008f1))
- **[🧹 Chores]** Update claude.install.sh ([2b6b2b3](https://github.com/Ronnasayd/aipp/commit/2b6b2b3))
- **[🧹 Chores]** Add ai-memory ([25e4cf1](https://github.com/Ronnasayd/aipp/commit/25e4cf1))
- **[🧹 Chores]** Add status line command script for model and context display ([f47d186](https://github.com/Ronnasayd/aipp/commit/f47d186))
- **[🧹 Chores]** Add status line command script and update settings ([e10a2fd](https://github.com/Ronnasayd/aipp/commit/e10a2fd))

### **2026-06-12**

- **[✨ Features]** Update claude settings and installation script ([37605f9](https://github.com/Ronnasayd/aipp/commit/37605f9))

### **2026-06-11**

- **[🧹 Chores]** Remove skills-lock.json during clean mode execution ([c2ed163](https://github.com/Ronnasayd/aipp/commit/c2ed163))
- **[✨ Features]** Update installation scripts to use npx for adding skills instead of curl ([a84c67d](https://github.com/Ronnasayd/aipp/commit/a84c67d))
- **[🧹 Chores]** Update .gitignore entries for caveman and cavecrew, add skills-lock.json and .agents/skills/* feat: add activate-caveman command documentation ([8e65962](https://github.com/Ronnasayd/aipp/commit/8e65962))
- **[📚 Documentation]** Clarify instructions for creating files in create-tlc-files prompt ([879dc2c](https://github.com/Ronnasayd/aipp/commit/879dc2c))
- **[✨ Features]** Add create-tlc-files command documentation ([5362dfb](https://github.com/Ronnasayd/aipp/commit/5362dfb))
- **[✨ Features]** Add task conversion script and restore orchestrate taskmaster prompt ([f76aa78](https://github.com/Ronnasayd/aipp/commit/f76aa78))

### **2026-06-10**

- **[✨ Features]** Add mcp_config.json and update installation script to manage mcp configuration ([a5d5e3b](https://github.com/Ronnasayd/aipp/commit/a5d5e3b))
- **[✨ Features]** Add antigravity backend support and clean scripts ([3b68c45](https://github.com/Ronnasayd/aipp/commit/3b68c45))
- **[📚 Documentation]** Add response style guidelines for agent interactions ([0e38632](https://github.com/Ronnasayd/aipp/commit/0e38632))
- **[🧹 Chores]** Add .sessions/* to .gitignore if not already present ([4ce19af](https://github.com/Ronnasayd/aipp/commit/4ce19af))

### **2026-06-09**

- **[🐛 Bug Fixes]** Correct condition checks for existing copilot configuration files ([c289ae9](https://github.com/Ronnasayd/aipp/commit/c289ae9))

### **2026-06-06**

- **[🧹 Chores]** Update ignore scripts to ensure all ignore files are added to .gitignore ([e3e0b12](https://github.com/Ronnasayd/aipp/commit/e3e0b12))
- **[🚧 Other Changes]** Uncomment test.instructions.md for clarity ([b7d06e6](https://github.com/Ronnasayd/aipp/commit/b7d06e6))
- **[📚 Documentation]** Update mcp-manager instructions for clarity and consistency ([b6f49cd](https://github.com/Ronnasayd/aipp/commit/b6f49cd))

### **2026-06-05**

- **[✨ Features]** Enable additional services in mcp-server-enablement.json configuration ([fd85997](https://github.com/Ronnasayd/aipp/commit/fd85997))
- **[✨ Features]** Implement replace_between function and update claude.md and gemini.md with dynamic instructions ([33800a8](https://github.com/Ronnasayd/aipp/commit/33800a8))
- **[🚧 Other Changes]** Comment out specific entries in ignore files for clarity ([c6b0368](https://github.com/Ronnasayd/aipp/commit/c6b0368))

### **2026-06-03**

- **[✨ Features]** Set asdf_nodejs_version in install script for environment configuration ([4d217b9](https://github.com/Ronnasayd/aipp/commit/4d217b9))

### **2026-06-02**

- **[✨ Features]** Update installation scripts to check for skills-lock.json before executing installation and updating .gitignore ([115e054](https://github.com/Ronnasayd/aipp/commit/115e054))
- **[✨ Features]** Add caveman installation and update .gitignore for new patterns ([24385fa](https://github.com/Ronnasayd/aipp/commit/24385fa))
- **[✨ Features]** Add new prompt files for memory management and task conversion functionalities ([0d1dc05](https://github.com/Ronnasayd/aipp/commit/0d1dc05))
- **[✨ Features]** Update ignore files to enable specified agents and rules for improved functionality ([14f65c5](https://github.com/Ronnasayd/aipp/commit/14f65c5))

### **2026-05-29**

- **[✨ Features]** Add transcript path handling in session header for improved session continuity ([0714b57](https://github.com/Ronnasayd/aipp/commit/0714b57))
- **[✨ Features]** Update configuration file copying to append missing entries instead of overwriting ([123e882](https://github.com/Ronnasayd/aipp/commit/123e882))
- **[✨ Features]** Add new skills and update agent descriptions for improved task orchestration and execution ([016d67d](https://github.com/Ronnasayd/aipp/commit/016d67d))

### **2026-05-28**

- **[✨ Features]** Add tcl-execute-tasks-by-orchestrate-taskmaster command prompt documentation ([72bb25a](https://github.com/Ronnasayd/aipp/commit/72bb25a))
- **[✨ Features]** Add new commands for task orchestration and memory management ([b4fcac1](https://github.com/Ronnasayd/aipp/commit/b4fcac1))
- **[✨ Features]** Add mcp-manager instructions for tool usage and examples ([5bdbf11](https://github.com/Ronnasayd/aipp/commit/5bdbf11))
- **[🧹 Chores]** Remove outdated command documentation and add new prompts for task management and ai setup audit ([f53a17b](https://github.com/Ronnasayd/aipp/commit/f53a17b))
- **[✨ Features]** Add new command prompts for task conversion and simulation ([598c087](https://github.com/Ronnasayd/aipp/commit/598c087))

### **2026-05-26**

- **[🐛 Bug Fixes]** Update .skillsignore and skill.md for task delegation clarity ([26c7cce](https://github.com/Ronnasayd/aipp/commit/26c7cce))
- **[✨ Features]** Add orchestrate to skills ignore list ([297009e](https://github.com/Ronnasayd/aipp/commit/297009e))
- **[✨ Features]** Add orchestrate skill documentation for task coordination and execution strategy ([e73d777](https://github.com/Ronnasayd/aipp/commit/e73d777))
- **[🐛 Bug Fixes]** Update .gitignore entries to include wildcard patterns for skills, commands, instructions, agents, and hooks ([74edca5](https://github.com/Ronnasayd/aipp/commit/74edca5))
- **[✨ Features]** Add orchestrate command documentation for task coordination and execution strategy ([2bd9a10](https://github.com/Ronnasayd/aipp/commit/2bd9a10))
- **[🐛 Bug Fixes]** Correct skill-architect entry to skill-specialist in .agentsignore ([2e461a7](https://github.com/Ronnasayd/aipp/commit/2e461a7))
- **[🐛 Bug Fixes]** Update agent description and instructions for clarity and accuracy ([14247e5](https://github.com/Ronnasayd/aipp/commit/14247e5))
- **[✨ Features]** Add openapi instructions for creating *.openapi.ts files ([3f3cb36](https://github.com/Ronnasayd/aipp/commit/3f3cb36))
- **[✨ Features]** Add comprehensive documentation for claude code hooks ([af7ebef](https://github.com/Ronnasayd/aipp/commit/af7ebef))
- **[🚧 Other Changes]** Fix formatting by removing trailing commas in function parameters and object literals ([d279f13](https://github.com/Ronnasayd/aipp/commit/d279f13))

### **2026-05-25**

- **[🐛 Bug Fixes]** Update cleanignore alias to remove all ignore files and refine jsdoc applyto patterns ([ad6246d](https://github.com/Ronnasayd/aipp/commit/ad6246d))
- **[🚧 Other Changes]** Fix formatting by adding missing commas in function parameters and object literals ([456ec34](https://github.com/Ronnasayd/aipp/commit/456ec34))
- **[✨ Features]** Add jsdocs instructions and update task documentation for clarity ([52be539](https://github.com/Ronnasayd/aipp/commit/52be539))

### **2026-05-22**

- **[✨ Features]** Add output tag resolution step to tlc-tasks-to-taskmaster skill documentation ([b611a5b](https://github.com/Ronnasayd/aipp/commit/b611a5b))
- **[✨ Features]** Add tasks-md-to-taskmaster-json skill for converting tasks.md to taskmaster format ([cf22525](https://github.com/Ronnasayd/aipp/commit/cf22525))
- **[✨ Features]** Add tlc-tasks-to-taskmaster skill and update related documentation ([080a8eb](https://github.com/Ronnasayd/aipp/commit/080a8eb))
- **[🧹 Chores]** Remove unused aliases for ignore and ai context cleanup ([97b334a](https://github.com/Ronnasayd/aipp/commit/97b334a))
- **[🧹 Chores]** Update file permissions for clean scripts to executable ([699e2c2](https://github.com/Ronnasayd/aipp/commit/699e2c2))
- **[✨ Features]** Add clean functionality for install scripts to remove symlinks ([7ccd56c](https://github.com/Ronnasayd/aipp/commit/7ccd56c))

### **2026-05-21**

- **[🧹 Chores]** Update .skillsignore to reorganize skills and remove commented entries ([8fb4905](https://github.com/Ronnasayd/aipp/commit/8fb4905))
- **[✨ Features]** Add figma-capture skill to capture screenshots and jsx from figma nodes ([6ddcbd0](https://github.com/Ronnasayd/aipp/commit/6ddcbd0))
- **[♻️ Refactoring]** Streamline symlink management for skills, commands, hooks, and agents in installation scripts ([301f11e](https://github.com/Ronnasayd/aipp/commit/301f11e))
- **[🧹 Chores]** Update symlink management for skills, prompts, hooks, agents, and instructions in copilot installation script ([814c818](https://github.com/Ronnasayd/aipp/commit/814c818))
- **[✨ Features]** Enable modular-monolith-decomposer in skills ignore list ([1699da1](https://github.com/Ronnasayd/aipp/commit/1699da1))
- **[✨ Features]** Add modular monolith decomposer skill and folder structure rules documentation ([06be7a2](https://github.com/Ronnasayd/aipp/commit/06be7a2))
- **[📚 Documentation]** Improve formatting and clarity in documentation sections for srs and task generation steps ([fc92d04](https://github.com/Ronnasayd/aipp/commit/fc92d04))

### **2026-05-20**

- **[📚 Documentation]** Remove context section from code instructions to clarify scope of rules ([2c476ec](https://github.com/Ronnasayd/aipp/commit/2c476ec))
- **[📚 Documentation]** Update agent behavior documentation; simplify descriptions and enhance clarity on interactive question tools ([223701e](https://github.com/Ronnasayd/aipp/commit/223701e))
- **[✨ Features]** Update documentation for agent behavior, http api, node.js/typescript, react, and vue standards; remove outdated reactjs instructions ([67d46e0](https://github.com/Ronnasayd/aipp/commit/67d46e0))
- **[✨ Features]** Add rules management to ignore file manager ([c40c93b](https://github.com/Ronnasayd/aipp/commit/c40c93b))
- **[✨ Features]** Add .rulesignore file and update scripts to handle rules ignoring ([2371fbd](https://github.com/Ronnasayd/aipp/commit/2371fbd))
- **[✨ Features]** Add vuejs 3 development instructions and best practices documentation ([e8a0955](https://github.com/Ronnasayd/aipp/commit/e8a0955))
- **[✨ Features]** Add additional rules for vue code standards and split complex computed properties into simpler ones ([a6364df](https://github.com/Ronnasayd/aipp/commit/a6364df))
- **[✨ Features]** Add rules for code standards in vue_rules_prompt.md ([0ac19e2](https://github.com/Ronnasayd/aipp/commit/0ac19e2))
- **[✨ Features]** Add initial rules for code standards in react_rules_prompt.md ([a890f6e](https://github.com/Ronnasayd/aipp/commit/a890f6e))

### **2026-05-19**

- **[✨ Features]** Remove command for protecting sensitive files from hooks ([bdd0826](https://github.com/Ronnasayd/aipp/commit/bdd0826))
- **[📚 Documentation]** Refine documentation on context search directories for clarity and order ([c478897](https://github.com/Ronnasayd/aipp/commit/c478897))
- **[✨ Features]** Update documentation skill version and refine documentation file references ([f66c7b6](https://github.com/Ronnasayd/aipp/commit/f66c7b6))
- **[✨ Features]** Enhance documentation templates with new sections for models and endpoints ([c9e994e](https://github.com/Ronnasayd/aipp/commit/c9e994e))
- **[✨ Features]** Update module context documentation template and enhance versioning ([bc7ad2f](https://github.com/Ronnasayd/aipp/commit/bc7ad2f))
- **[✨ Features]** Add documentation templates for project structure and guidelines ([b16a1be](https://github.com/Ronnasayd/aipp/commit/b16a1be))
- **[📚 Documentation]** Update code standards with comprehensive guidelines for naming conventions, function structure, and readability ([1754172](https://github.com/Ronnasayd/aipp/commit/1754172))
- **[✨ Features]** Add new command to protect sensitive files and enhance code modification guidelines ([04968c7](https://github.com/Ronnasayd/aipp/commit/04968c7))
- **[📚 Documentation]** Add typescript coding guidelines and best practices ([5d4d41c](https://github.com/Ronnasayd/aipp/commit/5d4d41c))
- **[📚 Documentation]** Add comprehensive guidelines for code standards, http api standards, react standards, and testing practices ([494d378](https://github.com/Ronnasayd/aipp/commit/494d378))
- **[♻️ Refactoring]** Rename technical-decision-maker to technical-decision-helper across documentation and skills ([b6e3f9a](https://github.com/Ronnasayd/aipp/commit/b6e3f9a))
- **[🧹 Chores]** Add cleanignore alias to remove ignore files ([10a81f0](https://github.com/Ronnasayd/aipp/commit/10a81f0))
- **[📚 Documentation]** Enhance interaction rules for using interactive question tools ([be5b85d](https://github.com/Ronnasayd/aipp/commit/be5b85d))
- **[📚 Documentation]** Enhance interaction rules for technical decision-making process ([118e4ac](https://github.com/Ronnasayd/aipp/commit/118e4ac))

### **2026-05-18**

- **[♻️ Refactoring]** Consolidate figma server entries in configuration files ([21c6cb8](https://github.com/Ronnasayd/aipp/commit/21c6cb8))
- **[♻️ Refactoring]** Consolidate atlassian server entries in configuration files ([da4f8ad](https://github.com/Ronnasayd/aipp/commit/da4f8ad))
- **[📚 Documentation]** Update wording for clarity in skills discovery documentation ([193b33f](https://github.com/Ronnasayd/aipp/commit/193b33f))
- **[✨ Features]** Add skills-discovery skill with detailed description and update .skillsignore ([75d4926](https://github.com/Ronnasayd/aipp/commit/75d4926))
- **[🧹 Chores]** Remove empty code change entries from the changes log ([0053946](https://github.com/Ronnasayd/aipp/commit/0053946))
- **[✨ Features]** Add seo and subagent creator skills with comprehensive guidelines and best practices ([0aed118](https://github.com/Ronnasayd/aipp/commit/0aed118))
- **[✨ Features]** Update .agentsignore and .skillsignore to include and reorganize agent and skill entries ([4bb4b71](https://github.com/Ronnasayd/aipp/commit/4bb4b71))
- **[✨ Features]** Update .agentsignore to include file extensions for agent specifications ([e6fb5af](https://github.com/Ronnasayd/aipp/commit/e6fb5af))
- **[✨ Features]** Reorganize .agentsignore and .skillsignore files, add new skills, and remove obsolete entries ([83b46ef](https://github.com/Ronnasayd/aipp/commit/83b46ef))
- **[✨ Features]** Enable plan in settings and add agents overrides section ([e4c4275](https://github.com/Ronnasayd/aipp/commit/e4c4275))
- **[✨ Features]** Update mcp server configurations to include new figma and github entries with distinct labels ([b6f13b1](https://github.com/Ronnasayd/aipp/commit/b6f13b1))
- **[✨ Features]** Add metadata section to multiple skill.md files and remove prompt-optimizer skill ([fdd489a](https://github.com/Ronnasayd/aipp/commit/fdd489a))
- **[✨ Features]** Add rendering and validation scripts for mermaid diagrams ([06cc5ab](https://github.com/Ronnasayd/aipp/commit/06cc5ab))
- **[🚧 Other Changes]** Update .skillsignore to uncomment tlc-spec-driven entry ([b9de09e](https://github.com/Ronnasayd/aipp/commit/b9de09e))
- **[✨ Features]** Add detailed methodologies for research and plan phases, including migration patterns and testing strategies ([1a8e86d](https://github.com/Ronnasayd/aipp/commit/1a8e86d))
- **[✨ Features]** Enhance gghget script with sha1 comparison and improved error handling for github api calls ([c902ec9](https://github.com/Ronnasayd/aipp/commit/c902ec9))
- **[✨ Features]** Add project initialization, quick mode, roadmap creation, session handoff, specification, state management, task breakdown, and validation processes ([2a9e2d6](https://github.com/Ronnasayd/aipp/commit/2a9e2d6))

### **2026-05-17**

- **[✨ Features]** Add comprehensive documentation for database migrations, deployment patterns, docker best practices, and regex vs llm structured text parsing ([94fc90e](https://github.com/Ronnasayd/aipp/commit/94fc90e))
- **[✨ Features]** Add comprehensive documentation for database migrations, deployment patterns, docker patterns, and regex vs llm structured text parsing ([82d19ee](https://github.com/Ronnasayd/aipp/commit/82d19ee))
- **[✨ Features]** Add api design patterns and guidelines, including resource naming, status codes, pagination, filtering, error responses, versioning, and rate limiting for production apis; introduce agent harness construction and ai regression testing strategies ([c044376](https://github.com/Ronnasayd/aipp/commit/c044376))
- **[✨ Features]** Add python mcp server implementation guide and evaluation scripts ([67338ee](https://github.com/Ronnasayd/aipp/commit/67338ee))
- **[✨ Features]** Add skill evaluation and improvement scripts ([82caa9f](https://github.com/Ronnasayd/aipp/commit/82caa9f))
- **[🧹 Chores]** Update vendoring instructions for skill.md to reflect correct file path ([c7e345f](https://github.com/Ronnasayd/aipp/commit/c7e345f))
- **[✨ Features]** Add tdd and test coverage review skills for enhanced testing practices ([9bdfa42](https://github.com/Ronnasayd/aipp/commit/9bdfa42))
- **[✨ Features]** Implement structured framework for resolving git merge conflicts ([720a946](https://github.com/Ronnasayd/aipp/commit/720a946))
- **[✨ Features]** Rename deep-research skill to deep-research-web and update .skillsignore ([8193a8f](https://github.com/Ronnasayd/aipp/commit/8193a8f))
- **[🧹 Chores]** Update .skillsignore to include git-guide for improved skill management ([9785f1d](https://github.com/Ronnasayd/aipp/commit/9785f1d))
- **[✨ Features]** Add new taskmaster skills for task management and validation ([9a88687](https://github.com/Ronnasayd/aipp/commit/9a88687))
- **[✨ Features]** Add figma-to-code agentic skill for automated design-to-development handoff ([222a639](https://github.com/Ronnasayd/aipp/commit/222a639))
- **[✨ Features]** Add skill architecture references and validation scripts ([b8f81bb](https://github.com/Ronnasayd/aipp/commit/b8f81bb))
- **[✨ Features]** Add skill-architect to .skillsignore for improved skill management ([fb0b415](https://github.com/Ronnasayd/aipp/commit/fb0b415))
- **[✨ Features]** Add skill-architect to .skillsignore and update external tools script for skill management ([0bea538](https://github.com/Ronnasayd/aipp/commit/0bea538))
- **[✨ Features]** Add skill architecture references and validation scripts ([5d28ab9](https://github.com/Ronnasayd/aipp/commit/5d28ab9))

### **2026-05-16**

- **[✨ Features]** Add prd-from-codebase to .skillsignore for improved skill management ([5c7c20e](https://github.com/Ronnasayd/aipp/commit/5c7c20e))
- **[✨ Features]** Add prd generation skill and stack hints reference for improved documentation ([4855d7d](https://github.com/Ronnasayd/aipp/commit/4855d7d))
- **[♻️ Refactoring]** Update script paths in skill.md and handle-deleted-modified.sh for consistency ([2bb9bb5](https://github.com/Ronnasayd/aipp/commit/2bb9bb5))
- **[♻️ Refactoring]** Uncomment specialists in .agentsignore for improved visibility ([bbe5eae](https://github.com/Ronnasayd/aipp/commit/bbe5eae))
- **[♻️ Refactoring]** Update exit menu option from '0' to 'q' for consistency ([de4773f](https://github.com/Ronnasayd/aipp/commit/de4773f))
- **[♻️ Refactoring]** Uncomment skills in .skillsignore for better visibility ([ab853ac](https://github.com/Ronnasayd/aipp/commit/ab853ac))
- **[♻️ Refactoring]** Comment out echo statements for removed skills and agents in ignores.sh ([cb8d6f0](https://github.com/Ronnasayd/aipp/commit/cb8d6f0))
- **[♻️ Refactoring]** Reorganize .skillsignore entries and update comments in manage-ignore-files.py for clarity ([9967cc6](https://github.com/Ronnasayd/aipp/commit/9967cc6))
- **[♻️ Refactoring]** Update .skillsignore to toggle comments for better organization ([201484a](https://github.com/Ronnasayd/aipp/commit/201484a))
- **[♻️ Refactoring]** Clarify comments and logic in ignore file processing ([571e1fa](https://github.com/Ronnasayd/aipp/commit/571e1fa))
- **[✨ Features]** Update .skillsignore to enable specific skills and remove comments ([303a6f0](https://github.com/Ronnasayd/aipp/commit/303a6f0))
- **[✨ Features]** Add alias for managing ignore files in .ai.alias.zshrc ([1e8638d](https://github.com/Ronnasayd/aipp/commit/1e8638d))
- **[✨ Features]** Add symlink for manage-ignore-files script in install.sh and update workspace root resolution in manage-ignore-files.py ([d5d8f9e](https://github.com/Ronnasayd/aipp/commit/d5d8f9e))
- **[✨ Features]** Add interactive script for managing .skillsignore and .agentsignore files ([5323120](https://github.com/Ronnasayd/aipp/commit/5323120))

### **2026-05-13**

- **[✨ Features]** Add skill-advisor documentation and update .skillsignore ([e504c95](https://github.com/Ronnasayd/aipp/commit/e504c95))
- **[🧹 Chores]** Remove evals.json files for document summarizer, requirements screen mapper, figma to code agentic, and tailwind config conformance skills ([4c7d7eb](https://github.com/Ronnasayd/aipp/commit/4c7d7eb))
- **[✨ Features]** Add event-storming skill documentation and ignore file entry ([087a705](https://github.com/Ronnasayd/aipp/commit/087a705))
- **[✨ Features]** Enhance install script with argument parsing and help display ([65aa8a8](https://github.com/Ronnasayd/aipp/commit/65aa8a8))
- **[♻️ Refactoring]** Improve cleanai alias for better readability and maintainability ([ccaa0ae](https://github.com/Ronnasayd/aipp/commit/ccaa0ae))
- **[✨ Features]** Enable claude installation script in the setup process ([562d27a](https://github.com/Ronnasayd/aipp/commit/562d27a))

### **2026-05-12**

- **[✨ Features]** Enhance figma requirements conformance skill with detailed design context and reporting structure ([5842b4d](https://github.com/Ronnasayd/aipp/commit/5842b4d))
- **[🧹 Chores]** Update changelog for version 2026.05.12 with recent features and fixes ([c21c96d](https://github.com/Ronnasayd/aipp/commit/c21c96d))
- **[✨ Features]** Add figma requirements screen mapper skill and evaluation prompts ([070418a](https://github.com/Ronnasayd/aipp/commit/070418a))
- **[✨ Features]** Add figma requirements conformance skill and evaluation prompts ([99139f7](https://github.com/Ronnasayd/aipp/commit/99139f7))
- **[✨ Features]** Add dynamic programming analysis skill for structured problem-solving ([45afee9](https://github.com/Ronnasayd/aipp/commit/45afee9))

### **2026-05-08**

- **[✨ Features]** Add cleanai alias for removing all ai contexts and configurations ([8dd3c70](https://github.com/Ronnasayd/aipp/commit/8dd3c70))
- **[✨ Features]** Update initai alias to use absolute path and add symlink creation in install script ([27bba6a](https://github.com/Ronnasayd/aipp/commit/27bba6a))
- **[✨ Features]** Update session file naming to include time for better uniqueness ([f750683](https://github.com/Ronnasayd/aipp/commit/f750683))
- **[🐛 Bug Fixes]** Update .skillsignore to include apk in ignored skills ([b21249b](https://github.com/Ronnasayd/aipp/commit/b21249b))
- **[✨ Features]** Add apk reverse engineering skill and analysis script with detailed reporting ([ccc25d8](https://github.com/Ronnasayd/aipp/commit/ccc25d8))

### **2026-05-07**

- **[🐛 Bug Fixes]** Correct markdown syntax in documentation for clarity and consistency ([2ef4a14](https://github.com/Ronnasayd/aipp/commit/2ef4a14))

### **2026-05-05**

- **[✨ Features]** Add integration-testing to .skillsignore ([ee31141](https://github.com/Ronnasayd/aipp/commit/ee31141))
- **[✨ Features]** Add integration testing skill with comprehensive guidance and approaches ([9535a42](https://github.com/Ronnasayd/aipp/commit/9535a42))
- **[✨ Features]** Add initai alias for executing ai-generated context commands ([7155a8a](https://github.com/Ronnasayd/aipp/commit/7155a8a))
- **[✨ Features]** Update alias to reloadignore for removing .skillsignore and .agentsignore files ([0838f41](https://github.com/Ronnasayd/aipp/commit/0838f41))
- **[✨ Features]** Add alias for removing .skillsignore and .agentsignore files ([5e7d4f9](https://github.com/Ronnasayd/aipp/commit/5e7d4f9))
- **[✨ Features]** Add mermaid class diagram and erd skills for visualizing relationships ([a08481f](https://github.com/Ronnasayd/aipp/commit/a08481f))

### **2026-05-04**

- **[🧹 Chores]** Update model version in linter_solver to claude-haiku-4.5 ([406b5f9](https://github.com/Ronnasayd/aipp/commit/406b5f9))

### **2026-05-03**

- **[✨ Features]** Add opencv skill for image and video processing reference ([0fe74d2](https://github.com/Ronnasayd/aipp/commit/0fe74d2))

### **2026-04-29**

- **[✨ Features]** Add leet-code patterns skill for coding interview preparation ([9389c63](https://github.com/Ronnasayd/aipp/commit/9389c63))

### **2026-04-28**

- **[🚧 Other Changes]** Enhance output formatting with color for linter messages ([5d59c2b](https://github.com/Ronnasayd/aipp/commit/5d59c2b))
- **[🐛 Bug Fixes]** Improve directory and file handling in main function of linter_solver ([8aaa560](https://github.com/Ronnasayd/aipp/commit/8aaa560))
- **[🐛 Bug Fixes]** Add linter command output logging in run_linter function ([a7d9f33](https://github.com/Ronnasayd/aipp/commit/a7d9f33))
- **[🐛 Bug Fixes]** Enhance linter error fixing process by including command verification in fix_linter_errors ([8b327db](https://github.com/Ronnasayd/aipp/commit/8b327db))
- **[🐛 Bug Fixes]** Simplify linter error fix prompt and remove unnecessary file write ([fcca653](https://github.com/Ronnasayd/aipp/commit/fcca653))
- **[✨ Features]** Enhance context bar display and improve event handling in linter session ([94b5172](https://github.com/Ronnasayd/aipp/commit/94b5172))
- **[🐛 Bug Fixes]** Correct event subscription handling in fix_linter_errors function ([1f60573](https://github.com/Ronnasayd/aipp/commit/1f60573))
- **[🚧 Other Changes]** Fix formatting and variable assignment in linter_solver.py fix: update key names in config.json for consistency ([2b83615](https://github.com/Ronnasayd/aipp/commit/2b83615))
- **[✨ Features]** Add linter auto-fix script using github copilot python sdk ([bc3674a](https://github.com/Ronnasayd/aipp/commit/bc3674a))
- **[✨ Features]** Add copilot-sdk to .skillsignore for improved skill management ([a4142ef](https://github.com/Ronnasayd/aipp/commit/a4142ef))
- **[✨ Features]** Add copilot-sdk skill documentation for python applications using github copilot ([0b72f83](https://github.com/Ronnasayd/aipp/commit/0b72f83))
- **[✨ Features]** Add python sdk skill documentation for github copilot integration and update .skillsignore ([93d7c06](https://github.com/Ronnasayd/aipp/commit/93d7c06))

### **2026-04-20**

- **[🐛 Bug Fixes]** Update tool reference for fetching task definition in execute-task skill ([5fe0bae](https://github.com/Ronnasayd/aipp/commit/5fe0bae))
- **[✨ Features]** Add taskmaster-mapper skill to enrich tasks with suggested skills and agents ([400f7f2](https://github.com/Ronnasayd/aipp/commit/400f7f2))

### **2026-04-17**

- **[✨ Features]** Update config.json keys for consistency and add github-copilot-sdk to requirements ([8ab6760](https://github.com/Ronnasayd/aipp/commit/8ab6760))
- **[✨ Features]** Add config.json for github copilot configuration and update installation script ([413dd7b](https://github.com/Ronnasayd/aipp/commit/413dd7b))
- **[🧹 Chores]** Remove input prompts and update environment variable references in mcp-config.json ([2971fed](https://github.com/Ronnasayd/aipp/commit/2971fed))
- **[✨ Features]** Add mcp-config.json for github copilot configuration ([6be95ed](https://github.com/Ronnasayd/aipp/commit/6be95ed))
- **[✨ Features]** Enhance taskmaster-prd-generator skill description and usage scenarios ([032eded](https://github.com/Ronnasayd/aipp/commit/032eded))
- **[✨ Features]** Add srs-generator skill for generating software requirements specification documents ([9f5da3f](https://github.com/Ronnasayd/aipp/commit/9f5da3f))
- **[🧹 Chores]** Update date format in documentation and skills to yyyy-mm-dd ([d739bd3](https://github.com/Ronnasayd/aipp/commit/d739bd3))

### **2026-04-16**

- **[✨ Features]** Add design-image-diff skill for comparing design and implementation visuals ([57074a7](https://github.com/Ronnasayd/aipp/commit/57074a7))

### **2026-04-14**

- **[🧹 Chores]** Remove unused burp server configuration from vscode.mcp.json ([4e7c1c2](https://github.com/Ronnasayd/aipp/commit/4e7c1c2))
- **[🧹 Chores]** Add keycloack to skillsignore for improved skill management ([db1c1e3](https://github.com/Ronnasayd/aipp/commit/db1c1e3))
- **[✨ Features]** Add keycloak documentation index skill for structured navigation and reference ([46ca745](https://github.com/Ronnasayd/aipp/commit/46ca745))

### **2026-04-10**

- **[🧹 Chores]** Add safe-refactor skill for structured code refactoring guidance ([cf06ed9](https://github.com/Ronnasayd/aipp/commit/cf06ed9))
- **[♻️ Refactoring]** Update command execution for mcp-manager and database types to use uvx ([c068845](https://github.com/Ronnasayd/aipp/commit/c068845))
- **[♻️ Refactoring]** Update command execution for postgresql, mysql, and sqlite to use uvx ([8b1e032](https://github.com/Ronnasayd/aipp/commit/8b1e032))
- **[🧹 Chores]** Update project structure and remove unused code ([7c15bdf](https://github.com/Ronnasayd/aipp/commit/7c15bdf))
- **[🧹 Chores]** Remove psycopg2 dependency from pyproject.toml ([8e61ce9](https://github.com/Ronnasayd/aipp/commit/8e61ce9))
- **[🧹 Chores]** Add mysql-connector-python and psycopg2 dependencies in pyproject.toml ([d77fbf8](https://github.com/Ronnasayd/aipp/commit/d77fbf8))
- **[✨ Features]** Update mongodb command and refactor main execution in mcp scripts ([a1eeb00](https://github.com/Ronnasayd/aipp/commit/a1eeb00))
- **[♻️ Refactoring]** Encapsulate main execution logic in a separate function ([66b1933](https://github.com/Ronnasayd/aipp/commit/66b1933))
- **[🧹 Chores]** Uncomment dependencies in pyproject.toml for clarity and consistency ([1b92773](https://github.com/Ronnasayd/aipp/commit/1b92773))
- **[🐛 Bug Fixes]** Remove unnecessary 'from' attribute in package configuration for clarity ([75593d8](https://github.com/Ronnasayd/aipp/commit/75593d8))
- **[🧹 Chores]** Comment out dependencies in pyproject.toml for clarity and consistency ([8affc67](https://github.com/Ronnasayd/aipp/commit/8affc67))
- **[🧹 Chores]** Uncomment dependencies in pyproject.toml for clarity and consistency ([d6b66f7](https://github.com/Ronnasayd/aipp/commit/d6b66f7))
- **[🧹 Chores]** Comment out unused dependencies in pyproject.toml for clarity ([b57884b](https://github.com/Ronnasayd/aipp/commit/b57884b))
- **[✨ Features]** Update package configuration in pyproject.toml for correct module inclusion ([582fcc1](https://github.com/Ronnasayd/aipp/commit/582fcc1))
- **[✨ Features]** Update mcp-manager command to use uvx and add git source configuration ([d484c90](https://github.com/Ronnasayd/aipp/commit/d484c90))
- **[✨ Features]** Replace protect_files.py with strategic compact suggester for improved tool usage management ([f5d59ed](https://github.com/Ronnasayd/aipp/commit/f5d59ed))
- **[✨ Features]** Add session cleanup functionality to main process for better resource management ([0531334](https://github.com/Ronnasayd/aipp/commit/0531334))
- **[✨ Features]** Enhance protect_files.py with improved pattern matching and project boundary checks ([6020ed6](https://github.com/Ronnasayd/aipp/commit/6020ed6))

### **2026-04-09**

- **[✨ Features]** Add new html files for agent and skill mapping documentation ([9bb77fd](https://github.com/Ronnasayd/aipp/commit/9bb77fd))
- **[✨ Features]** Add script to list agent and skill names and descriptions from markdown files ([c3de739](https://github.com/Ronnasayd/aipp/commit/c3de739))
- **[🧹 Chores]** Add task verification guidelines to agent instructions for improved task management ([89ec615](https://github.com/Ronnasayd/aipp/commit/89ec615))
- **[🧹 Chores]** Comment out unused skills in .skillsignore for better organization ([64fc5d1](https://github.com/Ronnasayd/aipp/commit/64fc5d1))
- **[🧹 Chores]** Reorganize and enhance .agentsignore and .skillsignore for improved structure and clarity ([1f12161](https://github.com/Ronnasayd/aipp/commit/1f12161))
- **[🧹 Chores]** Reorganize .skillsignore for better structure and clarity ([8dac6b7](https://github.com/Ronnasayd/aipp/commit/8dac6b7))
- **[🧹 Chores]** Update .skillsignore to include taskmaster, tdd, generate-docs, and resolve-conflicts ([0a778ed](https://github.com/Ronnasayd/aipp/commit/0a778ed))
- **[📚 Documentation]** Enhance skill.md by clarifying question types and improving structure for prd generation ([56135c7](https://github.com/Ronnasayd/aipp/commit/56135c7))
- **[📚 Documentation]** Update default num_tasks from 5 to 10 in skill.md ([9aae4b0](https://github.com/Ronnasayd/aipp/commit/9aae4b0))
- **[🧹 Chores]** Update .gitignore and .skillsignore, remove deprecated taskmaster scripts, and enhance skill.md documentation ([682d1d2](https://github.com/Ronnasayd/aipp/commit/682d1d2))

### **2026-04-08**

- **[🐛 Bug Fixes]** Ensure .agentsignore and .skillsignore are added to .gitignore if not present ([f6dffa0](https://github.com/Ronnasayd/aipp/commit/f6dffa0))

### **2026-04-07**

- **[🐛 Bug Fixes]** Lower ssim threshold from 0.95 to 0.9 across documentation and scripts ([a0cd8ad](https://github.com/Ronnasayd/aipp/commit/a0cd8ad))
- **[🐛 Bug Fixes]** Ensure correct data types for ssim_score and is_match in comparisonresult ([801e516](https://github.com/Ronnasayd/aipp/commit/801e516))
- **[🚧 Other Changes]** Format code for improved readability and consistency ([45af9cc](https://github.com/Ronnasayd/aipp/commit/45af9cc))
- **[✨ Features]** Enhance agentic loop with session management and logging capabilities ([99f281f](https://github.com/Ronnasayd/aipp/commit/99f281f))
- **[🐛 Bug Fixes]** Ensure .skillsignore is copied only if it doesn't exist ([895427f](https://github.com/Ronnasayd/aipp/commit/895427f))
- **[🐛 Bug Fixes]** Ensure .agentsignore is copied only if it doesn't exist ([796b08a](https://github.com/Ronnasayd/aipp/commit/796b08a))
- **[✨ Features]** Add figma-to-code-agentic skill with quick start guide, readme, and evaluation scripts ([91e2c67](https://github.com/Ronnasayd/aipp/commit/91e2c67))

### **2026-04-02**

- **[🐛 Bug Fixes]** Update log size limit to prevent log flooding ([a89f4ff](https://github.com/Ronnasayd/aipp/commit/a89f4ff))

### **2026-04-01**

- **[✨ Features]** Add conflict resolution skills and supporting scripts for handling merge conflicts ([3025447](https://github.com/Ronnasayd/aipp/commit/3025447))
- **[🐛 Bug Fixes]** Increase log size limit to prevent log flooding ([a27d54b](https://github.com/Ronnasayd/aipp/commit/a27d54b))
- **[🐛 Bug Fixes]** Increase log size limit and update regex for attachment parsing ([1be6d30](https://github.com/Ronnasayd/aipp/commit/1be6d30))
- **[🐛 Bug Fixes]** Limit logged request and response body sizes to improve performance and prevent excessive logging ([71f2f53](https://github.com/Ronnasayd/aipp/commit/71f2f53))
- **[🧹 Chores]** Remove commented-out rtk instructions from claude.install.sh ([407724f](https://github.com/Ronnasayd/aipp/commit/407724f))
- **[🧹 Chores]** Comment out rtk instructions generation in claude.install.sh ([0b38da0](https://github.com/Ronnasayd/aipp/commit/0b38da0))
- **[✨ Features]** Update .gitignore and installation script to include commands directory and streamline hooks configuration ([63e9a00](https://github.com/Ronnasayd/aipp/commit/63e9a00))
- **[🐛 Bug Fixes]** Update instruction paths in claude.install.sh to correct directory references ([836ac25](https://github.com/Ronnasayd/aipp/commit/836ac25))
- **[✨ Features]** Add settings.local.json for configuration and update installation script to link it ([a4591a0](https://github.com/Ronnasayd/aipp/commit/a4591a0))
- **[✨ Features]** Update .gitignore to include claude.md and enhance installation scripts for claude ([864bf43](https://github.com/Ronnasayd/aipp/commit/864bf43))
- **[✨ Features]** Add .mcp.json to .gitignore and update installation scripts for claude ([c25969e](https://github.com/Ronnasayd/aipp/commit/c25969e))
- **[✨ Features]** Add claude installation script and update .gitignore for new directories ([54bc84a](https://github.com/Ronnasayd/aipp/commit/54bc84a))
- **[✨ Features]** Improve code formatting and add anthropic-compatible messages endpoint ([4c03dea](https://github.com/Ronnasayd/aipp/commit/4c03dea))

### **2026-03-31**

- **[✨ Features]** Enhance model response structure to include tools capability in json output ([b125d79](https://github.com/Ronnasayd/aipp/commit/b125d79))

### **2026-03-30**

- **[📚 Documentation]** Update descriptions in skill.md files for clarity and precision ([874c764](https://github.com/Ronnasayd/aipp/commit/874c764))
- **[🚧 Other Changes]** Update echo statements in ignores.sh to include folder context for removed skills and agents ([0ac9910](https://github.com/Ronnasayd/aipp/commit/0ac9910))
- **[🧹 Chores]** Update changelog for version 2026.03.30 with recent changes and enhancements ([ec665d8](https://github.com/Ronnasayd/aipp/commit/ec665d8))
- **[✨ Features]** Refactor installation scripts to use centralized ignore handling; add ignores.sh for skill and agent removal ([35f78d0](https://github.com/Ronnasayd/aipp/commit/35f78d0))
- **[✨ Features]** Add .agentsignore file and implement agent removal based on ignore patterns; improve formatting in skill.md files ([338c826](https://github.com/Ronnasayd/aipp/commit/338c826))
- **[✨ Features]** Add context7 documentation lookup and figma code connect components skills; remove obsolete skill.md files ([0373883](https://github.com/Ronnasayd/aipp/commit/0373883))
- **[✨ Features]** Add skillsignore functionality to remove specified skills and update gemini installation command ([3ea8d34](https://github.com/Ronnasayd/aipp/commit/3ea8d34))

### **2026-03-29**

- **[🧹 Chores]** Update rtk instructions file by replacing copilot instructions with structured format ([82340d7](https://github.com/Ronnasayd/aipp/commit/82340d7))
- **[✨ Features]** Integrate rtk initialization for copilot and gemini in installation scripts ([1f29c7b](https://github.com/Ronnasayd/aipp/commit/1f29c7b))
- **[🧹 Chores]** Reorder rtk initialization commands and update instructions file path ([2773d6b](https://github.com/Ronnasayd/aipp/commit/2773d6b))
- **[✨ Features]** Initialize rtk with gemini and copilot in install script ([e68d80b](https://github.com/Ronnasayd/aipp/commit/e68d80b))
- **[✨ Features]** Add support for postgresql, mysql, mongodb, and sqlite in settings configuration ([b7eb6d0](https://github.com/Ronnasayd/aipp/commit/b7eb6d0))
- **[🚧 Other Changes]** Update shebang and fix environment variable name for sqlite database path ([00fecd4](https://github.com/Ronnasayd/aipp/commit/00fecd4))
- **[✨ Features]** Add sqlite support with new fastmcp server tool for database interaction ([44f74fe](https://github.com/Ronnasayd/aipp/commit/44f74fe))
- **[✨ Features]** Add mongodb support with new tool for database interaction and update requirements ([fe90060](https://github.com/Ronnasayd/aipp/commit/fe90060))
- **[✨ Features]** Add mysql support and refactor postgresql interaction in fastmcp server ([5175ca2](https://github.com/Ronnasayd/aipp/commit/5175ca2))
- **[♻️ Refactoring]** Enhance postgresql query execution to enforce read-only sessions and improve result fetching ([d96b6d2](https://github.com/Ronnasayd/aipp/commit/d96b6d2))
- **[♻️ Refactoring]** Update postgresql server configuration and enhance query execution documentation ([23d8cda](https://github.com/Ronnasayd/aipp/commit/23d8cda))
- **[✨ Features]** Implement postgresql interaction and add fastmcp server tools for code review and context generation ([dad71ec](https://github.com/Ronnasayd/aipp/commit/dad71ec))

### **2026-03-27**

- **[♻️ Refactoring]** Update documentation file patterns in check_documentation_files function ([105143a](https://github.com/Ronnasayd/aipp/commit/105143a))
- **[♻️ Refactoring]** Remove unnecessary global statements and improve file handling in memory.py ([79f0b01](https://github.com/Ronnasayd/aipp/commit/79f0b01))
- **[✨ Features]** Implement per-language helpers for quality gate checks ([5e65820](https://github.com/Ronnasayd/aipp/commit/5e65820))
- **[🧹 Chores]** Add inputs field to vscode.mcp.json configuration ([f48f229](https://github.com/Ronnasayd/aipp/commit/f48f229))
- **[✨ Features]** Add aftertool hook for running quality gate checks post tool usage ([4665860](https://github.com/Ronnasayd/aipp/commit/4665860))
- **[✨ Features]** Add memory-add command for persisting memory entries with optional file association ([af5beae](https://github.com/Ronnasayd/aipp/commit/af5beae))
- **[🚧 Other Changes]** Format imports and improve logging messages in quality_gate.py ([abaa404](https://github.com/Ronnasayd/aipp/commit/abaa404))
- **[🚧 Other Changes]** Format code for consistency in check_documentation_files and get_diff_files functions ([b03964a](https://github.com/Ronnasayd/aipp/commit/b03964a))
- **[🐛 Bug Fixes]** Set quality gate fix to true and strict to false by default ([11e04b7](https://github.com/Ronnasayd/aipp/commit/11e04b7))
- **[✨ Features]** Add new agents for prd and srs generation with detailed instructions ([4c74cfe](https://github.com/Ronnasayd/aipp/commit/4c74cfe))
- **[✨ Features]** Add symlink creation for .geminignore in gemini.install.sh ([5f33998](https://github.com/Ronnasayd/aipp/commit/5f33998))
- **[✨ Features]** Add .geminignore file to exclude common development artifacts ([891702b](https://github.com/Ronnasayd/aipp/commit/891702b))

### **2026-03-26**

- **[✨ Features]** Reorganize scripts and implement md2toml and toml2md converters ([04a8836](https://github.com/Ronnasayd/aipp/commit/04a8836))
- **[✨ Features]** Update documentation skills for generating and syncing project documentation ([7b558c6](https://github.com/Ronnasayd/aipp/commit/7b558c6))
- **[✨ Features]** Add rule to allow listing servers in mcp-manager ([259354d](https://github.com/Ronnasayd/aipp/commit/259354d))
- **[♻️ Refactoring]** Remove unused context7 and chrome-devtools entries from mcp-server-enablement.json ([4d13c68](https://github.com/Ronnasayd/aipp/commit/4d13c68))
- **[♻️ Refactoring]** Clean up mcpservers configuration by removing unused entries and fixing url typo ([dd6b4c7](https://github.com/Ronnasayd/aipp/commit/dd6b4c7))
- **[♻️ Refactoring]** Remove github server configuration and add web_search_exa rule in policies ([f2472b7](https://github.com/Ronnasayd/aipp/commit/f2472b7))
- **[🧹 Chores]** Remove commented-out server configurations from vscode.mcp.json ([8cdc97d](https://github.com/Ronnasayd/aipp/commit/8cdc97d))
- **[♻️ Refactoring]** Update mcp-manager configuration and clean up commented server entries ([ce56c19](https://github.com/Ronnasayd/aipp/commit/ce56c19))
- **[✨ Features]** Add get_diff_files function to retrieve modified files using git diff ([df47979](https://github.com/Ronnasayd/aipp/commit/df47979))

### **2026-03-25**

- **[🐛 Bug Fixes]** Improve error handling in run_command and update version in copilot_ollama ([9eef266](https://github.com/Ronnasayd/aipp/commit/9eef266))
- **[♻️ Refactoring]** Add debug logging in detect_formatter for improved traceability ([f430e00](https://github.com/Ronnasayd/aipp/commit/f430e00))
- **[♻️ Refactoring]** Enhance resolve_formatter_bin function with logger for improved debugging ([3c82e1b](https://github.com/Ronnasayd/aipp/commit/3c82e1b))
- **[♻️ Refactoring]** Add debug logging to detect_formatter for improved traceability ([90ec48f](https://github.com/Ronnasayd/aipp/commit/90ec48f))
- **[♻️ Refactoring]** Enhance detect_formatter function with logging for better debugging ([98a82ca](https://github.com/Ronnasayd/aipp/commit/98a82ca))
- **[♻️ Refactoring]** Enhance debug logging in quality gate checks for better traceability ([6c6cd8a](https://github.com/Ronnasayd/aipp/commit/6c6cd8a))
- **[♻️ Refactoring]** Replace direct dictionary access with utility function get_by_key for improved readability and consistency ([3cbe675](https://github.com/Ronnasayd/aipp/commit/3cbe675))
- **[♻️ Refactoring]** Update logger names and enhance utility function imports across multiple scripts ([2c481db](https://github.com/Ronnasayd/aipp/commit/2c481db))
- **[♻️ Refactoring]** Enhance utility functions with key normalization and improved logging ([6fec693](https://github.com/Ronnasayd/aipp/commit/6fec693))
- **[♻️ Refactoring]** Add debug logging for ruff results in quality gate checks ([599d3e5](https://github.com/Ronnasayd/aipp/commit/599d3e5))
- **[🚧 Other Changes]** Update log message format to include logger name, level, and timestamp ([2942f25](https://github.com/Ronnasayd/aipp/commit/2942f25))
- **[♻️ Refactoring]** Implement centralized logging across multiple scripts ([5e6c934](https://github.com/Ronnasayd/aipp/commit/5e6c934))
- **[♻️ Refactoring]** Consolidate formatter detection and project root resolution logic ([91a06a7](https://github.com/Ronnasayd/aipp/commit/91a06a7))
- **[🚧 Other Changes]** Improve session file output message for clarity ([a0f0f67](https://github.com/Ronnasayd/aipp/commit/a0f0f67))

### **2026-03-24**

- **[🧹 Chores]** Remove orchestration instructions from installation scripts ([ef2a78a](https://github.com/Ronnasayd/aipp/commit/ef2a78a))
- **[🚧 Other Changes]** Remove checklist formatting for clarity in agent instructions ([f602614](https://github.com/Ronnasayd/aipp/commit/f602614))
- **[🚧 Other Changes]** Update code generation instructions for clarity and conciseness ([f6c6384](https://github.com/Ronnasayd/aipp/commit/f6c6384))
- **[🚧 Other Changes]** Refine agent instructions by removing redundant rules and clarifying retrieval process ([536bf64](https://github.com/Ronnasayd/aipp/commit/536bf64))
- **[🚧 Other Changes]** Improve clarity and consistency in agent instructions and documentation retrieval rules ([18071ac](https://github.com/Ronnasayd/aipp/commit/18071ac))
- **[✨ Features]** Add ai-setup-audit prompt for auditing ai setup and identifying improvements ([de77226](https://github.com/Ronnasayd/aipp/commit/de77226))
- **[🚧 Other Changes]** Update wording for clarity on testability and validation instructions in code generation rules ([c3cafb2](https://github.com/Ronnasayd/aipp/commit/c3cafb2))
- **[🚧 Other Changes]** Update formatting for code generation rules and anti-patterns in instructions ([b74447d](https://github.com/Ronnasayd/aipp/commit/b74447d))
- **[🚧 Other Changes]** Update formatting and wording for rules to avoid and follow in agent instructions ([314881a](https://github.com/Ronnasayd/aipp/commit/314881a))
- **[📚 Documentation]** Add guidelines for module exports and database interactions in agent instructions ([2b08f4f](https://github.com/Ronnasayd/aipp/commit/2b08f4f))
- **[✨ Features]** Add document summarizer skill and evaluation prompts for structured summaries ([fcb710a](https://github.com/Ronnasayd/aipp/commit/fcb710a))
- **[🚧 Other Changes]** Improve code formatting and consistency across multiple skills documentation ([e3fd4a9](https://github.com/Ronnasayd/aipp/commit/e3fd4a9))
- **[✨ Features]** Add quality gate checks to posttooluse hook for auditing ([c9a0892](https://github.com/Ronnasayd/aipp/commit/c9a0892))
- **[✨ Features]** Update task prompt generation to include context from specification files ([0f15cdd](https://github.com/Ronnasayd/aipp/commit/0f15cdd))

### **2026-03-23**

- **[🧹 Chores]** Remove outdated cli integration examples from taskmaster-task-validator documentation ([b57054e](https://github.com/Ronnasayd/aipp/commit/b57054e))
- **[✨ Features]** Add new rules for skill activation and web search commands in auto-saved.toml ([0c2cff8](https://github.com/Ronnasayd/aipp/commit/0c2cff8))
- **[🐛 Bug Fixes]** Update transcript path handling for summary extraction in session end ([1d56bff](https://github.com/Ronnasayd/aipp/commit/1d56bff))
- **[✨ Features]** Add session end logging hook for auditing in afteragent configuration ([f18e5ea](https://github.com/Ronnasayd/aipp/commit/f18e5ea))
- **[✨ Features]** Streamline summary extraction in session end handling for gemini and copilot transcripts ([6b8ec4b](https://github.com/Ronnasayd/aipp/commit/6b8ec4b))
- **[✨ Features]** Refactor session end handling to extract summaries from gemini sessions and update hook configuration ([36d9978](https://github.com/Ronnasayd/aipp/commit/36d9978))
- **[✨ Features]** Update memory.py and hooks.json descriptions for improved clarity on functionality ([5cb8099](https://github.com/Ronnasayd/aipp/commit/5cb8099))
- **[✨ Features]** Enhance markdown generation in memory.py for improved session documentation ([c4105f5](https://github.com/Ronnasayd/aipp/commit/c4105f5))
- **[✨ Features]** Replace check_available_files.py with memory.py for improved file management in hooks ([4433d71](https://github.com/Ronnasayd/aipp/commit/4433d71))
- **[✨ Features]** Update get_session_id_short to accept session_id parameter for improved session identification ([a94c4fb](https://github.com/Ronnasayd/aipp/commit/a94c4fb))
- **[✨ Features]** Add utility functions for session management and update .gitignore for session files ([dffe70c](https://github.com/Ronnasayd/aipp/commit/dffe70c))
- **[✨ Features]** Remove notes and context sections from session summary output ([f0fec00](https://github.com/Ronnasayd/aipp/commit/f0fec00))
- **[✨ Features]** Add session end logging and update session file structure for better auditing ([325ded8](https://github.com/Ronnasayd/aipp/commit/325ded8))
- **[✨ Features]** Add support for features documentation directory in check_documentation_files ([99ae846](https://github.com/Ronnasayd/aipp/commit/99ae846))
- **[✨ Features]** Update task file paths in check_documentation_files for accuracy ([4171d23](https://github.com/Ronnasayd/aipp/commit/4171d23))
- **[✨ Features]** Add check_available_files command to session hooks for file availability checks ([2537eeb](https://github.com/Ronnasayd/aipp/commit/2537eeb))
- **[✨ Features]** Write markdown instructions for available files to repository for easier access ([95f4c0a](https://github.com/Ronnasayd/aipp/commit/95f4c0a))
- **[✨ Features]** Add check_available_files command to session start hook for file availability checks ([958706b](https://github.com/Ronnasayd/aipp/commit/958706b))

### **2026-03-22**

- **[🧹 Chores]** Update changelog for version 2026.03.22 with recent changes and enhancements ([b79476b](https://github.com/Ronnasayd/aipp/commit/b79476b))
- **[🧹 Chores]** Remove check_available_files script from session hooks for cleanup ([ead42ec](https://github.com/Ronnasayd/aipp/commit/ead42ec))
- **[✨ Features]** Add check_available_files script to log documentation file availability in session hooks ([158aecd](https://github.com/Ronnasayd/aipp/commit/158aecd))
- **[✨ Features]** Refactor log file handling to improve session log file retrieval and creation ([6ad0995](https://github.com/Ronnasayd/aipp/commit/6ad0995))
- **[✨ Features]** Add check_available_files script to log documentation file availability and update session log file naming ([58a0627](https://github.com/Ronnasayd/aipp/commit/58a0627))
- **[✨ Features]** Add session start hook to log session initiation for auditing ([4d908f4](https://github.com/Ronnasayd/aipp/commit/4d908f4))
- **[🧹 Chores]** Remove deprecated javascript hooks and replace with python scripts for session management ([525efd4](https://github.com/Ronnasayd/aipp/commit/525efd4))
- **[✨ Features]** Add session start and end hooks for task management and performance evaluation ([8a13854](https://github.com/Ronnasayd/aipp/commit/8a13854))
- **[✨ Features]** Add session evaluation script to log performance metrics ([b25f995](https://github.com/Ronnasayd/aipp/commit/b25f995))
- **[✨ Features]** Add precompact hook to save state before context compaction ([14f6c58](https://github.com/Ronnasayd/aipp/commit/14f6c58))
- **[✨ Features]** Add session management features with aliases and session persistence ([2e1b4ca](https://github.com/Ronnasayd/aipp/commit/2e1b4ca))
- **[✨ Features]** Add new skills for task retrospective, task validation, task management overview, and related workflows ([0e8139c](https://github.com/Ronnasayd/aipp/commit/0e8139c))
- **[♻️ Refactoring]** Remove .git pattern from protected file patterns ([b8cdff4](https://github.com/Ronnasayd/aipp/commit/b8cdff4))

### **2026-03-20**

- **[♻️ Refactoring]** Add additional hook categories for improved tool management ([5e8bc9c](https://github.com/Ronnasayd/aipp/commit/5e8bc9c))
- **[♻️ Refactoring]** Update workflow guidelines for significant code changes and improve clarity ([b7fce1a](https://github.com/Ronnasayd/aipp/commit/b7fce1a))
- **[♻️ Refactoring]** Clean up comments and improve terminal auto-approve settings in settings.json ([9ce292e](https://github.com/Ronnasayd/aipp/commit/9ce292e))
- **[🐛 Bug Fixes]** Correct typo in url for atlassian service in vscode.mcp.json ([756f2c1](https://github.com/Ronnasayd/aipp/commit/756f2c1))
- **[🐛 Bug Fixes]** Update applyto pattern in code instructions for specific file types ([9f0adc1](https://github.com/Ronnasayd/aipp/commit/9f0adc1))
- **[✨ Features]** Enhance protect_files script to extract file paths from cat commands and deny access to protected files ([8b7563d](https://github.com/Ronnasayd/aipp/commit/8b7563d))
- **[✨ Features]** Add descriptions for log-tools-call and protect-files commands in hooks ([1e4962b](https://github.com/Ronnasayd/aipp/commit/1e4962b))
- **[♻️ Refactoring]** Consolidate hook commands into a single hooks.json file ([26721de](https://github.com/Ronnasayd/aipp/commit/26721de))
- **[🐛 Bug Fixes]** Clarify task retrieval tool reference in execute-task skill documentation ([9b91aea](https://github.com/Ronnasayd/aipp/commit/9b91aea))
- **[🐛 Bug Fixes]** Improve task retrieval instructions and enhance task prompt formatting ([cde0ec0](https://github.com/Ronnasayd/aipp/commit/cde0ec0))
- **[✨ Features]** Update task prompts in create-task and expand-task scripts to include spec_file references ([ca5aac9](https://github.com/Ronnasayd/aipp/commit/ca5aac9))
- **[♻️ Refactoring]** Simplify argument parsing and update task prompts in taskmaster scripts ([1ced3e2](https://github.com/Ronnasayd/aipp/commit/1ced3e2))
- **[📚 Documentation]** Enhance execute-task skill documentation with xp principles and detailed workflow steps ([41096ab](https://github.com/Ronnasayd/aipp/commit/41096ab))
- **[✨ Features]** Add taskmaster-prd-generator skill for generating structured prds ([fd93e42](https://github.com/Ronnasayd/aipp/commit/fd93e42))

### **2026-03-19**

- **[✨ Features]** Rename log-tools-call script to log_tools_call and update references ([39ade23](https://github.com/Ronnasayd/aipp/commit/39ade23))
- **[🐛 Bug Fixes]** Update command paths in settings.json to use environment variable and improve output structure in protect_files.py ([7df298a](https://github.com/Ronnasayd/aipp/commit/7df298a))
- **[✨ Features]** Add centralized hook configuration and scripts for logging tool calls and file protection ([bde5a7d](https://github.com/Ronnasayd/aipp/commit/bde5a7d))
- **[✨ Features]** Update hook configuration and generator script for output directory support ([4a82122](https://github.com/Ronnasayd/aipp/commit/4a82122))
- **[✨ Features]** Remove deprecated logging scripts and add centralized hook configuration ([db3e9e2](https://github.com/Ronnasayd/aipp/commit/db3e9e2))
- **[✨ Features]** Add log-tools-call script for logging tool calls ([f134711](https://github.com/Ronnasayd/aipp/commit/f134711))
- **[🐛 Bug Fixes]** Remove debug print statement from json loading in protect_files.py ([dd9e6b2](https://github.com/Ronnasayd/aipp/commit/dd9e6b2))
- **[✨ Features]** Replace shell script with python script for file protection logic ([095e266](https://github.com/Ronnasayd/aipp/commit/095e266))
- **[📚 Documentation]** Correct spacing in section header for mandatory rules in agent instructions ([b68f248](https://github.com/Ronnasayd/aipp/commit/b68f248))
- **[🐛 Bug Fixes]** Update codex installation script to use agents.toml for configuration and manage prompts directory ([1c1ab31](https://github.com/Ronnasayd/aipp/commit/1c1ab31))
- **[📚 Documentation]** Update mandatory agents list in skill.md for code review ([f9570f6](https://github.com/Ronnasayd/aipp/commit/f9570f6))
- **[📚 Documentation]** Update agent instructions and skill.md for improved code review guidelines ([f707a65](https://github.com/Ronnasayd/aipp/commit/f707a65))
- **[🐛 Bug Fixes]** Disable enableconseca option in security settings ([929e9aa](https://github.com/Ronnasayd/aipp/commit/929e9aa))
- **[🐛 Bug Fixes]** Update commandregex patterns to remove unnecessary word boundaries and improve command matching ([6017a48](https://github.com/Ronnasayd/aipp/commit/6017a48))
- **[✨ Features]** Add make-code-review prompt for comprehensive security and quality assessment ([f753ebc](https://github.com/Ronnasayd/aipp/commit/f753ebc))
- **[✨ Features]** Add code review prompt for comprehensive security and quality assessment ([236fc61](https://github.com/Ronnasayd/aipp/commit/236fc61))
- **[🐛 Bug Fixes]** Correct prompts directory handling in copilot installation script ([2e39a12](https://github.com/Ronnasayd/aipp/commit/2e39a12))
- **[✨ Features]** Add save-session command documentation for session state management ([21be70f](https://github.com/Ronnasayd/aipp/commit/21be70f))
- **[🧹 Chores]** Update gemini installation script to handle commands directory and improve symlink management ([8305370](https://github.com/Ronnasayd/aipp/commit/8305370))
- **[✨ Features]** Remove obsolete prompt files and update installation scripts for new command structure ([02a01f0](https://github.com/Ronnasayd/aipp/commit/02a01f0))
- **[🧹 Chores]** Refactor installation scripts to use default_folder variable for consistency ([1f4b9f4](https://github.com/Ronnasayd/aipp/commit/1f4b9f4))
- **[✨ Features]** Restore sonarqube configuration in settings.json ([ae7ff17](https://github.com/Ronnasayd/aipp/commit/ae7ff17))
- **[🧹 Chores]** Disable sonarqube configuration and update mcp-server settings ([c961fe4](https://github.com/Ronnasayd/aipp/commit/c961fe4))
- **[✨ Features]** Add atlassian server configuration with http type and url ([089bee9](https://github.com/Ronnasayd/aipp/commit/089bee9))
- **[✨ Features]** Add github server configuration with http type and url ([fa41242](https://github.com/Ronnasayd/aipp/commit/fa41242))
- **[✨ Features]** Add exa server configuration with http type and url ([089087d](https://github.com/Ronnasayd/aipp/commit/089087d))
- **[✨ Features]** Add exa server configuration with http type and url ([4c0ffbc](https://github.com/Ronnasayd/aipp/commit/4c0ffbc))
- **[✨ Features]** Add comprehensive documentation for srs generation, including templates, workflows, and guidelines for requirements analysis and task decomposition ([d8268da](https://github.com/Ronnasayd/aipp/commit/d8268da))
- **[🧹 Chores]** Comment out codex installation script in install.sh ([4f7d956](https://github.com/Ronnasayd/aipp/commit/4f7d956))
- **[✨ Features]** Add new skills for python testing, regex vs llm structured text parsing, and tdd workflow ([36b8c0b](https://github.com/Ronnasayd/aipp/commit/36b8c0b))
- **[✨ Features]** Add comprehensive coding standards for javascript, typescript, react, node.js, c++, and content-hash caching pattern ([dd4a76c](https://github.com/Ronnasayd/aipp/commit/dd4a76c))
- **[✨ Features]** Add ai-regression-testing and api-design skill documentation ([82c96d1](https://github.com/Ronnasayd/aipp/commit/82c96d1))
- **[✨ Features]** Add agent-harness-construction skill documentation and enable codex installation script ([8e13f07](https://github.com/Ronnasayd/aipp/commit/8e13f07))

### **2026-03-18**

- **[✨ Features]** Add mcp server configuration for figma and taskmaster in config.toml ([ae0dd5c](https://github.com/Ronnasayd/aipp/commit/ae0dd5c))
- **[🧹 Chores]** Update gitignore installation script permissions ([c391cc3](https://github.com/Ronnasayd/aipp/commit/c391cc3))
- **[✨ Features]** Update taskmaster installation scripts and improve gitignore management ([a5b3eb9](https://github.com/Ronnasayd/aipp/commit/a5b3eb9))
- **[🐛 Bug Fixes]** Correct logic for copying taskmaster configuration and state files ([f70b775](https://github.com/Ronnasayd/aipp/commit/f70b775))
- **[✨ Features]** Add taskmaster tasks directory to documentation search context ([6762365](https://github.com/Ronnasayd/aipp/commit/6762365))
- **[✨ Features]** Rename taskmaster skills for consistency and update usage instructions in skill.md files ([0904689](https://github.com/Ronnasayd/aipp/commit/0904689))
- **[✨ Features]** Add new skills for task management including append, create, and expand functionalities ([aade7b5](https://github.com/Ronnasayd/aipp/commit/aade7b5))
- **[✨ Features]** Enhance task conversion with per-tag markdown generation and metadata extraction ([ddc2b46](https://github.com/Ronnasayd/aipp/commit/ddc2b46))
- **[✨ Features]** Enhance task specification skills with additional argument options and improved usage instructions ([295cc3f](https://github.com/Ronnasayd/aipp/commit/295cc3f))
- **[✨ Features]** Consolidate command execution rules into auto-saved.toml and remove rules.toml ([c706888](https://github.com/Ronnasayd/aipp/commit/c706888))
- **[✨ Features]** Add security settings for tool approval and policy defaults in settings.json; create initial policy for shell command execution ([cd3d163](https://github.com/Ronnasayd/aipp/commit/cd3d163))
- **[✨ Features]** Add policies for command execution rules in rules.toml and update gemini.install.sh for policies symlink ([77b4c90](https://github.com/Ronnasayd/aipp/commit/77b4c90))
- **[✨ Features]** Add semantic commit message generation skill based on staged changes ([2fad5ca](https://github.com/Ronnasayd/aipp/commit/2fad5ca))
- **[🧹 Chores]** Remove unused terminal and remote extension settings from configuration ([6122601](https://github.com/Ronnasayd/aipp/commit/6122601))
- **[✨ Features]** Implement ai-jail script for sandboxing ai coding agents with customizable mounts ([86a76f0](https://github.com/Ronnasayd/aipp/commit/86a76f0))
- **[✨ Features]** Enhance expand-task script with task id and prompt parameters for complexity analysis ([c0b72c9](https://github.com/Ronnasayd/aipp/commit/c0b72c9))

### **2026-03-17**

- **[🧹 Chores]** Remove redundant command for expanding tasks in append-tasks.sh ([741c586](https://github.com/Ronnasayd/aipp/commit/741c586))
- **[✨ Features]** Add configuration file for gemini model settings and global parameters ([c56efdf](https://github.com/Ronnasayd/aipp/commit/c56efdf))
- **[✨ Features]** Add task-retrospective skill for structured evaluation and rule generation after task completion ([6b5e05a](https://github.com/Ronnasayd/aipp/commit/6b5e05a))
- **[✨ Features]** Add agent-creator skill with comprehensive guidelines for creating and improving specialist agents ([1b8f951](https://github.com/Ronnasayd/aipp/commit/1b8f951))
- **[🧹 Chores]** Update project dependencies to latest versions ([4403c7f](https://github.com/Ronnasayd/aipp/commit/4403c7f))
- **[✨ Features]** Add tailwind config conformance skill with validation and refactoring capabilities ([0e4e8f3](https://github.com/Ronnasayd/aipp/commit/0e4e8f3))
- **[✨ Features]** Enhance execute-task skill with detailed workflow and delegation guidelines ([14c5bc0](https://github.com/Ronnasayd/aipp/commit/14c5bc0))
- **[✨ Features]** Implement model configuration loading and validation for copilot ollama proxy ([e23faa0](https://github.com/Ronnasayd/aipp/commit/e23faa0))
- **[✨ Features]** Add frontend-design skill with comprehensive guidelines for creating high-quality interfaces ([2ae179b](https://github.com/Ronnasayd/aipp/commit/2ae179b))
- **[✨ Features]** Add python mcp server implementation guide and evaluation scripts ([8cb0f01](https://github.com/Ronnasayd/aipp/commit/8cb0f01))
- **[✨ Features]** Add skill-creator documentation for creating and improving skills ([c6b6850](https://github.com/Ronnasayd/aipp/commit/c6b6850))
- **[♻️ Refactoring]** Simplify plan-generator skill description and structure ([b47d95b](https://github.com/Ronnasayd/aipp/commit/b47d95b))
- **[✨ Features]** Add technical decision maker skill with structured workflow and analysis guidelines ([5eaf8d8](https://github.com/Ronnasayd/aipp/commit/5eaf8d8))

### **2026-03-16**

- **[🐛 Bug Fixes]** Update agents.md references to use correct paths for instructions ([fde0ada](https://github.com/Ronnasayd/aipp/commit/fde0ada))
- **[✨ Features]** Add symbolic links for instruction files in agents.md and create instructions directory ([4a19c00](https://github.com/Ronnasayd/aipp/commit/4a19c00))
- **[♻️ Refactoring]** Remove exec prefix from task-master commands in task scripts ([912806a](https://github.com/Ronnasayd/aipp/commit/912806a))
- **[🧹 Chores]** Comment out codex installation script in install.sh ([aacfba4](https://github.com/Ronnasayd/aipp/commit/aacfba4))
- **[✨ Features]** Update install scripts to manage agents.md and improve gitignore entries ([5531b9a](https://github.com/Ronnasayd/aipp/commit/5531b9a))
- **[✨ Features]** Implement task expansion skill and update task scripts for improved execution ([98f9db7](https://github.com/Ronnasayd/aipp/commit/98f9db7))
- **[✨ Features]** Enhance append-tasks and create-task scripts with extreme programming workflow and task tagging ([c179e1a](https://github.com/Ronnasayd/aipp/commit/c179e1a))
- **[🧹 Chores]** Remove deprecated execute_task command configuration ([77abc8d](https://github.com/Ronnasayd/aipp/commit/77abc8d))
- **[✨ Features]** Update argument placeholders in skill.md files for consistency and clarity ([319fa2c](https://github.com/Ronnasayd/aipp/commit/319fa2c))
- **[📚 Documentation]** Update description and task instructions for generate-docs-init skill ([bd4b932](https://github.com/Ronnasayd/aipp/commit/bd4b932))
- **[✨ Features]** Update append-tasks skill with command execution instructions and add new script for task processing ([f518f4e](https://github.com/Ronnasayd/aipp/commit/f518f4e))
- **[✨ Features]** Update create-task skill documentation with command execution instructions ([c2fc7e1](https://github.com/Ronnasayd/aipp/commit/c2fc7e1))
- **[✨ Features]** Add code block formatting to prompts in md2tasks and tasks2md for improved clarity ([e94b563](https://github.com/Ronnasayd/aipp/commit/e94b563))
- **[✨ Features]** Update prompts in md2tasks and tasks2md for clearer command execution instructions ([59df2ef](https://github.com/Ronnasayd/aipp/commit/59df2ef))
- **[🐛 Bug Fixes]** Update symlink paths in installation scripts for prompts and commands ([d1e6b3c](https://github.com/Ronnasayd/aipp/commit/d1e6b3c))
- **[✨ Features]** Remove deprecated prompts and add new task management commands ([c454bea](https://github.com/Ronnasayd/aipp/commit/c454bea))
- **[✨ Features]** Add plan-generator skill for structured task and project planning ([42b4168](https://github.com/Ronnasayd/aipp/commit/42b4168))
- **[✨ Features]** Add new benchmark files for agent documentation retrieval, code compliance, and orchestration ([9ad291e](https://github.com/Ronnasayd/aipp/commit/9ad291e))
- **[✨ Features]** Add new benchmark files for agent orchestration and code compliance tests ([009bbe6](https://github.com/Ronnasayd/aipp/commit/009bbe6))
- **[🐛 Bug Fixes]** Update documentation references to include 'docs/' prefix for consistency ([c5aaacf](https://github.com/Ronnasayd/aipp/commit/c5aaacf))
- **[✨ Features]** Update instruction files and remove deprecated ones for improved clarity and organization ([819f88b](https://github.com/Ronnasayd/aipp/commit/819f88b))
- **[🐛 Bug Fixes]** Update plan directory path in settings.json and adjust formatting in vscode.mcp.json ([90c55c6](https://github.com/Ronnasayd/aipp/commit/90c55c6))
- **[✨ Features]** Add directwebfetch option and update respectgitignore setting in settings.json ([33b66a4](https://github.com/Ronnasayd/aipp/commit/33b66a4))
- **[🧹 Chores]** Add 'docs/agents/' to .gitignore if not present ([cf27b03](https://github.com/Ronnasayd/aipp/commit/cf27b03))
- **[🐛 Bug Fixes]** Update file paths in documentation to use 'docs/agents/' directory ([278e89e](https://github.com/Ronnasayd/aipp/commit/278e89e))
- **[🐛 Bug Fixes]** Update file paths in documentation and settings to use 'docs/' directory ([cdb0b92](https://github.com/Ronnasayd/aipp/commit/cdb0b92))
- **[✨ Features]** Add plan configuration and billing strategy to settings.json ([e8414a7](https://github.com/Ronnasayd/aipp/commit/e8414a7))

### **2026-03-15**

- **[✨ Features]** Add checkpointing configuration to settings.json ([81da5f8](https://github.com/Ronnasayd/aipp/commit/81da5f8))
- **[✨ Features]** Implement large prompt handling with attachment conversion and cleanup functions ([203e9dc](https://github.com/Ronnasayd/aipp/commit/203e9dc))
- **[✨ Features]** Add task creation script with detailed execution workflow ([693d766](https://github.com/Ronnasayd/aipp/commit/693d766))
- **[🐛 Bug Fixes]** Remove redundant reference headers in gemini.md updates ([06f6a04](https://github.com/Ronnasayd/aipp/commit/06f6a04))
- **[✨ Features]** Implement setup function for instruction file symlinks and restore lessons instructions ([4ebf09e](https://github.com/Ronnasayd/aipp/commit/4ebf09e))
- **[📚 Documentation]** Add mandatory guidelines for avoiding common pitfalls and best practices ([5573652](https://github.com/Ronnasayd/aipp/commit/5573652))
- **[✨ Features]** Add task orchestration specialist agent and orchestration skill documentation ([34ae921](https://github.com/Ronnasayd/aipp/commit/34ae921))

### **2026-03-14**

- **[🐛 Bug Fixes]** Update documentation path for generated rules file ([53fe440](https://github.com/Ronnasayd/aipp/commit/53fe440))

### **2026-03-13**

- **[🧹 Chores]** Comment out codex installation script in install.sh ([098b391](https://github.com/Ronnasayd/aipp/commit/098b391))
- **[🐛 Bug Fixes]** Rename 'prompt' to 'developer_instructions' in agent toml files ([acccb27](https://github.com/Ronnasayd/aipp/commit/acccb27))
- **[🐛 Bug Fixes]** Rename developer_instructions to prompt for consistency in toml generation ([3652001](https://github.com/Ronnasayd/aipp/commit/3652001))
- **[🐛 Bug Fixes]** Update variable names for clarity and enhance codex configuration validation ([c3ced31](https://github.com/Ronnasayd/aipp/commit/c3ced31))
- **[🐛 Bug Fixes]** Update codex installation paths to use home directory ([153f776](https://github.com/Ronnasayd/aipp/commit/153f776))
- **[🧹 Chores]** Comment out codex installation script in install.sh ([698b53c](https://github.com/Ronnasayd/aipp/commit/698b53c))
- **[🐛 Bug Fixes]** Update codex installation script to use home directory for skills path ([4df9360](https://github.com/Ronnasayd/aipp/commit/4df9360))
- **[🐛 Bug Fixes]** Correct syntax for agent_id in codex configuration generation ([9e07b30](https://github.com/Ronnasayd/aipp/commit/9e07b30))
- **[✨ Features]** Add codebase-rules-extractor-specialist agent and skill documentation for code analysis ([a6ecb53](https://github.com/Ronnasayd/aipp/commit/a6ecb53))
- **[🧹 Chores]** Comment out codex installation script in install.sh ([5eaf2e3](https://github.com/Ronnasayd/aipp/commit/5eaf2e3))
- **[✨ Features]** Enhance codex installation script and configuration generation ([581ec13](https://github.com/Ronnasayd/aipp/commit/581ec13))
- **[✨ Features]** Add missing .agent/agents/ entry to .gitignore in codex.install.sh ([f9072d3](https://github.com/Ronnasayd/aipp/commit/f9072d3))
- **[✨ Features]** Update install.sh to dynamically set source and local based on script location ([6403193](https://github.com/Ronnasayd/aipp/commit/6403193))
- **[✨ Features]** Add md2toml.py for converting markdown files to toml format and update install scripts ([bcfc303](https://github.com/Ronnasayd/aipp/commit/bcfc303))
- **[✨ Features]** Replace converter.py with toml2md.py for toml to markdown conversion ([393f258](https://github.com/Ronnasayd/aipp/commit/393f258))

### **2026-03-12**

- **[✨ Features]** Enable respect for .gitignore in file filtering configuration ([f750915](https://github.com/Ronnasayd/aipp/commit/f750915))
- **[✨ Features]** Add context configuration for file filtering in settings.json ([ac85afc](https://github.com/Ronnasayd/aipp/commit/ac85afc))
- **[✨ Features]** Add chrome-devtools command to vscode.mcp.json and update installation script for mcp.json symlink ([6ca3294](https://github.com/Ronnasayd/aipp/commit/6ca3294))
- **[✨ Features]** Add mcp-server-enablement.json and update installation script for server configuration ([32f4753](https://github.com/Ronnasayd/aipp/commit/32f4753))
- **[✨ Features]** Add append-tasks-taskmaster skill for enhancing task specifications with new context and action plans ([9cb6655](https://github.com/Ronnasayd/aipp/commit/9cb6655))
- **[✨ Features]** Add prd-reviewer-specialist and test-coverage-specialist agents with detailed analysis frameworks ([f3dcb9d](https://github.com/Ronnasayd/aipp/commit/f3dcb9d))
- **[✨ Features]** Add create-task-taskmaster skill for generating structured task specifications ([e91303b](https://github.com/Ronnasayd/aipp/commit/e91303b))
- **[✨ Features]** Create new skill for generating structured task specifications based on detailed analysis ([c2bfa97](https://github.com/Ronnasayd/aipp/commit/c2bfa97))
- **[📚 Documentation]** Enhance skill.md with compact specification best practices and formatting guidelines ([fec90bf](https://github.com/Ronnasayd/aipp/commit/fec90bf))
- **[🐛 Bug Fixes]** Correct task and impact sections in pr description template for clarity ([6bc2da4](https://github.com/Ronnasayd/aipp/commit/6bc2da4))
- **[✨ Features]** Add generate-pr-description skill for automated pr description generation ([443155f](https://github.com/Ronnasayd/aipp/commit/443155f))

### **2026-03-11**

- **[✨ Features]** Add orchestration instructions and update references in installation scripts ([a460c16](https://github.com/Ronnasayd/aipp/commit/a460c16))
- **[✨ Features]** Add tdd guidelines and steps for writing tests in skill.md ([039cbea](https://github.com/Ronnasayd/aipp/commit/039cbea))
- **[🐛 Bug Fixes]** Update tool references in create_task and execute_task prompts for consistency ([3c3b5f4](https://github.com/Ronnasayd/aipp/commit/3c3b5f4))
- **[🐛 Bug Fixes]** Update tool references in create_task and execute_task prompts for consistency ([36b3e58](https://github.com/Ronnasayd/aipp/commit/36b3e58))
- **[✨ Features]** Add new skills for task management and documentation generation ([d08076d](https://github.com/Ronnasayd/aipp/commit/d08076d))
- **[📚 Documentation]** Update changelog for version 2026.03.11 with new features and chore updates ([4940149](https://github.com/Ronnasayd/aipp/commit/4940149))
- **[🐛 Bug Fixes]** Correct file path key in protect-files script for consistency ([af9016b](https://github.com/Ronnasayd/aipp/commit/af9016b))
- **[✨ Features]** Add protect-files hook and script to block access to sensitive files ([23b2fd7](https://github.com/Ronnasayd/aipp/commit/23b2fd7))
- **[✨ Features]** Update documentation generation instructions to enforce agent usage ([4d8948f](https://github.com/Ronnasayd/aipp/commit/4d8948f))
- **[✨ Features]** Update documentation generation tools to enforce agent usage and remove developer instructions ([e732ffd](https://github.com/Ronnasayd/aipp/commit/e732ffd))
- **[✨ Features]** Remove my_mcp_generate_docs_update tool and add generate-docs-update skill for structured documentation updates ([bd81e92](https://github.com/Ronnasayd/aipp/commit/bd81e92))
- **[🧹 Chores]** Update command execution instructions for code review skill to allow alternative diff-like outputs ([a281499](https://github.com/Ronnasayd/aipp/commit/a281499))
- **[✨ Features]** Implement code review skill with structured analysis instructions ([eee7994](https://github.com/Ronnasayd/aipp/commit/eee7994))

### **2026-03-10**

- **[🧹 Chores]** Remove my_mcp_run_command tool from the server implementation ([80f229c](https://github.com/Ronnasayd/aipp/commit/80f229c))
- **[✨ Features]** Enhance task creation instructions with user confirmation for single or multiple tasks ([4d2894d](https://github.com/Ronnasayd/aipp/commit/4d2894d))
- **[✨ Features]** Add codex installation script and update .gitignore for agent skills ([3803096](https://github.com/Ronnasayd/aipp/commit/3803096))
- **[📚 Documentation]** Update changelog for version 2026.03.10 with new features and chore updates ([fe16963](https://github.com/Ronnasayd/aipp/commit/fe16963))
- **[✨ Features]** Add comprehensive readme.md for ai pair programming workspace with project overview, key directories, and usage instructions ([d6af762](https://github.com/Ronnasayd/aipp/commit/d6af762))
- **[✨ Features]** Consolidate gitignore updates into installation scripts and remove redundant gitignore.install.sh ([e957e31](https://github.com/Ronnasayd/aipp/commit/e957e31))
- **[✨ Features]** Add installation scripts for github copilot, gemini, gitignore, and taskmaster ([4089358](https://github.com/Ronnasayd/aipp/commit/4089358))
- **[✨ Features]** Add logging hooks for session start, end, and user prompt submission ([e556f12](https://github.com/Ronnasayd/aipp/commit/e556f12))
- **[✨ Features]** Add comprehensive reactjs development standards and best practices documentation ([feb0311](https://github.com/Ronnasayd/aipp/commit/feb0311))
- **[📚 Documentation]** Update changelog for version 2026.03.10 with new features and chore updates ([b8ea125](https://github.com/Ronnasayd/aipp/commit/b8ea125))
- **[✨ Features]** Add reference check for github copilot instructions in gemini.md ([bbbf0f5](https://github.com/Ronnasayd/aipp/commit/bbbf0f5))
- **[✨ Features]** Add context architect specialist and context map skills for multi-file change planning ([e140a97](https://github.com/Ronnasayd/aipp/commit/e140a97))
- **[✨ Features]** Add figma design system to tailwind css conversion skill documentation ([c0bba2a](https://github.com/Ronnasayd/aipp/commit/c0bba2a))
- **[🧹 Chores]** Update project dependencies to latest versions ([36038df](https://github.com/Ronnasayd/aipp/commit/36038df))
- **[✨ Features]** Add tailwind css documentation and configuration resources ([cbbab73](https://github.com/Ronnasayd/aipp/commit/cbbab73))

### **2026-03-09**

- **[🧹 Chores]** Update changelog for version 2026.03.09 with new features, bug fixes, and documentation improvements ([df2c751](https://github.com/Ronnasayd/aipp/commit/df2c751))
- **[✨ Features]** Add environment preferences for javascript/typescript and python projects in instructions ([0b4ad5f](https://github.com/Ronnasayd/aipp/commit/0b4ad5f))
- **[🐛 Bug Fixes]** Correct symlink creation for gemini settings.json in install script ([54947a7](https://github.com/Ronnasayd/aipp/commit/54947a7))
- **[✨ Features]** Add symlink creation for gemini settings.json in install script ([3a99799](https://github.com/Ronnasayd/aipp/commit/3a99799))
- **[✨ Features]** Add new settings configuration for mcp servers and ui preferences ([9c6db9a](https://github.com/Ronnasayd/aipp/commit/9c6db9a))
- **[🧹 Chores]** Remove unused api key and token from context7 and sonarqube configurations ([5ad7dc8](https://github.com/Ronnasayd/aipp/commit/5ad7dc8))
- **[✨ Features]** Add comprehensive git-guide skill with detailed commands and workflows ([eae300a](https://github.com/Ronnasayd/aipp/commit/eae300a))
- **[✨ Features]** Add git-specialist agent with comprehensive git and devops guidance ([61fc463](https://github.com/Ronnasayd/aipp/commit/61fc463))
- **[📚 Documentation]** Add comprehensive testing guidelines for typescript/node.js backend projects ([ae7d38c](https://github.com/Ronnasayd/aipp/commit/ae7d38c))
- **[📚 Documentation]** Update description in execute_task prompt for clarity and add new figma mcp skill documentation ([97e9835](https://github.com/Ronnasayd/aipp/commit/97e9835))
- **[📚 Documentation]** Improve description clarity in execute_task prompt ([5c02b1e](https://github.com/Ronnasayd/aipp/commit/5c02b1e))
- **[📚 Documentation]** Add comprehensive guidelines for srs and testing in typescript/node.js backend projects ([37f03a8](https://github.com/Ronnasayd/aipp/commit/37f03a8))
- **[✨ Features]** Add new prompts for creating react components and simulating roundtable discussions ([dbf24b8](https://github.com/Ronnasayd/aipp/commit/dbf24b8))
- **[📚 Documentation]** Refine go style guide for clarity and conciseness ([1b0fea5](https://github.com/Ronnasayd/aipp/commit/1b0fea5))
- **[✨ Features]** Enhance copilot instructions with delegation and skill usage guidelines ([6ba69cd](https://github.com/Ronnasayd/aipp/commit/6ba69cd))
- **[📚 Documentation]** Update python style guide with modern conventions and best practices ([89d0fb3](https://github.com/Ronnasayd/aipp/commit/89d0fb3))
- **[✨ Features]** Add file processing patterns, token estimation strategies, tools reference, and analysis scripts ([8e17f31](https://github.com/Ronnasayd/aipp/commit/8e17f31))
- **[🧹 Chores]** Update .gitignore and gemini.md references in install script ([ecd222d](https://github.com/Ronnasayd/aipp/commit/ecd222d))
- **[✨ Features]** Add taskmaster skill with project management workflows and command references ([7345471](https://github.com/Ronnasayd/aipp/commit/7345471))
- **[♻️ Refactoring]** Enhance clarity and consistency in skill architect documentation ([491cd33](https://github.com/Ronnasayd/aipp/commit/491cd33))
- **[✨ Features]** Add skill architect agent with comprehensive guidelines for designing and optimizing claude agent skills ([523a5f0](https://github.com/Ronnasayd/aipp/commit/523a5f0))
- **[📚 Documentation]** Restructure and clarify code generation instructions in copilot guide ([a24eae5](https://github.com/Ronnasayd/aipp/commit/a24eae5))

### **2026-03-07**

- **[✨ Features]** Add developer planning specialist agent with detailed instructions and responsibilities ([df1366a](https://github.com/Ronnasayd/aipp/commit/df1366a))
- **[♻️ Refactoring]** Update task creation and execution prompts for clarity and consistency ([258da2c](https://github.com/Ronnasayd/aipp/commit/258da2c))
- **[✨ Features]** Add comprehensive guidelines for srs generation and testing in typescript/node.js backend projects ([517a186](https://github.com/Ronnasayd/aipp/commit/517a186))
- **[✨ Features]** Add new specialist agents for srs generation and frontend refactoring with detailed instructions ([1cf0e27](https://github.com/Ronnasayd/aipp/commit/1cf0e27))
- **[♻️ Refactoring]** Remove unused tools section from prd and review-refactor specialist documentation chore: update install script to copy agents instead of creating symbolic links ([d5a03bb](https://github.com/Ronnasayd/aipp/commit/d5a03bb))
- **[♻️ Refactoring]** Remove unused tools section from various specialist agent documentation ([72e690d](https://github.com/Ronnasayd/aipp/commit/72e690d))
- **[✨ Features]** Add tools section to various specialist agents for enhanced functionality ([47a4fda](https://github.com/Ronnasayd/aipp/commit/47a4fda))
- **[✨ Features]** Add new agent specialists for prd generation, review, srs generation, product ownership, and task reviewing ([282e717](https://github.com/Ronnasayd/aipp/commit/282e717))
- **[✨ Features]** Add new specialist agents for documentation, usability, teaching, generative ai, and code review ([98636be](https://github.com/Ronnasayd/aipp/commit/98636be))
- **[✨ Features]** Add database specialist and usability agent with detailed instructions ([b768758](https://github.com/Ronnasayd/aipp/commit/b768758))
- **[✨ Features]** Add cybersecurity agent with detailed instructions and update .gitignore for new directories ([2ee69fd](https://github.com/Ronnasayd/aipp/commit/2ee69fd))
- **[✨ Features]** Enhance task creation and execution prompts with detailed tool instructions ([018910f](https://github.com/Ronnasayd/aipp/commit/018910f))
- **[✨ Features]** Update task prompts for mcp developer guidance and enhance documentation ([c31a4af](https://github.com/Ronnasayd/aipp/commit/c31a4af))
- **[✨ Features]** Recreate and enhance task prompts for mcp developer guidance ([3377222](https://github.com/Ronnasayd/aipp/commit/3377222))
- **[🧹 Chores]** Update .gitignore to include new directories for github and taskmaster ([39dc8c9](https://github.com/Ronnasayd/aipp/commit/39dc8c9))
- **[✨ Features]** Add comprehensive testing guidelines for typescript/node.js backend projects ([36b92ef](https://github.com/Ronnasayd/aipp/commit/36b92ef))
- **[✨ Features]** Add golang style guide documentation for readability and maintainability ([eea4617](https://github.com/Ronnasayd/aipp/commit/eea4617))
- **[✨ Features]** Add python and typescript style guide documentation ([7cfe4c0](https://github.com/Ronnasayd/aipp/commit/7cfe4c0))
- **[✨ Features]** Add gemini and github copilot sections to install.sh; implement taskmaster setup and state management ([0ad17b9](https://github.com/Ronnasayd/aipp/commit/0ad17b9))
- **[🧹 Chores]** Reorganize install.sh script for better structure and clarity ([e92d366](https://github.com/Ronnasayd/aipp/commit/e92d366))
- **[✨ Features]** Add prompts for creating and executing tasks for mcp developers ([471f1f8](https://github.com/Ronnasayd/aipp/commit/471f1f8))
- **[🧹 Chores]** Restructure install.sh script and update typescript skill description for clarity ([8f05b8e](https://github.com/Ronnasayd/aipp/commit/8f05b8e))
- **[✨ Features]** Update python skill description for clarity and conciseness ([6e837af](https://github.com/Ronnasayd/aipp/commit/6e837af))

### **2026-03-06**

- **[🧹 Chores]** Remove task implementation steps from copilot instructions ([2fadab5](https://github.com/Ronnasayd/aipp/commit/2fadab5))
- **[✨ Features]** Add python style guide for coding conventions and best practices ([67d1cc0](https://github.com/Ronnasayd/aipp/commit/67d1cc0))
- **[✨ Features]** Add typescript style guide for coding conventions and best practices ([c78c883](https://github.com/Ronnasayd/aipp/commit/c78c883))
- **[✨ Features]** Add install.sh script for symlinking task configuration files ([38b2515](https://github.com/Ronnasayd/aipp/commit/38b2515))
- **[✨ Features]** Add create_task.toml for task creation instructions and tools ([bc1f605](https://github.com/Ronnasayd/aipp/commit/bc1f605))

### **2026-03-05**

- **[✨ Features]** Add write_todos tool to execute_task.toml for task execution guidance ([f771f57](https://github.com/Ronnasayd/aipp/commit/f771f57))
- **[✨ Features]** Add execute_task.toml for task execution instructions and tools ([f79f480](https://github.com/Ronnasayd/aipp/commit/f79f480))
- **[🧹 Chores]** Update sensitive api keys in gemini.mcp.json and vscode.mcp.json to placeholders ([b71ead1](https://github.com/Ronnasayd/aipp/commit/b71ead1))
- **[✨ Features]** Add new mcp.json and vscode.mcp.json configurations for server setup ([31ecf57](https://github.com/Ronnasayd/aipp/commit/31ecf57))
- **[✨ Features]** Add mcp.json configuration for server setup and environment variables ([4640ef8](https://github.com/Ronnasayd/aipp/commit/4640ef8))

### **2026-03-03**

- **[✨ Features]** Add comprehensive instructions for technical analysis and requirement assessment ([2ca9f27](https://github.com/Ronnasayd/aipp/commit/2ca9f27))

### **2026-02-21**

- **[✨ Features]** Add comprehensive instructions for generative ai specialists to enhance workflow and problem-solving capabilities ([3319f67](https://github.com/Ronnasayd/aipp/commit/3319f67))

### **2026-02-11**

- **[✨ Features]** Add context map section to task creation for improved documentation and clarity ([81f9792](https://github.com/Ronnasayd/aipp/commit/81f9792))

### **2026-02-08**

- **[✨ Features]** Add optional filter parameter to documentation sync tool for targeted git diff ([f83fedf](https://github.com/Ronnasayd/aipp/commit/f83fedf))
- **[✨ Features]** Add documentation synchronization tool to generate context from git diff ([e218cba](https://github.com/Ronnasayd/aipp/commit/e218cba))

### **2026-02-05**

- **[✨ Features]** Add comprehensive testing guidelines for typescript/node.js backend projects ([5df5391](https://github.com/Ronnasayd/aipp/commit/5df5391))
- **[✨ Features]** Enhance copilot instructions for clarity and structure in code generation tasks ([b8b3d48](https://github.com/Ronnasayd/aipp/commit/b8b3d48))
- **[✨ Features]** Update code review output rules and structure for improved clarity and compliance ([deaabc2](https://github.com/Ronnasayd/aipp/commit/deaabc2))
- **[✨ Features]** Enhance code review process with structured output rules and detailed task analysis instructions ([cf47b92](https://github.com/Ronnasayd/aipp/commit/cf47b92))
- **[✨ Features]** Enhance task creation workflow with detailed phases for context discovery, specification generation, and user review ([be12cb7](https://github.com/Ronnasayd/aipp/commit/be12cb7))
- **[🐛 Bug Fixes]** Clarify task implementation instructions and emphasize rule precedence ([d7ebb9b](https://github.com/Ronnasayd/aipp/commit/d7ebb9b))
- **[🐛 Bug Fixes]** Correct task creation instructions and improve code comments for clarity ([4830bc4](https://github.com/Ronnasayd/aipp/commit/4830bc4))
- **[🚧 Other Changes]** Format code for improved readability and consistency ([5b2b8ec](https://github.com/Ronnasayd/aipp/commit/5b2b8ec))
- **[✨ Features]** Refactor instruction loading to use dedicated functions for improved readability and maintainability ([c723a59](https://github.com/Ronnasayd/aipp/commit/c723a59))

### **2026-02-03**

- **[✨ Features]** Enhance code review instructions with detailed task creation workflow ([fb04ed7](https://github.com/Ronnasayd/aipp/commit/fb04ed7))

### **2026-01-30**

- **[🐛 Bug Fixes]** Remove unnecessary comment from task creation function ([55e3785](https://github.com/Ronnasayd/aipp/commit/55e3785))
- **[✨ Features]** Enhance task creation instructions to include web search for documentation ([afb0c6c](https://github.com/Ronnasayd/aipp/commit/afb0c6c))
- **[✨ Features]** Update task creation instructions and modify model configuration for improved task description generation ([76f631a](https://github.com/Ronnasayd/aipp/commit/76f631a))

### **2026-01-27**

- **[✨ Features]** Add comprehensive design conversion instructions for react components ([14224f7](https://github.com/Ronnasayd/aipp/commit/14224f7))

### **2026-01-26**

- **[✨ Features]** Update task creation instructions to include dynamic filename for generated task specs ([2cc3dcd](https://github.com/Ronnasayd/aipp/commit/2cc3dcd))
- **[✨ Features]** Update task creation instructions to include user review step before executing terminal commands ([817b614](https://github.com/Ronnasayd/aipp/commit/817b614))
- **[✨ Features]** Add unchangeable text block to task creation workflow instructions ([b25a53a](https://github.com/Ronnasayd/aipp/commit/b25a53a))
- **[✨ Features]** Add command to expand tasks in task creation instructions ([1b6df93](https://github.com/Ronnasayd/aipp/commit/1b6df93))
- **[✨ Features]** Update task creation instructions to include terminal command execution ([a581d29](https://github.com/Ronnasayd/aipp/commit/a581d29))
- **[✨ Features]** Refine task creation instructions for clarity and format adherence ([04901f1](https://github.com/Ronnasayd/aipp/commit/04901f1))
- **[✨ Features]** Restore task reviewer instructions with detailed guidelines for task refinement and team interaction ([b122a75](https://github.com/Ronnasayd/aipp/commit/b122a75))
- **[✨ Features]** Add task creation tool with detailed instructions for taskmaster integration ([ae458df](https://github.com/Ronnasayd/aipp/commit/ae458df))
- **[✨ Features]** Enhance search functionality by adding top_n parameter for result ranking ([ba07916](https://github.com/Ronnasayd/aipp/commit/ba07916))

### **2026-01-21**

- **[✨ Features]** Remove outdated run command instructions and add style guide references for code generation ([1778eb0](https://github.com/Ronnasayd/aipp/commit/1778eb0))

### **2026-01-20**

- **[✨ Features]** Update copilot instructions and enhance task implementation guidelines for clarity and completeness ([f3eb152](https://github.com/Ronnasayd/aipp/commit/f3eb152))

### **2025-12-21**

- **[✨ Features]** Translate and update instructions for srs and tasks generation to english, enhancing clarity and consistency ([3492493](https://github.com/Ronnasayd/aipp/commit/3492493))

### **2025-12-19**

- **[✨ Features]** Restore and update guidelines for asking questions ([aa8f39e](https://github.com/Ronnasayd/aipp/commit/aa8f39e))
- **[✨ Features]** Add guidelines for asking questions and integrate into mcp server ([7f3d583](https://github.com/Ronnasayd/aipp/commit/7f3d583))
- **[🧹 Chores]** Translate to english ([50ccf20](https://github.com/Ronnasayd/aipp/commit/50ccf20))
- **[🧹 Chores]** Translate to english ([55a4d2d](https://github.com/Ronnasayd/aipp/commit/55a4d2d))

### **2025-12-16**

- **[📚 Documentation]** Translate instructions to english for consistency and clarity ([7f6d5d9](https://github.com/Ronnasayd/aipp/commit/7f6d5d9))
- **[🐛 Bug Fixes]** Update error messages to english for consistency and clarity ([0f10971](https://github.com/Ronnasayd/aipp/commit/0f10971))
- **[📚 Documentation]** Update developer instructions to improve clarity and consistency in software development guidelines ([a880371](https://github.com/Ronnasayd/aipp/commit/a880371))
- **[✨ Features]** Add comprehensive guidelines for english language teaching and assessment ([1316e8c](https://github.com/Ronnasayd/aipp/commit/1316e8c))

### **2025-12-15**

- **[✨ Features]** Enhance task markdown generation to include descriptions and additional fields ([f9274c8](https://github.com/Ronnasayd/aipp/commit/f9274c8))
- **[📚 Documentation]** Add validation instructions for rules, avoidance, preview code, and action plan ([9da10d9](https://github.com/Ronnasayd/aipp/commit/9da10d9))

### **2025-12-05**

- **[🐛 Bug Fixes]** Enhance attachment extraction logic to handle file paths and improve matching ([fd06c57](https://github.com/Ronnasayd/aipp/commit/fd06c57))
- **[🐛 Bug Fixes]** Update version numbers in root and version endpoints to 0.6.4 ([86c1431](https://github.com/Ronnasayd/aipp/commit/86c1431))

### **2025-12-04**

- **[📚 Documentation]** Add comprehensive usability documentation and workflow guidelines ([06ca4f7](https://github.com/Ronnasayd/aipp/commit/06ca4f7))

### **2025-12-01**

- **[♻️ Refactoring]** Rename functions to include 'mcp' prefix for consistency ([59eb3f3](https://github.com/Ronnasayd/aipp/commit/59eb3f3))

### **2025-11-27**

- **[📚 Documentation]** Add instruction to include relevant code snippets in markdown format ([430ff8b](https://github.com/Ronnasayd/aipp/commit/430ff8b))
- **[🐛 Bug Fixes]** Improve attachment extraction logic to handle optional comments in file paths ([ae3c558](https://github.com/Ronnasayd/aipp/commit/ae3c558))

### **2025-11-18**

- **[🧹 Chores]** Add new dependencies to requirements.txt ([3468872](https://github.com/Ronnasayd/aipp/commit/3468872))

### **2025-11-14**

- **[📚 Documentation]** Enhance workflow instructions for task implementation with detailed checks and references ([3b7fcf1](https://github.com/Ronnasayd/aipp/commit/3b7fcf1))

### **2025-10-30**

- **[📚 Documentation]** Add task_master section with detailed task workflow instructions ([d3c2819](https://github.com/Ronnasayd/aipp/commit/d3c2819))

### **2025-10-29**

- **[📚 Documentation]** Add initial changelog entries for 2025‑10‑29 and update generate‑documentation instructions ([18e0bd1](https://github.com/Ronnasayd/aipp/commit/18e0bd1))
- **[📚 Documentation]** Add initial changelog entries for 2025‑10‑29 with features, bug fixes, documentation updates, and refactoring details ([1ac50a1](https://github.com/Ronnasayd/aipp/commit/1ac50a1))
- **[✨ Features]** Add initial changelog with features, bug fixes, documentation updates, and refactoring details ([aed572b](https://github.com/Ronnasayd/aipp/commit/aed572b))
- **[📚 Documentation]** Update generate-documentation instructions with detailed file purpose and structure guidelines ([8d56ae4](https://github.com/Ronnasayd/aipp/commit/8d56ae4))

### **2025-10-24**

- **[✨ Features]** Enable headless mode in get_cookies function for improved automation ([1cd41b2](https://github.com/Ronnasayd/aipp/commit/1cd41b2))
- **[✨ Features]** Add comprehensive cybersecurity instructions for secure software development and operations ([30bc11d](https://github.com/Ronnasayd/aipp/commit/30bc11d))
- **[✨ Features]** Add comprehensive coding guidelines and best practices to copilot.instructions.md ([b23a71e](https://github.com/Ronnasayd/aipp/commit/b23a71e))

### **2025-10-21**

- **[✨ Features]** Enhance my_search_references function to support optional rootproject and globs parameters; add ag_search function for improved codebase searching ([1f11f14](https://github.com/Ronnasayd/aipp/commit/1f11f14))

### **2025-10-20**

- **[✨ Features]** Implement search functionality in search_engine module; add my_search_references tool and update developer instructions ([2156a74](https://github.com/Ronnasayd/aipp/commit/2156a74))

### **2025-10-13**

- **[✨ Features]** Add prd generation instructions and template handling in my_generate_prd function; update documentation workflow instructions ([3998654](https://github.com/Ronnasayd/aipp/commit/3998654))

### **2025-10-10**

- **[✨ Features]** Add my_generate_docs_init function to return documentation generation instructions ([d93b105](https://github.com/Ronnasayd/aipp/commit/d93b105))
- **[📚 Documentation]** Enhance documentation structure and provide detailed file descriptions in generate-documentation.instructions.md ([86fdbc8](https://github.com/Ronnasayd/aipp/commit/86fdbc8))
- **[✨ Features]** Add documentation workflow instructions and enhance git diff handling in my_generate_docs_update function ([ea3e61c](https://github.com/Ronnasayd/aipp/commit/ea3e61c))

### **2025-10-09**

- **[✨ Features]** Add input_text extraction from request body in generate_embeddings function ([e63c875](https://github.com/Ronnasayd/aipp/commit/e63c875))
- **[🧹 Chores]** Update logging file path to /tmp for consistency across modules ([d35035a](https://github.com/Ronnasayd/aipp/commit/d35035a))

### **2025-10-07**

- **[✨ Features]** Update my_get_context function to accept multiple parameters for context generation ([6800a0b](https://github.com/Ronnasayd/aipp/commit/6800a0b))
- **[♻️ Refactoring]** Update my_run_command to use rootproject instead of cwd for directory execution ([47e44fb](https://github.com/Ronnasayd/aipp/commit/47e44fb))

### **2025-10-03**

- **[✨ Features]** Add task implementation instructions and attachment references to prompt documentation ([8a5944d](https://github.com/Ronnasayd/aipp/commit/8a5944d))

### **2025-10-02**

- **[♻️ Refactoring]** Clean up attachment extraction logic and improve prompt handling in chat function ([c730205](https://github.com/Ronnasayd/aipp/commit/c730205))
- **[✨ Features]** Add attachment extraction function and integrate it into chat completion process ([d39e151](https://github.com/Ronnasayd/aipp/commit/d39e151))
- **[♻️ Refactoring]** Enhance file exclusion logic and improve read_file function parameters ([30fc9a4](https://github.com/Ronnasayd/aipp/commit/30fc9a4))

### **2025-10-01**

- **[✨ Features]** Add meta extraction and merging functions for tasks and subtasks in my_mcp_server ([799cc04](https://github.com/Ronnasayd/aipp/commit/799cc04))
- **[✨ Features]** Add my_developer_workflow function to load and return developer workflow instructions ([585b964](https://github.com/Ronnasayd/aipp/commit/585b964))
- **[♻️ Refactoring]** Improve path handling and enhance markdown generation in my_mcp_server ([8ba5da9](https://github.com/Ronnasayd/aipp/commit/8ba5da9))
- **[✨ Features]** Add my_styleguide function to return style guide for specified programming language ([f29cf5b](https://github.com/Ronnasayd/aipp/commit/f29cf5b))
- **[🧹 Chores]** Update .gitignore to include .github and remove teste.py file ([4ad102d](https://github.com/Ronnasayd/aipp/commit/4ad102d))

### **2025-09-30**

- **[♻️ Refactoring]** Enhance logging in chat method and adjust response handling in call_copilot ([752c825](https://github.com/Ronnasayd/aipp/commit/752c825))

### **2025-09-29**

- **[✨ Features]** Convert call_copilot function to asynchronous and update api calls accordingly ([191794a](https://github.com/Ronnasayd/aipp/commit/191794a))
- **[✨ Features]** Refactor copilotapi methods to be asynchronous and update authentication flow ([360854a](https://github.com/Ronnasayd/aipp/commit/360854a))

### **2025-09-27**

- **[♻️ Refactoring]** Update logging level to info and streamline logging configuration in copilotapi and ollama ([e00970a](https://github.com/Ronnasayd/aipp/commit/e00970a))
- **[✨ Features]** Implement streaming response handling in call_copilot function and add test script for openai integration ([8cf3b3e](https://github.com/Ronnasayd/aipp/commit/8cf3b3e))
- **[♻️ Refactoring]** Simplify chat response handling and remove unused chat_complete method ([0b14835](https://github.com/Ronnasayd/aipp/commit/0b14835))
- **[♻️ Refactoring]** Update logging configuration to debug level and replace logging calls with logger instance in copilotapi ([c68e219](https://github.com/Ronnasayd/aipp/commit/c68e219))
- **[✨ Features]** Refactor get_cookies function to be asynchronous and update related calls in copilotapi ([6708464](https://github.com/Ronnasayd/aipp/commit/6708464))
- **[✨ Features]** Enhance logging in copilotapi chat methods for improved debugging ([6fb7135](https://github.com/Ronnasayd/aipp/commit/6fb7135))
- **[✨ Features]** Add logging to copilotapi methods for better traceability ([cf07e51](https://github.com/Ronnasayd/aipp/commit/cf07e51))
- **[✨ Features]** Add comprehensive developer instructions for software development and debugging processes ([7b1bb04](https://github.com/Ronnasayd/aipp/commit/7b1bb04))

### **2025-09-25**

- **[♻️ Refactoring]** Update my_code_review and my_convert_markdown_to_tasks functions to use rootproject parameter instead of cwd ([b842fbd](https://github.com/Ronnasayd/aipp/commit/b842fbd))
- **[✨ Features]** Refactor my_convert_markdown_to_tasks function to accept cwd and create tasks.json in specified directory ([66d60bd](https://github.com/Ronnasayd/aipp/commit/66d60bd))
- **[✨ Features]** Implement markdown to tasks conversion and add test script for validation ([b0b9e88](https://github.com/Ronnasayd/aipp/commit/b0b9e88))
- **[✨ Features]** Add main entry point to start mcp server and include example test calls ([fecb551](https://github.com/Ronnasayd/aipp/commit/fecb551))
- **[✨ Features]** Enhance task conversion functions to support markdown format and improve validation ([f00d803](https://github.com/Ronnasayd/aipp/commit/f00d803))

### **2025-09-24**

- **[🐛 Bug Fixes]** Update authorization handling in auth method to include github-bearer token for requests ([6d448c4](https://github.com/Ronnasayd/aipp/commit/6d448c4))
- **[✨ Features]** Implement streaming response handling in copilotapi and update chat method to support streaming ([75790da](https://github.com/Ronnasayd/aipp/commit/75790da))
- **[✨ Features]** Add tokenizer capabilities and additional parameters for model configuration ([113eeb0](https://github.com/Ronnasayd/aipp/commit/113eeb0))
- **[🧹 Chores]** Update server port from 11435 to 11434 in copilot ollama api proxy ([ff1ac8a](https://github.com/Ronnasayd/aipp/commit/ff1ac8a))
- **[🐛 Bug Fixes]** Update error handling to re-authenticate on 401 status code in copilotapi ([9c373b3](https://github.com/Ronnasayd/aipp/commit/9c373b3))

### **2025-09-23**

- **[✨ Features]** Remove expand_task.json and update taskmaster.request.json with new prd processing logic; add tasksmaster-template.json for task schema validation ([cd0189d](https://github.com/Ronnasayd/aipp/commit/cd0189d))
- **[🐛 Bug Fixes]** Handle 400 response by re-authenticating and refreshing token in copilotapi ([8f41742](https://github.com/Ronnasayd/aipp/commit/8f41742))
- **[✨ Features]** Implement copilotapi and associated functionalities for github copilot integration; update requirements and add initial module files ([87936a5](https://github.com/Ronnasayd/aipp/commit/87936a5))

### **2025-09-22**

- **[✨ Features]** Implement copilotapi class with chat and create_chat methods for github copilot integration ([e8b3d65](https://github.com/Ronnasayd/aipp/commit/e8b3d65))
- **[✨ Features]** Add expand_task.json with task breakdown and subtasks generation logic ([b095800](https://github.com/Ronnasayd/aipp/commit/b095800))

### **2025-09-20**

- **[🐛 Bug Fixes]** Update command arguments for my_run_command in my_mcp_client_stdio.py ([961ab19](https://github.com/Ronnasayd/aipp/commit/961ab19))

### **2025-09-19**

- **[✨ Features]** Implement flexible model naming and enhance model validation in ollama api proxy server ([d414f2f](https://github.com/Ronnasayd/aipp/commit/d414f2f))
- **[🐛 Bug Fixes]** Update remote ollama url and clear excluded paths in proxy server configuration ([bed810b](https://github.com/Ronnasayd/aipp/commit/bed810b))
- **[✨ Features]** Enhance logging functionality in ollama api proxy server and add openai-compatible endpoints ([8ed3d79](https://github.com/Ronnasayd/aipp/commit/8ed3d79))
- **[✨ Features]** Implement ollama api proxy server with request logging and model management endpoints ([a168b67](https://github.com/Ronnasayd/aipp/commit/a168b67))

### **2025-09-18**

- **[✨ Features]** Add comprehensive guidelines for creating software requirements specification (srs) documents ([ba1872e](https://github.com/Ronnasayd/aipp/commit/ba1872e))

### **2025-09-17**

- **[✨ Features]** Add new plan template for project and task management with detailed structure ([52723b9](https://github.com/Ronnasayd/aipp/commit/52723b9))
- **[🐛 Bug Fixes]** Update documentation instructions to reflect changes in file naming conventions and structure. ([2acd947](https://github.com/Ronnasayd/aipp/commit/2acd947))

### **2025-09-16**

- **[✨ Features]** Add 'design' category to tasks in tasks template for improved categorization ([0e89d59](https://github.com/Ronnasayd/aipp/commit/0e89d59))
- **[✨ Features]** Remove summary and notes fields from requirements in srs and tasks templates for clarity ([d386c5b](https://github.com/Ronnasayd/aipp/commit/d386c5b))
- **[✨ Features]** Enhance srs and tasks templates with detailed user stories and requirements structure ([3820914](https://github.com/Ronnasayd/aipp/commit/3820914))
- **[✨ Features]** Remove epics, prioritization, and roadmap sections from tasks template for simplification ([0a26b4f](https://github.com/Ronnasayd/aipp/commit/0a26b4f))
- **[✨ Features]** Update prd structure and add prompt template file ([a685983](https://github.com/Ronnasayd/aipp/commit/a685983))

### **2025-09-12**

- **[✨ Features]** Add tasks template json structure for project management ([3ce1f48](https://github.com/Ronnasayd/aipp/commit/3ce1f48))
- **[✨ Features]** Update prd and srs instructions to include structured input fields and optional parameters ([6731e61](https://github.com/Ronnasayd/aipp/commit/6731e61))
- **[✨ Features]** Add general recommendations for srs generation process ([d7a643c](https://github.com/Ronnasayd/aipp/commit/d7a643c))
- **[✨ Features]** Add prd and srs templates for structured documentation ([17eecb5](https://github.com/Ronnasayd/aipp/commit/17eecb5))
- **[♻️ Refactoring]** Update file paths to reflect new project structure in my_mcp_server.py ([1147d37](https://github.com/Ronnasayd/aipp/commit/1147d37))
- **[✨ Features]** Update output format to markdown template for task generation instructions ([40b6186](https://github.com/Ronnasayd/aipp/commit/40b6186))
- **[✨ Features]** Add structured instructions for generating tasks from requirements across multiple methodologies ([eb3b633](https://github.com/Ronnasayd/aipp/commit/eb3b633))
- **[✨ Features]** Add comprehensive instructions for generating prd and srs documents ([cef05f1](https://github.com/Ronnasayd/aipp/commit/cef05f1))
- **[📚 Documentation]** Update srs structure formatting for consistency across instructions ([cf7876d](https://github.com/Ronnasayd/aipp/commit/cf7876d))

### **2025-09-11**

- **[🧹 Chores]** Remove install script for generating context and coverage links ([0b08a62](https://github.com/Ronnasayd/aipp/commit/0b08a62))
- **[🧹 Chores]** Update file permissions and relocate requirements file to src directory ([f475f8e](https://github.com/Ronnasayd/aipp/commit/f475f8e))
- **[🧹 Chores]** Rename markdown and python files to appropriate directories for better organization ([6014938](https://github.com/Ronnasayd/aipp/commit/6014938))
- **[🚧 Other Changes]** First commit ([f70e7ce](https://github.com/Ronnasayd/aipp/commit/f70e7ce))

---

Generated on 2026-11-04 13:15:41
