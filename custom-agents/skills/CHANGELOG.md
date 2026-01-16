# Changelog: skills/

All notable changes to skills in this directory.

---

## [Thu Jan 16 15:05:00 PST 2026] — Logging Standards Refinement

### collaboration-tracking/SKILL.md
- **Changed**: Handoff log file from `[ID]-handoffs.md` to unified `handoff_history.log`.
- **Changed**: Handoff format to `[Timestamp] [SourceAgent] -> [TargetAgent]`.
- **Changed**: Tool usage log file from `[ID]-tool_usage.log` to `tool_usage_history.log`.
- **Changed**: Tool usage format to `[Timestamp] [Agent] [Tool]`.
- **Changed**: CLI history format to `[Timestamp] [Agent] [Tool] [Command]`.
- **Changed**: Exclusions list updated to reference new `.log` filenames.

## [Thu Jan 16 15:18:00 PST 2026] — Timestamp Format Update

### collaboration-tracking/SKILL.md
- **Changed**: All `$(date)` commands updated to `$(date '+%a %b %d %H:%M:%S %Z %Y')` for format `[Fri Jan 16 14:51:14 PST 2026]`.

---

## [Wed Jan 15 23:29:00 PST 2026] — Non-Blocking Execution Enhancement

### non-blocking-execution/SKILL.md
- **Changed**: Updated to clearly explain use of `WaitMsBeforeAsync` to detach long-running processes.
- **Added**: Instructions for using `send_command_input` with `Terminate: true` to stop background processes.
- **Added**: Polling loop guidance for monitoring background tasks.

---

## [Wed Jan 15 23:19:00 PST 2026] — Copilot Resources Integration

### Various Skills (from awesome-copilot-main)
- **Added**: React, .NET Maui, and general engineering best practices skills integrated.
- **Added**: New `collections/` directory created with linked resources.
