# Changelog: instructions/

All notable changes to global and specific instructions in this directory.

---

## [Thu Jan 16 15:05:00 PST 2026] — Logging Standards Refinement

### global.instructions.md
- **Changed**: Handoff log file from `handoff_history.md` to `handoff_history.log`.
- **Changed**: Handoff format to `[Timestamp] SourceAgent -> TargetAgent`.
- **Changed**: CLI history log file from `cli_history.md` to `cli_history.log`.
- **Changed**: CLI history format to `[Timestamp] [Agent] [Tool] [Command]`.
- **Changed**: Tool usage log file from `tool_usage_history.md` to `tool_usage_history.log`.
- **Changed**: Tool usage format to `[Timestamp] [Agent] [Tool]`.

## [Thu Jan 16 15:18:00 PST 2026] — Timestamp Format Update

### global.instructions.md
- **Changed**: All `$(date)` commands updated to `$(date '+%a %b %d %H:%M:%S %Z %Y')` for format `[Fri Jan 16 14:51:14 PST 2026]`.

---

## [Wed Jan 15 22:47:00 PST 2026] — Global Instructions Creation

### global.instructions.md
- **Created**: New global instruction file with emphasis on task adherence and collaboration skill usage.
- **Added**: Core Mandate: "FINISH WHAT YOU START" section.
- **Added**: Collaboration Contract (Mandatory logging of handoffs, CLI, tool usage).
- **Added**: Memory Contract.
- **Added**: Document Lifecycle rules.
- **Added**: TDD Gate Procedure.
- **Added**: Workflow Execution Rules (including `// turbo` annotations).
- **Added**: Fresh Context Protocol (Anti-Amnesia) for truncated chat scenarios.
- **Added**: Data-Only Output Protocol for token optimization.

### task-adherence.instructions.md
- **Created**: Instructions for strong adherence to tasks and use of `collaboration-tracking` skill.
