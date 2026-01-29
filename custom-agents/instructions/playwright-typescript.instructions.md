---
description: 'Playwright for TypeScript testing guidelines'
applyTo: '**/*.spec.ts, **/*.test.ts'
---

# Playwright TypeScript Testing

## Playwright TS Code Style and Structure

- Write idiomatic TypeScript test code using `@playwright/test`.
- Use the `Page` object model pattern for maintainability.
- Keep tests independent and deterministic.
- Use `await expect(...)` for assertions to leverage auto-retrying.

## Naming Conventions

- File names should end in `.spec.ts`.
- Describe blocks should represent the feature/component.
- Test names should read like sentences ("should login successfully").

## Playwright Specific Guidelines

- Use `Locator` objects strictly; avoid `ElementHandle`.
- Use user-facing locators (`getByRole`, `getByText`) over CSS/XPath selectors.
- Leverge `playwright.config.ts` for global configuration.
- Use Fixtures for test setup and sharing state/context.

## Critical Rules (Consistency)

- NEVER use `page.waitForTimeout` or hard waits. Use web assertions.
- NEVER share mutable state between tests without isolating via `test.beforeEach`.
- NEVER use internal selectors (`>>`) if a semantic locator exists.
- NEVER ignore existing fixtures; extend them if needed.
- NEVER commit screenshots (snapshots) for visual regression without verifying they match the CI environment (platform differences).

## Page Object Model

- Encapsulate page-specific logic and locators.
- Use `readonly` properties for locators in the constructor.
- Return `this` or other Page Objects from actions for chaining.

## Debugging and Reporting

- Use strict mode to catch multiple elements matching a locator.
- Enable tracing on 'retain-on-failure' in config.
- Use `console.log` sparingly; prefer Playwright's reporter API.

## Parallel Execution

- Tests run in parallel by default; ensure isolation.
- Use `test.describe.configure({ mode: 'parallel' })` explicitly if needed.
- Avoid colliding on shared backend resources; use unique IDs for generated data.
