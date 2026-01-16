# Global Agent Instructions

> [!IMPORTANT]
> These instructions apply to **ALL AGENTS** in the system and must be followed with the highest priority. Load this file at the start of every session.

---

## 1. Core Mandate: FINISH WHAT YOU START

**Autonomy means autonomous COMPLETION, not autonomous STOPPING.**

Every agent is assigned a specific role and responsibility. **YOU MUST NOT STOP** until your assigned task is completely finished. Half-done work is worse than no work—it creates technical debt and breaks the chain of accountability.

### Non-Negotiable Requirements
1.  **Execute All Steps Sequentially**: If your task has multiple steps (e.g., in a workflow), execute them ALL.
2.  **Verify Each Step**: After each major action, verify success before proceeding.
3.  **Fix Failures Immediately**: If something fails, troubleshoot and fix it immediately.
4.  **No Premature Halting**: Do not stop after a single tool call unless blocked.
5.  **Anti-Stalling**: Do not ask "What should I do next?" if your instructions or workflow already answer that.

### Valid Stop Conditions (ONLY)
1.  **User Approval Required**: Critical/breaking changes or decisions needing high-level input.
2.  **Technically Blocked**: Missing credentials or unrecoverable external dependency failures.
3.  **Task Fully Complete**: All deliverables created, verified, tested, and handed off.
4.  **Explicit Handoff**: Your workflow explicitly requires handoff to another agent.

---

## 2. Collaboration Contract (MANDATORY)

The `collaboration-tracking` skill is **NON-OPTIONAL**. Failure to log your actions breaks the audit trail.

### A. Check Global Context
*   **File**: `agent-output/cli.md`
*   **Action**: ALWAYS check this file at the start of your task for shared context.

### B. Log ALL Handoffs
### B. Log ALL Handoffs
*   **File**: `agent-output/logs/handoff_history.log`
*   **Format**: `[Timestamp] SourceAgent -> TargetAgent`
*   **Command**:
    ```bash
    mkdir -p agent-output/logs && echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [Source] -> [Target]" >> agent-output/logs/handoff_history.log
    ```

### C. Log CLI History
### C. Log CLI History
*   **File**: `agent-output/logs/cli_history.log`
*   **Requirement**: Log ALL `run_command` executions.
*   **Format**: `[Timestamp] [Agent] [Tool] [Command]`
*   **Command**:
    ```bash
    echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [Agent] [run_command] [Command]" >> agent-output/logs/cli_history.log
    ```

### D. Log Side-Effect Tool Usage
### D. Log Side-Effect Tool Usage
*   **File**: `agent-output/logs/tool_usage_history.log`
*   **Scope**: Log `write_to_file`, `replace_file_content`, `run_command` (side-effects only). Do not log read-only tools.
*   **Format**: `[Timestamp] [Agent] [Tool]`
*   **Command**:
    ```bash
    echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [YourAgent] [Tool]" >> agent-output/logs/tool_usage_history.log
    ```

---

## 3. Memory Contract

**Key behaviors:**
*   **Retrieval**: Retrieve context at decision points (2–5 times per task) using semantic search (e.g., `@codebase`).
*   **Storage**: Store critical info at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`.
*   **Failure Mode**: If memory tools fail, announce "No-Memory Mode" immediately but PROCEED.

---

## 4. Document Lifecycle

**ID Inheritance**: When creating a new document, copy `ID`, `Origin`, and `UUID` from the parent/triggering document.

**Document Header Format**:
```yaml
---
ID: [from parent]
Origin: [from parent]
UUID: [from parent]
Status: Active
---
```

**Self-Check**: Before starting work, scan your output directory. If you find docs with terminal Status (Committed, Released, Abandoned, Deferred, Superseded) outside `closed/`, move them to `closed/` immediately.

---

## 5. TDD Gate Procedure (Mandatory for Code Changes)

**Execute for EACH new function or class:**
1.  **STOP**: Do NOT write implementation code yet.
2.  **WRITE**: Create test file with failing test.
3.  **RUN**: Execute test and verify it fails with the RIGHT reason (ModuleNotFoundError, undefined, AssertionError).
4.  **REPORT**: State "TDD Gate: Test `test_X` fails as expected: [error]. Proceeding."
5.  **IMPLEMENT**: Write ONLY the minimal code to make the test pass.
6.  **VERIFY**: Run test again, confirm it passes.

---

## 6. Workflow Execution Rules

1.  **Read the ENTIRE Workflow First**: Understand the full sequence.
2.  **Execute Phases Completely**: Do not stop between steps within a phase.
3.  **Follow Turbo Annotations**:
    *   `// turbo`: Auto-run the next command (`SafeToAutoRun: true`).
    *   `// turbo-all`: Auto-run ALL commands in the workflow.
4.  **Anti-Pattern**: Do NOT stop after Phase 1 of a multi-phase workflow.

---

## 7. Communication Protocol

*   **Be Direct**: State what you did, what you found, or what you need.
*   **Report Progress**: Say "Completed X", not "I will do X".
*   **Provide Context**: Link to files, reference line numbers.

**Response Format Template**:
```markdown
```
**Next Steps**:
- [ ] [Next action 1]
```

---

## 8. General Operation & Safety

### A. Drift Check Protocol
**Frequency**: Every 5 steps or major actions.
**Action**: Re-read the original PROMPT document (e.g., `user_request.md` or the prompt file passed in arguments).
**Check**: "Have I drifted into a generic template? Am I still referencing the specific 'Blues Harmonica' or 'Pixel Arcade' details?"

### B. Artifact Integrity Protocol
**Trigger**: Before marking ANY task/file creation as "Done".
**Action**: Verify the file size of the generated artifact.
**Rule**: If file size is 0 bytes, **FAIL** and **RETRY**. Do not proceed with empty files.
**Command**: `ls -l [file_path]` to verify size > 0.

---

## 9. Fresh Context Protocol (Anti-Amnesia)

**Problem**: Chat history is truncated in long workflows.
**Solution**: Rely on **FILES**, not Chat.

### A. Start of Task: Read-First Mandate
At the beginning of ANY phase or task, you **MUST**:
1.  **Ignore Chat History**: Assume the chat context is incomplete or summarized.
2.  **Read the Anchor Artifact**: Read the specific `Handoff Artifact` or `Report` defined as your input (e.g., `Phase1-Complete.md`).
3.  **Trust the File**: The file contains the ground truth. If chat history contradicts the file, the file wins.

### B. End of Task: The "No-Fluff" Handoff
When handing off to the next agent, you **MUST** create a `[Phase]-Handoff.md`.
**Constraint**: **ZERO FLUFF**.
-   **BANNED**: "Here is the report", "I hope this helps", "As per your request", "In this document we will...".
-   **REQUIRED**: Bullet points, direct links, data tables, raw facts.
-   **Goal**: Maximum information density per token.

**Template**:
```markdown
# Phase X Handoff
**Source**: [Agent Name]
**Target**: [Next Agent Name]
**Context**: [Link to main report]

## Critical Context
- Key Decision 1: [Result]
- Constraint: [Constraint]

## Required Next Actions
1. [Action]
2. [Action]
```

## 10. Data-Only Output Protocol (Token Optimization)

**Objective**: Maximize "Fresh Context" efficiency by eliminating token waste.
**Target**: All artifacts in `agent-output/`.

**OUTPUT CONSTRAINT**: Artifacts must be **DATA-ONLY**.
*   **BANNED**: Introductions, conclusions, "As requested", "Here is the file", "I hope this helps".
*   **BANNED**: Explanations of standard technologies (e.g., "Redis is a specific key-value store...").
*   **BANNED**: Generic best practices (e.g., "We will ensure clean code...").
*   **REQUIRED**: Tables for stacks, Mermaid for flows, JSON for config.
*   **Format Constraint**: If you write "This document outlines...", **YOU FAIL**.
*   **Style**: Dense, Senior-Level Technical. Assume the reader knows the basics. Do NOT list "Clean Code" principles. Just write clean code.
