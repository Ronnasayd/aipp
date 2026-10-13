# sd-planning — Flow Diagram

```mermaid
flowchart TD
    Start([SRS + context map
    from sd-interview or user]) --> A0{"Context map
    missing/stale?"}
    A0 -- yes --> A1["/context-map
    re-run using SRS
    requirements as input"]
    A0 -- no --> B
    A1 --> B["2. /tlc-spec-driven
    generate plan/spec from SRS
    + context map"]
    B --> C["3. /spec-to-requirements-table
    generate requirements.md"]
    C --> V["4. Verifier (fresh sub-agent, no inherited context)
    /sd-review-spec report-only vs SRS + code"]
    V --> V2{"Gaps found?"}
    V2 -- yes --> V3["Show gaps to user,
    apply fixes (/sd-review-spec steps 4-7)"]
    V3 --> V
    V2 -- no --> D{"Register in
    taskmaster?"}
    D -- yes --> E["/sd-insert-taskmaster"]
    D -- no --> F
    E --> F["6. Check docs-adr criteria
    offer ADR if met"]
    F --> G["7. Evaluate durable memory
    (reason/invariant/preference only)
    /ai-memory-durable-pages"]
    G --> End([Plan complete])
```

Track via `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` through all steps — status updates keep user informed.
