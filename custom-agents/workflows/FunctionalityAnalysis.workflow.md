# Functionality Analysis Workflow

This workflow provides a structured approach to deeply analyzing specific application functionality (e.g., submission flows, user interactions). It delivers a comprehensive critique, structural breakdown, visual diagrams, and improvement suggestions.

## Workflow Overview

This workflow is designed to be thorough and agent-driven, utilizing the Analyst, Critic, Architect, and Planner agents to deconstruct, evaluate, and reimagine parts of the codebase. It moves from **Discovery -> Analysis -> Critique -> Visualization -> Recommendation**.

## Workflow Steps

### 1. Scope Definition & Discovery (Analyst Agent)
- **Agent**: Analyst
- **Input**: User-defined functionality name or entry point (e.g., "User Submission Flow").
- **Action**: Identify the core files, entry points, and dependencies related to the requested functionality.
- **Mandatory MCP Usage**:
  - Use `find_by_name` to locate relevant files matching the functionality keywords.
  - Use `grep_search` to find usage of key terms or components.
  - Use `list_dir` to understand the surrounding file structure.
- **Output**: A Scope Definition document in `agent-output/analysis/` (e.g., `001-scope-definition.md`) listing all relevant files and entry points.
- **Handoff**: Passed to Analyst for Phase 2.

### 2. Structural Analysis & Logic Tracing (Analyst Agent)
- **Agent**: Analyst
- **Input**: Scope Definition document.
- **Action**: Deep dive into the code to trace execution paths, data flow, and state management.
- **Mandatory MCP Usage**:
  - Use `view_file` to read the code logic.
  - Use `view_code_item` to inspect specific functions or classes.
  - Use `context7` (if applicable) to understand library usage.
- **Output**: An "Existing Structure" document in `agent-output/analysis/` (e.g., `002-existing-structure.md`) detailing:
  - Step-by-step logic flow.
  - State changes and side effects.
  - Data models involved.
- **Handoff**: Passed to Critic.

### 3. Code Critique (Critic Agent)
- **Agent**: Critic
- **Input**: Existing Structure document and Raw Code.
- **Action**: Evaluate the implementation against best practices, performance standards, and maintainability guidelines.
- **Checks**:
  - **Code Quality**: DRY principles, naming conventions, complexity.
  - **Performance**: Potential bottlenecks, unnecessary renders/computations.
  - **Security**: Basic vulnerability checks (input validation, auth checks).
  - **UX/UI**: (If applicable) Interaction feedback, state handling.
- **Output**: A Critique document in `agent-output/analysis/` (e.g., `003-critique.md`) with rated severity (Low/Medium/High) for each issue.
- **Handoff**: Passed to Architect.

### 4. Visual Synthesis (Architect Agent)
- **Agent**: Architect
- **Input**: Existing Structure document.
- **Action**: Generate Mermaid diagrams to visualize the control flow and architecture.
- **Visual Requirements**:
  - **Mandatory Skill**: Load `mermaid-diagramming` skill.
  - **Action**: Follow all syntax rules and best practices defined in the skill to generate error-free diagrams.
- **Output**: An Architecture Diagrams document in `agent-output/architecture/` (e.g., `004-current-flow-diagrams.md`).
- **Handoff**: Passed to Planner.

### 5. Improvement Proposals (Planner Agent)
- **Agent**: Planner
- **Input**: Critique document and Architecture Diagrams.
- **Action**: Propose concrete, actionable updates to address the critique and improve the structure.
- **Action**: Create a plan for refactoring or enhancing the functionality.
- **Output**: A "Suggested Updates" document in `agent-output/planning/` (e.g., `005-suggested-updates.md`) containing:
  - Refactoring plan.
  - New feature suggestions.
  - Architecture improvements.
- **Handoff**: Passed to Orchestrator.

### 6. Final Report Assembly (Orchestrator Agent)
- **Agent**: Orchestrator
- **Input**: All previous artifacts.
- **Action**: Compile a single, comprehensive report for the user.
- **Output**: `Functionality-Analysis-Report.md` in `agent-output/`.
  - Executive Summary.
  - Current Structure & Diagrams.
  - Critical Findings.
  - Recommended Next Steps.
  - **STOP** (End of Workflow).

## Agent Roles Summary

| Agent | Role | Output Location |
| :--- | :--- | :--- |
| **Analyst** | Discovery & Structure Analysis | `agent-output/analysis/` |
| **Critic** | Code & Design Critique | `agent-output/analysis/` |
| **Architect** | Visual Diagrams (Mermaid) | `agent-output/architecture/` |
| **Planner** | Improvement Proposals | `agent-output/planning/` |
| **Orchestrator** | Final Report Assembly | `agent-output/` |

## Workflow Diagram

```mermaid
flowchart TD
    A[Start: Analysis Request] --> B[Scope Definition]
    B -->|Scope Doc| C[Structural Analysis]
    C -->|Structure Doc| D[Code Critique]
    C -->|Structure Doc| E[Visual Synthesis]
    D -->|Critique Doc| F[Improvement Proposals]
    E -->|Diagrams| F
    F -->|Suggestions| G[Final Report Assembly]
    G --> H[End]
```
