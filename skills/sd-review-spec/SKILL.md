---
name: sd-review-spec
description: "Review and correct a feature's spec documents (spec.md, design.md, tasks.md, requirements.md, context-map.md, ADRs) by verifying every claim against the real code, classifying gaps by severity, and applying fixes. Use when user says 'review this spec', 'audit the spec against the code', 'find gaps in the spec', 'check spec inconsistencies', 'find implicit requirements', or 'validate design.md and tasks.md'."
model: claude-opus-5-5[1m]
---

## Guide: Technical Spec Review (gaps, inconsistencies, implicit requirements)

Audit spec docs (spec.md, design.md, tasks.md, requirements.md, context-map.md, cited ADRs) against actual code, then apply corrections. Spec = hypothesis, never truth. Ask user once before editing (Step 4).

| #   | Step                 | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Output / Gate                                                          |
| --- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| 1   | Gather               | List feature spec dir; count lines (whole vs parts); read every file fully + cited ADRs                                                                                                                                                                                                                                                                                                                                                                | Full picture of problem, goals, ACs, design, tasks, requirements       |
| 2   | Verify vs code       | Confirm each decision/assumption/contract in source — checklist: [verification-checklist.md](references/verification-checklist.md)                                                                                                                                                                                                                                                                                                                     | Claim → confirmed / false / unverifiable                               |
| 3   | Classify             | Group findings by severity (table below)                                                                                                                                                                                                                                                                                                                                                                                                               | Report to user                                                         |
| 4   | Confirm scope        | **One** question round: (a) severity groups to fix now (offer "report only"); (b) design decisions with >1 reasonable solution → options + technical implication each                                                                                                                                                                                                                                                                                  | User answers before any edit                                           |
| 5   | Apply fixes          | Tracker task per file/group (in-progress → complete). Per-file edits: [fix-by-file.md](references/fix-by-file.md)                                                                                                                                                                                                                                                                                                                                      | Docs consistent with each other + code                                 |
| 5.5 | Re-verify High fixes | After applying every High-severity fix, re-run Step 2 (Verify vs code) scoped to the files/claims touched by those fixes. If any High finding remains (new or unresolved), repeat Steps 4-5.5 on the remaining items. Bounded to 3 rounds total. If High findings still exist after round 3, STOP — do not apply a 4th fix unsupervised — and escalate to the user with the remaining findings (BLOCKED / TRIED / NEED format if the project uses it). | Zero High findings, or an explicit escalation with the user's decision |
| 6   | Sync derived system  | Only if spec feeds separate tracker (taskmaster): [taskmaster-sync.md](references/taskmaster-sync.md)                                                                                                                                                                                                                                                                                                                                                  | Only derived fields changed                                            |
| 7   | Residue check        | Grep every replaced term/snippet (nonexistent command, removed FK, old route, truncation marker) across touched files; each remaining hit must be intentional (explains the change)                                                                                                                                                                                                                                                                    | Zero forgotten leftovers                                               |
| 8   | Report               | See report table below                                                                                                                                                                                                                                                                                                                                                                                                                                 | Direct summary to user                                                 |

## Severity (Step 3)

| Level                           | Examples                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High                            | Breaks existing contract (API, CLI output, component props, exported signature, error/exit behavior); cited command/API/flag missing in installed version; corrupted/truncated content in doc; validation rejecting a real system case (e.g. input in format not guaranteed by its producer); missing invariant/constraint that logic assumes; success criterion with no real test |
| Medium                          | External dependency (relation, service, file, env var) can be absent on valid path; justification doesn't match cited code; task underestimates blast radius of contract change; accepted consequence unrecorded; unspecified data normalization/format                                                                                                                            |
| Inconsistencies / implicit reqs | Docs stale vs each other (one superseded another); declared deps diverge from real tracker; incomplete "files to modify"; broken req ID ↔ task ID traceability; out-of-scope item unrelated to card; type/value specified but unused in any rule                                                                                                                                   |

Notes:

- Re-verification loop (Step 5.5) applies **only to High**. Medium and
  Inconsistency stay single-pass (fix once per Step 5, no re-verification) —
  their cost of being wrong is lower, and re-verifying every Medium would
  make routine reviews expensive for little gain.
- Round count and "same finding vs new finding" are judged by the agent: a
  fix that only moved a line number is the same finding resolved; a fix that
  triggered a different claim to break is a new finding and still counts
  toward the 3-round budget.
- Step 7 (Residue check) still runs once at the end, after the Step 5.5 loop
  closes (clean or escalated) — it's a grep sweep for leftovers, not a
  code-correctness check, so it doesn't repeat per round.

## Report (Step 8)

| #   | Include                                                                                     |
| --- | ------------------------------------------------------------------------------------------- |
| 1   | Fixes by severity — don't repeat full earlier report                                        |
| 2   | Decisions that change implementation — highlight separately (matter most to task executors) |
| 3   | State explicitly: no build/test run when change was docs only                               |
| 4   | Items deliberately kept despite being raised as possible problem + reason                   |

## Reference files

- [references/verification-checklist.md](references/verification-checklist.md) — 10-point stack-agnostic code verification list (entry points, access control, data contracts, runtime inputs, errors, reused patterns, versions, state write paths, affected tests, atomicity/side effects)
- [references/fix-by-file.md](references/fix-by-file.md) — per-file edit rules (spec, design, tasks, requirements, context-map, ADRs)
- [references/taskmaster-sync.md](references/taskmaster-sync.md) — disposable-script procedure to sync tracker derived fields
