#!/usr/bin/python3
"""PR Review Context Hook.

SessionStart hook. When the current branch has an open GitHub PR that already
received a formal review or has unresolved inline review threads, inject a
short summary (number, URL, decision, latest review per author, unresolved
thread count, and the gh commands to read the details) as additionalContext.

Review bodies are never injected: they are external text, and the agent can
fetch them on demand with the commands in the summary.

Silent (exit 0, no stdout) on detached HEAD, no github.com remote, gh missing
or unauthenticated, no open PR, or an open PR without any review.
"""

from __future__ import annotations

import json
import os
import shutil
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from utils import get_hooks_logger, project_dir, run_command_cwd  # noqa: E402

logger = get_hooks_logger("PrReviewContext")

MAX_STDIN = 1024 * 1024
COMMAND_TIMEOUT_SECONDS = 5
PR_FIELDS = "number,url,state,headRefName,baseRefName,reviewDecision,latestReviews"
THREADS_QUERY = (
    "query($owner:String!,$name:String!,$number:Int!){"
    "repository(owner:$owner,name:$name){pullRequest(number:$number){"
    "reviewThreads(first:100){nodes{isResolved}}}}}"
)


def run(cmd: str, cwd: str) -> str | None:
    """Run a shell command in cwd.

    Args:
        cmd: Shell command to run.
        cwd: Working directory.

    Returns:
        The command's stdout, or None when it failed or timed out.
    """
    result = run_command_cwd(cmd, cwd=cwd, timeout=COMMAND_TIMEOUT_SECONDS)
    if not result["success"]:
        return None
    return result["output"]


def current_branch(cwd: str) -> str | None:
    """Resolve the checked-out branch.

    Args:
        cwd: Repository directory.

    Returns:
        The branch name, or None on detached HEAD or outside a repository.
    """
    branch = run("git rev-parse --abbrev-ref HEAD", cwd)
    if not branch or branch == "HEAD":
        return None
    return branch


def has_github_remote(cwd: str) -> bool:
    """Check whether any git remote points at github.com.

    Args:
        cwd: Repository directory.

    Returns:
        True when a github.com remote exists.
    """
    return "github.com" in (run("git remote -v", cwd) or "")


def fetch_open_pr(cwd: str) -> dict | None:
    """Fetch the PR gh resolves for the current branch.

    Args:
        cwd: Repository directory.

    Returns:
        The PR fields when the PR is OPEN, else None.
    """
    raw = run(f"gh pr view --json {PR_FIELDS}", cwd)
    if not raw:
        return None
    pr = json.loads(raw)
    if pr.get("state") != "OPEN":
        return None
    return pr


def repo_slug(pr_url: str) -> tuple[str, str]:
    """Split a PR URL into owner and repository name.

    Args:
        pr_url: URL like https://github.com/<owner>/<name>/pull/<n>.

    Returns:
        The (owner, name) pair.
    """
    parts = pr_url.rstrip("/").split("/")
    return parts[-4], parts[-3]


def count_unresolved_threads(pr: dict, cwd: str) -> int | None:
    """Count the PR's unresolved inline review threads via GraphQL.

    Args:
        pr: PR fields from fetch_open_pr.
        cwd: Repository directory.

    Returns:
        The unresolved thread count, or None when the query failed.
    """
    owner, name = repo_slug(pr["url"])
    raw = run(
        f"gh api graphql -f query='{THREADS_QUERY}' "
        f"-F owner={owner} -F name={name} -F number={pr['number']}",
        cwd,
    )
    if not raw:
        return None
    try:
        pull = json.loads(raw)["data"]["repository"]["pullRequest"]
        nodes = pull["reviewThreads"]["nodes"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    return sum(1 for node in nodes if not node.get("isResolved"))


def format_reviews(reviews: list[dict]) -> str:
    """Render the latest review of each author on one line.

    Args:
        reviews: gh latestReviews entries.

    Returns:
        'login STATE, login STATE', or 'none' when empty.
    """
    rendered = [
        f"{(review.get('author') or {}).get('login', '?')} {review.get('state', '?')}"
        for review in reviews
    ]
    return ", ".join(rendered) or "none"


def render_summary(pr: dict, unresolved: int | None) -> str:
    """Render the markdown block injected as additionalContext.

    Args:
        pr: PR fields from fetch_open_pr.
        unresolved: Unresolved thread count, None when unknown.

    Returns:
        The markdown summary.
    """
    owner, name = repo_slug(pr["url"])
    number = pr["number"]
    branches = f"{pr.get('headRefName')} → {pr.get('baseRefName')}"
    threads = "unknown" if unresolved is None else str(unresolved)
    return "\n".join(
        [
            "## Open PR review",
            "",
            f"PR #{number} ({branches}): {pr['url']}",
            f"Decision: {pr.get('reviewDecision') or 'none'}",
            f"Latest reviews: {format_reviews(pr.get('latestReviews') or [])}",
            f"Unresolved threads: {threads}",
            f"Details: `gh pr view {number} --comments` / "
            f"`gh api repos/{owner}/{name}/pulls/{number}/comments`",
        ]
    )


def build_context(cwd: str) -> str | None:
    """Build the PR review summary for the branch checked out in cwd.

    Args:
        cwd: Repository directory.

    Returns:
        The summary, or None when there is no open PR with a review.
    """
    if not shutil.which("gh"):
        return None
    if not current_branch(cwd) or not has_github_remote(cwd):
        return None
    pr = fetch_open_pr(cwd)
    if pr is None:
        return None
    unresolved = count_unresolved_threads(pr, cwd)
    if not pr.get("latestReviews") and not unresolved:
        return None
    return render_summary(pr, unresolved)


def main() -> None:
    """Read the SessionStart payload and emit the PR review summary if any."""
    try:
        payload = json.loads(sys.stdin.read(MAX_STDIN))
    except (json.JSONDecodeError, TypeError, OSError):
        sys.exit(0)
    if not isinstance(payload, dict):
        sys.exit(0)

    context = build_context(project_dir(payload))
    if not context:
        sys.exit(0)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    logger.debug("[additionalContext]: %s", json.dumps(output, ensure_ascii=False))
    sys.stdout.write(json.dumps(output, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("pr_review_context hook failed")
        sys.exit(0)
