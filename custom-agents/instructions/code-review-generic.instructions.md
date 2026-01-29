---
description: 'Generic code review operational guidelines'
applyTo: 'agent-output/**/*.md'
---

# Code Review Guidelines

## Core Review Philosophy

- Reviewers act as quality gates, not just spell checkers.
- Critique architecture, security, and maintainability first; syntax errors second.
- Suggest improvements with high confidence.

## Tone and Style

- Be constructive and polite.
- Focus on the code, not the coder.
- Use "We" instead of "You" (e.g., "We should handle this exception").

## Critical Rules (Consistency)

- NEVER approve code with known security vulnerabilities.
- NEVER approve code that breaks the build or tests.
- NEVER approve PRs with commented-out code (unless explained).
- NEVER approve giant PRs without requesting a breakdown (if possible).
- NEVER assume; ask questions if intent is unclear.

## Review Checklist

- [ ] Does it meet requirements?
- [ ] Is it readable and maintainable?
- [ ] Are variable/function names descriptive?
- [ ] Are tests included and passing?
- [ ] Are edge cases handled?
- [ ] Is documentation updated?

## Feedback Format

- Use [Suggestion] for improvements.
- Use [Question] for clarifications.
- Use [Blocker] for issues that must be fixed before merge.
