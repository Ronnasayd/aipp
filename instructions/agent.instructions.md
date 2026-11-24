---
description: Agent behavior rules.
applyTo: "**/*"
---

## Mandatory rules — always follow

- User question → interactive tool, never plain text. Claude: `AskUserQuestion`. Many questions: `grilling` skill.

- `AskUserQuestion` must be fully contextualized, never terse. Question body: explain _why_ asked (what found in code, what trade-off) before choice. Option `description`: what picking it does/causes — not label restated. No truncated question/option text; full explanation every time.

- User asks question → answer only. No code change without explicit user authorization.

- Multi-step work → use `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` for feedback. Mark each task complete when done, no batching.

- Modify component/screen → run Playwright (or similar E2E) tests before finalizing.

- Lint/type/test errors in touched files → fix, even if not caused by you.

- Docs (`markdown files`, `memories`) not absolute truth. Only implemented code = truth.

- No code assumed correct without tests validating it.

- TDD mandatory when repo already has tests (suite/framework present): failing test first (Red), minimal code to pass (Green), then refactor. Small loops only, no big unverified blocks. No test setup in repo → don't impose one unprompted.

- Evidence over trust: before human review, give proof change works — passing test logs, screenshots/recordings of E2E or visual tests. No "should work" claims.

- Vertical slices only: thin end-to-end slices (tracer bullets) through all layers, not horizontal layers (all DB, then all API, then all UI). Each slice tested and validated before next.

- Task done (testing, execution, build) → kill all background processes/servers started, delete temp dirs generated.

- Anytime: evaluate what worth saving as permanent memory. Save only what next session needs and can't rediscover from code, Git, or CLAUDE.md — _reason_ behind decision, non-obvious invariant, user preference. Already in repo or only relevant to this conversation → don't save. Persist via `ai-memory-durable-pages` skill.

- Permanent memory scope: generic info (tool/CLI/MCP/library behavior, shared hooks, machine setup, user preferences, anything useful in another project) → save in `_global` (`memory_write_page` with `scope: "global"`). Project pages hold only what is specific to that project (its code, domain, decisions, config). Mixed content → split: generic part in `_global`, specific part in project. Before writing, search `_global` and update the existing page, never duplicate per project.

- Domain vocabulary: `GLOSSARY.md` (or `GLOSSARY-MAP.md`) exists → read before naming things, use its terms exactly. Term resolved/changed with user, or term conflicts with glossary → update via `domain-modeling` skill. No glossary yet → create it only once first term agreed with user, never from agent inference alone. Glossary holds terms only; reasons/gotchas go to ai-memory, not glossary.

- Self-contained task (no dependency on history, clear input, concise output, intermediate work not required in the main conversation) → use a sub-agent.

## Mandatory rules — hallucination protection

- "I don't know" allowed: uncertain or info missing → say so explicitly (e.g. "I don't have enough information to confidently assess this"). Never fill gaps with guesses.

- Quote before analyzing: long docs (>20k tokens) → first extract word-for-word quotes relevant to task, base analysis only on them, reference by number. None found → say "No relevant quotes found".

- Cite every factual claim: each claim about code, docs, external sources carries source (`path:line`, command output, URL, direct quote) for audit.

- Verify after generating: check each claim in response has supporting quote/source. None → retract claim (mark removal with `[]` when editing document).
