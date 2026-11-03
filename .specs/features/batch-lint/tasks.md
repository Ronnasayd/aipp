# Batch Lint Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, the walk, check_proofs, the Verifier and the screens sub-agent).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: `.specs/features/batch-lint/design.md`
**Status**: Approved
**Approved**: 2026-11-03 - user: "Aprovar spec e tasks"
**Mutations**: 3
**Build**: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py scripts/; uv run ruff check hooks/scripts/lint_changed.py hooks/scripts/python_lint.py hooks/scripts/typescript_lint.py hooks/scripts/golang_lint.py hooks/scripts/php_lint.py hooks/scripts/utils.py hooks/scripts/test_lint_changed.py`

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: `AGENTS.md` (TDD mandatory when a suite exists; pytest via `uv run --with pytest pytest scripts/`). No pytest config in `pyproject.toml`; samples: `scripts/test_aipp_settings.py`, `scripts/test_link_with_backup.py`. Test mechanics: design.md `## Test Strategy`.

| Code Layer                       | Required Test Type                               | Coverage Expectation                                                                   | Location Pattern                     | Run Command                                                      |
| -------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------------------------- |
| Lint modules (`*_lint.py`)       | unit (fake executables logging argv)             | 1:1 to spec ACs; every listed edge case, per module where the edge case applies to all | `hooks/scripts/test_lint_changed.py` | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py` |
| Orchestrator (`lint_changed.py`) | integration (temp git repo, in-process `main()`) | Happy + every edge case + error paths                                                  | `hooks/scripts/test_lint_changed.py` | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py` |
| Shared helpers (`utils.py`)      | unit                                             | All branches of changed functions                                                      | `hooks/scripts/test_lint_changed.py` | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py` |

## Gate Check Commands

> Generated from codebase - confirm before Execute.

| Gate Level | When to Use                 | Command                                                                                                                                  |
| ---------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Quick      | After each module task      | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`                                                                         |
| Full       | After the orchestrator task | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py scripts/`                                                                |
| Build      | After the last task         | `uv run --with pytest pytest hooks/scripts/test_lint_changed.py scripts/; uv run ruff check <touched files>` (full line in `**Build**:`) |

---

## Execution Plan

### Phase 1: Batch every module, then switch the orchestrator

One phase: 7 tasks form a single dependency chain and fit one batch. The orchestrator is last so that, between commits, `lint_changed.py` keeps passing one-file lists to modules - every intermediate commit lints exactly what it linted before.

```
T1 → T2 → T3 → T4 → T5 → T6 → T7
```

---

## Task Breakdown

### T1: Set-based jscpd with lint timeout

**What**: `run_jscpd` takes `list[Path]`, keeps pairs touching any of them, runs with `timeout=LINT_TIMEOUT_S`; add `LINT_TIMEOUT_S = 300`; the four module call sites pass `[resolved]`.
**Where**: `hooks/scripts/utils.py`
**Depends on**: None
**Reuses**: `_filter_jscpd_duplicates_for_file` (`utils.py:253`), renamed `_filter_jscpd_duplicates`
**Requirement**: BLINT-04, BLINT-07

**Done when**:

- [x] Tests for C7, C8, C10a written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 3 tests pass (no silent deletions)

**Tests**: unit
**Gate**: quick
**Commit**: `refactor(hooks): make run_jscpd filter by a set of files`

---

### T2: List signature for every maybe_run_* (behaviour preserved)

**What**: `maybe_run_{python,typescript,golang,php}_lint(file_paths: list[str], jscpd: bool = True)`; each `main()` passes `lambda p: maybe_run_X([p] if p else [])`; `lint_changed._lint_failures` passes `[abs_path]` per file (still per file).
**Where**: `hooks/scripts/python_lint.py` (signature only; same mechanical edit in the three sibling modules and `lint_changed.py:83`)
**Granularity note**: deliberately one task - the signature switch must land atomically, or `lint_changed.py` would pass a `str` to a list-taking dispatcher (iterating characters, silently skipping lint) between commits. Until T3-T6, a module given K>1 files may process only per-file logic internally; no caller passes K>1 before T7.
**Depends on**: T1
**Reuses**: `run_lint_hook_main` (`utils.py:338`) unchanged
**Requirement**: BLINT-05, BLINT-11, BLINT-12

**Done when**:

- [x] Tests for C17, C18 (parametrized over the 4 modules) written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 8 tests pass

**Tests**: unit
**Gate**: quick
**Commit**: `refactor(hooks): take a file list in lint dispatchers`

---

### T3: Python tools run once over the file list

**What**: `_run_mypy/_run_ruff/_run_pylint` take `list[Path]`; `_exec` uses `shlex.join` and `timeout=LINT_TIMEOUT_S`; nonexistent / non-`.py` paths dropped.
**Where**: `hooks/scripts/python_lint.py`
**Depends on**: T2
**Reuses**: `parse_json_output`, `parse_jsonlines_output`, `truncate_large_output`
**Requirement**: BLINT-01, BLINT-03, BLINT-07, BLINT-12

**Done when**:

- [x] Tests for C1, C6, C10[python], C19, C20, C21[python], C25 written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 15 tests pass

**Tests**: unit
**Gate**: quick
**Commit**: `perf(hooks): batch mypy, ruff and pylint over all files`

---

### T4: TypeScript tools batched

**What**: `_run_typescript` / `_run_eslint` take `list[Path]`; `_exec` uses `shlex.join` + timeout.
**Where**: `hooks/scripts/typescript_lint.py`
**Depends on**: T3
**Reuses**: T3 pattern
**Requirement**: BLINT-08, BLINT-07, BLINT-12

**Done when**:

- [x] Tests for C11, C10[typescript], C21[typescript] written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 18 tests pass

**Tests**: unit
**Gate**: quick
**Commit**: `perf(hooks): batch tsc-files and eslint over all files`

---

### T5: PHP phpstan batched

**What**: `_run_phpstan` takes `list[Path]`; `_exec` uses `shlex.join` + timeout.
**Where**: `hooks/scripts/php_lint.py`
**Depends on**: T4
**Reuses**: T3 pattern
**Requirement**: BLINT-09, BLINT-07, BLINT-12

**Done when**:

- [x] Tests for C12, C10[php], C21[php] written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 21 tests pass

**Tests**: unit
**Gate**: quick
**Commit**: `perf(hooks): batch phpstan over all files`

---

### T6: Go tools batched with package dedupe and set filtering

**What**: gofmt gets the file list; go vet / golangci-lint get deduplicated package dirs; filters keep issues whose `./`-stripped path resolved against the project root equals a changed file, dropping `# <pkg>` headers; generated files dropped; `_exec` uses `shlex.join` + timeout.
**Where**: `hooks/scripts/golang_lint.py`
**Depends on**: T5
**Reuses**: `_filter_issues_by_file`, `_filter_lines_by_file`, `_is_generated`
**Requirement**: BLINT-10, BLINT-07, BLINT-12

**Done when**:

- [x] Tests for C13, C14, C15, C16, C10[go], C21[go] written first and red, then green
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py`
- [x] Test count: 27 tests pass

**Tests**: unit
**Gate**: quick
**Commit**: `perf(hooks): batch go vet, golangci-lint and gofmt`

---

### T7: Orchestrator groups by language and root, jscpd once, no cap

**What**: `lint_changed.py` drops nonexistent paths, groups by (dispatcher, `find_project_root`), calls `maybe_run(paths, jscpd=False)` per group, runs `run_jscpd(all_files, cwd, logger, "LintChanged")` once when any file remains, emits `{tool: res}` (nested by relative root when >1 root fails, `jscpd` always top level), removes `MAX_FILES`.
**Where**: `hooks/scripts/lint_changed.py`
**Depends on**: T6
**Reuses**: `_porcelain_paths`, `_staged_paths`, `_is_ignored`, `minify_json`
**Requirement**: BLINT-01, BLINT-02, BLINT-04, BLINT-06, BLINT-12

**Done when**:

- [x] Tests for C2, C3, C4, C5, C7a, C9, C18a, C22, C23, C24, C26 written first and red, then green
- [x] `test_changed.py` still imports its helpers: `uv run hooks/scripts/test_changed.py` exits 0
- [x] Gate check passes: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py scripts/`
- [x] Test count: 38 tests pass in `test_lint_changed.py`

**Tests**: integration
**Gate**: full
**Commit**: `perf(hooks): lint changed files in per-root batches`

---

## Checks

**C1** - With K changed `.py` files under one root, mypy, ruff and pylint are each invoked exactly once with all K paths (BLINT-01, AC 1)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_python_tools_called_once_with_all_files"`

**C2** - `.py` files under two roots produce one call per tool per root, each with only that root's files (BLINT-01, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_python_groups_by_project_root"`

**C3** - A failing tool yields top-level JSON key `ruff` and exit code 1 (BLINT-02, AC 3)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_failure_keyed_by_tool_exit_1"`

**C4** - Failures from two roots nest under relative root paths (`.` for cwd) (BLINT-02, AC 4)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_multi_root_failures_nested_by_root"`

**C5** - All tools passing (fake `npx` included) prints nothing and exits 0 (BLINT-02, AC 5)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_all_pass_silent_exit_0"`

**C6** - A tool exiting non-zero with non-JSON stdout is reported failed with raw stdout and stderr (BLINT-03, AC 6)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_crash_reports_raw_output"`

**C7** - `run_jscpd` keeps a pair where either side is in the given file set (BLINT-04, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_keeps_pairs_touching_set"`

**C7a** - `lint_changed.py` with mixed-language changed files invokes jscpd exactly once (BLINT-04, AC 1)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_invoked_once"`

**C8** - A report with no pair touching the set is treated as passing (BLINT-04, AC 3)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_unrelated_pairs_pass"`

**C9** - 51 changed `.py` files are all passed to ruff (BLINT-06, AC 1)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_no_file_cap"`

**C10** - Every language module's `_exec` runs with timeout 300 s (BLINT-07, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_lint_exec_timeout_300"`

**C10a** - `run_jscpd` runs with timeout 300 s (BLINT-07, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_timeout_300"`

**C11** - Two `.ts` files under one root give one tsc-files and one eslint call, each with both paths (BLINT-08, AC 1)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_typescript_tools_called_once"`

**C12** - Two `.php` files under one root give one phpstan call with both paths (BLINT-09, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_phpstan_called_once"`

**C13** - Two `.go` files give one gofmt call with both paths (BLINT-10, AC 3)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_gofmt_called_once"`

**C14** - Three `.go` files in two packages give one go vet and one golangci-lint call with the two package dirs (BLINT-10, AC 4)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_go_packages_deduplicated"`

**C15** - go vet lines (with `./` prefix and `# pkg` header) and golangci-lint issues for unchanged files in the package are dropped; a sibling file whose name ends with a changed file's name is not kept (BLINT-10, AC 5)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_go_issues_filtered_to_changed"`

**C16** - A go-bindata generated file is absent from every Go tool call (BLINT-10, AC 6)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_go_generated_excluded"`

**C17** - `maybe_run_python_lint([path])` on a ruff-failing file returns keys `mypy, ruff, pylint, jscpd` with ruff failed and runs jscpd for that file (BLINT-11, AC 1; BLINT-05, AC 4)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_single_file_mode_keys"`

**C18** - Each `maybe_run_*([])` invokes no tool and returns all-`None` results (BLINT-12)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_maybe_run_empty_list_no_tools"`

**C18a** - Orchestrator with only non-lintable changes invokes no tool (jscpd included) and exits 0 (BLINT-12; BLINT-04, AC 5)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_no_lintable_files_exit_0"`

**C19** - A deleted path is absent from every Python tool call (BLINT-12)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_missing_path_excluded"`

**C20** - A language tool reported not installed is skipped and treated as passing (BLINT-12)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_missing_tool_passes"`

**C21** - A path with a space reaches the tool as one argument, in every language module (BLINT-12)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_path_with_space_single_arg"`

**C22** - jscpd failure sits under top-level `jscpd` in both flat and nested output (BLINT-02, AC 7)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_key_top_level"`

**C23** - Orchestrator with all changed lintable files deleted invokes no jscpd (BLINT-04, AC 5)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_jscpd_skipped_when_no_files"`

**C24** - Orchestrator reports a duplicate pair touching a changed file under `jscpd` and exits 1 (BLINT-04, AC 2)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_orchestrator_reports_jscpd_pair"`

**C25** - A tool exceeding the timeout is reported failed with the timeout message and is invoked once (BLINT-07; BLINT-12 timeout edge case)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_timeout_reported_no_retry"`

**C26** - A changed file inside a deleted directory is excluded before grouping and the gate does not crash (BLINT-12)
Proof: `uv run --with pytest pytest hooks/scripts/test_lint_changed.py -k "test_deleted_dir_excluded"`

---

## Handoff

**Settled mid-build:** none
**Dispatched:** none
**Walked:** none

---

## Phase Execution Map

```
Phase 1:  T1 → T2 → T3 → T4 → T5 → T6 → T7
```

Execution is strictly sequential. 7 tasks fit one batch → inline execution, no batch sub-agents.
