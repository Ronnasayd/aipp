# Environment Variables

Hook-specific env vars: [`hooks/ENVIRONMENTS.md`](../hooks/ENVIRONMENTS.md).

## Scripts

| Variable                                                                                                                                            | Default                       | Used in                                                           | Description                                                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_INSTALL_SKIP_AUTO_CONTEXT`                                                                                                                  | unset                         | `scripts/claude.install.sh`                                       | Set to `1` to skip regenerating the `<!-- INIT AUTO-CONTEXT -->` block in `AGENTS.md` on install.                               |
| `CLAUDE_INSTALL_SKIP_CLAUDE_MD`                                                                                                                     | unset                         | `scripts/claude.install.sh`                                       | Set to `1` to skip (re)writing `CLAUDE.md` on install.                                                                          |
| `SKIP_MCP_MERGE`                                                                                                                                    | unset                         | `scripts/claude.install.sh`                                       | Set to `1` to leave an existing project `.mcp.json` untouched (no merge, no relink). Ignored when the project has none yet.     |
| `LOCAL`                                                                                                                                             | `$PWD`                        | `scripts/_git-exclude.sh`                                         | Directory whose git repo receives the `.git/info/exclude` patterns. `install.sh` sets it before sourcing this helper.           |
| `CLAUDE_PROJECT_DIR`                                                                                                                                | project path                  | `scripts/claude.install.sh`, `scripts/statusline-command.sh`      | Local project dir written to `settings.local.json`; used to locate `rag-rat.toml`/index cbm for the statusline.                 |
| `AI_PROJECT_ROOT_DIR`                                                                                                                               | unset                         | `scripts/ai-jail.sh`                                              | Root dir (hooks/statusline/skills live here via symlinks) read-only-bind-mounted into the sandbox.                              |
| `AI_JAIL`                                                                                                                                           | unset                         | `scripts/ai-jail.sh`, `scripts/statusline-command.sh`             | Set to `1` inside the sandbox by `ai-jail.sh`; read by the statusline to show a jail indicator.                                 |
| `GITHUB_PAT_TOKEN`                                                                                                                                  | none (required)               | `scripts/update-external-tools.sh`, `claude/.mcp.json`            | GitHub PAT used to authenticate API calls when syncing external tools, and as the bearer token of the `aipp:github` MCP server. |
| `NERD_FONT`                                                                                                                                         | `1`                           | `scripts/statusline-command.sh`, `scripts/subagent-statusline.sh` | Set to anything other than `1` to disable Nerd Font glyphs in the statusline.                                                   |
| `CBM_PORT`                                                                                                                                          | `9749`                        | `scripts/statusline-command.sh`                                   | Port of the local codebase-memory web UI; the statusline probes `http://localhost:$CBM_PORT` to show its status dot.            |
| `CLAUDE_CONFIG_DIR`                                                                                                                                 | `$HOME/.claude`               | `scripts/statusline-command.sh`, `scripts/claude.refresh.sh`      | Claude config dir; used to locate the caveman-mode flag file, detect the `-L` (local) profile and derive `ACCOUNTS_DIR`.        |
| `ACCOUNTS_DIR`                                                                                                                                      | `$CLAUDE_CONFIG_DIR/accounts` | `scripts/claude.refresh.sh`                                       | Directory holding the per-account credential files whose OAuth tokens get refreshed.                                            |
| `CLAUDE_SECRETS_JSON`                                                                                                                               | `$HOME/.secrets/claude.json`  | `scripts/claude.warmup.sh`                                        | Single JSON file with the accounts used by the warmup/account-rotation workflow.                                                |
| `ANTHROPIC_BASE_URL`, `ANTHROPIC_MODEL`, `ANTHROPIC_API_KEY`, `CLAUDE_PROJECT_DIR`, `ENABLE_TOOL_SEARCH`, `ASDF_NODEJS_VERSION`, `CONTEXT7_API_KEY` | unset                         | `scripts/ai-jail.sh`                                              | Passed through into the sandbox when set (see `PASSTHROUGH_VARS`).                                                              |

## Hook decision backend

Read by `decide()` in `hooks/scripts/utils.py`, which hooks call to answer typed questions through a hosted classifier.

| Variable                | Default         | Used in                  | Description                                                                                     |
| ----------------------- | --------------- | ------------------------ | ----------------------------------------------------------------------------------------------- |
| `DECISION_BACKEND`      | `clef`          | `hooks/scripts/utils.py` | Selects the backend from `DECISION_BACKENDS`. Only `clef` exists; other values return an error. |
| `CLEF_MODEL`            | `clef`          | `hooks/scripts/utils.py` | Model name sent to the Cloudflare Clef API. Also part of the decision cache key.                |
| `CLOUDFLARE_ACCOUNT_ID` | none (required) | `hooks/scripts/utils.py` | Cloudflare account used to build the Clef API URL.                                              |
| `CLOUDFLARE_API_TOKEN`  | none (required) | `hooks/scripts/utils.py` | Bearer token for the Clef API. Without it or the account ID, `decide()` returns an error.       |

## MCP servers (`claude/.mcp.json`)

Unset values fall back to the placeholder `add-value-to-env-vars` unless a default is listed.

| Variable                         | Default                 | Server                  | Description                                                |
| -------------------------------- | ----------------------- | ----------------------- | ---------------------------------------------------------- |
| `GITHUB_PAT_TOKEN`               | placeholder             | `aipp:github`           | Bearer token for the GitHub Copilot MCP endpoint.          |
| `CONTEXT7_API_KEY`               | placeholder             | `aipp:context7`         | API key passed to `@upstash/context7-mcp`.                 |
| `OMNIROUTE_ADMIN_TOKEN`          | placeholder             | `aipp:omniroute`        | Bearer token for the local OmniRoute MCP endpoint.         |
| `SSH_MCP_HOST`                   | placeholder             | `aipp:ssh-mcp`          | SSH host.                                                  |
| `SSH_MCP_PORT`                   | placeholder             | `aipp:ssh-mcp`          | SSH port.                                                  |
| `SSH_MCP_USER`                   | placeholder             | `aipp:ssh-mcp`          | SSH user.                                                  |
| `SSH_MCP_PASSWORD`               | placeholder             | `aipp:ssh-mcp`          | SSH password.                                              |
| `MCP_POSTGRES_URL`               | placeholder             | `aipp:postgresql`       | PostgreSQL connection URL (`POSTGRES_URL`).                |
| `MCP_MYSQL_URL`                  | placeholder             | `aipp:mysql`            | MySQL connection URL (`MYSQL_URL`).                        |
| `MCP_MONGODB_URL`                | placeholder             | `aipp:mongodb`          | MongoDB connection URL (`MONGODB_URL`).                    |
| `MCP_MONGODB_DATABASE`           | placeholder             | `aipp:mongodb`          | MongoDB database name (`MONGODB_DATABASE`).                |
| `MCP_SQLITEDB_PATH`              | placeholder             | `aipp:sqlite`           | Path to the SQLite database file (`SQLITEDB_PATH`).        |
| `MCP_KEYCLOAK_BASE_URL`          | `http://localhost:8080` | `aipp:keycloak`         | Keycloak server URL.                                       |
| `MCP_KEYCLOAK_AUTH_METHOD`       | `client_credentials`    | `aipp:keycloak`         | Authentication method.                                     |
| `MCP_KEYCLOAK_CLIENT_ID`         | placeholder             | `aipp:keycloak`         | Client ID.                                                 |
| `MCP_KEYCLOAK_CLIENT_SECRET`     | placeholder             | `aipp:keycloak`         | Client secret.                                             |
| `MCP_KEYCLOAK_ADMIN_USERNAME`    | placeholder             | `aipp:keycloak`         | Admin username.                                            |
| `MCP_KEYCLOAK_ADMIN_PASSWORD`    | placeholder             | `aipp:keycloak`         | Admin password.                                            |
| `MCP_KEYCLOAK_DEFAULT_REALM`     | `master`                | `aipp:keycloak`         | Realm used when a call does not name one.                  |
| `MCP_GOOGLE_OAUTH_CLIENT_ID`     | placeholder             | `aipp:google-workspace` | Google OAuth client ID (`GOOGLE_OAUTH_CLIENT_ID`).         |
| `MCP_GOOGLE_OAUTH_CLIENT_SECRET` | placeholder             | `aipp:google-workspace` | Google OAuth client secret (`GOOGLE_OAUTH_CLIENT_SECRET`). |

LiteLLM stack vars (`LITELLM_MASTER_KEY`, `OMNIROUTER_API_KEY`): [`docker/litellm/README.md`](../docker/litellm/README.md).
