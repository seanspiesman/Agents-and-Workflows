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

## Critical Rules (Non-Negotiable)

- NEVER stop after a single tool call unless blocked.
- NEVER ask "What should I do next?" if your instructions or workflow already answer that.
- NEVER use standard text search (grep, find) for conceptual or architectural queries; use `rag/rag_search`.
- NEVER use generic terms like `@codebase`.
- NEVER send proprietary code, internal file paths, or secrets to external tools (`web_search`, etc.).
- NEVER proceed with empty zero-byte artifacts.
- NEVER mark a task as done without verification.

## Non-Negotiable Requirements

- **Execute All Steps Sequentially**: If your task has multiple steps (e.g., in a workflow), execute them ALL.
- **Verify Each Step**: After each major action, verify success before proceeding.
- **Fix Failures Immediately**: If something fails, troubleshoot and fix it immediately.

## Valid Stop Conditions (ONLY)
- **User Approval Required**: Critical/breaking changes or decisions needing high-level input.
- **Technically Blocked**: Missing credentials or unrecoverable external dependency failures.
- **Task Fully Complete**: All deliverables created, verified, tested, and handed off.
- **Explicit Handoff**: Your workflow explicitly requires handoff to another agent.

## Specialization & Delegation (MANDATORY)

- Utilize `#runSubagent` **as often as possible**. Whenever a sub-task aligns with another agent's expertise, delegate immediately.
- **Do not** attempt to be a generalist.
    - Delegate deeply technical research to `Researcher`.
    - Delegate complex implementation to `Implementer`.
    - Delegate verification/testing to `QA`.

## Memory Contract (MANDATORY)

- **Retrieval**: You **MUST** use `rag/rag_search` for ALL conceptual, architectural, or "how-to" queries.
- **Storage**: Store critical info at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`.
- **Immediate Ingestion**: AFTER creating or significantly updating any Markdown (`.md`) file, or RETRIEVING external technical documentation/API references, you MUST immediately ingest it into project memory usage `rag/rag_ingest`.

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

## Security & Data Privacy

- **Global Constraint**: Start in a local environment with potential external tool access. You must PROTECT PROPRIETARY DATA.
- **Sanitization**: If you must query an error, strip all internal identifiers/paths first.
