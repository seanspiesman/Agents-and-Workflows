# Bug Fix & Incident Response Workflow

This workflow provides a standardized process for reproducible bug fixes, ensuring root cause analysis and non-regression.

## Workflow Overview

"Quick fixes" often cause regressions. This workflow enforces **Reproduction -> Root Cause -> Fix -> Verify**.

## Workflow Steps

### 1. Reproduction & Analysis (Analyst Agent)
- **Agent**: Analyst
- **Input**: Bug Report (User feedback, Sentry issue, etc.).
- **Action**:
  1.  Create a minimal reproduction case.
  2.  Identify the Root Cause (Code, Config, or Data?).
- **Mandatory MCP Usage**:
  - Use `grep_search` to trace the error log.
  - Use `view_file` to find the buggy logic.
  - Use `context7` to verify library behavior against documentation if external libraries are involved.
- **Output**: `agent-output/analysis/Root-Cause-Analysis.md`
- **Handoff**: `agent-output/handoffs/BugFix-Phase1-Handoff.md` (Template: Data-Only, No Fluff)

### 2. Fix Planning (Planner Agent)
- **Agent**: Planner
- **Agent**: Planner
- **Input**: `agent-output/handoffs/BugFix-Phase1-Handoff.md` AND `agent-output/analysis/Root-Cause-Analysis.md`
- **Action**: Plan the fix + determine the Regression Test strategy.
- **Output**: `agent-output/planning/Fix-Plan.md`
- **Handoff**: `agent-output/handoffs/BugFix-Phase2-Handoff.md` (Template: Data-Only, No Fluff)

### 2a. Plan Critique (Critic Agent)
- **Agent**: Critic
- **Input**: Fix Plan.
- **Action**: Assess technical soundness, regression risks, and completeness.
- **Iteration Link**: If rejected, return to **Planner**.

### 2b. Documentation Detail Verification (Critic Agent)
- **Agent**: Critic
- **Input**: `agent-output/planning/Fix-Plan.md`
- **Action**: **CRITICAL**: Review specifically for "lack of detail in the documentation". Ensure steps are explicit, context is clear, and no ambiguity exists.
- **Iteration Link**: If lacking detail, return to **Planner**.
- **Handoff**: To Implementer.

### 3. Implementation (Implementer Agent)
- **Agent**: Implementer
- **Input**: `agent-output/handoffs/BugFix-Phase2-Handoff.md` AND `agent-output/planning/Fix-Plan.md`
- **Action**:
  1.  Write a failing test (reproduction).
  2.  Fix the code.
  3.  Verify the test passes.
- **Output**: Code changes + New Test + `agent-output/implementation/Fix-Implementation.md`
- **Handoff**: `agent-output/handoffs/BugFix-Phase3-Handoff.md` (Template: Data-Only, No Fluff)

### 3b. Code Review & Refinement (Critic Agent)
- **Agent**: Critic
- **Input**: Code changes.
- **Action**: Strict code review against standards (SOLID, DRY, etc.).
- **Checks**:
  - Code Style & Standards.
  - Potential performance issues.
  - Maintainability & Readability.
- **Iteration**: Any findings must be addressed by **Implementer** before QA.
- **Handoff**: To QA.

### 4. Verification (QA Agent)
- **Agent**: QA
- **Input**: `agent-output/handoffs/BugFix-Phase3-Handoff.md` AND `agent-output/implementation/Fix-Implementation.md`
- **Action**: Verify the fix and run regression suite.
- **Mandatory MCP Usage**:
  - Use `playwright` to verify web bug fixes.
  - Use `ios-simulator` to verify mobile bug fixes. **(Always check [Troubleshooting Guide](https://github.com/joshuayoes/ios-simulator-mcp/blob/main/TROUBLESHOOTING.md) / [LLM Guide](https://raw.githubusercontent.com/joshuayoes/ios-simulator-mcp/refs/heads/main/TROUBLESHOOTING.md) first)**
  - Use `context7` to verify fix implementation against library documentation.
- **Output**: `agent-output/qa/Fix-Verification.md`
- **Iteration Loop**:
  - **FAIL**: Return to **Analyst** (if reproduction was wrong) or **Implementer**.
  - **PASS**: Bug Squashed. Create `agent-output/handoffs/BugFix-Phase4-Handoff.md` (Template: Data-Only, No Fluff).

### 5. Project Completion (Orchestrator)
- **Agent**: Orchestrator
- **Action**: Archive artifacts and generate final report.
- **Output**:
  - Move terminal artifacts to `agent-output/closed/`
  - Generate **Single** Project Completion Report: `agent-output/reports/[ID]-completion-report.md`
  - **STOP** (End of Workflow)

## Agent Roles Summary

| Agent | Role | Output Location |
| :--- | :--- | :--- |
| **Analyst** | Repro & Root Cause | `agent-output/analysis/` |
| **Planner** | Fix Strategy | `agent-output/planning/` |
| **Implementer** | Fix & Test | Codebase |
| **QA** | Verify | `agent-output/qa/` |
| **Orchestrator** | Final Report | `agent-output/reports/` |

## Workflow Diagram

```mermaid
flowchart TD
    A[Bug Report] --> B[Analyst Repro]
    B -->|Repro Fail| A
    B -->|Root Cause| C[Planner Strategy]
    C -->|Plan| D[Implementer Fix]
    D -->|Code + Test| E[QA Verification]
    E -->|Fix Failed| D
    E -->|Regression| C
    E -->|Verified| F[Released]
    F --> G[Project Completion]
    G --> H[End]
```
