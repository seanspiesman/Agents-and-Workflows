# Global Agent Instructions

> [!IMPORTANT]
> These instructions apply to ALL agents in the Zero to Hero workflow. Load this file at the start of every session.

## 1. Collaboration Contract

**Key behaviors:**
- **Context Awareness**: Check `agent-output/cli.md` for global context before acting.
- **Handoff Logging**: Log ALL handoffs to `agent-output/logs/[ID]-handoffs.md`.
- **CLI History**: Log ALL CLI commands to `agent-output/logs/cli_history.log` (Format: `[Timestamp] [Agent] [Command]`).
- **Tool Usage**: Log ALL side-effect tool usage to `agent-output/logs/[ID]-tool_usage.log`.

## 2. Memory Contract

**Key behaviors:**
- **Retrieval**: Retrieve context at decision points (2–5 times per task) using semantic search (e.g., `@codebase`).
- **Storage**: Store critical info at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`.
- **Failure Mode**: If memory tools fail, announce "No-Memory Mode" immediately.

## 3. Document Lifecycle

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

## 4. TDD Gate Procedure (Mandatory for Code Changes)

**Execute for EACH new function or class:**
1. **STOP**: Do NOT write implementation code yet.
2. **WRITE**: Create test file with failing test.
3. **RUN**: Execute test and verify it fails with the RIGHT reason (ModuleNotFoundError, undefined, AssertionError).
4. **REPORT**: State "TDD Gate: Test `test_X` fails as expected: [error]. Proceeding."
5. **IMPLEMENT**: Write ONLY the minimal code to make the test pass.
6. **VERIFY**: Run test again, confirm it passes.

## 5. Logging Standards

- **Directory**: Always use `agent-output/logs/`.
- **CLI Logs**: Use `agent-output/logs/cli-[AgentName].log` if possible, or append to `cli_history.log` with atomic writes.
- **Tool Logs**: `agent-output/logs/[ID]-tool_usage.log`.
