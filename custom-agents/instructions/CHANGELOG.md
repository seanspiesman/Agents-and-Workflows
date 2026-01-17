# Changelog: instructions/

All notable changes to global and specific instructions in this directory.

---

## [Fri Jan 16 16:42:00 PST 2026] — Enforce Agent Identity in Logs

### global.instructions.md
- **Changed**: Updated logging commands (`handoff`, `cli`, `tool_usage`) to use `[YourAgentName]` placeholder.
- **Changed**: Added explicit instructions to substitute placeholders with actual agent names.

## [Fri Jan 16 16:35:00 PST 2026] — Enforce Handoff Logging

### global.instructions.md, skills/collaboration-tracking/SKILL.md
- **Changed**: Updated instructions to make `handoff_history.log` logging a **BLOCKING** pre-condition. Agents are explicitly forbidden from handing off until they have executed the log command.

## [Fri Jan 16 16:11:00 PST 2026] — Refined Instruction Loading Scope

### Multiple instruction files
- **Changed**: Refined `applyTo` patterns to reduce context bloat.
    - **Tests**: Restrict Playwright instructions to `*.spec.ts` and `*Test.cs`.
    - **Code**: Restrict "Code Commenting" and "Code Review" to specific code extensions.
    - **Architecture/Performance**: Limit global loading to code files AND `agent-output/**/*.md`.
    - **Stack-Specific**: Narrowed `**/*.md` to `agent-output/**/*.md` to focus on planning artifacts while ignoring generic documentation.

## [Fri Jan 16 16:06:50 PST 2026] — Global Instructions Loading Fix

### global.instructions.md
- **Changed**: Added `applyTo: '*'` to frontmatter. This forces the global instructions to load in all contexts, ensuring that critical protocols (logging, handoffs) are always available.

## [Fri Jan 16 16:00:21 PST 2026] — Enabled Instructions in Markdown Files

### nextjs.instructions.md, reactjs.instructions.md, dotnet-maui.instructions.md, csharp.instructions.md, html-css-style-color-guide.instructions.md
- **Changed**: Updated `applyTo` pattern to include `**/*.md`. This ensures technical stack instructions are available to agents during Planning/Architecture phases where they work primarily in Markdown.

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
