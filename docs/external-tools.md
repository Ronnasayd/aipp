# External Tools

Non-native (non-coreutils) tools required or installed by this project's bash/python scripts.

| Tool                                                 | Purpose                                                                                                         |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `uv`                                                 | Python package/dependency manager                                                                               |
| spaCy models (`pt_core_news_sm`, `en_core_web_sm`)   | NLP models used by Python tooling                                                                               |
| `claude` (Claude Code CLI)                           | Plugin marketplace management                                                                                   |
| `rag-rat` plugin (cq27-dev/rag-rat)                  | Claude Code plugin: repo intelligence                                                                           |
| `codebase-memory-mcp` (DeusData/codebase-memory-mcp) | MCP server: repo intelligence fallback for languages rag-rat doesn't index here (162 languages via tree-sitter) |
| `caveman` plugin (JuliusBrussee/caveman)             | Claude Code plugin: token-compressed communication mode                                                         |
| `ponytail` plugin (DietrichGebert/ponytail)          | Claude Code plugin: lazy/minimal-code enforcement mode                                                          |
| `serena`                                             | Code agent / LSP-backed coding tool                                                                             |
| `rtk`                                                | Token-usage-reducing CLI proxy                                                                                  |
| `bat`                                                | Syntax-highlighted `cat` replacement                                                                            |
| `jq`                                                 | JSON processor                                                                                                  |
| `fzf`                                                | Fuzzy finder                                                                                                    |
| `lefthook`                                           | Git hooks manager                                                                                               |
| `ai-memory`                                          | Persistent cross-session memory CLI                                                                             |
| `curl`                                               | HTTP client (GitHub Contents API)                                                                               |
| `python3`                                            | Config merging, inline JSON parsing                                                                             |
| `skillspector` (via `uv run`)                        | Security scan of downloaded skills, quarantines findings                                                        |
| `security` (macOS Keychain CLI)                      | Stores/reads Claude OAuth token in `scripts/claude.accounts.sh`                                                 |
| `bwrap` (bubblewrap)                                 | Sandboxing for `scripts/ai-jail.sh`                                                                             |
| `docker`                                             | Runs sandbox mounts (`ai-jail.sh`) and the litellm proxy container                                              |
| `litellm` (Docker image `ghcr.io/berriai/litellm`)   | LLM proxy service, `docker/litellm/docker-compose.yml`                                                          |
| `ai-memory` container (`akitaonrails/ai-memory`)     | Docker image run by `aims`/`aimsllm` aliases in `.aipp.alias.zshrc`                                             |
| `codeburn` (via `npx`)                               | CLI run by `codeburn` alias                                                                                     |
| `agent-flow-app` (via `npx`)                         | CLI run by `afa` alias                                                                                          |
| `omniroute` (via `npx`)                              | CLI run by `omniroute` alias                                                                                    |
| `detect-secrets`                                     | Secret scanning in `hooks/scripts/secret_scan.py` (regex fallback if absent)                                    |
