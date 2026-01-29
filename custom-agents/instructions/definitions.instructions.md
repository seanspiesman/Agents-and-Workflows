---
description: 'Project-wide definitions and terminology'
applyTo: '*'
---

# Project Definitions and Terminology

## Core Terminology

- **Agent**: An AI entity with a specific role.
- **Workflow**: A defined sequence of steps to achieve a task.
- **Instruction**: A set of rules effectively programming the agent's behavior.
- **Artifact**: A file created by an agent (e.g., task.md, implementation_plan.md).

## Naming Conventions

- Agents: Kebab-case filenames (e.g., `qa.agent.md`).
- Instructions: `*.instructions.md`.
- Workflows: `*.workflow.md`.

## Critical Rules (Consistency)

- NEVER invent new terms for existing concepts.
- NEVER conflict with industry-standard definitions unless explicitly documented.
- NEVER circular references in definitions.

## Project Structure Definitions

- `custom-agents/`: Contains all agent logic and config.
- `agent-output/`: Directory for runtime artifacts and logs.
- `.agent/workflows/`: User-accessible workflows.
