# Grilling — why a dedicated sub-agent

Structured interrogation to extract clear requirements, map business rules, and
align the **shared design concept** before any spec or code gets written. Early
on nobody — including the user — knows every detail of what they want; the gap
between vague human intent and model execution has to close before planning
starts.

## Why delegate instead of asking inline

A general-purpose agent that already knows its next step is writing a
plan/spec tends to cut the interview short:

- **Eager to produce an artifact.** Most LLMs are optimized to deliver a
  solution fast; questions become an obstacle to skip past rather than real
  groundwork.
- **Tool-scope pressure.** If the agent holds file-edit or task-creation tools
  in its current context, it feels pressure to use them instead of staying in
  the alignment loop.

A dedicated sub-agent fixes both:

- **Hides the downstream goal.** The sub-agent never sees the later steps
  (spec generation, code). Its only stop condition is reaching shared
  understanding, so it has no reason to rush.
- **Context isolation.** A fork avoids spillover from unrelated context and
  keeps the sub-agent's sole focus on being an adversarial interviewer.
- **Separates sync from async work.** Requirement alignment is inherently
  human-in-the-loop (synchronous). Once it's done, the synthesized Q&A history
  feeds a separate, autonomous step (spec generation) with clean context.

## How to delegate it

1. **No code or task tools.** The sub-agent must not have file-edit, commit,
   or task-creation tools — only the ability to ask questions and read
   docs/code to inform them.
2. **User-controlled stop condition.** `/grilling` is a user-invoked skill, not
   model-auto-triggered — the orchestrator (not the sub-agent) decides when
   the interview ends.
3. **Strong persistence instruction**, passed verbatim as the sub-agent's
   prompt:

   > "Interview me relentlessly about every aspect of this idea/plan until we
   > reach a shared understanding. Walk every branch of the decision tree,
   > resolving dependencies one at a time. For each question, provide your
   > recommended default answer. Ask one question at a time. Do not generate
   > final plans or code at this stage."

## Conduct principles (what the sub-agent must do)

1. **Option-driven querying.** Never ask open questions like "how do you want
   this to work?" — propose a default and ask for confirmation/adjustment
   (e.g. "How should we handle a connection failure? Recommendation: retry 3x
   with exponential backoff, then show the user an error. Agree or adjust?").
2. **One question at a time** (or small batches) — avoids overload and allows
   methodical coverage of edge cases and dependencies.
3. **Three mandatory dimensions**: business rules/edge cases (missing data,
   limits exceeded, flow failures), boundaries/architecture (impacted
   modules, interface contracts), acceptance criteria/testability
   (deterministic proof of done).

## Flow

```
[ Vague idea / raw ticket ]
        │
        ▼
1. Grilling session (dedicated sub-agent) ──► Q&A exchange until the
        │                                      design concept is aligned
        ▼
2. Spec/PRD generation ──► synthesizes the conversation into a structured artifact
        │
        ▼
[ Execution/code agent ]
```

The resulting spec should contain: problem/solution statement, user stories
and requirements, vertical slices (tracer bullets) for implementation order,
a validation contract (objective assertions/tests), and an explicit
out-of-scope section to block scope creep.
