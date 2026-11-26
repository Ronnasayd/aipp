---
name: sd-planning
description: Generate a feature plan through iterative problem breakdown, codebase research, and clarifying questions before handing off to tlc-spec-driven and requirements-table generation. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', or 'walk through planning this feature'.
argument-hint: "[depth=low|medium|high] <feature request> — depth skips the step 3 depth question"
model: opus
effort: high
disable-model-invocation: true
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "2.1.0"
---

# sd-planning

Drives a feature from request to verified plan: `/tlc-spec-driven` writes the docs, an independent fresh sub-agent audits them against the code and the original request, and a depth-driven loop fixes the gaps. The verifier pass is always-on and author ≠ verifier. Track every step with `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList`. Flow: [diagram.md](references/diagram.md).

| #   | Step          | Action                                                                                                                                                                                             | Output / Gate                                            |
| --- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | Spec          | Run `/tlc-spec-driven` on the described problem                                                                                                                                                    | `spec.md`, `design.md`, `tasks.md`                       |
| 2   | Requirements  | Settle output language with the user first (`/spec-to-requirements-table` runs isolated, can't ask), then run it with the spec dir + language as arguments                                         | `requirements.md`                                        |
| 3   | Verifier pass | Depth from `depth=` arg, else ask once (`low`/`medium`/`high`); fresh opus/high sub-agent runs `/sd-review-spec` report-only; fix loop per depth — [verifier-pass.md](references/verifier-pass.md) | Zero High findings, or BLOCKED / TRIED / NEED escalation |
| 4   | Taskmaster    | Ask whether to register the feature; yes → `/sd-insert-taskmaster` with the feature tag                                                                                                            | Registered, or skipped by the user                       |
| 5   | ADR           | Check criteria in [docs-adr.md](references/docs-adr.md); offer an ADR when all are met                                                                                                             | ADR offered or not applicable                            |
| 6   | Memory        | Save only what the next session needs and can't rediscover from code, Git or CLAUDE.md (reason behind a decision, non-obvious invariant, user preference) via `ai-memory-durable-pages`            | Durable page, or nothing worth saving                    |

## Reference files

- [references/verifier-pass.md](references/verifier-pass.md) — step 3: depth question, verifier dispatch rules, fix-loop flowchart, round limits (3 `medium` / 5 `high`), settled list
- [references/diagram.md](references/diagram.md) — mermaid flow of all six steps
- [references/docs-adr.md](references/docs-adr.md) — ADR template, numbering, and the three criteria for offering one
