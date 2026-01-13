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
- **Action**: The Planner agent creates a detailed action plan based on the feedback.
- **Output**: A plan document in `agent-output/planning/` with:
  - Value Statement and Business Objective
  - Detailed steps for implementation
  - Acceptance criteria
  - Dependencies and risks
  - Target release version (aligned with roadmap)
- **Handoff**: The plan is submitted to the Critic agent for review.
- **Validation**: Planner ensures the plan aligns with the Master Product Objective and architectural guidelines.
- **Mandatory Tools**: Use `context7` to research capabilities if external libraries are involved.

### 3. Plan Review (Critic Agent)
- **Agent**: Critic
- **Action**: The Critic agent reviews the plan for clarity, completeness, and alignment with architectural guidelines.
- **Output**: A critique document in `agent-output/critiques/` with:
  - Findings (Critical/Medium/Low)
  - Questions or concerns
  - Recommendations for improvement
- **Handoff**: If the plan is approved, it is handed off to the Implementer agent. If not, it is sent back to the Planner for revisions.

### 4. Architectural Validation (Architect Agent)
- **Agent**: Architect
- **Action**: The Architect agent validates the plan's architectural alignment and identifies potential risks or improvements.
- **Output**: Architectural review document with:
  - Alignment assessment
  - Potential risks or improvements
  - Recommendations for implementation
- **Handoff**: If approved, the plan is handed off to the Implementer agent. If not, it is sent back to the Planner for revisions.

### 6. Quality Assurance (QA Agent)
- **Agent**: QA
- **Action**: The QA agent verifies the implementation through testing and validation.
- **Output**: QA report in `agent-output/qa/` with:
  - Test execution results
  - Coverage analysis
  - Issues or failures
- **Handoff**: If QA passes, the implementation is handed off to the UAT agent. If not, it is sent back to the Implementer for fixes.
- **Validation**: QA ensures all tests pass and coverage meets requirements. TDD compliance is verified
- **Validation**: Implementer ensures all new functions/classes follow TDD (Test-Driven Development) principles
- **7. User Acceptance Testing (UAT Agent)
- **Agent**: UAT
- **Action**: The UAT agent validates that the implementation meets user expectations and delivers the intended value.
- **Output**: UAT report in `agent-output/uat/` with:
  - User-facing validation
  - Feedback on usability and functionality
- **Handoff**: If UAT passes, the workflow is complete. If not, it may loop back to the Planner or Implementer for adjustments.
- **Validation**: UAT ensures the implementation delivers the stated value and meets acceptance criteria
  - 8. Retrospective (Retrospective Agent)
- **Agent**: Retrospective
- **Action**: The Retrospective agent captures lessons learned from the process.
- **Output**: Retrospective document in `agent-output/retrospectives/` with:
  - What went well
  - Areas for improvement
  - Process recommendations
- **Handoff**: Recommendations are sent to the PI agent for process improvements.
- **Validation**: Retrospective ensures lessons learned are documented and shared
  - User-facing validation
  - Feedback on usability and functionality
- **Handoff**: If UAT passes, the workflow is complete. If not, it may loop back to the Planner or Implementer for adjustments.

### 7. Retrospective (Retrospective Agent)
- **Agent**: Retrospective
- **Action**: The Retrospective agent captures lessons learned from the process.
- **Output**: Retrospective document in `agent-output/retrospectives/` with:
  - What went well
  - Areas for improvement
  - 9. Process Improvement (PI Agent)
- **Agent**: PI
- **Action**: The PI agent analyzes the retrospective and updates workflows or agent instructions as needed.
- **Output**: Process improvement document in `agent-output/process-improvement/` with:
  - Changes made to agent instructions
  - Updated workflows or guidelines
- **Handoff**: The workflow is complete.
- **Validation**: PI ensures process improvements are implemented and documentedent in `agent-output/process-improvement/` with:
  - Changes made to agent instructions
  - Updated workflows or guidelines
- **Handoff**: The workflow is complete.

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