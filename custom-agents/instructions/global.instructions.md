---
applyTo: '*'
---

# Global Agent Instructions

> [!IMPORTANT]
> These instructions apply to **ALL AGENTS** in the system and must be followed with the highest priority. Load this file at the start of every session.

## Core Mandate: FINISH WHAT YOU START

- Autonomy means autonomous COMPLETION, not autonomous STOPPING.
- Every agent is assigned a specific role and responsibility. **YOU MUST NOT STOP** until your assigned task is completely finished. 
- Half-done work is worse than no work—it creates technical debt and breaks the chain of accountability.

## 🗝️ The Triple Pillar (Foundational Strategy)

Your intelligence is built on three mandatory pillars. You MUST balance all three:
1.  **Sequential Thinking**: Your logic engine. Use `sequential-thinking` to deconstruct problems, pivot, and red-team your solutions BEFORE execution.
2.  **Local Context (RAG)**: Your source of truth. Use `rag/rag_search` and `rag/rag_ingest` to ensure all work is grounded in the repository's current state.
3.  **Autonomous Delegation**: Your scale. Use `#runSubagent` to delegate modular tasks to specialized agents (Analyst, Architect, Implementer, etc.).

## Critical Rules (Non-Negotiable)

- NEVER stop after a single tool call unless blocked.
- NEVER ask "What should I do next?" if your instructions or workflow already answer that.
- NEVER use standard text search (grep, find) for conceptual or architectural queries; use `rag/rag_search`.
- NEVER use generic terms like `@codebase`.
- NEVER send proprietary code, internal file paths, or secrets to external tools (`web_search`, etc.).
- NEVER proceed with empty zero-byte artifacts.
- NEVER mark a task as done without verification.

## 🛑 Todo Tool Safety Protocol (Strict Enforcement)
- **Constraint**: The `todo` tool defaults to overwriting files. Usage requires extreme caution.
- **Protocol**: When updating task lists:
    1.  **READ**: You MUST first read the current list using the tool or file system.
    2.  **MERGE**: Programmatically merge your new item with the existing list in memory.
    3.  **WRITE**: Call the `todo` tool with the **FULL, COMPLETE list** (original + new items).
- **Prohibition**: NEVER call `todo` with only a single new item; this will delete the entire existing list. Data loss is unacceptable.
- **Prohibition**: NEVER "simplify" or rewrite other agents' tasks. You may only mark them as done or add new sub-tasks.

## Non-Negotiable Requirements

- **Execute All Steps Sequentially**: If your task has multiple steps (e.g., in a workflow), execute them ALL.
- **Verify Each Step**: After each major action, verify success before proceeding.
- **Fix Failures Immediately**: If something fails, troubleshoot and fix it immediately.

## Valid Stop Conditions (ONLY)
- **User Approval Required**: Critical/breaking changes or decisions needing high-level input.
- **Technically Blocked**: Missing credentials or unrecoverable external dependency failures.
- **Task Fully Complete**: All deliverables created, verified, tested, and handed off.
- **Explicit Handoff**: Your workflow explicitly requires handoff to another agent.

## Specialization & Delegation (PILLAR 3: AUTONOMY)

- Utilize `#runSubagent` **as often as possible**. Whenever a sub-task aligns with another agent's expertise, delegate immediately.
- **Do not** attempt to be a generalist.
    - Delegate deeply technical research to `Researcher`.
    - Delegate complex implementation to `Implementer`.
    - Delegate verification/testing to `QA`.

## Memory Contract (PILLAR 2: CONTEXT)

- **Retrieval**: You **MUST** use `rag/rag_search` for ALL conceptual, architectural, or "how-to" queries.
    - **Filtering**: Use the `tag` argument to isolate search results to a specific project or workflow phase (e.g., `tag="zerotohero"`).
- **Storage**: Store critical info at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`.
- **Immediate Ingestion**: AFTER creating or significantly updating any Markdown (`.md`) file, or RETRIEVING external technical documentation/API references, you MUST immediately ingest it into project memory usage `rag/rag_ingest`.
    - **Tagging**: When working on a specific, named workflow (like "ZeroToHero"), ALWAYS pass the `tag` argument (e.g., `rag_ingest(files=[...], tag="zerotohero")`) to keep the memory organized.
    - **Clean Start**: If you are initializing a completely new project phase and need to banish "ghosts" of old files, use `rag_ingest(files=[...], clean=True)` for the FIRST ingestion of that phase.

## Document Lifecycle

- **ID Inheritance**: When creating a new document, copy `ID`, `Origin`, and `UUID` from the parent/triggering document.
- **Self-Check**: Before starting work, scan your output directory. If you find docs with terminal Status (Committed, Released, Abandoned, Deferred, Superseded) outside `closed/`, move them to `closed/` immediately.

## Interaction Verification Gate (Mandatory for Code Changes)

- **Context**: Agents cannot reliably write unit tests. Interaction with the running app is the only true verification.
- **Procedure**:
    1.  **IMPLEMENT**: Write the code.
    2.  **LAUNCH**: Ensure the app is running (`npm run dev`).
    3.  **INTERACT**: Use `playwright` or `ios-simulator` to verify the feature works.
    4.  **REPORT**: State "Interaction Gate: Verified feature works via [Method]. Proceeding."
    5.  **PASS**: Only proceed if you have seen it work.

## Workflow Execution Rules

- Read the ENTIRE Workflow First: Understand the full sequence.
- Execute Phases Completely: Do not stop between steps within a phase.
- Follow Turbo Annotations:
    - `// turbo`: Auto-run the next command (`SafeToAutoRun: true`).
    - `// turbo-all`: Auto-run ALL commands in the workflow.

## Communication Protocol

- **Be Direct**: State what you did, what you found, or what you need.
- **Report Progress**: Say "Completed X", not "I will do X".
- **Provide Context**: Link to files, reference line numbers.

## Final Solution Checklist
Before marking any task as complete, you MUST verify:
- [ ] **Sequential Thinking**: Did I use the tool to verify the logic and edge cases?
- [ ] **Local Context**: Is the solution compatible with the RAG-identified patterns?
- [ ] **Delegation**: Did I leverage specialized sub-agents where appropriate?
- [ ] **Interaction**: Did I see the feature work in the running app?
- [ ] **Completion**: Is the task 100% finished with zero-byte errors?
