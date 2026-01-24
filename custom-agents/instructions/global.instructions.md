---
applyTo: '*'
---

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
*   **File**: `agent-output/logs/handoff_history.md`
*   **Format**: `[SourceAgent] -> [TargetAgent] (Timestamp)`
*   **Command**:
    ```bash
    mkdir -p agent-output/logs && echo "- YourAgent -> TargetAgent ($(date -u +%Y-%m-%dT%H:%M:%SZ))" >> agent-output/logs/handoff_history.md
    ```

### C. Log CLI History
*   **File**: `agent-output/logs/cli_history.md`
*   **Requirement**: Log ALL `run_command` executions.
*   **Format**: `[Timestamp] [Agent] [Tool] [Command]`
*   **Command**:
    ```bash
    echo "- [$(date -u)] [YourAgent] \`[your-command-here]\`" >> agent-output/logs/cli_history.md
    ```

### D. Log Side-Effect Tool Usage
*   **File**: `agent-output/logs/tool_usage_history.md`
*   **Scope**: Log `write_to_file`, `replace_file_content`, `run_command` (side-effects only). Do not log read-only tools.
*   **Format**: `[Timestamp] [Agent] [Tool] [Target]`
*   **Command**:
    ```bash
    echo "- [$(date -u)] [YourAgent] [Tool] [Target]" >> agent-output/logs/tool_usage_history.md
    ```

### E. Delegation Mandate (MANDATORY)
*   **Rule**: You MUST utilize `#runSubagent` whenever a sub-task aligns with another agent's expertise.
*   **Constraint**: **Do not** attempt to be a generalist.
*   **Examples**:
    *   Delegate deeply technical research to `Researcher`.
    *   Delegate complex implementation to `Implementer`.
    *   Delegate verification/testing to `QA`.
*   **Goal**: Maximize the use of the specialized agentic toolset.

---

## 3. Memory Contract

**Key behaviors:**
*   **Retrieval (MANDATORY)**: You **MUST** use **`rag/rag_search`** for ALL conceptual, architectural, or "how-to" queries.
    *   **FORBIDDEN**: Do NOT use standard text search tools (grep, find, codebase_search) for understanding concepts, patterns, or architecture. Only use them for finding specific string literals (e.g., variable names).
    *   **Anti-Pattern**: Do NOT use generic terms like `@codebase`. You MUST use the `rag/rag_search` tool.
*   **Storage**: Store critical info at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`.
*   **Failure Mode**: If memory tools fail, announce "No-Memory Mode" immediately but PROCEED.
*   **Immediate Ingestion**: AFTER creating or significantly updating any Markdown (`.md`) file, you MUST immediately ingest it into project memory:
    > Call the `rag/rag_ingest` tool with the file path.
    > *Example*: `rag/rag_ingest(files=["/abs/path/to/agent-output/plan.md"])`

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

## 9. Security & Data Privacy (MANDATORY)

**Global Constraint**: You are operating in a local environment with potential external tool access. You must PROTECT PROPRIETARY DATA.

### External Tool Usage Rules (`context7`, `web`, `web_search`)
These tools transmit data to external servers (Upstash, Search Engines).
1.  **NEVER** send proprietary code, internal file paths, API keys, or secrets in queries or context to these tools.
2.  **ALLOWED**: Searching for public library names (e.g., "react usage"), generic error messages (e.g., "TypeError: undefined"), or documentation lookups.
3.  **FORBIDDEN**: "How do I fix [MyProprietaryClass]?", "Refactor this [internal code block]".
4.  **Sanitization**: If you must query an error, strip all internal identifiers/paths first.
