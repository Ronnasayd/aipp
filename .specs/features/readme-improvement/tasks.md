# README Improvement + Safe Global Config Linking Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/readme-improvement/design.md`
**Status**: Draft

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: `AGENTS.md` (TDD mandatory when a suite exists; evidence over trust), `lefthook/lefthook.yml` (pre-commit format/lint/test/comment-policy; commit-msg rules), existing sample `scripts/test_aipp_settings.py` (subprocess + temp `HOME`). No coverage thresholds configured.

| Code Layer                                | Required Test Type                                 | Coverage Expectation                                                                                                                            | Location Pattern                   | Run Command                                                    |
| ----------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------- |
| Shell helper (`scripts/_*.sh` function)   | unit (pytest via `bash -c` subprocess)             | 1:1 to LINK-01..07; every spec edge case (dangling link, spaces, second run)                                                                    | `scripts/test_*.py`                | `uv run --with pytest pytest scripts/test_link_with_backup.py` |
| Installer wiring (`scripts/*.install.sh`) | unit (static assertion on script text) + smoke run | LINK-08: no `rm` of the global path; one `link_with_backup` call per path; `bash -n` clean; claude fake-`HOME` smoke run shows symlink + `.bak` | `scripts/test_link_with_backup.py` | `uv run --with pytest pytest scripts/test_link_with_backup.py` |
| Docs (`*.md`)                             | none (doc check snippet)                           | Links resolve; flags exist in `install.sh`; aliases exist in `.aipp.alias.zshrc`; tables byte-identical                                         | -                                  | inline doc-check snippet (design.md "Doc check")               |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use                                  | Command                                                                                                                                                                                           |
| ---------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quick      | After helper / installer tasks               | `uv run --with pytest pytest scripts/test_link_with_backup.py`                                                                                                                                    |
| Full       | After AGENTS.md change and end of each phase | `uv run --with pytest pytest scripts/`                                                                                                                                                            |
| Build      | After doc tasks and final phase              | `uv run --with pytest pytest scripts/ && for f in scripts/*.sh; do bash -n "$f" \|\| exit 1; done` + doc-check snippet; lefthook pre-commit (format/lint/test/comment-policy) runs on each commit |

---

## Execution Plan

Phases are ordered and run sequentially - each phase completes before the next begins, and tasks within a phase execute in order.

### Phase 1: Safe linking

```
T1 → T2 → T3 → T4
```

### Phase 2: Test command

```
T5
```

### Phase 3: Docs

T8 also waits on T4 (Phase 1): the README warning describes the backup behavior.

```
T6 → T7 → T8 → T9
T4 → T8
```

---

## Task Breakdown

### T1: Create link_with_backup helper (TDD)

**What**: Sourced shell function `link_with_backup <src> <dst>` per design, driven by failing tests first.
**Where**: `scripts/_link-with-backup.sh` (tests in `scripts/test_link_with_backup.py`)
**Depends on**: None
**Reuses**: header/sourcing style of `scripts/_git-exclude.sh`; subprocess pattern of `scripts/test_aipp_settings.py:20-30`
**Requirement**: LINK-01, LINK-02, LINK-03, LINK-04, LINK-05, LINK-06, LINK-07
**Review rows**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Red: tests for missing dst, symlink dst, dangling symlink, regular file (`.bak` content == original, `readlink dst` == src), regular file with old `.bak` (overwritten), directory (unchanged, rc 1, stderr non-empty), missing parent dir, `backup: <dst> -> <dst>.bak` stdout line, paths with spaces, second call leaves `.bak` unchanged - run fails because helper is absent
- [ ] Green: helper implemented; quick gate passes
- [ ] FR-011: `mv` runs before `ln -s` in the helper (code read), so an `ln` failure leaves the original at `<dst>.bak`
- [ ] Test count: 10 tests pass in `scripts/test_link_with_backup.py`

**Tests**: unit
**Gate**: quick

**Commit**: `feat(scripts): add link_with_backup helper`

---

### T2: Route claude global settings through helper

**What**: Replace `scripts/claude.install.sh:123-126` delete-then-link block with `link_with_backup`; source the helper.
**Where**: `scripts/claude.install.sh`
**Depends on**: T1
**Reuses**: `scripts/_link-with-backup.sh`
**Requirement**: LINK-08
**Review rows**: FR-012, FR-016

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Static test added: script contains `link_with_backup "$SOURCE/claude/settings.json" "$HOME/$DEFAULT_FOLDER/settings.json"` and no `rm` of `$HOME/$DEFAULT_FOLDER/settings.json`
- [ ] `bash -n scripts/claude.install.sh` clean
- [ ] Smoke: `HOME=<tmp> LOCAL=<tmp-project> SOURCE=$PWD bash scripts/claude.install.sh` with a regular `<tmp>/.claude/settings.json` → `ls -la` shows symlink + `settings.json.bak` byte-identical (output captured as evidence)
- [ ] FR-016: installer has no `set -e` (grep), so a helper `return 1` does not abort the remaining steps
- [ ] Quick gate passes; test count: 11

**Tests**: unit
**Gate**: quick

**Commit**: `fix(scripts): back up claude settings before linking`

---

### T3: Route gemini global settings through helper

**What**: Replace `scripts/gemini.install.sh:95-98` block with `link_with_backup`; source the helper.
**Where**: `scripts/gemini.install.sh`
**Depends on**: T2
**Reuses**: `scripts/_link-with-backup.sh`
**Requirement**: LINK-08
**Review rows**: FR-013

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Static test case added for `$SOURCE/gemini/settings.json` → `$HOME/$DEFAULT_FOLDER/settings.json`, no `rm` of that path
- [ ] `bash -n scripts/gemini.install.sh` clean
- [ ] Quick gate passes; test count: 12

**Tests**: unit
**Gate**: quick

**Commit**: `fix(scripts): back up gemini settings before linking`

---

### T4: Route copilot global configs through helper

**What**: Replace both blocks in `scripts/copilot.install.sh:6-9` and `:11-14` with two `link_with_backup` calls; source the helper.
**Where**: `scripts/copilot.install.sh`
**Depends on**: T3
**Reuses**: `scripts/_link-with-backup.sh`
**Requirement**: LINK-08
**Review rows**: FR-014, FR-015

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Static test cases added for `mcp-config.json` and `config.json` under `$HOME/.copilot/`, no `rm` of either
- [ ] `bash -n scripts/copilot.install.sh` clean
- [ ] Full gate passes; test count in `scripts/test_link_with_backup.py`: 14

**Tests**: unit
**Gate**: full

**Commit**: `fix(scripts): back up copilot configs before linking`

---

### T5: Fix documented test command in AGENTS.md

**What**: Replace `cd src && uv run pytest` with `uv run --with pytest pytest scripts/` in the "Run tests" block only.
**Where**: `AGENTS.md`
**Depends on**: None
**Reuses**: NONE
**Requirement**: TEST-01, TEST-02, TEST-03
**Review rows**: FR-017, FR-018, FR-019

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] `grep -c "cd src && uv run pytest" AGENTS.md` = 0
- [ ] `uv run --with pytest pytest scripts/` collects ≥ 1 test and exits 0 (log captured)
- [ ] `git diff AGENTS.md` = owner's pending hunks + this hunk; commit stages only this hunk (`git add -p`)

**Tests**: none
**Gate**: full

**Commit**: `docs(agents): fix test command`

---

### T6: Move env-var table to docs/environment.md

**What**: Create `docs/environment.md` with a title and the README "Environment Variables" table verbatim.
**Where**: `docs/environment.md`
**Depends on**: None
**Reuses**: `git show HEAD:README.md` table rows
**Requirement**: REF-01
**Review rows**: FR-020

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Row diff between `git show HEAD:README.md` env table and new file is empty

**Tests**: none
**Gate**: build

**Commit**: `docs: move environment variables reference`

---

### T7: Move external-tools table to docs/external-tools.md

**What**: Create `docs/external-tools.md` with a title and the README "External Tools" table verbatim.
**Where**: `docs/external-tools.md`
**Depends on**: T6
**Reuses**: `git show HEAD:README.md` table rows
**Requirement**: REF-02
**Review rows**: FR-021

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [ ] Row diff between `git show HEAD:README.md` tools table and new file is empty

**Tests**: none
**Gate**: build

**Commit**: `docs: move external tools reference`

---

### T8: Rewrite README.md

**What**: Rewrite README in the spec README-01 section order, linking T6/T7 docs and `CONTRIBUTING.md`.
**Where**: `README.md`
**Depends on**: T4, T7
**Reuses**: `install.sh` flag `case` block; `.aipp.alias.zshrc`; current "Directory Structure" list
**Requirement**: README-01, README-02, README-03, README-04, README-05, README-06, README-07, README-08, README-09, README-10
**Review rows**: FR-022, FR-023, FR-024, FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, FR-035

**Tools**:

- MCP: NONE
- Skill: `generate-docs`

**Done when**:

- [ ] Section order matches README-01; no numeric component counts
- [ ] Doc check: every flag in flags table is a `case` label in `install.sh`; every alias is defined in `.aipp.alias.zshrc`; every relative link resolves (except `CONTRIBUTING.md`, created in T9 - re-checked there)
- [ ] Warning block states rc-file edits and `<path>.bak` backup; Uninstall section states manual `.bak` restore

**Tests**: none
**Gate**: build

**Commit**: `docs(readme): rewrite with quickstart and install side effects`

---

### T9: Create CONTRIBUTING.md

**What**: Contributor guide: adding a skill/agent, adding a hook, tests, commit rules.
**Where**: `CONTRIBUTING.md`
**Depends on**: T8
**Reuses**: `scripts/list_skills_agents.py`, `scripts/build-skill-index.py`, `claude/settings.json`, `hooks/README.md`, `lefthook/lefthook.yml`
**Requirement**: CONTRIB-01, CONTRIB-02, CONTRIB-03, CONTRIB-04, CONTRIB-05
**Review rows**: FR-036, FR-037, FR-038, FR-039, FR-040, FR-041, FR-042, FR-043

**Tools**:

- MCP: NONE
- Skill: `generate-docs`

**Done when**:

- [ ] Doc check: every relative link and script path in `CONTRIBUTING.md` resolves; README link to `CONTRIBUTING.md` now resolves
- [ ] Build gate passes

**Tests**: none
**Gate**: build

**Commit**: `docs: add contributing guide`

---

## Phase Execution Map

```
Phase 1 → Phase 2 → Phase 3

Phase 1:  T1 ------→ T2 ------→ T3 ------→ T4
Phase 2:  T5
Phase 3:  T6 ------→ T7 ------→ T8 ------→ T9
          (T4 ----------------→ T8)
```

---

## Task Granularity Check

| Task                   | Scope                      | Status                 |
| ---------------------- | -------------------------- | ---------------------- |
| T1: helper             | 1 function + its test file | ✅ Granular (TDD pair) |
| T2: claude call site   | 1 block, 1 file            | ✅ Granular            |
| T3: gemini call site   | 1 block, 1 file            | ✅ Granular            |
| T4: copilot call sites | 2 blocks, 1 file           | ✅ Cohesive            |
| T5: AGENTS.md          | 1 line                     | ✅ Granular            |
| T6: environment.md     | 1 file                     | ✅ Granular            |
| T7: external-tools.md  | 1 file                     | ✅ Granular            |
| T8: README.md          | 1 file                     | ✅ Granular            |
| T9: CONTRIBUTING.md    | 1 file                     | ✅ Granular            |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows    | Status   |
| ---- | ---------------------- | ---------------- | -------- |
| T1   | None                   | none             | ✅ Match |
| T2   | T1                     | T1 → T2          | ✅ Match |
| T3   | T2                     | T2 → T3          | ✅ Match |
| T4   | T3                     | T3 → T4          | ✅ Match |
| T5   | None                   | none             | ✅ Match |
| T6   | None                   | none             | ✅ Match |
| T7   | T6                     | T6 → T7          | ✅ Match |
| T8   | T4, T7                 | T4 → T8, T7 → T8 | ✅ Match |
| T9   | T8                     | T8 → T9          | ✅ Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says                   | Status |
| ---- | --------------------------- | --------------- | --------------------------- | ------ |
| T1   | Shell helper                | unit            | unit                        | ✅ OK  |
| T2   | Installer wiring            | unit + smoke    | unit (+ smoke in Done when) | ✅ OK  |
| T3   | Installer wiring            | unit            | unit                        | ✅ OK  |
| T4   | Installer wiring            | unit            | unit                        | ✅ OK  |
| T5   | Docs                        | none            | none                        | ✅ OK  |
| T6   | Docs                        | none            | none                        | ✅ OK  |
| T7   | Docs                        | none            | none                        | ✅ OK  |
| T8   | Docs                        | none            | none                        | ✅ OK  |
| T9   | Docs                        | none            | none                        | ✅ OK  |
