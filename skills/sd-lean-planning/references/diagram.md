# sd-lean-planning — Flow Diagram

```mermaid
flowchart TD
    Start([Feature request]) --> A{"1. Open architectural bet?"}
    A -- yes --> A2["Settle it in an ADR"]
    A -- no --> B
    A2 --> B["2. /tlc-spec-lean Plan
    validate_plan.py exits 0, not presented yet"]
    B --> C["3. /spec-to-requirements-table
    generate requirements.md"]
    C --> V["4. Verifier (fresh sub-agent, no inherited context)
    /sd-review-spec report-only vs original request + code"]
    V --> V2{"Gaps found?"}
    V2 -- yes --> V3["Show gaps to user,
    apply fixes (/sd-review-spec steps 4-7)"]
    V3 --> V
    V2 -- no --> P["5. Present plan + requirements.md
    STOP for approval"]
    P --> K["6. Write checks.md
    fresh criterion-to-check review
    validate_checks.py exits 0, checks frozen"]
    K --> D{"7. Register in
    taskmaster?"}
    D -- yes --> E["/sd-insert-taskmaster"]
    D -- no --> G
    E --> G["8. Evaluate durable memory
    /ai-memory-durable-pages"]
    G --> End([Planned: next is /sd-lean-execute])
```

Track via `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` through all steps — status updates keep user informed.
