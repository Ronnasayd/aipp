---
name: sd-review-spec
description: "Review and correct a feature's spec documents (spec.md, design.md, tasks.md, plan.md, checks.md, requirements.md, context-map.md, ADRs) by verifying every claim against the real code, classifying gaps by severity, and applying fixes. Use when user says 'review this spec', 'audit the spec against the code', 'find gaps in the spec', 'check spec inconsistencies', 'find implicit requirements', 'validate design.md and tasks.md', or 'validate plan.md and checks.md'."
model: opus
effort: high
---

## Guide: Technical Spec Review (gaps, inconsistencies, implicit requirements)

Audit spec docs (spec.md, design.md, tasks.md, or tlc-spec-lean's plan.md and checks.md, plus requirements.md, context-map.md, cited ADRs) against actual code, then apply corrections. Spec = hypothesis, never truth. Ask user once before editing (Step 4). Code verification runs in a fresh-context subagent, not in this conversation (see Fresh-context verifier).

| #   | Step                 | Action                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Output / Gate                                                            |
| --- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| 1   | Gather               | List feature spec dir; count lines (whole vs parts); read every file fully + cited ADRs                                                                                                                                                                                                                                                                                                                                                                                                                                              | Full picture of problem, goals, ACs, design, tasks, requirements         |
| 2   | Verify vs code       | Spawn a fresh-context verifier (section below) to confirm each decision/assumption/contract in source — checklist: [verification-checklist.md](references/verification-checklist.md). Do not verify inline                                                                                                                                                                                                                                                                                                                           | Claim → confirmed / false / unverifiable, each with `path:line` evidence |
| 3   | Classify             | Group findings by severity; give each a disposition (tables below)                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Report to user                                                           |
| 4   | Confirm scope        | **One** question round: (a) severity groups to fix now (offer "report only"); (b) design decisions with >1 reasonable solution → options + technical implication each; (c) each ESCALATE finding, listed first → user confirms no change or supplies the fact to add                                                                                                                                                                                                                                                                 | User answers before any edit                                             |
| 5   | Apply fixes          | Tracker task per file/group (in-progress → complete). Per-file edits: [fix-by-file.md](references/fix-by-file.md)                                                                                                                                                                                                                                                                                                                                                                                                                    | Docs consistent with each other + code                                   |
| 5.5 | Re-verify High fixes | After applying every High-severity fix, re-run Step 2 (Verify vs code) with a **new** fresh-context verifier scoped to the files/claims touched by those fixes, passing the settled list (Notes below). If any High finding remains (new or unresolved), repeat Steps 4-5.5 on the remaining items. Bounded to 3 rounds total. If High findings still exist after round 3, STOP — do not apply a 4th fix unsupervised — and escalate to the user with the remaining findings (BLOCKED / TRIED / NEED format if the project uses it). | Zero High findings, or an explicit escalation with the user's decision   |
| 6   | Sync derived system  | Only if spec feeds separate tracker (taskmaster): [taskmaster-sync.md](references/taskmaster-sync.md)                                                                                                                                                                                                                                                                                                                                                                                                                                | Only derived fields changed                                              |
| 7   | Residue check        | Grep every replaced term/snippet (nonexistent command, removed FK, old route, truncation marker) across touched files (skip `review/`, which quotes old text on purpose); each remaining hit must be intentional (explains the change)                                                                                                                                                                                                                                                                                               | Zero forgotten leftovers                                                 |
| 8   | Report               | See report table below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Direct summary to user                                                   |

## Fresh-context verifier (Steps 2, 5.5)

Whoever drafted or discussed the spec shares its blind spots, so verification runs in a subagent that has never seen this conversation.

- Spawn with the `Agent` tool (`general-purpose`). Never use `subagent_type: "fork"`: a fork inherits this conversation, which defeats the purpose. Each Step 2 run and each Step 5.5 round gets a **new** agent. Never continue an earlier verifier with `SendMessage`, because it keeps the previous round's context.
- Prompt contains only: repo root, absolute paths of the spec files and cited ADRs, the path of [verification-checklist.md](references/verification-checklist.md), the output file path, and in Step 5.5 the scope (touched files/claims) plus the settled-list file path. Never include a conversation summary, author rationale, your own suspicions or expected findings.
- Verifier does not edit code or spec docs. It writes its result, in English, to `<spec-dir>/review/verify-round-<N>.md` (Step 2 = round 1; each Step 5.5 round increments N), with one row per claim: quoted claim + doc `path:line`, status (confirmed / false / unverifiable), evidence (`path:line` or command output), proposed severity.
- Verifier's final message is only the file path plus counts per status and severity, never the findings themselves. A missing or empty file means the verifier did not run: retry once, then stop and tell the user.
- The main agent reads the file and assigns dispositions (Step 3) in a `Disposition` column of that same file. It may not drop a finding without one. Keep the settled list in `<spec-dir>/review/settled.md`.
- No subagent tool in the harness → verify inline and state in the Step 8 report: "verification was not fresh-context".

## Disposition (Step 3)

Every finding gets exactly one:

| Disposition | When                                                                                                         | Effect                                      |
| ----------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| PROPOSE FIX | Finding valid                                                                                                | Precise edit, applied in Step 5 if approved |
| CONTEST     | Finding wrong, with evidence the verifier could read: file + symbol, or a decision recorded in the spec docs | No edit; becomes settled                    |
| ESCALATE    | Finding looks wrong, but the evidence is outside the repo (team convention, verbal decision)                 | No edit; user decides in Step 4             |
| DECLINE     | Inconsistency-level finding not worth fixing (never High or Medium)                                          | Recorded, no edit; becomes settled          |

Rules: "it was intentional" is not evidence. Without checkable evidence, use ESCALATE or PROPOSE FIX. Do not lower a severity. If you disagree with it, CONTEST and state why. Do not add text to the spec only to satisfy the verifier. Add it when a human reader needs it, otherwise ESCALATE.

## Severity (Step 3)

| Level                           | Examples                                                                                                                                                                                                                                                                                                                                                                           |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| High                            | Breaks existing contract (API, CLI output, component props, exported signature, error/exit behavior); cited command/API/flag missing in installed version; corrupted/truncated content in doc; validation rejecting a real system case (e.g. input in format not guaranteed by its producer); missing invariant/constraint that logic assumes; success criterion with no real test |
| Medium                          | External dependency (relation, service, file, env var) can be absent on valid path; justification doesn't match cited code; task underestimates blast radius of contract change; accepted consequence unrecorded; unspecified data normalization/format                                                                                                                            |
| Inconsistencies / implicit reqs | Docs stale vs each other (one superseded another); declared deps diverge from real tracker; incomplete "files to modify"; broken req ID ↔ task ID traceability (lean: criterion ↔ check); out-of-scope item unrelated to card; type/value specified but unused in any rule                                                                                                         |

Notes:

- Re-verification loop (Step 5.5) applies **only to High**. Medium and
  Inconsistency stay single-pass (fix once per Step 5, no re-verification) —
  their cost of being wrong is lower, and re-verifying every Medium would
  make routine reviews expensive for little gain.
- Round count and "same finding vs new finding" are judged by the agent: a
  fix that only moved a line number is the same finding resolved; a fix that
  triggered a different claim to break is a new finding and still counts
  toward the 3-round budget.
- Settled list: a finding is settled when it is CONTEST, DECLINE, or
  ESCALATE that the user confirmed without change. Keep the list in
  `review/settled.md` across Step 5.5 rounds and pass its path to each new
  verifier. If a verifier raises a
  settled finding again (same scope, same issue), do not reopen it and do not
  count it as a new finding.
- An applied fix does not settle a finding. If a later verifier raises the
  same issue at the same scope, the fix failed or a later edit reintroduced
  it: reopen it.
- Step 7 (Residue check) still runs once at the end, after the Step 5.5 loop
  closes (clean or escalated) — it's a grep sweep for leftovers, not a
  code-correctness check, so it doesn't repeat per round.

## Report (Step 8)

| #   | Include                                                                                     |
| --- | ------------------------------------------------------------------------------------------- |
| 1   | Fixes by severity — don't repeat full earlier report                                        |
| 2   | Decisions that change implementation — highlight separately (matter most to task executors) |
| 3   | State explicitly: no build/test run when change was docs only                               |
| 4   | Items deliberately kept (CONTEST + evidence, ESCALATE + user decision, DECLINE + reason)    |
| 5   | Whether verification was fresh-context (state it explicitly when it was not)                |
| 6   | Paths of the `review/verify-round-<N>.md` files and `review/settled.md`                     |

## Reference files

- [references/verification-checklist.md](references/verification-checklist.md) — 10-point stack-agnostic code verification list (entry points, access control, data contracts, runtime inputs, errors, reused patterns, versions, state write paths, affected tests, atomicity/side effects)
- [references/fix-by-file.md](references/fix-by-file.md) — per-file edit rules (spec, design, tasks, plan, checks, requirements, context-map, ADRs)
- [references/taskmaster-sync.md](references/taskmaster-sync.md) — disposable-script procedure to sync tracker derived fields
