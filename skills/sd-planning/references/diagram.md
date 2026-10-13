# sd-planning — Flow Diagram

```mermaid
flowchart TD
    Start([Feature request]) --> Loop

    subgraph Loop["1. Understand loop — repeat till context sufficient"]
        direction TB
        A1["sequentialthinking (mcp-manager)
        break into sub-issues:
        scope, constraints, edge cases, deps
        (use /dynamic-programming-analysis
        if breakdown itself is hard)"] --> A2a
        A2a["Codebase = source of truth
        traverse file-by-file to limits,
        full understanding of current flow"] --> A2c["Transversal search:
        keywords/terms not directly linked
        or unseen in inspected files
        (all tools: semantic search,
        sub-agents, CLI, MCPs, skills)"]
        A2c --> A3{"Gap remains that
        codebase + context7
        can't cover?"}
        A3 -- yes --> A2b["WebSearch
        market patterns, RFCs,
        security advisories, precedent"]
        A3 -- no --> A4b
        A2b --> A4b
        A4b["Dedicated sub-agent runs /grilling
        (no code/task tools, hides downstream goal)
        clarify w/ user,
        check unlisted implicit reqs
        — see references/grilling.md"] --> A5{"Enough context?"}
        A5 -- no --> A1
    end

    A5 -- ask user: finish or refine? --> Decide{"User: continue
    or proceed?"}
    Decide -- continue --> A1
    Decide -- proceed --> M["2. /context-map
    anchors, dependents, tests,
    patterns, risks
    (rag-rat / cbm / serena)
    + grep/Read to fill gaps"]
    M --> B["3. /tlc-spec-driven
    generate plan"]
    B --> C["4. /spec-to-requirements-table
    generate requirements.md"]
    C --> V["5. Verifier (fresh sub-agent, no inherited context)
    /sd-review-spec report-only vs original request + code"]
    V --> V2{"Gaps found?"}
    V2 -- yes --> V3["Show gaps to user,
    apply fixes (/sd-review-spec steps 4-7)"]
    V3 --> V
    V2 -- no --> D{"Register in
    taskmaster?"}
    D -- yes --> E["/sd-insert-taskmaster"]
    D -- no --> F
    E --> F["7. Check docs-adr criteria
    offer ADR if met"]
    F --> G["8. Evaluate durable memory
    (reason/invariant/preference only)
    /ai-memory-durable-pages"]
    G --> End([Plan complete])
```

Track via `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` through all steps — status updates keep user informed.
