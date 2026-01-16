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
- **File**: `agent-output/logs/handoff_history.log`
- **Usage**: You MUST log every handoff you perform to another agent.
- **Format**: Append a new line in the format: `[Timestamp] [SourceAgent] -> [TargetAgent]`
- **Action**: Use `run_command` to append specifically to the log:
  ```bash
  # Ensure the logs directory exists
  mkdir -p agent-output/logs
  # Append to the handoff log
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] Architect -> Critic" >> agent-output/logs/handoff_history.log
  ```

## Tool Usage Logging
- **File**: `agent-output/logs/tool_usage_history.log`
- **Goal**: Track significant modifications and executions to understand agent actions.
- **Scope**: Log ONLY "Side-Effect" tools.
- **Method**: Use `run_command` to append via shell.
- **Command**:
  ```bash
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [Agent] [Tool]" >> agent-output/logs/tool_usage_history.log
  ```
- **Example**:
  ```bash
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] Architect write_to_file" >> agent-output/logs/tool_usage_history.log
  ```

## CLI Command Logging
- **File**: `agent-output/logs/cli_history.log`
- **Goal**: Maintain a detailed, linear history of all terminal commands executed for debugging and auditing.
- **Requirement**: Whenever you use the `run_command` tool, you MUST also log the command to this file.
- **Exclusions**: Do NOT log commands that write to collaboration tracking logs (`handoff_history.log`, `tool_usage_history.log`, `cli_history.log`) to avoid circular/redundant logging.
- **Format**: `[Timestamp] [Agent] [Tool] [Command]`
- **Command**:
  ```bash
  # Example: Logging a git commit
  echo "[$(date '+%a %b %d %H:%M:%S %Z %Y')] [DevOps] [run_command] [git commit -m 'feat: init']" >> agent-output/logs/cli_history.log
  ```
- **Note**: This mimics a persistent `.bash_history` but attributed to specific agents and timestamps, excluding the logging commands themselves.
