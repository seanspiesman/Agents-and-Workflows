---
description: 'Rule to enforce documentation updates alongside code changes'
applyTo: '*'
---

# Update Docs on Code Change

## Core Mandate

- Code and Documentation must remain in sync.
- "Definition of Done" includes updated docs.

## What to Update

- **READMEs**: If setup or run instructions change.
- **API Docs**: If endpoints or signatures change.
- **Architecture Diagrams**: If system design changes.
- **Comments**: If the logic explained changes.

## Critical Rules (Consistency)

- NEVER change a public API without updating the reference.
- NEVER specific behavior changes in commit messages only; put it in the docs.
- NEVER assume "someone else will document it".

## Process

1. Make Code Change.
2. Identify affected documentation.
3. Update documentation in the same PR/Commit.
