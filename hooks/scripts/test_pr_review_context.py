"""Tests for the SessionStart open-PR review summary hook."""

# pylint: disable=missing-param-doc,missing-return-doc,missing-any-param-doc
# pylint: disable=missing-type-doc,missing-return-type-doc
# why: test names and docstrings state intent; fake runners need no param docs

from __future__ import annotations

import json

import pr_review_context
import pytest  # type: ignore[import-not-found]  # pylint: disable=import-error

GITHUB_REMOTES = (
    "origin\tgit@github.com:o/r.git (fetch)\norigin\tgit@github.com:o/r.git (push)"
)

OPEN_PR = {
    "number": 81,
    "url": "https://github.com/o/r/pull/81",
    "state": "OPEN",
    "headRefName": "feat/x",
    "baseRefName": "master",
    "reviewDecision": "CHANGES_REQUESTED",
    "latestReviews": [
        {"author": {"login": "github-actions"}, "state": "CHANGES_REQUESTED"},
        {"author": {"login": "alice"}, "state": "COMMENTED"},
    ],
}


def threads_payload(resolved_flags: list[bool]) -> str:
    """GraphQL reviewThreads response with one node per resolved flag."""
    nodes = [{"isResolved": flag} for flag in resolved_flags]
    return json.dumps(
        {"data": {"repository": {"pullRequest": {"reviewThreads": {"nodes": nodes}}}}}
    )


def ok(output: str) -> dict:
    """Successful run_command_cwd result."""
    return {"success": True, "output": output, "error": ""}


def fail() -> dict:
    """Failed run_command_cwd result."""
    return {"success": False, "output": "", "error": "boom"}


def make_runner(
    *,
    branch: str = "feat/x",
    remotes: str = GITHUB_REMOTES,
    pr: dict | None = None,
    threads: list[bool] | None = None,
    graphql_ok: bool = True,
) -> tuple[list[str], object]:
    """Fake run_command_cwd routing on the command prefix; records each call."""
    calls: list[str] = []

    def runner(cmd: str, cwd: str | None = None, timeout: int = 30) -> dict:
        del cwd, timeout
        calls.append(cmd)
        if cmd.startswith("git rev-parse"):
            return ok(branch)
        if cmd.startswith("git remote"):
            return ok(remotes)
        if cmd.startswith("gh pr view"):
            return ok(json.dumps(pr)) if pr is not None else fail()
        if cmd.startswith("gh api graphql"):
            return ok(threads_payload(threads or [])) if graphql_ok else fail()
        return fail()

    return calls, runner


@pytest.fixture
def use_runner(monkeypatch: pytest.MonkeyPatch):
    """Install a fake runner on the hook module and return its call log."""

    def install(**kwargs) -> list[str]:
        calls, runner = make_runner(**kwargs)
        monkeypatch.setattr(pr_review_context, "run_command_cwd", runner)
        monkeypatch.setattr(pr_review_context.shutil, "which", lambda _: "/usr/bin/gh")
        return calls

    return install


def test_open_pr_with_reviews_renders_summary(use_runner) -> None:
    """Open PR with reviews: number, url, decision, reviewers, threads, hint."""
    use_runner(pr=OPEN_PR, threads=[False, False, True, False])

    context = pr_review_context.build_context("/repo")

    assert context is not None
    assert "PR #81 (feat/x → master): https://github.com/o/r/pull/81" in context
    assert "Decision: CHANGES_REQUESTED" in context
    assert (
        "Latest reviews: github-actions CHANGES_REQUESTED, alice COMMENTED" in context
    )
    assert "Unresolved threads: 3" in context
    assert "`gh pr view 81 --comments`" in context
    assert "`gh api repos/o/r/pulls/81/comments`" in context


def test_open_pr_without_reviews_or_threads_is_silent(use_runner) -> None:
    """No review and no unresolved thread means nothing to report."""
    use_runner(
        pr={**OPEN_PR, "latestReviews": [], "reviewDecision": ""}, threads=[True]
    )

    assert pr_review_context.build_context("/repo") is None


def test_unresolved_thread_alone_triggers_summary(use_runner) -> None:
    """An inline thread without a formal review still counts as review."""
    use_runner(
        pr={**OPEN_PR, "latestReviews": [], "reviewDecision": ""}, threads=[False]
    )

    context = pr_review_context.build_context("/repo")

    assert context is not None
    assert "Decision: none" in context
    assert "Latest reviews: none" in context
    assert "Unresolved threads: 1" in context


def test_merged_pr_is_silent(use_runner) -> None:
    """gh pr view can return a merged PR for the branch; only OPEN counts."""
    use_runner(pr={**OPEN_PR, "state": "MERGED"}, threads=[False])

    assert pr_review_context.build_context("/repo") is None


def test_no_pr_for_branch_is_silent(use_runner) -> None:
    """gh pr view failing (no PR for branch) produces nothing."""
    use_runner(pr=None)

    assert pr_review_context.build_context("/repo") is None


def test_detached_head_skips_gh(use_runner) -> None:
    """Detached HEAD has no branch, so gh is never called."""
    calls = use_runner(branch="HEAD", pr=OPEN_PR)

    assert pr_review_context.build_context("/repo") is None
    assert not any(c.startswith("gh ") for c in calls)


def test_non_github_remote_skips_gh(use_runner) -> None:
    """A repo without a github.com remote never pays for a gh call."""
    calls = use_runner(remotes="origin\tgit@gitlab.com:o/r.git (fetch)", pr=OPEN_PR)

    assert pr_review_context.build_context("/repo") is None
    assert not any(c.startswith("gh ") for c in calls)


def test_missing_gh_binary_is_silent(
    use_runner, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without gh on PATH the hook stays quiet and runs nothing."""
    calls = use_runner(pr=OPEN_PR)
    monkeypatch.setattr(pr_review_context.shutil, "which", lambda _: None)

    assert pr_review_context.build_context("/repo") is None
    assert calls == []


def test_graphql_failure_still_reports_reviews(use_runner) -> None:
    """If the threads query fails, reviews alone still produce the summary."""
    use_runner(pr=OPEN_PR, graphql_ok=False)

    context = pr_review_context.build_context("/repo")

    assert context is not None
    assert "Unresolved threads: unknown" in context


def test_graphql_failure_without_reviews_is_silent(use_runner) -> None:
    """Unknown thread count plus no reviews gives no evidence of review."""
    use_runner(pr={**OPEN_PR, "latestReviews": []}, graphql_ok=False)

    assert pr_review_context.build_context("/repo") is None
