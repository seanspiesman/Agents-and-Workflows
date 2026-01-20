# Changelog: workflows/

All notable changes to workflow definitions in this directory.

---

## [Thu Jan 16 14:51:00 PST 2026] — Agent Improvements Implementation

### ZeroToHero.workflow.md
- **Added**: Phase 1 now requires creation of `agent-output/project_context.md` (Single Source of Truth for Name, Stack, Constraints).
- **Added**: Phase 3 now includes `Constraint Audit (QA)` step to validate System Architecture against `project_context.md`.
- **Added**: Explicit FAIL condition if "Local-Only" app has server components (AWS, Kubernetes, Auth wrappers).

---

## [Thu Jan 16 15:05:00 PST 2026] — User Edit

### ZeroToHero.workflow.md
- **Changed**: Phase 0 (Environment Validation) commented out by user.

---

## [Thu Jan 16 08:03:00 PST 2026] — Token Efficiency Optimization

### ZeroToHero.workflow.md
- **Changed**: Refactored handoff protocol to enforce "Dense Handoffs" (Data-Only Protocol) instead of verbose reports.

---

## [Thu Jan 16 02:28:00 PST 2026] — Logging/Output Standardization

### ZeroToHero.workflow.md
- **Added**: `Workflow Governance` section enforcing logging of tool usage and CLI commands to `agent-output/logs/`.
- **Added**: Output Structure rules: Agents write only to `agent-output/[role]/`.
- **Added**: Handoffs saved to `agent-output/handoffs/`.
