# Refactoring & Tech Debt Paydown Workflow

This workflow defines a systematic, safe approach to addressing technical debt. It prioritizes stability and regression testing over speed.

## Workflow Overview

Refactoring is high-risk if done ad-hoc. This workflow enforces a cycle of **Analysis -> Design -> Implementation -> Verification**, ensuring that structure changes without altering behavior.

## Workflow Steps

### 1. Hotspot Identification (Analyst Agent)
- **Agent**: Analyst
- **Input**: Codebase, complexity metrics, or "gut feel" from developers.
- **Execution**: Use the `runSubagent` tool to run the **Analyst** agent.
    - **Task**: "Read `custom-agents/instructions/output_standards.md`. Identify hotspots (complexity, legacy patterns). Output Refactoring Opportunity Doc."
- **Handoff**: `agent-output/handoffs/refactor-phase-1-handoff.md` (Template: Data-Only, No Fluff)

### 2. Pattern Selection (Architect Agent)
- **Agent**: Architect
- **Input**: `agent-output/handoffs/refactor-phase-1-handoff.md` AND `agent-output/analysis/refactoring-opp.md`
- **Execution**: Use the `runSubagent` tool to run the **Architect** agent.
    - **Task**: "Read `custom-agents/instructions/output_standards.md`. Propose new structure/design patterns. Output Architecture Decision Record (ADR)."
- **Output**: An Architecture Decision Record (ADR) or Design Sketch in `agent-output/architecture/adr.md`.
- **Handoff**: `agent-output/handoffs/refactor-phase-2-handoff.md` (Template: Data-Only, No Fluff)

### 3. Step-by-Step Planning (Planner Agent)
- **Agent**: Planner
- **Input**: `agent-output/handoffs/refactor-phase-2-handoff.md` AND `agent-output/architecture/adr.md`
- **Execution**: Use the `runSubagent` tool to run the **Planner** agent.
    - **Task**: "Read `custom-agents/instructions/output_standards.md`. Break refactoring into atomic, safe steps that maintain compiling state. Output Refactoring Plan."
- **Constraint**: Each step must leave the system in a compiling, passing state.
- **Output**: A Refactoring Plan in `agent-output/planning/refactor-plan.md`.
- **Handoff**: `agent-output/handoffs/refactor-phase-3-handoff.md` (Template: Data-Only, No Fluff)

### 3a. Method Critique (Critic Agent)
- **Agent**: Critic
- **Input**: Refactoring Plan.
- **Action**: Use the `runSubagent` tool to run the Critic agent to verify the plan follows the pattern correctly and maintains safety.
- **Iteration**: Return to **Planner** if unsafe.

### 3b. Documentation Detail Verification (Critic Agent)
- **Agent**: Critic
- **Input**: `agent-output/planning/refactor-plan.md`
- **Action**: **CRITICAL**: Use the `runSubagent` tool to run the Critic agent to review specifically for "lack of detail". Refactoring requires atomic precision. Ensure no step is vague.
- **Iteration**: Return to **Planner** if lacking detail.
- **Handoff**: To Implementer.

### 4. Safe Implementation (Implementer Agent)
- **Agent**: Implementer
- **Input**: `agent-output/handoffs/refactor-phase-3-handoff.md` AND `agent-output/planning/refactor-plan.md`
- **Execution**: Use the `runSubagent` tool to run the **Implementer** agent.
    - **Task**: "Read `custom-agents/instructions/output_standards.md`. Execute plan safely (Test -> Refactor -> Test cycle). Output Code changes."
- **Output**: Code changes + `agent-output/implementation/refactor-impl.md`
- **Handoff**: `agent-output/handoffs/refactor-phase-4-handoff.md` (Template: Data-Only, No Fluff)

### 4b. Code Review & Refinement (Critic Agent)
- **Agent**: Critic
- **Input**: Code changes.
- **Action**: Use the `runSubagent` tool to run the Critic agent to check for regression in code quality or readability.
- **Checks**:
  - Code Style & Standards.
  - Complexity metrics.
- **Iteration**: Any findings must be addressed by **Implementer** before QA.
- **Handoff**: To QA.

### 5. Regression Verification (QA Agent)
- **Agent**: QA
- **Input**: `agent-output/handoffs/refactor-phase-4-handoff.md` AND `agent-output/implementation/refactor-impl.md`
- **Action**: Use the `runSubagent` tool to run the QA agent to run the full regression suite. Verify no behavior changes.
- **Mandatory MCP Usage**:
  - Use `run_command` to execute test suites.
  - Use `playwright` (Web) or `ios-simulator` (Mobile) to verify UI behavior if applicable. **(For ios-simulator: check [Troubleshooting Guide](https://github.com/joshuayoes/ios-simulator-mcp/blob/main/TROUBLESHOOTING.md) / [LLM Guide](https://raw.githubusercontent.com/joshuayoes/ios-simulator-mcp/refs/heads/main/TROUBLESHOOTING.md))**
  - Use `context7` to verify refactored code usage against library documentation.
  - Use `view_code_item` to manually verify signatures if needed.
- **Iteration Loop**:
  - **FAIL**: Return to **Implementer**. The refactoring broke something. Revert or Fix.
  - **PASS**: Refactor successful. Create `agent-output/handoffs/refactor-phase-5-handoff.md` (Template: Data-Only, No Fluff).

### 6. Project Completion (Orchestrator)
- **Agent**: Orchestrator
- **Action**: Archive artifacts and generate final report.
- **Output**:
  - Move terminal artifacts to `agent-output/closed/`
  - Generate **Single** Project Completion Report: `agent-output/reports/[ID]-completion-report.md`
  - **STOP** (End of Workflow)

## Agent Roles Summary

| Agent | Role | Output Location |
| :--- | :--- | :--- |
| **Analyst** | Identify Debt | `agent-output/analysis/` |
| **Architect** | Define Target State | `agent-output/architecture/` |
| **Planner** | Atomic Steps | `agent-output/planning/` |
| **Implementer** | Execute Refactor | Codebase |
| **QA** | Regression Test | `agent-output/qa/` |
| **Orchestrator** | Final Report | `agent-output/reports/` |

## Workflow Diagram

```mermaid
flowchart TD
    A[Codebase Hotspot] --> B[Analyst Analysis]
    B -->|Opportunity Doc| C[Architect Design]
    C -->|Pattern/ADR| D[Planner Strategy]
    D -->|Atomic Plan| E[Safe Implementation]
    E -->|Code Change| F[QA Regression]
    F -->|Tests Fail| E
    F -->|Tests Pass| G[Success]
    G --> H[Project Completion]
    H --> I[End]
```
