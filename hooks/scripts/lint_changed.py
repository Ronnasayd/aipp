#!/usr/bin/python3
"""Lint every changed file in the working tree; exit 1 if any fails.

Standalone entry for harness `grind.lintCommand`: no hook payload on stdin,
no loop counter, no pinned turn SHA (the harness owns those).
"""

from collections.abc import Callable
from fnmatch import fnmatch
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from golang_lint import maybe_run_golang_lint
from php_lint import maybe_run_php_lint
from python_lint import maybe_run_python_lint
from typescript_lint import maybe_run_typescript_lint
from utils import (
    find_project_root,
    get_hooks_logger,
    minify_json,
    run_command_cwd,
    run_jscpd,
)

logger = get_hooks_logger("LintChanged")
# Always skipped; `--ignore GLOB` adds to these.
DEFAULT_IGNORE = (
    "legacy/**",
    "node_modules/**",
    "vendor/**",
)
_LINT_DISPATCH: dict[str, Callable[..., dict]] = {
    ".py": maybe_run_python_lint,
    ".ts": maybe_run_typescript_lint,
    ".tsx": maybe_run_typescript_lint,
    ".go": maybe_run_golang_lint,
    ".php": maybe_run_php_lint,
}


def _porcelain_paths(project_root: str) -> set[str]:
    """Paths from `git status --porcelain`, relative to project_root."""
    result = run_command_cwd("git status --porcelain", cwd=project_root)
    if not result["success"]:
        return set()
    paths = set()
    for line in result["output"].splitlines():
        if len(line) < 4:
            continue
        # porcelain format: "XY path" (renames use "XY old -> new")
        entry = line[3:]
        if " -> " in entry:
            entry = entry.split(" -> ", 1)[1]
        paths.add(entry.strip('"'))
    return paths


def _staged_paths(project_root: str) -> set[str]:
    """Paths staged for commit (added/copied/modified), relative to project_root."""
    result = run_command_cwd(
        "git diff --cached --name-only --diff-filter=ACM", cwd=project_root
    )
    if not result["success"]:
        return set()
    return {line.strip() for line in result["output"].splitlines() if line.strip()}


def _ignore_globs(argv: list[str]) -> list[str]:
    """Collect globs from repeatable `--ignore GLOB` / `--ignore=GLOB` args."""
    globs = []
    for i, arg in enumerate(argv):
        if arg == "--ignore" and i + 1 < len(argv):
            globs.append(argv[i + 1])
        elif arg.startswith("--ignore="):
            globs.append(arg.split("=", 1)[1])
    return globs


def _is_ignored(rel_path: str, globs: list[str]) -> bool:
    """Match rel_path to any glob; the leading "/" lets `**/dir/**` hit root dirs."""
    return any(fnmatch(rel_path, g) or fnmatch("/" + rel_path, g) for g in globs)


def _groups(
    project_root: str, files: list[str]
) -> dict[tuple[Callable[..., dict], str], list[str]]:
    """Group existing changed files by (lint dispatcher, project root).

    Args:
        project_root: Directory the changed paths are relative to.
        files: Changed paths relative to `project_root`.

    Returns:
        dict: (dispatcher, project root) -> absolute paths, in `files` order.
    """
    groups: dict[tuple[Callable[..., dict], str], list[str]] = {}
    for rel_path in files:
        path = Path(project_root) / rel_path
        # why: a deleted file has nothing to lint, and find_project_root must
        # never be asked about a directory that no longer exists.
        if not path.exists():
            continue
        key = (_LINT_DISPATCH[path.suffix], find_project_root(str(path.parent)))
        groups.setdefault(key, []).append(str(path))
    return groups


def _lint_failures(project_root: str, files: list[str]) -> dict:
    """Lint changed files in one batch per (language, project root).

    Args:
        project_root: Directory the changed paths are relative to.
        files: Changed paths relative to `project_root`.

    Returns:
        dict: `{tool: result}` when one project root has failures, else
        `{relative_root: {tool: result}}`; a jscpd failure is always keyed
        `jscpd` at the top level. Empty when everything passes.
    """
    groups = _groups(project_root, files)
    by_root: dict[str, dict[str, dict]] = {}
    for (maybe_run_lint, group_root), paths in groups.items():
        results = maybe_run_lint(paths, jscpd=False)
        by_root.setdefault(group_root, {}).update(
            {
                tool: res
                for tool, res in results.items()
                if res and not res.get("success", True)
            }
        )
    failed_roots = {root: tools for root, tools in by_root.items() if tools}

    failures: dict = {}
    if len(failed_roots) == 1:
        failures.update(next(iter(failed_roots.values())))
    else:
        failures.update(
            {os.path.relpath(root, project_root): t for root, t in failed_roots.items()}
        )

    changed = [Path(path).resolve() for paths in groups.values() for path in paths]
    if changed:
        jscpd = run_jscpd(changed, project_root, logger, "LintChanged")
        if not jscpd.get("success", True):
            failures["jscpd"] = jscpd
    return failures


def main() -> int:
    """Lint changed files under cwd and print failures as JSON.

    With `--staged` (lefthook pre-commit) only files staged for the commit are
    linted; otherwise every file dirty in the working tree. Repeatable
    `--ignore GLOB` skips matching paths (e.g. `--ignore '**/unused/**'`).

    Returns:
        int: 1 if any file fails lint, else 0.
    """
    root = str(Path.cwd())
    changed = (
        _staged_paths(root) if "--staged" in sys.argv[1:] else _porcelain_paths(root)
    )
    ignore = [*DEFAULT_IGNORE, *_ignore_globs(sys.argv[1:])]
    files = sorted(
        p
        for p in changed
        if Path(p).suffix in _LINT_DISPATCH and not _is_ignored(p, ignore)
    )
    failures = _lint_failures(root, files)
    if failures:
        print(minify_json(failures))  # noqa: T201 - CLI output
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
