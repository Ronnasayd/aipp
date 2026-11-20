#!/usr/bin/python3
"""Central eval runner for Claude Code hook scripts.

Usage:
    python3 eval.py                # run every *.json in this dir
    python3 eval.py <eval.json> ...

Each eval JSON: {"hook": "scripts/x.py", "mode": "exit_code"|"stdout", "cases": [...]}

mode "exit_code" (PreToolUse allow/deny hooks):
    tool_name       str, default "Bash"
    tool_input      dict
    cwd             optional, default repo root
    branch          optional; run in a throwaway git repo checked out on this
                     branch (also exported as CLAUDE_PROJECT_DIR)
    expect          "allow" | "deny"   (deny == exit code 2)
    expect_pattern  optional substr required in stderr

mode "stdout" (hooks that print JSON/context to stdout, always exit 0):
    input           dict, raw stdin payload
    raw_stdin       optional str sent verbatim instead of json.dumps(input)
    expect_output   bool, required
    expect_pattern  optional substr required in stdout
    cache_files     optional list[str] of cache file paths (supports "{session_id}"
                     and "{short_id}" placeholders) to delete before running
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

EVALS_DIR = Path(__file__).resolve().parent
HOOKS_DIR = EVALS_DIR.parent
REPO_ROOT = HOOKS_DIR.parent

GIT = shutil.which("git") or "git"

ENV = {
    **os.environ,
    "CLAUDE_PROJECT_DIR": os.environ.get("CLAUDE_PROJECT_DIR", str(REPO_ROOT)),
}


def run_exit_code_case(hook_path: Path, case: dict) -> tuple[bool, str]:
    """Run one allow/deny case; exit code 2 means deny.

    Args:
        hook_path: Hook script to execute.
        case: Eval case spec.

    Returns:
        tuple[bool, str]: (passed, failure message).
    """
    payload = {
        "tool_name": case.get("tool_name", "Bash"),
        "tool_input": case.get("tool_input", {}),
    }
    if "branch" in case:
        with tempfile.TemporaryDirectory() as repo:
            subprocess.run(  # noqa: S603 -- argv built from repo-owned paths, no shell
                [GIT, "init", "-q", "-b", case["branch"], repo],
                check=True,
            )
            return _run_exit_code(
                hook_path, payload, case, repo, {**ENV, "CLAUDE_PROJECT_DIR": repo}
            )
    return _run_exit_code(
        hook_path,
        payload,
        case,
        os.path.expandvars(case.get("cwd", str(REPO_ROOT))),
        ENV,
    )


def _run_exit_code(
    hook_path: Path, payload: dict, case: dict, cwd: str, env: dict
) -> tuple[bool, str]:
    """Run the hook with payload in cwd and check its allow/deny result.

    Args:
        hook_path: Hook script to execute.
        payload: JSON payload sent on stdin.
        case: Eval case spec.
        cwd: Working directory for the hook.
        env: Environment for the hook.

    Returns:
        tuple[bool, str]: (passed, failure message).
    """
    try:
        proc = subprocess.run(  # noqa: S603 -- argv built from repo-owned paths, no shell
            [sys.executable, str(hook_path)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=cwd,
            env=env,
            timeout=10,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"

    decision = "deny" if proc.returncode == 2 else "allow"
    expect = case.get("expect", "allow")
    if decision != expect:
        return False, (
            f"expected '{expect}' got '{decision}' "
            f"(exit={proc.returncode}, stderr={proc.stderr.strip()!r})"
        )

    pattern = case.get("expect_pattern")
    if pattern and pattern not in proc.stderr:
        return (
            False,
            f"expected stderr to contain {pattern!r}, got {proc.stderr.strip()!r}",
        )

    return True, ""


def run_stdout_case(hook_path: Path, case: dict) -> tuple[bool, str]:
    """Run one stdout case and match its output.

    Args:
        hook_path: Hook script to execute.
        case: Eval case spec.

    Returns:
        tuple[bool, str]: (passed, failure message).
    """
    session_id = case.get("input", {}).get("session_id", "")
    for template in case.get("cache_files", []):
        path = Path(template.format(session_id=session_id, short_id=session_id[:8]))
        path.unlink(missing_ok=True)

    stdin_data = (
        case["raw_stdin"] if "raw_stdin" in case else json.dumps(case.get("input", {}))
    )

    try:
        proc = subprocess.run(  # noqa: S603 -- argv built from repo-owned paths, no shell
            [sys.executable, str(hook_path)],
            input=stdin_data,
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            env=ENV,
            timeout=90,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"

    if proc.returncode != 0:
        return (
            False,
            f"expected exit 0, got {proc.returncode} (stderr={proc.stderr.strip()!r})",
        )

    stdout = proc.stdout.strip()
    expect_output = case.get("expect_output", False)

    if expect_output and not stdout:
        return (
            False,
            f"expected non-empty stdout, got empty (stderr={proc.stderr.strip()!r})",
        )
    if not expect_output and stdout:
        return False, f"expected empty stdout, got {stdout!r}"

    pattern = case.get("expect_pattern")
    if pattern and pattern not in stdout:
        return False, f"expected stdout to contain {pattern!r}, got {stdout!r}"

    return True, ""


RUNNERS = {"exit_code": run_exit_code_case, "stdout": run_stdout_case}


def run_eval_file(eval_path: Path) -> tuple[int, int]:
    """Run every case in one eval JSON.

    Args:
        eval_path: Eval JSON file.

    Returns:
        tuple[int, int]: (passed, failed) case counts.
    """
    spec = json.loads(eval_path.read_text())
    hook_path = HOOKS_DIR / spec["hook"]
    mode = spec.get("mode", "exit_code")
    runner = RUNNERS[mode]

    if not hook_path.exists():
        sys.stdout.write(f"[{eval_path.name}] SKIP: hook not found: {hook_path}\n")
        return 0, 0

    passed = 0
    failed = 0
    sys.stdout.write(f"\n=== {eval_path.name} -> {spec['hook']} ({mode}) ===\n")
    for case in spec.get("cases", []):
        name = case["name"]
        ok, msg = runner(hook_path, case)
        if ok:
            passed += 1
            sys.stdout.write(f"  PASS  {name}\n")
        else:
            failed += 1
            sys.stdout.write(f"  FAIL  {name}: {msg}\n")

    return passed, failed


def main() -> None:
    """Run the given eval files, or all of them, and exit 1 on failure."""
    args = sys.argv[1:]
    eval_files = (
        sorted(EVALS_DIR.glob("*.json")) if not args else [Path(a) for a in args]
    )

    if not eval_files:
        sys.stdout.write("No eval files found.\n")
        sys.exit(1)

    total_passed = 0
    total_failed = 0
    for eval_path in eval_files:
        p, f = run_eval_file(eval_path)
        total_passed += p
        total_failed += f

    sys.stdout.write(f"\n{'=' * 40}\n")
    sys.stdout.write(f"TOTAL: {total_passed} passed, {total_failed} failed\n")
    sys.exit(1 if total_failed else 0)


if __name__ == "__main__":
    main()
