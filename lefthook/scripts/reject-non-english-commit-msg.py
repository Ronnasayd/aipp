#!/usr/bin/env python3
"""git commit-msg hook: reject messages not written in English.

Symlinked into each project's .git/hooks/commit-msg by scripts/claude.install.sh
(the install loop symlinks every git-hooks/* into .git/hooks/).

Uses langdetect to classify the message language. Fails open (allows the
commit) when the message is too short/empty for reliable detection, or when
detection raises.

Bypass for a deliberate exception: git commit --no-verify
"""

from __future__ import annotations

from pathlib import Path
import sys

from _commit_msg_shared import strip_comments
from langdetect import (  # type: ignore[import-untyped]
    DetectorFactory,
    LangDetectException,
    detect_langs,
)

# why: langdetect's n-gram model is probabilistic; pin the seed so the same
# message always gets the same candidate ranking across runs/machines
DetectorFactory.seed = 0

# why: short commit subjects are inherently ambiguous (3-6 words); requiring
# "en" merely among the top candidates, rather than the single best guess,
# avoids rejecting real English messages that langdetect leans toward a
# lookalike language (e.g. Danish, Croatian) on so little text
_TOP_CANDIDATES = 2


def main() -> int:
    """Validate the commit message file passed as argv[1].

    Returns:
        0 if the message is English (or too short to classify), 1 if it was
        confidently detected as a different language.
    """
    if len(sys.argv) < 2:
        return 0
    raw = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    msg = strip_comments(raw).strip()
    if not msg:
        return 0

    try:
        candidates = detect_langs(msg)
    except LangDetectException:
        return 0

    top_langs = [c.lang for c in candidates[:_TOP_CANDIDATES]]
    if "en" in top_langs:
        return 0

    first_line = msg.splitlines()[0]
    sys.stderr.write(
        "\n✖ commit rejected: message does not look like English "
        f"(detected: {top_langs[0]}).\n"
        f"  message: {first_line}\n"
        "  Rewrite it in English, or use `git commit --no-verify` to bypass.\n\n"
    )
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as exc:  # never wedge commits on a hook bug
        sys.stderr.write(f"[reject-non-english-commit-msg] error: {exc}\n")
        sys.exit(0)
