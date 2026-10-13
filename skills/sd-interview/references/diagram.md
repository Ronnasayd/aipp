# sd-interview — Flow Diagram

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
    M --> S["3. srs-generator
    fill SRS template from
    sub-issues + grilling Q&A + context map"]
    S --> H["4. Hand off to user:
    SRS path (docs/srs/...) + context map
    → consumed by sd-planning"]
    H --> G["5. Evaluate durable memory
    (reason/invariant/preference only)
    /ai-memory-durable-pages"]
    G --> End([Interview complete])
```

Track via `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` through all steps — status updates keep user informed.
