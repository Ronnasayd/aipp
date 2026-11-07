# Workflows and enforcement

Sources of truth: each skill's own `SKILL.md`, `agents/*.agent.md`, `commands/`, `claude/settings.json` (hook wiring), `hooks/README.md`, `lefthook/lefthook.yml`, `tlc-harness-toolkit/`.

This file lists the default-enabled workflows. For anything else, use `skills-discovery`.

## Choose a workflow

The `sd-*` planning and execution skills set `disable-model-invocation: true`, so an agent cannot start them on its own: the user types the slash command.

| Situation                                                     | Run                                          |
| ------------------------------------------------------------- | -------------------------------------------- |
| Idea is still unshaped, unsure whether to build it            | `tlc-discover`                               |
| Plan needs to be pressure-tested through questions            | `/sd-grilling`                               |
| Feature that needs a spec, a design and a task list           | `/sd-planning`, then `/sd-execute`           |
| Feature that needs one plan and proof-backed checks, no tasks | `/sd-lean-planning`, then `/sd-lean-execute` |
| See which files a change touches before starting              | `context-map`                                |
| Audit an existing spec against the code                       | `sd-review-spec`                             |
| Compare technical options                                     | `technical-decision-helper`                  |
| Break down a large problem                                    | `dynamic-programming-analysis`               |
| Review a PR                                                   | `the-judge`                                  |
| Write the PR description                                      | `generate-pr-description`                    |
| Resolve merge conflicts                                       | `resolve-merge-conflicts`                    |
| Write or sync docs                                            | `generate-docs`                              |

### Full path: `/sd-planning` then `/sd-execute`

1. `/sd-planning` runs `tlc-spec-driven`, writing `.specs/features/<tag>/` (`spec.md`, `design.md`, `tasks.md`).
2. `spec-to-requirements-table` produces `requirements.md`. It runs isolated, so settle the output language first.
3. An independent sub-agent audits the docs against the code with `sd-review-spec`. This step always runs.
4. The user may register the feature in Task Master with `sd-insert-taskmaster`, which gives it a tag.
5. `/sd-execute` needs `spec.md` and a matching tag in `.taskmaster/tasks/tasks.json`. It runs the `tlc-spec-driven` Execute phase and syncs task status after each unit. Task Master mirrors progress and does not drive the order.

### Lean path: `/sd-lean-planning` then `/sd-lean-execute`

1. `/sd-lean-planning` writes `plan.md` with `tlc-spec-lean`, adds an independent review, then waits for approval.
2. After approval it writes `checks.md` and freezes it with `validate_checks.py`. It stops there and does not build.
3. A change under roughly three files with no one-way door takes a short path: only `checks.md`.
4. `/sd-lean-execute` needs `checks.md` passing `validate_checks.py`. It builds slice by slice, then runs `check_proofs.py`, a Verifier and `validate_verification.py`.

`/sd-execute` needs the Task Master tag. If the feature was not registered, run `sd-insert-taskmaster` first. The lean path does not use Task Master.

## Agents

Enabled by default: `developer-specialist`, `planner-specialist`, `reviewer-specialist`, `qa-specialist`, `interview-specialist`. Their definitions are in `agents/`, and the others can be enabled with `mif`. Choose by role: planner to research and design before coding, developer to implement, reviewer to review or refactor, QA for test plans and release checks, interview to gather requirements through questions.

## Commands

| Command                 | Use                                                                 |
| ----------------------- | ------------------------------------------------------------------- |
| `/create-commit.prompt` | Create a commit from the current changes                            |
| `/readonly`             | Toggle readonly mode, which blocks edits and write-capable commands |
| `/save-session-memory`  | Evaluate the session and save what is worth keeping                 |
| `/step-by-step.prompt`  | Write up how a result was reached, reusable as a skill later        |
| `/verify-hook`          | Verify a hook script works end to end                               |

## What blocks you and why

Each layer is separate, so check the right one. A branch protection denial, for example, comes from a Claude Code hook and does not appear in the lefthook config or in GitHub's branch protection.

| Symptom                                                               | Layer                                        | What to do                                                                                                                                          |
| --------------------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Commit or mutation denied on `main`, `master`, `develop` or `homolog` | `protect_branches.py` (PreToolUse)           | Create the branch in a separate command first. The check reads the current branch before a chained `git switch -c ... && git commit` runs           |
| Read or write of a sensitive path denied                              | `protect_files.py` (PreToolUse)              | Do not work around it. The project's `PROTECT_FILES_EXTRA_ALLOWED` in `.claude/settings.local.json` holds any extra allowed paths                   |
| Dev server command denied                                             | `dev_server_tmux_check.py` (PreToolUse)      | Run it inside tmux or screen                                                                                                                        |
| Asked to confirm Portuguese markdown                                  | `md_language_check.py` (PreToolUse)          | Files under `docs/` and `.specs/` are expected in English                                                                                           |
| Turn cannot end, lint or tests fail                                   | tlc harness grind gate                       | Fix the failure. `SKIP_LINT=1` or `SKIP_TESTS=1` at Claude launch skips it                                                                          |
| Told to use `AskUserQuestion`                                         | `question_tool_enforcer.py` (Stop)           | Ask through the question tool                                                                                                                       |
| Commit rejected at pre-commit                                         | lefthook: format, lint, test, comment policy | Run `uv run hooks/scripts/lint_changed.py --staged` to reproduce it. Added comments need a `why:`, `hazard:` or `invariant:` prefix                 |
| Commit message rejected                                               | lefthook `commit-msg`                        | Use Conventional Commits, English only, no emoji, no mention of AI tools. Very short subjects can fail language detection, so write a full sentence |
| Push rejected                                                         | lefthook `pre-push`: jest, typecheck         | Fix the failures                                                                                                                                    |

`LEFTHOOK=0` and `git commit --no-verify` bypass git hooks. Mention them only if the user asks how, and never use them on your own initiative.

For the rest of the hook catalog by event, read `hooks/README.md`. For the wiring actually in effect, read `claude/settings.json`. For harness rules, read `tlc-harness-toolkit/rules.md`, and use `tlc harness handoff` to see the saved state.
