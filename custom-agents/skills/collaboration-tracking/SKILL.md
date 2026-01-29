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

## Legacy Logging (Deprecated)
 
Logging to `agent-output/logs/` is no longer required as RAG captures context.

