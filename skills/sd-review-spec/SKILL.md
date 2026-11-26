---
name: sd-review-spec
description: "Review and correct a feature's spec documents (spec.md, design.md, tasks.md, plan.md, checks.md, requirements.md, context-map.md, ADRs) by verifying every claim against the real code, classifying gaps by severity, and applying fixes. Use when user says 'review this spec', 'audit the spec against the code', 'find gaps in the spec', 'check spec inconsistencies', 'find implicit requirements', 'validate design.md and tasks.md', or 'validate plan.md and checks.md'."
argument-hint: "[depth=low|medium|high] [spec dir] — depth sets how far Step 5.5 re-verifies fixes; default medium"
model: opus
effort: high
---

## Guide: Technical Spec Review (gaps, inconsistencies, implicit requirements)

Audit spec docs (spec.md, design.md, tasks.md, or tlc-spec-lean's plan.md + checks.md, plus requirements.md, context-map.md, cited ADRs) against real code, then fix them. Spec = hypothesis, never truth. Code verification runs in a fresh-context subagent, never inline ([verifier-loop.md](references/verifier-loop.md)). Ask the user once, before any edit (Step 4).

## Review depth (argument)

`depth=low|medium|high` or the bare word; missing/unrecognized → `medium`. Changes only Step 5.5. Report-only runs never reach Step 5.5: sd-planning skips it and applies depth to its own loop; sd-lean-planning runs report-only.

| Depth            | Step 5.5 re-verifies fixes of                                    | Loop ends when                                   | Cost    | Use when                                            |
| ---------------- | ---------------------------------------------------------------- | ------------------------------------------------ | ------- | --------------------------------------------------- |
| low              | none (Step 5.5 skipped)                                          | n/a                                              | Lowest  | Quick audit, small spec, or report-only run         |
| medium (default) | High only                                                        | zero High findings, or escalation after 3 rounds | Medium  | Routine reviews                                     |
| high             | High; Medium and Inconsistencies only while the round has a High | zero High findings, or escalation after 5 rounds | Highest | Critical spec where a wrong Medium fix is expensive |

## Steps

| #   | Step                | Action                                                                                                                                                                                                                                                     | Output / Gate                                                            |
| --- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 1   | Gather              | List spec dir; count lines (whole vs parts); read every file fully + cited ADRs                                                                                                                                                                            | Full picture: problem, goals, ACs, design, tasks, requirements           |
| 2   | Verify vs code      | New fresh-context verifier ([verifier-loop.md](references/verifier-loop.md)) checks each decision/assumption/contract per [verification-checklist.md](references/verification-checklist.md)                                                                | Claim → confirmed / false / unverifiable, each with `path:line` evidence |
| 3   | Classify            | Severity + one disposition per finding (tables below)                                                                                                                                                                                                      | Report to user                                                           |
| 4   | Confirm scope       | **One** question round: (a) severity groups to fix now (offer "report only"); (b) design decisions with >1 reasonable solution → options + technical implication each; (c) ESCALATE findings, listed first → user confirms no change or supplies the fact  | User answers before any edit                                             |
| 5   | Apply fixes         | Tracker task per file/group (in-progress → complete); per-file rules: [fix-by-file.md](references/fix-by-file.md)                                                                                                                                          | Docs consistent with each other + code                                   |
| 5.5 | Re-verify fixes     | Per depth: new scoped verifier per round, repeat Steps 4-5.5 while High remains, max 3 (`medium`) / 5 (`high`) rounds, then STOP + escalate — rules in [verifier-loop.md](references/verifier-loop.md)                                                     | Zero High findings, or explicit escalation with the user's decision      |
| 6   | Sync derived system | Only if spec feeds a separate tracker (taskmaster): [taskmaster-sync.md](references/taskmaster-sync.md)                                                                                                                                                    | Only derived fields changed                                              |
| 7   | Residue check       | Once, after the 5.5 loop closes (clean or escalated): grep every replaced term/snippet (nonexistent command, removed FK, old route, truncation marker) across touched files, skipping `review/` (quotes old text on purpose); each hit must be intentional | Zero forgotten leftovers                                                 |
| 8   | Report              | Report table below                                                                                                                                                                                                                                         | Direct summary to user                                                   |

## Severity (Step 3)

| Level                           | Examples                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High                            | Breaks existing contract (API, CLI output, component props, exported signature, error/exit behavior); cited command/API/flag missing in installed version; corrupted/truncated content in doc; validation rejecting a real system case (e.g. input in format not guaranteed by its producer); missing invariant/constraint that logic assumes; success criterion with no real test |
| Medium                          | External dependency (relation, service, file, env var) can be absent on valid path; justification doesn't match cited code; task underestimates blast radius of contract change; accepted consequence unrecorded; unspecified data normalization/format                                                                                                                            |
| Inconsistencies / implicit reqs | Docs stale vs each other (one superseded another); declared deps diverge from real tracker; incomplete "files to modify"; broken req ID ↔ task ID traceability (lean: criterion ↔ check); out-of-scope item unrelated to card; type/value specified but unused in any rule                                                                                                         |

## Disposition (Step 3)

Exactly one per finding:

| Disposition | When                                                                                                         | Effect                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| PROPOSE FIX | Finding valid                                                                                                | Precise edit, applied in Step 5 if approved |
| CONTEST     | Finding wrong, with evidence the verifier could read: file + symbol, or a decision recorded in the spec docs | No edit; becomes settled                    |
| ESCALATE    | Finding looks wrong, but the evidence is outside the repo (team convention, verbal decision)                 | No edit; user decides in Step 4             |
| DECLINE     | Inconsistency-level finding not worth fixing (never High or Medium)                                          | Recorded, no edit; becomes settled          |

Rules: "it was intentional" is not evidence — without checkable evidence, ESCALATE or PROPOSE FIX. Never lower a severity; disagree → CONTEST + reason. Add spec text only when a human reader needs it, never just to satisfy the verifier; otherwise ESCALATE.

## Report (Step 8)

| #   | Include                                                                                     |
| --- | ------------------------------------------------------------------------------------------- |
| 1   | Fixes by severity — don't repeat full earlier report                                        |
| 2   | Decisions that change implementation — highlight separately (matter most to task executors) |
| 3   | State explicitly: no build/test run when change was docs only                               |
| 4   | Items deliberately kept (CONTEST + evidence, ESCALATE + user decision, DECLINE + reason)    |
| 5   | Whether verification was fresh-context (state it explicitly when it was not)                |
| 6   | Paths of the `review/verify-round-<N>.md` files and `review/settled.md`                     |
| 7   | Depth used (`low` / `medium` / `high`) and how many Step 5.5 rounds ran                     |

## Reference files

- [references/verifier-loop.md](references/verifier-loop.md) — fresh-context verifier spawn/prompt/output rules (Steps 2, 5.5) and Step 5.5 loop: round limits, same-vs-new finding, settled list, reopen rule
- [references/verification-checklist.md](references/verification-checklist.md) — 10-point stack-agnostic code verification list (entry points, access control, data contracts, runtime inputs, errors, reused patterns, versions, state write paths, affected tests, atomicity/side effects)
- [references/fix-by-file.md](references/fix-by-file.md) — per-file edit rules (spec, design, tasks, plan, checks, requirements, context-map, ADRs)
- [references/taskmaster-sync.md](references/taskmaster-sync.md) — disposable-script procedure to sync tracker derived fields
