---
name: generate-pr-description
description: "Generate structured Pull Request descriptions from git diffs (staged or branch) and commit history. Auto-detects .github/pull_request_template.md; falls back to Description/Impact/Task sections. Use when user says 'generate PR description', 'write PR description', 'create pull request description', 'draft the PR description', or 'summarize this branch for a PR'. Requires the output language as an argument; ask the user before invoking if not specified."
argument-hint: "<language>: (Required) Language for PR description (e.g., 'English', 'Portuguese'). Ask the user before invoking if unknown."
context: fork
agent: reviewer-specialist
background: false
model: sonnet
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

Language: $ARGUMENTS

This skill runs as an isolated subagent: it has no conversation history and cannot ask the user anything. It only reads and reports; it does not change code.
MANDATORY: language above is empty → stop and return `status: partial` with `reason: missing language`, so the caller can ask and invoke again.

Objective: generate professional, comprehensive PR description by analyzing staged changes + recent commit history.

====================
PHASE 1 — TEMPLATE DETECTION
====================

1. Check if `.github/pull_request_template.md` exists in workspace.
2. Exists → read content, use as MANDATORY structure for PR description.
3. Not exist → use default topics as sections:
   - ## Description: High-level overview of what PR does.
   - ## Impact: Technical + functional impact of changes.
   - ## Task: List of specific tasks or user stories addressed.

====================
PHASE 2 — CONTEXT GATHERING
====================

1. Identify changes to describe:
   - Run `git diff --staged`. Not empty → use as primary source.
   - `git diff --staged` empty → run `git diff main...HEAD` (or default branch) for current branch changes.
   - Still empty → stop and return `status: partial` with `reason: no changes found`.
2. Run `git log -n 10 --oneline` to understand commit sequence + intent.
3. Search `.taskmaster/` or `docs/` for relevant PRDs/task specs matching branch name or commit keywords.

====================
PHASE 3 — GENERATION
====================

Based on analysis, generate PR description:

1. Follow detected or default template strictly.
2. Tone professional, content accurate.
3. Generate entire description in the specified language.

====================
PHASE 4 — VALIDATION
====================

Run `python3 skills/generate-pr-description/scripts/validate_pr_description.py --message "<generated description>"` before presenting it.
FAIL (exit 1) → fix flagged sections (missing/empty/placeholder text) and re-run until it passes.

====================
PHASE 5 — OUTPUT
====================

Your final response must contain the complete PR description verbatim in a Markdown block, alongside any other fields your final response requires.

Example Output (Default Template):

```markdown
## Description

This PR introduces a new skill for generating PR descriptions automatically...

## Impact

- Improves developer productivity by automating repetitive documentation tasks.
- Ensures consistent PR descriptions across the project.

## Task

- Create skills/generate-pr-description/SKILL.md
- Implement template detection logic.
- Add language selection support.
```

====================
WORKFLOW
====================

- Always verify PR template exists before proposing structure.
- Use commit history to add context not obvious from diff alone.
