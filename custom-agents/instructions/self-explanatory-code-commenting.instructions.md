---
description: 'Guidelines for writing self-documenting code and comments'
applyTo: '**/*.cs, **/*.ts, **/*.js'
---

# Self-Explanatory Code & Commenting

## Core Philosophy

- Code should tell the "How" and "What".
- Comments should tell the "Why".
- The best comment is a good variable/function name.

## Naming as Documentation

- Use intention-revealing names (`daysSinceModification` vs `dsm`).
- Avoid mapping loops with single-letter variables (`i`, `j`) in complex logic; use meaningful names (`row`, `col`).

## Critical Rules (Consistency)

- NEVER comment out old code; delete it. Git remembers.
- NEVER write comments that just repeat the code (e.g., `i++ // increment i`).
- NEVER leave TODOs without a ticket link or owner.
- NEVER lie in comments; update them when code changes.

## When to Comment

- **Business Logic**: Explain complex business rules.
- **Workarounds**: Explain why a hack was necessary (link to issue).
- **Public APIs**: Document inputs, outputs, and exceptions (JSDoc/XML Docs).
- **RegEx**: Explain what the pattern matches.

## Comment Style

- Use complete sentences for block comments.
- Keep inline comments short and on the same line if possible.
