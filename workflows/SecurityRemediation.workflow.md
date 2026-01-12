# Security Remediation Workflow

This workflow defines the standard process for addressing security vulnerabilities. It emphasizes root cause analysis and comprehensive verification.

## Workflow Overview

Security fixes must be precise. This workflow ensures we don't just "patch" the symptom but understand and fix the root cause, verifying it with the same rigor used to find it.

## Workflow Steps

### 1. Triage & Assessment (Security Agent)
- **Agent**: Security
- **Input**: Vulnerability report (from tool or external source).
- **Action**: Assess severity (CVSS), impact, and risk.
- **Output**: Security Incident Ticket in `agent-output/security/` (e.g., `SEC-001-sql-injection.md`).
- **Handoff**: Passed to Analyst.

### 2. Root Cause Analysis (Analyst Agent)
- **Agent**: Analyst
- **Input**: Security Incident Ticket.
- **Action**: Locate the vulnerability in code and uncovers the root cause.
- **Mandatory MCP Usage**:
  - Use `grep_search` to find all occurrences of the pattern.
  - User `view_file` to trace the data flow from sink to source.
- **Output**: Analysis Report detailing the "Sink", "Source", and "Data Flow".
- **Handoff**: Passed to Planner.

### 3. Remediation Planning (Planner Agent)
- **Agent**: Planner
- **Input**: Analysis Report.
- **Action**: Plan the fix.
- **Considerations**: patches, library upgrades, or code rewrites. Must consider side effects.
- **Output**: Remediation Plan.
- **Handoff**: Passed to Implementer.

### 4. Application of Fix (Implementer Agent)
- **Agent**: Implementer
- **Input**: Remediation Plan.
- **Action**: Apply the fix.
- **Output**: Code changes.
- **Handoff**: Passed to Security.

### 5. Verification (Security Agent)
- **Agent**: Security
- **Input**: Code changes.
- **Action**: Verify the fix *specifically* addresses the vulnerability.
- **Mandatory MCP Usage**:
  - Use `view_file` to inspect the diff.
  - Use `run_command` to run security scanners if available.
- **Iteration Loop**:
  - **FAIL**: Fix is ineffective or incomplete. Return to **Analyst** (if root cause wrong) or **Implementer** (if implementation flawed).
  - **PASS**: Issue Resolved.

## Agent Roles Summary

| Agent | Role | Output Location |
| :--- | :--- | :--- |
| **Security** | Triage & Verify | `agent-output/security/` |
| **Analyst** | Root Cause | `agent-output/analysis/` |
| **Planner** | Plan Fix | `agent-output/planning/` |
| **Implementer** | Apply Fix | Codebase |

## Workflow Diagram

```mermaid
flowchart TD
    A[Vulnerability Found] --> B[Security Triage]
    B -->|Incident Ticket| C[Analyst Root Cause]
    C -->|Analysis Doc| D[Planner Strategy]
    D -->|Remediation Plan| E[Implement Fix]
    E -->|Code Change| F[Security Verification]
    F -->|Fix Failed| E
    F -->|Root Cause Missed| C
    F -->|Verified| G[Resolved]
```
