# sd-planning checklist

Detail: [SKILL.md](SKILL.md) · step 3: [references/verifier-pass.md](references/verifier-pass.md)

- [ ] 1. `/tlc-spec-driven` → spec docs
- [ ] 2. Language settled with user → `/spec-to-requirements-table <spec-dir> <language>`
- [ ] 3. Depth (`depth=` arg or one `AskUserQuestion`) → fresh sonnet verifier, `/sd-review-spec` report-only, original request verbatim + spec dir only
  - [ ] Fixes per `/sd-review-spec` steps 4-5, 6-7; skip its Step 5.5
  - [ ] Re-verify only re-verified severities (`medium`: High; `high`: High, plus Medium and Inconsistency only while the round has a High; `low`: none), new scoped verifier + `review/settled.md`
  - [ ] Stop at zero High, or after 3 (`medium`) / 5 (`high`) rounds → BLOCKED / TRIED / NEED
- [ ] 4. Ask: register in taskmaster? → `/sd-insert-taskmaster <tag>`
- [ ] 5. ADR criteria met? → offer ADR
- [ ] 6. Durable memory worth saving? → `ai-memory-durable-pages`
