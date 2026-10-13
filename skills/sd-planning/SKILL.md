---
name: sd-planning
description: Turn an SRS and context map into verified specs, requirements table, and planning docs — the second half of feature planning. Use when user says 'generate specs from this SRS', 'turn this SRS into a plan', 'continue planning from the requirements doc', or hands over an SRS file produced by sd-interview.
model: claude-opus-5-5[1m]
---

# Steps

See [diagram](references/diagram.md) for a visual flow overview.

**Input required:** an SRS file path (`docs/srs/yyyy-mm-dd-<short-description>.md`, from `sd-interview` or supplied directly by the user) and, when available, the context map produced alongside it. If either is missing, ask the user for the SRS path before continuing — do not run `/sd-interview` yourself; direct the user to it if no SRS exists yet.

Add the following steps as tasks using the `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` tools. Update the status as you progress through each step to keep the user informed.

1. Read the SRS and context map in full. If the context map is missing or stale (file paths that no longer resolve, flows that changed since it was generated), re-run `/context-map` using the SRS requirements as the task description before continuing.
2. Execute the `/tlc-spec-driven` skill to generate a plan/spec, using the SRS as the source of requirements and the context map as verified anchors/dependents/risks.
3. Execute the `/spec-to-requirements-table` skill to generate a `requirements.md` file.
4. **Verifier pass (always-on, author ≠ verifier):** dispatch a fresh sub-agent — no inherited context from steps 1-3 — to run `/sd-review-spec` in report-only mode against the generated `spec.md`, `design.md`, `tasks.md`, `requirements.md`, and any cited ADRs. Give it only: the SRS file path, and the feature's spec dir path. It audits every doc claim against the real code and checks the full set covers everything the SRS needs — scope, constraints, edge cases, dependencies, and every requirement in `requirements.md` traced to a task. It does not edit anything; it returns the severity-classified gap report (same table as `/sd-review-spec` step 8). If gaps exist: show them to the user and apply fixes per `/sd-review-spec` steps 4-7 before continuing. Do not skip this step and do not ask the user whether to run it — only ask what to do with findings.
5. Once planning is complete, ask the user if they wish to register the feature in _taskmaster_. If the answer is "yes," use the `/sd-insert-taskmaster` skill.
6. Check the definitions in [docs-adr](./references/docs-adr.md) and consider offering to create an ADR when the criteria are met.
7. At the end of the session, evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.
