---
model: haiku
disable-model-invocation: true
---

Thoroughly analyze the changes and create a clear, concise commit message following the _Conventional Commits_ format. Do not start the commit message with anything other than: feat, fix, docs, style, refactor, perf, test, or chore. Do not include emojis. Ensure the message accurately reflects the changes made.

If the changes introduce a breaking change (API removed/renamed, behavior change that breaks existing callers, incompatible config/schema change), signal it in combined mode: add `!` right after the type/scope and before the `:`, AND add a `BREAKING CHANGE: <description>` footer explaining what broke and how to migrate. Example:

```
feat(api)!: remove endpoint /v1/users

BREAKING CHANGE: /v1/users removed, use /v2/users instead
```

If the changes do not warrant a commit, respond with "No commit needed." and stop.

Check the current branch with `git branch --show-current`.

- Not one of `master`, `main`, `develop`, `homolog`: run `git commit` with the generated message.
- On one of those protected branches: use `AskUserQuestion` (in Portuguese) to ask whether to create a new branch for this commit. Show the proposed branch name in the question.
  - Yes: run `git switch -c <prefix>/<description>`, then `git commit` with the generated message. `<prefix>` comes from the commit type: `feat` → `feature`, every other type keeps its name (`fix`, `chore`, `docs`, `refactor`, `perf`, `test`, `style`). `<description>` is a short kebab-case summary of the change (lowercase, ASCII, max ~5 words), e.g. `feature/add-user-export`.
  - No: do not commit; display the message on the screen so the user can copy it.

Your final response must contain the complete commit message verbatim in a code block, alongside any other fields your final response requires.
