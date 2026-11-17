---
name: sd-grilling
description: Explore the codebase and relentlessly interview the user about a plan, feature, or idea until shared understanding is reached. Use when user says 'plan this feature step by step', 'help me plan this properly', 'generate a plan for this problem', 'walk through planning this feature', 'grill me about X', or uses any 'grill' trigger phrases.
model: opus
effort: high
disable-model-invocation: true
---

# Steps

Repeat phases 1 and 2 together, as one loop, until you have a complete understanding of the problem and how it fits into the current codebase. Never end the loop on your own judgment alone — follow phase 3 before stopping.

1. **Exploration phase.**
   1. Use `sequentialthinking` to break down the request into sub-issues (scope, constraints, edge cases, dependencies).
   2. Use `/dynamic-programming-analysis` when the breakdown itself is hard (unclear where to start, many interdependent sub-problems).
   3. Use `/context-map` to get verified anchors, dependents, tests, reference patterns, and risks. It runs isolated and sees no conversation, so pass as arguments the sub-issues, every decision already settled, and on later loop iterations the path of the earlier map. Re-run it when new sub-issues open unmapped areas. Its `Open questions:` go into the next grilling round.

   Across all of the above: treat the codebase as the absolute source of truth — navigate file-by-file, following the flows that will be modified/adjusted, until you reach the limits of what's there and have a full understanding of current behavior. Search transversally too, not just along linear flows: hunt keywords/terms possibly related but not directly linked, or absent from files already inspected (config, feature flags, error codes, event names, shared constants). If a knowledge gap remains that the codebase and `context7` (library docs) can't cover — market patterns, RFCs, security advisories, precedent for a novel architectural decision — use `WebSearch` to fill it. Skip this when the codebase/context7 already answer the question.

2. **Grilling phase.** Invoke the `/grilling` skill directly (inline, not as a sub-agent) over the open branches surfaced by phase 1 (scope, constraints, edge cases, dependencies). Follow its design-tree/frontier/round format exactly: one numbered round of questions via `AskUserQuestion`, each with a recommended default, waiting for answers before recomputing the frontier. Never ask the user for a fact you can look up yourself — only put genuine decisions to them. Any answer that opens a sub-issue not yet explored sends the loop back to phase 1 for that branch before the next round.

3. **Closing check.** Distrust the feeling that understanding is sufficient — it is a hypothesis, not a conclusion. Before offering to stop:
   1. Try to break your own understanding: list the assumptions you made without a user answer or a code citation, the branches you pruned or deferred, and the edge cases, failure modes, and dependents (from `/context-map`) not yet discussed. Any of these that could change the plan is an open branch.
   2. Play back the shared understanding to the user in a short summary — goal, scope in/out, decisions taken (with who decided: user answer or code evidence), and remaining risks — so the user can spot a misread before it becomes a plan.
   3. Ask via `AskUserQuestion` with the open branches as concrete options (each saying what exploring it would resolve and the risk of skipping it), plus a "summary is wrong/incomplete" option and a "finish" option. `AskUserQuestion` takes at most 4 options, so offer the 2 highest-risk branches and name any others in the question body (the user can pick them via "Other"). Recommend the branch with the highest risk; recommend "finish" only when no open branch could change the plan.
   4. If the user picks a branch or corrects the summary, return to phase 1 for it. Only a "finish" answer to a summary the user confirmed ends the loop.
