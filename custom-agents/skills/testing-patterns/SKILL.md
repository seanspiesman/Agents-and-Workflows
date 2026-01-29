---
name: Testing Patterns
description: Guidelines for interactive and black-box testing.
---

# Testing Patterns

## 1. Interactive Testing (MANDATORY)
All verification MUST be done by interacting with the running application.
- **Tools**: Playwright, Puppeteer, iOS Simulator.
- **Process**: Launch app -> Perform user actions -> Verify UI state.

## 2. Unit Testing (PROHIBITED)
- Do NOT write `.spec.ts`, `.test.ts`, or use `jest`/`mocha`.
- Agents must rely on side-effects observable in the UI.

## 3. Automation
- Use `playwright` MCP to script user journeys.
- Verify "Happy Path" and "Error States" via the UI.
