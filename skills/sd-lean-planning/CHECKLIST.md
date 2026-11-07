Checklist for `sd-lean-planning` skill, sequential:

1. **Architecture** — open bet meeting docs-adr criteria settled in an ADR before the plan. None → skip.
2. **Plan** — `/tlc-spec-lean` plan phase until `validate_plan.py` exits 0. Not presented yet. Short path (<~3 files, no one-way door): `checks.md` with `## Intent` only, `validate_checks.py` not run yet.
3. **Verifier** — fresh sub-agent, `/sd-review-spec` report-only. Gaps → user decides, apply fixes, rerun `validate_plan.py`.
4. **Approval** — present plan, offer `/spec-to-requirements-table` (optional, language settled first), stop. `**Approved**:` line only from the user's words.
5. **Checks** — write `checks.md`, fresh criterion-to-check review, then `validate_checks.py` exits 0. Stop: no Build here.
6. **Save permanent memory** — only what the next session cannot rediscover. Persist via `ai-memory-durable-pages`.

Next step for the user: `/sd-lean-execute <feature>`.
