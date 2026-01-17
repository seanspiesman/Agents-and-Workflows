# Changelog: agents/

All notable changes to agent definitions in this directory.

---

## [Fri Jan 16 16:40:00 PST 2026] — No Silent Failures Protocol

### global.instructions.md
- **Added**: `Tool Warning Protocol`. Agents must now treat tool warnings (e.g., "fuzzy match applied") as potential failures.
- **Requirement**: Mandatory verification step if a tool returns a warning. If verification fails, the agent must notify the user instead of proceeding silently.

## [Fri Jan 16 16:35:00 PST 2026] — Agent Model Optimization

### Multiple agents
- **Changed**: Updated model selection to align context window with agent role responsibilities.
    - **High Context (devstral-M4MAX)**: Analyst, Architect, Critic, Orchestrator, PI, Planner, Researcher, Retrospective, Roadmap, Security.
    - **Fast Execution (devstral-3090)**: DevOps, Implementer, Navigator, QA, UAT (Unchanged).

## [Thu Jan 16 14:51:00 PST 2026] — Agent Improvements Implementation

### orchestrator.agent.md
- **Added**: `project_context.md` verification step in Phase 1 Inception.
- **Added**: Strict file naming convention (`[ProjectName]-[ArtifactType].md`) in Artifact Management.

### architect.agent.md
- **Added**: `CONSTRAINT: LOCAL-ONLY` block forbidding SaaS, Cloud Infrastructure, Kubernetes, Docker, Microservices, Server-side Auth, Backend APIs, Remote Databases.
- **Added**: `REQUIRED` section for Client-side logic, Local Storage, Static Hosting, PWA features.
- **Added**: Instruction to read `project_context.md` (SSOT) before designing.
- **Added**: `Micro-Artifacts` instruction to break down files > 500 lines.

### implementer.agent.md
- **Added**: `CONSTRAINT: LOCAL-ONLY` block (same restrictions as Architect).
- **Added**: Instruction to read `project_context.md` in Core Responsibility #1.

### qa.agent.md
- **Added**: Instruction to read `project_context.md` before designing test strategy.
- **Added**: `Constraint Audit` responsibility to validate implementation against global constraints (e.g., "Local Only").

---

## [Thu Jan 16 15:05:00 PST 2026] — Logging Standards Refinement

### orchestrator.agent.md
- **Changed**: Logging initialization to use `.log` files (`cli_history.log`, `tool_usage_history.log`, `handoff_history.log`).
- **Removed**: `status.md` creation on initialization.
- **Changed**: Test log format to `[Timestamp] [Agent] [Tool] [Command]`.

### roadmap.agent.md
- **Changed**: Handoff logging reference from `agent-output/logs/[ID]-handoffs.md` to unified `agent-output/logs/handoff_history.log`.

---

## [Thu Jan 16 08:03:00 PST 2026] — Token Efficiency Optimization

### All Agents
- **Changed**: Generic Best Practices sections were commented out to reduce token consumption.
- **Changed**: Response Style sections were commented out.

---

## [Thu Jan 16 04:01:00 PST 2026] — Navigator/Researcher Role Correction

### navigator.agent.md
- **Changed**: Removed research handoffs that were incorrectly assigned; Navigator should focus on app exploration, not research.

### researcher.agent.md
- **Created/Restored**: Assigned all research tasks previously on Navigator.

---

## [Thu Jan 16 03:27:00 PST 2026] — Workflow/Handoff Unification (Phase 2)

### All Agents
- **Added**: Standardized handoff templates across all agents.
- **Changed**: Broken links in workflows fixed to create a closed-loop system.
- **Added**: Consolidated logging logic instructions.

---

## [Thu Jan 16 02:47:00 PST 2026] — Researcher Agent Restoration

### researcher.agent.md
- **Created**: Agent restored as vital for "zero to hero" workflow, responsible for subject matter research using `context7`, `fetch`, and other sources.
