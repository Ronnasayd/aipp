# sd-planning — Flow Diagram

```mermaid
flowchart TD
    Start([Feature request / spec input]) --> B["1. /tlc-spec-driven
    generate plan"]
    B --> C["2. /spec-to-requirements-table
    generate requirements.md"]
    C --> V["3. Verifier (fresh sub-agent, no inherited context)
    /sd-review-spec report-only vs original request + code"]
    V --> V2{"Gaps found?"}
    V2 -- yes --> V3["Show gaps to user,
    apply fixes (/sd-review-spec steps 4-7)"]
    V3 --> V
    V2 -- no --> D{"Register in
    taskmaster?"}
    D -- yes --> E["/sd-insert-taskmaster"]
    D -- no --> F
    E --> F["5. Check docs-adr criteria
    offer ADR if met"]
    F --> G["6. Evaluate durable memory
    (reason/invariant/preference only)
    /ai-memory-durable-pages"]
    G --> End([Plan complete])
```

Track via `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` through all steps — status updates keep user informed.
