# Feedback Workflow

This workflow defines the process for handling feedback, implementing changes, and ensuring quality through agent collaboration.

## Workflow Overview

This workflow ensures that feedback is systematically analyzed, planned, implemented, tested, and validated before being released. It follows a structured approach to maintain quality and alignment with the project's objectives.

## Workflow Steps

### 1. Receive Feedback
- **Input**: A piece of feedback describing a desired change or improvement.
- **Action**: The user provides the feedback to the system.
- **Output**: Feedback is documented and assigned a unique identifier for tracking.

### 2. Create Action Plan (Planner Agent)
- **Agent**: Planner
- **Execution**: Use the `runSubagent` tool to run the **Planner** agent.
    - **Task**: "Create a detailed action plan based on the feedback. Include Value Statement, Implementation Steps, Acceptance Criteria, and Risks. Use `context7` for research. Output to `agent-output/planning/`."

### 3. Plan Review (Critic Agent)
- **Agent**: Critic
- **Action**: Use the `runSubagent` tool to run the Critic agent to review the plan for clarity, completeness, and alignment with architectural guidelines.
- **Output**: A critique document in `agent-output/critiques/` with:
  - Findings (Critical/Medium/Low)
  - Questions or concerns
  - Recommendations for improvement
- **Handoff**: If the plan is approved, it is handed off to the Implementer agent. If not, it is sent back to the Planner for revisions.

### 4. Architectural Validation (Architect Agent)
- **Agent**: Architect
- **Action**: Use the `runSubagent` tool to run the Architect agent to validate the plan's architectural alignment and identify potential risks or improvements.
- **Output**: Architectural review document with:
  - Alignment assessment
  - Potential risks or improvements
  - Recommendations for implementation
- **Handoff**: If approved, the plan is handed off to the Implementer agent. If not, it is sent back to the Planner for revisions.

### 4b. Documentation Detail Verification (Critic Agent)
- **Agent**: Critic
- **Input**: Approved Plan.
- **Action**: **CRITICAL**: Use the `runSubagent` tool to run the Critic agent to review specifically for "lack of detail in the documentation". Ensure all acceptance criteria and implementation steps are exhaustive.
- **Iteration**: If lacking detail, return to **Planner**.

### 5. Implementation (Implementer Agent)
- **Agent**: Implementer
- **Execution**: Use the `runSubagent` tool to run the **Implementer** agent.
    - **Task**: "Implement the changes defined in the plan using `run_command` and file edits. Output code changes and tests."

- **Handoff**: Passed to Critic.

### 5b. Code Review & Refinement (Critic Agent)
- **Agent**: Critic
- **Input**: Code changes.
- **Action**: Use the `runSubagent` tool to run the Critic agent to perform strict code review against standards.
- **Checks**:
  - Code Style & Standards.
  - Potential performance issues.
  - Maintainability & Readability.
- **Iteration**: Any findings must be addressed by **Implementer** before QA.
- **Handoff**: Passed to QA.

### 6. Quality Assurance (QA Agent)
- **Agent**: QA
- **Action**: Use the `runSubagent` tool to run the QA agent to verify the implementation through testing and validation.
- **Output**: QA report in `agent-output/qa/`.
- **Handoff**: If QA passes, the implementation is handed off to the UAT agent. If not, it is sent back to the Implementer for fixes.

### 7. User Acceptance Testing (UAT Agent)
- **Agent**: UAT
- **Action**: Use the `runSubagent` tool to run the UAT agent to validate that the implementation meets user expectations and delivers the intended value.
- **Output**: UAT report in `agent-output/uat/`.
- **Handoff**: If UAT passes, the workflow is complete (to Retrospective).

### 8. Retrospective (Retrospective Agent)
- **Agent**: Retrospective
- **Action**: Use the `runSubagent` tool to run the Retrospective agent to capture lessons learned.
- **Output**: Retrospective document in `agent-output/retrospectives/`.

### 9. Process Improvement (PI Agent)
- **Agent**: PI
- **Action**: Use the `runSubagent` tool to run the PI agent to update workflows or agent instructions.
- **Output**: Process improvement document.
- **Handoff**: Workflow complete.

### 10. Project Completion (Orchestrator)
- **Agent**: Orchestrator
- **Action**: Archive artifacts and generate final report.
- **Output**:
  - Move terminal artifacts to `agent-output/closed/`
  - Generate **Single** Project Completion Report: `agent-output/completion/[ID]-completion-report.md`
  - **STOP** (End of Workflow)

## Agent Roles Summary

| Agent | Role | Output Location |
|-Architect | Validate architectural alignment | `agent-output/architecture/` |
| ------|------|-----------------|
| Planner | Create action plans | `agent-output/planning/` |
| Critic | Review and validate plans | `agent-output/critiques/` |
| Implementer | Execute implementation | `agent-output/implementation/` |
| QA | Test and validate code | `agent-output/qa/` |
| UAT | Validate user-facing changes | `agent-output/uat/` |
| Retrospective | Capture lessons learned | `agent-output/retrospectives/` |
| PI | Improve workflows | `agent-output/process-improvement/` |
| **Orchestrator** | Final Report | `agent-output/completion/` |

## Workflow Diagram

```mermaid
flowchart TD
    A[Receive Feedback] --> B[Create Action Plan]
    B -->|Plan| C[Review Plan]
    C -->|Approved| D[Implement Changes]
    C -->|Rejected| B
    D -->|Implementation| E[QA Testing]
    E -->|Passed| F[UAT Validation]
    E -->|Failed| D
    F -->|Passed| G[Retrospective]
    F -->|Failed| B
    G --> H[Process Improvement]
    H --> I[Project Completion]
    I --> J[End]
```