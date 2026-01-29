---
description: 'Operational guide for agents implementing user tasks'
applyTo: 'agent-output/*.md'
---

# Task Implementation Guide

## Task Execution Flow

1. **Understand**: Read the request and context deeply.
2. **Plan**: Create `implementation_plan.md` (mandatory for complex tasks).
3. **Execute**: Follow the plan step-by-step.
4. **Verify**: Test changes.

## Artifact Management

- Maintain the task list using the `todo` tool relative to the current objective.
- Update status frequently.

## Critical Rules (Consistency)

- NEVER start coding without a plan for complex features.
- NEVER ignore existing file patterns.
- NEVER leave the system in a broken state.
- NEVER mark a task complete if verification failed.

## Status Updates

- Use `task_boundary` tool updates to inform the user of HIGH-LEVEL progress.
- Do not spam updates for every single file edit.
