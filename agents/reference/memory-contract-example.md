# Project Memory Contract - Concrete Example

This document provides a concrete example of how to add Project Memory to your custom agents. All of the agents in this repo already use this feature.

## How to use this

1. Scroll to the "Copy this into your agent file" block below.
2. Copy into your `*.agent.md` file in VS Code.

---

## Copy this into your agent file

````markdown
# Memory Contract

**MANDATORY**: Load `memory-contract` skill at session start. Memory is core to your reasoning.

**Key behaviors:**
- Retrieve at decision points (2–5 times per task) using semantic search (e.g., `@codebase`)
- Store at value boundaries (decisions, findings, constraints) by creating files in `agent-output/memory/`
- If tools fail, announce no-memory mode immediately

**Quick reference:**
- Retrieve: Search `agent-output/memory/` for keywords.
- Store: Create `YYYY-MM-DD-topic.md` in `agent-output/memory/`.

Full contract details: `memory-contract` skill
````
