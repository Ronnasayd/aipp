---
model: haiku
context: fork
background: false
---

Thoroughly analyze the changes and create a clear, concise commit message following the _Conventional Commits_ format. Do not start the commit message with anything other than: feat, fix, docs, style, refactor, perf, test, or chore. Do not include emojis. Ensure the message accurately reflects the changes made.

If the changes introduce a breaking change (API removed/renamed, behavior change that breaks existing callers, incompatible config/schema change), signal it in combined mode: add `!` right after the type/scope and before the `:`, AND add a `BREAKING CHANGE: <description>` footer explaining what broke and how to migrate. Example:

```
feat(api)!: remove endpoint /v1/users

BREAKING CHANGE: /v1/users removed, use /v2/users instead
```

If you are on one of these branches—`master`, `main`, `develop`, or `homolog`—simply display the message on the screen so the user can copy it; otherwise, execute the `git commit` command with the generated message. If the changes do not warrant a commit, respond with "No commit needed."

Your final response must contain the complete commit message verbatim in a code block, alongside any other fields your final response requires.
