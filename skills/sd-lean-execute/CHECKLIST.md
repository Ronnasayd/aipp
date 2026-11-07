Checklist for `sd-lean-execute` skill, sequential:

1. **Validate feature** — `checks.md` exists, `validate_checks.py` exits 0. Red → stop.
2. **Read lean skill** — invoke `/tlc-spec-lean`; read `build.md` + `verify.md`, `verify-screens.md` with captures, `memory.md` on resume.
3. **Build** — as documented, up to before `check_proofs.py`.
4. **Sync docs** — `generate-docs` update mode, committed. Skip if no doc-worthy change.
5. **UI regression gate** — Playwright on screens the feature did not set out to change. Skip for non-UI.
6. **Verify** — `check_proofs.py`, then Verifier + screens sub-agent, unchanged.
7. **Fix findings** — fix in one pass, appended check for a missing obligation, commit, `check_proofs.py`.
8. **Gate** — `validate_verification.py` exits 0.
9. **Summary** — open with the gate's last line; docs outcome. Push/deploy wait for the user.
10. **Save permanent memory** — only what the next session cannot rediscover. Persist via `ai-memory-durable-pages`.

Invariant: nothing outside `.specs/` uncommitted, and no commit, after the last `check_proofs.py`.
