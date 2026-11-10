#!/usr/bin/python3
"""UserPromptSubmit hook: block prompts that carry credentials in plain text.

Reuses secret_scan (detect-secrets + its regex fallback) and adds a
prompt-only keyword pattern, because detect-secrets misses free-text
credentials such as `user:x pass:y` or `senha: ...` mid-sentence.
"""

import json
import os
import re
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from secret_scan import is_allowlisted_line, scan_content_for_secrets  # noqa: E402
from utils import get_by_key, get_hooks_logger  # noqa: E402

logger = get_hooks_logger("SecretGuard")

# why: `pass:x`, `senha=x`, `token: x` in prose are the leaks seen in real
# session logs that detect-secrets' KeywordDetector does not flag.
PROMPT_KEYWORD = re.compile(
    r"\b(?:pass(?:word|wd)?|senha|pwd|secret|token|api[_-]?key)\s*[:=]\s*"
    r"[\"']?(?P<value>[^\s\"';,]+)",
    re.IGNORECASE,
)
# why: values that reference a secret instead of containing one
# (<pass>, [secret], $VAR, ${VAR}, ***) must not block the prompt.
PLACEHOLDER = re.compile(r"^(?:[<\[$*{]|\.env$)")
MIN_SECRET_LENGTH = 4


def scan_keywords(prompt: str) -> list[dict]:
    """Find keyword=value credentials whose value is not a placeholder.

    Args:
        prompt: The user's prompt text.

    Returns:
        A finding dict (type, line) per flagged, non-allowlisted line.
    """
    lines = prompt.split("\n")
    findings = []
    for i, line in enumerate(lines):
        for match in PROMPT_KEYWORD.finditer(line):
            value = match.group("value")
            if len(value) < MIN_SECRET_LENGTH or PLACEHOLDER.match(value):
                continue
            if not is_allowlisted_line(lines, i + 1):
                findings.append({"type": "Keyword Credential", "line": i + 1})
    return findings


def find_secrets(prompt: str) -> dict[int, set[str]]:
    """Merge detect-secrets and keyword findings into line -> finding types.

    Args:
        prompt: The user's prompt text.

    Returns:
        Mapping of 1-based line number to the set of finding types on it.
    """
    findings = scan_content_for_secrets(prompt, "prompt.yaml", logger)
    findings += scan_keywords(prompt)
    by_line: dict[int, set[str]] = {}
    for f in findings:
        line = f.get("line") or f.get("line_number")
        if line:
            by_line.setdefault(line, set()).add(f.get("type", "Secret"))
    return by_line


def build_reason(by_line: dict[int, set[str]]) -> str:
    """Describe where secrets were found without echoing their values.

    Args:
        by_line: Output of find_secrets.

    Returns:
        A user-facing block reason.
    """
    where = "; ".join(
        f"line {line}: {', '.join(sorted(kinds))}"
        for line, kinds in sorted(by_line.items())
    )
    return (
        f"secret-guard: possible credential in prompt ({where}). "
        "Move it to an env var or .env file and reference it by name, "
        "or add `# pragma: allowlist secret` to the line if it is fake."
    )


def main() -> None:
    """Run the hook: block the prompt when it contains a credential."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        logger.debug("Invalid JSON: %s", e)
        sys.exit(0)

    prompt = get_by_key(payload, "prompt") or ""
    by_line = find_secrets(prompt)
    if not by_line:
        sys.exit(0)

    logger.debug("Blocked prompt: secrets on lines %s", sorted(by_line))
    sys.stdout.write(json.dumps({"decision": "block", "reason": build_reason(by_line)}))
    sys.exit(0)


if __name__ == "__main__":
    main()
