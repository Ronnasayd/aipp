## Mandatory rules that must always be followed

- Every user question → interactive tool, never plain text. Claude:
  `AskUserQuestion`. Multiple questions: `grilling` skill.

- When task list exists (multi-step work), use `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` to give user feedback. Mark tasks complete as done, don't batch.

- Whenever you modify a component or screen → run tests using Playwright (or a similar E2E tool) before finalizing.

- Whenever lint, type, or test errors are reported, fix them, even if they were not caused by your changes.

- Never treat documentation (`markdown files`,`memories`) as absolute truth. Only the implemented code should be treated as the truth.

- Never assume the code is correct without tests to validate it.

- TDD mandatory when repo/project already adopts tests (existing test suite/framework present): write failing test first (Red), then minimal code to pass (Green), then refactor. No large unverified code blocks — small loops only. If repo has no test setup, don't impose one unprompted.

- Evidence over trust: before asking human review, provide proof change works — passing test logs, screenshots/recordings of E2E or visual tests. No "should work" claims.

- Vertical slices only: implement thin end-to-end slices (tracer bullets) through all layers, not horizontal layers (all DB, then all API, then all UI). Each slice testable and validated before next.

- Whenever you create sub-agents, specify that they must use `caveman` in _full mode_.

- For sub-agents with simple tasks, use the `Haiku` model, and for medium tasks, use `Sonnet`.

- Avoid reading entire files unless necessary; prefer reading only relevant excerpts.

- Use `grilling` to request clarification from the user when necessary.

- If a task is complex, use `sequentialthinking` to break it down into smaller tasks.

- In any time evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.

## Documentation Language

Markdown files under `docs/`, `.specs/` (and nested dirs of those) must be in $MD_LANGUAGE.
