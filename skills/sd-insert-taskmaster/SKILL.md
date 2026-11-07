---
name: sd-insert-taskmaster
description: Convert tasks.md spec files into TaskMaster JSON format (.taskmaster/tasks/tasks.json), registering a tlc-spec-lean checks.md as one task per slice with one subtask per check, and falling back to one synthetic task per requirement from spec.md when neither exists. Use when user says 'convert tasks.md to taskmaster json', 'transform tasks.md to .taskmaster format', 'generate taskmaster json from this spec', or 'register this feature in taskmaster'.
argument-hint: "<tag>: (Required) Feature tag, used as the taskmaster root key and as the .specs/features/<tag>/ directory. Ask the user before invoking if unknown."
context: fork
background: false
model: haiku
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.3.0
---

# tasks-md-to-taskmaster-json

Converts a `tasks.md` spec into `.taskmaster/tasks/tasks.json` (TaskMaster-compatible task list, merge-safe).

## Input

Tag: $ARGUMENTS

This skill runs as an isolated subagent: it has no conversation history and cannot ask the user anything. If the tag above is empty, stop before writing anything and return `status: partial` with `reason: missing tag`, so the caller can ask and invoke again.

When the feature only has `spec.md` (no `tasks.md` -- tlc-spec-driven's auto-sizing decided the feature is Small/Medium and skipped the Tasks phase), this skill still registers it in taskmaster for tracking, via the spec-only fallback (Step 0.5) -- taskmaster stays a complete progress log regardless of feature size, even though execution itself stays inline and unbatched for these features.

## Steps

| #   | Step                   | Action                                                                                                                          | Output / Gate                                                                                                   |
| --- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 0   | Resolve tag            | Read the root key tag from Input                                                                                                | tag stored for steps 6-7 — see [json-schemas.md](references/json-schemas.md) for wrapper shape                  |
| 0.5 | Check for tasks.md     | If `.specs/features/{TAG}/tasks.md` is missing: `checks.md` exists → lean mode; otherwise `spec.md` exists → spec-only fallback | See "Lean mode" and "Spec-only fallback" below — skip steps 1-4, go straight to Step 5                          |
| 1   | Read tasks.md fully    | Read Execution Diagram, task tables, cross-checks before writing any JSON                                                       | diagram + cross-checks are source of truth, not just `Depends on` (which may omit transitive deps)              |
| 2   | Build dependency graph | Directed edges: `task_id → [deps]`                                                                                              | validate every dep against the ASCII diagram                                                                    |
| 3   | Calculate waves (BFS)  | Wave 1 = no deps; Wave N+1 = deps all in waves ≤N                                                                               | tasks in same wave have zero deps between each other — example in [json-schemas.md](references/json-schemas.md) |
| 4   | Identify critical path | Bottom-up traversal: longest sequential dependency chain                                                                        | determines minimum execution time                                                                               |
| 5   | Map fields             | Task → JSON schema                                                                                                              | field mapping table in [json-schemas.md](references/json-schemas.md)                                            |
| 6   | Assemble output        | Build tasks.json                                                                                                                | schema + examples in [json-schemas.md](references/json-schemas.md)                                              |
| 7   | Create + validate      | Run scripts (below)                                                                                                             | file must pass validation before delivery                                                                       |

## Lean mode (Step 0.5)

For tlc-spec-lean features, which have `checks.md` and no `tasks.md`. Lean has no task breakdown, so this is a registry of obligations, not an execution plan:

1. Read `checks.md` fully, and `plan.md` when it exists (a small change has only `checks.md`).
2. One task per slice heading `### S<n> - <title>`: `id` = `<n>`, `title` = `S<n> - <title>`, `description` = the slice's outcome line in `plan.md`, or its title when there is no plan. A `checks.md` with no slice heading gets a single task `S1` titled after the feature.
3. `priority` = `"high"` for a slice marked `(P1)` in `plan.md`, `"medium"` otherwise. `dependencies: []`, `wave 1`, `onCriticalPath: false`: slice order belongs to the builder.
4. `details` = the check range (`Checks C1-C7`). `testStrategy` = `"proofs per subtask"`.
5. One subtask per check `**C<n>** - <claim>`: `id` sequential inside the slice from 1, `title` = `C<n> - <claim>`, `description` = the claim, `status: "pending"`, `dependencies: []`, `details` = every `Proof:` line of that check. The `C<n>` prefix ties the subtask back to its check, so keep it.
6. Proceed to Step 5 (field mapping is already done above) then Steps 6-7 unchanged.

`merge-tasks.py` replaces the whole tag, so running this again resets progress. A check appended during the build goes in with taskmaster's `add_subtask`, not by registering the feature again.

## Spec-only fallback (Step 0.5)

For Small/Medium features with only `spec.md`:

1. Read `spec.md` fully -- extract every requirement ID and its acceptance criteria.
2. Create one synthetic task per requirement/AC: `title` = requirement summary, `description` = the AC text, `id` assigned sequentially in spec order.
3. All synthetic tasks go in `wave 1` with `dependencies: []` -- there is no real dependency graph to compute, this is a registry, not an execution plan.
4. `metadata.onCriticalPath` = `false` for all (no critical path concept applies).
5. `testStrategy` = `"none"` unless the AC itself specifies a test/verification method.
6. Proceed to Step 5 (field mapping is already done above) then Steps 6-7 unchanged.

### Step 7 commands

```bash
mkdir -p .taskmaster/tasks
cp <skill-path>/index.html .taskmaster/index.html   # Kanban viewer, static asset

python3 <skill-path>/scripts/merge-tasks.py \
  .taskmaster/tasks/tasks.json "<tag>" '<tasks_json_string>'

python3 <skill-path>/scripts/validate-tasks.py tasks .taskmaster/tasks/tasks.json
```

- `merge-tasks.py` preserves all existing tags while adding/updating the new one.
- If validation fails, fix and re-validate before confirming delivery.

## Final Checklist

### tasks.json

- [ ] All tasks.md tasks present (count matches) -- or, for lean mode, every slice is a task and every check a subtask -- or, for spec-only fallback, all requirement/AC ids present
- [ ] `dependencies` are integer ids, not `"T01"` strings
- [ ] Same-wave tasks have zero deps between each other
- [ ] `testStrategy` non-empty where tests exist
- [ ] `priority: "high"` only for critical-path/system-blocking tasks
- [ ] Each task has `metadata: { wave, onCriticalPath }`
- [ ] Valid JSON (`validate-tasks.py tasks` passes)
- [ ] New tag merged without overwriting existing tags
- [ ] Root key = resolved tag; `tasks` nested under it, no global metadata

## Final response

State the tag, the task count, the subtask count in lean mode, which source ran (tasks.md, lean mode or spec-only fallback), and the `validate-tasks.py` result, alongside any other fields your final response requires.

## Reference files

- [references/json-schemas.md](references/json-schemas.md) — tag wrapper, field mapping table, wave/critical-path examples, full tasks.json schema example
- [references/walkthrough-example.md](references/walkthrough-example.md) — end-to-end worked example (input → actions → result)
