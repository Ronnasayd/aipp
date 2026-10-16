#!/usr/bin/python3
"""PreToolUse hook: block dev-server commands run outside tmux/screen.

Avoids orphaned background processes.
"""

import io
import json
import os
from pathlib import Path
import re
import shlex
import sys

sys.path.insert(0, str(Path(__file__).parent))
from utils import get_by_key, get_hooks_logger, split_on_operators

LOG = get_hooks_logger("DevServerTmuxCheck")

DEV_SERVER_PATTERNS = [
    "npm run",
    "npm start",
    "npm exec",
    "yarn",
    "pnpm",
    "bun run",
    "bun --watch",
    "next dev",
    "next start",
    "vite",
    "webpack serve",
    "webpack --watch",
    "rollup --watch",
    "parcel",
    "nodemon",
    "ts-node-dev",
    "tsx watch",
    "tsc --watch",
    "astro dev",
    "nuxt dev",
    "nuxi dev",
    "ng serve",
    "remix vite:dev",
    "react-scripts start",
    "vue-cli-service serve",
    "storybook dev",
    "vitest",
    "jest --watch",
    "python -m http.server",
    "python -m flask run",
    "python manage.py runserver",
    "flask run",
    "fastapi dev",
    "uvicorn",
    "gunicorn",
    "hypercorn",
    "daphne",
    "waitress-serve",
    "celery",
    "rq worker",
    "dramatiq",
    "arq",
    "huey_consumer",
    "jupyter lab",
    "jupyter notebook",
    "marimo edit",
    "mkdocs serve",
    "hatch run",
    "poetry run",
    "uv run",
    "php -S",
    "php artisan serve",
    "php artisan queue:work",
    "php artisan queue:listen",
    "php artisan schedule:work",
    "symfony server:start",
    "composer run",
    "rails server",
    "bin/rails server",
    "rackup",
    "puma",
    "unicorn",
    "sidekiq",
    "jekyll serve",
    "go run",
    "air",
    "CompileDaemon",
    "reflex",
    "cargo run",
    "cargo watch",
    "trunk serve",
    "leptosfmt",
    "java -jar",
    "mvn spring-boot:run",
    "mvn quarkus:dev",
    "gradle bootRun",
    "gradle run",
    "gradlew bootRun",
    "gradlew run",
    "dotnet run",
    "dotnet watch",
    "dotnet test --watch",
    "mix phx.server",
    "iex -S mix",
    "rebar3 shell",
    "swift run",
    "swift test --parallel",
    "flutter run",
    "dart run",
    "hugo server",
    "zola serve",
    "eleventy --serve",
    "docker compose up",
    "docker-compose up",
    "docker logs -f",
    "docker stats",
    "kubectl logs -f",
    "kubectl port-forward",
    "kubectl proxy",
    "skaffold dev",
    "tilt up",
    "minikube tunnel",
    "redis-server",
    "redis-cli MONITOR",
    "mongod",
    "postgres",
    "mysqld",
    "mariadbd",
    "rabbitmq-server",
    "memcached",
    "elasticsearch",
    "ngrok http",
    "cloudflared tunnel",
    "ssh -N",
    "ollama serve",
    "comfyui",
    "vllm serve",
    "llama-server",
    "http-server",
    "serve",
    "live-server",
    "caddy run",
    "nginx",
    "apachectl",
]


def _unquoted_text(segment: str) -> str:
    """Reconstruct a command segment keeping only its unquoted tokens.

    Drops any token that came from inside '...' or "..." (e.g. the commit
    message in `git commit -m "npm run dev"`), so quoted text can't trigger
    a false match against DEV_SERVER_PATTERNS.

    Args:
        segment: A single shell command segment (already split on operators).

    Returns:
        The segment's unquoted tokens rejoined with spaces.
    """
    stream = io.StringIO(segment)
    lexer = shlex.shlex(stream, posix=True)
    lexer.whitespace_split = True
    lexer.commenters = ""
    tokens = []
    try:
        while True:
            start = stream.tell()
            token = lexer.get_token()
            if token is None:
                break
            raw = segment[start : stream.tell()]
            if raw.strip().startswith(("'", '"')):
                continue
            tokens.append(token)
    except ValueError:
        return segment
    return " ".join(tokens)


def is_dev_server(command: str) -> bool:
    """Check whether a shell command starts a long-running dev server.

    Only the text before the first heredoc marker is scanned, split on shell
    operators (&&, ||, ;, |, newlines) and stripped of quoted text, so a
    dev-server pattern occurring inside a quoted string (e.g. a commit
    message) doesn't trigger a false match. Patterns must also match on word
    boundaries: previously any text mentioning "invite" matched "vite" and
    blocked plain file writes.

    Args:
        command: The full shell command line submitted to the Bash tool.

    Returns:
        True when the command line invokes a known dev server.
    """
    head = command.split("<<", 1)[0]
    segments = split_on_operators(head)
    text = " ".join(_unquoted_text(segment) for segment in segments).lower()
    return any(
        re.search(rf"(?<![\w.-]){re.escape(pattern)}(?![\w.-])", text)
        for pattern in DEV_SERVER_PATTERNS
    )


def in_multiplexer() -> str | None:
    """Detect whether the current shell runs inside tmux or screen.

    Returns:
        "tmux" or "screen" when detected, else None.
    """
    tmux_val = os.environ.get("TMUX", "")
    if tmux_val and Path(tmux_val.split(",")[0]).exists():
        return "tmux"
    if os.environ.get("STY"):
        return "screen"
    return None


def main() -> None:
    """Read the PreToolUse payload from stdin and deny non-tmux dev servers."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        LOG.debug("Failed to parse JSON: %s", e)
        sys.exit(0)

    if get_by_key(payload, "tool_name") != "Bash":
        sys.exit(0)

    tool_input = get_by_key(payload, "tool_input") or {}
    command = get_by_key(tool_input, "command") or ""
    if not is_dev_server(command):
        sys.exit(0)

    multiplexer = in_multiplexer()
    if multiplexer:
        LOG.debug("dev server command allowed inside %s", multiplexer)
        sys.exit(0)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "Dev server commands should run inside tmux or screen to "
                "prevent orphaned processes. Start a tmux session first or "
                "run the command in the background."
            ),
        }
    }
    LOG.debug("[blocked]: %s", json.dumps(output, ensure_ascii=False))
    print(json.dumps(output, ensure_ascii=False))  # noqa: T201
    sys.exit(0)


if __name__ == "__main__":
    main()
