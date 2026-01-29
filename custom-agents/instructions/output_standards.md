# Agent Output Standards

All agents participating in the Zero to Hero workflow MUST adhere to these standards. Failure to do so will result in rejection by the Critic or automated checks.

## 1. Naming Conventions
-   **File Names**: strict `kebab-case`. Lowercase only. No spaces.
    -   ✅ `technical-feasibility.md`
    -   ❌ `Technical-Feasibility.md`, `TechnicalFeasibility.md`, `technical feasibility.md`
-   **No Redundant IDs**: Avoid generic IDs in filenames.
    -   ✅ `product-brief.md`
    -   ❌ `PRODUCT_BRIEF_FINAL.md`

## 2. Directory Structure
-   **Flat & Categorical**:
    -   `context/`: Input specs and briefs.
    -   `architecture/`: System design and ADRs.
    -   `planning/`: Implementation plans.
-   **No Redundant Reports**: Do not create summary or status reports for completed phases. Information should be stored in the primary deliverables or memory.

## 3. Handoff Protocol
-   **Link, Don't Copy**: A handoff is a *signal*. It should contain links to the relevant artifacts, not a copy of their content.
-   **Format**:
    ```markdown
    # Phase 1 Complete
    **Status**: ✅ Ready for Analysis
    **Deliverable**: [Product Brief](../context/product-brief.md)
    ```

## 4. Content Efficiency
-   **No "fluff"**: Avoid "Here is the file you asked for" or "I have thought about this".
-   **Single Source of Truth**: Do not repeat the Project Spec in the Architecture doc. Link to it.
-   **Updates over Rewrites**: If updating a document, modify the existing one (or append to changelog) rather than creating `v2`.

## 5. File Formats
-   **Markdown**: Standard GFM.
-   **Diagrams**: Mermaid `flowchart` or `sequenceDiagram` only.
-   **Code**: Fenced code blocks with language identifiers.
