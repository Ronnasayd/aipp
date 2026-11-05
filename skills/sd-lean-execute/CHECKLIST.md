Checklist for `sd-lean-execute` skill, sequential:

1. **Validate tag** — `checks.md` exists, `validate_checks.py` exits 0, tag in `.taskmaster/tasks/tasks.json`. Red → stop. Missing tag → run `sd-insert-taskmaster`, or proceed w/o sync.
2. **Read lean skill** — invoke `/tlc-spec-lean`; read `build.md` + `verify.md`, `verify-screens.md` with captures, `memory.md` on resume.
3. **Build** — as documented, up to before `check_proofs.py`.
4. **Sync per slice** — proofs green → subtasks `done`, then slice; `tag` + `projectRoot`, one id per call; `tasks.json` in the slice commit.
5. **Sync docs** — `generate-docs` update mode, committed. Skip if no doc-worthy change.
6. **UI regression gate** — Playwright on screens the feature did not set out to change. Skip for non-UI.
7. **Verify** — `check_proofs.py`, then Verifier + screens sub-agent, unchanged.
8. **Sync on Verifier outcome** — finding → `pending`/`deferred`; appended check → `add_subtask`; fix, re-sync, commit, `check_proofs.py --mutations`.
9. **Gate** — `validate_verification.py` exits 0.
10. **Summary** — open with the gate's last line; taskmaster ids + docs outcome. Push/deploy wait for the user.
11. **Save permanent memory** — only what the next session cannot rediscover. Persist via `ai-memory-durable-pages`.

Status mapping: slice committed+proofs green → `done` | Verifier gap → `pending` | deferred → `deferred` | skipped → `cancelled` | blocked → `blocked`.

Invariant: nothing outside `.specs/` uncommitted, and no commit, after the last `check_proofs.py`.
