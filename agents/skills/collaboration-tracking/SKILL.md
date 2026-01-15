---
name: collaboration-tracking
description: Instructions for checking global CLI context and logging handoffs.
---

# Collaboration Tracking

This skill ensures that all agents share a common CLI context and log their handoffs to maintain a clear chain of custody.

## Global Context (CLI)
- **File**: `agent-output/cli.md`
- **Usage**: Always check this file for shared command-line instructions or context that persists across agent sessions.
- **Action**: If you have relevant CLI output or instructions that other agents might need, append them to this file.

## Handoff Logging
- **File**: `agent-output/logs/[ID]-handoffs.md` (where [ID] is the content of `agent-output/.next-id`)
- **Usage**: You MUST log every handoff you perform to another agent.
- **Format**: Append a new line in the format: `[SourceAgent] -> [TargetAgent] (Timestamp)`
- **Action**: Use `run_command` to append specifically to the current task's log:
  ```bash
  # Ensure the logs directory exists
  mkdir -p agent-output/logs
  # Append to the current ID's handoff log
  echo "Architect -> Critic (2024-03-20T14:30:00Z)" >> agent-output/logs/$(cat agent-output/.next-id 2>/dev/null || echo "GLOBAL" | tr -d '[:space:]')-handoffs.md
  ```

## Tool Usage Logging
- **File**: `agent-output/logs/[ID]-tool_usage.log` (where [ID] is the content of `agent-output/.next-id`)
- **Goal**: Track significant modifications and executions to understand agent actions.
- **Scope**: Log ONLY "Side-Effect" tools: `run_command`, `write_to_file`, `replace_file_content`, `multi_replace_file_content`. DO NOT log read-only actions (view/list/read).
- **Method**: Use `run_command` to append via shell.
- **Command**:
  ```bash
  echo "[Timestamp] [Agent] [Tool] [Target]" >> agent-output/logs/$(cat agent-output/.next-id 2>/dev/null || echo "GLOBAL" | tr -d '[:space:]')-tool_usage.log
  ```
- **Batching**: To preserve step count, you MAY batch multiple log entries into a single `echo` command at the end of a turn or combined with other shell commands.
- **Example**:
  ```bash
  echo "$(date -u) Architect write_to_file agents/new.agent.md" >> agent-output/logs/$(cat agent-output/.next-id 2>/dev/null || echo "GLOBAL" | tr -d '[:space:]')-tool_usage.log
  ```

## CLI Command Logging
- **File**: `agent-output/logs/cli_history.log`
- **Goal**: Maintain a detailed, linear history of all terminal commands executed for debugging and auditing.
- **Requirement**: Whenever you use the `run_command` tool, you MUST also log the command to this file.
- **Format**: `[Timestamp] [Agent] [command]`
- **Command**:
  ```bash
  # Example: Logging a git commit
  echo "[$(date -u)] [DevOps] [git commit -m 'feat: init']" >> agent-output/logs/cli_history.log
  ```
- **Note**: This mimics a persistent `.bash_history` but attributed to specific agents and timestamps.
