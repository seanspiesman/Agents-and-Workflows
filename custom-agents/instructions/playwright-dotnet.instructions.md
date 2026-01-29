---
description: 'Playwright for .NET testing guidelines'
applyTo: '**/*.cs, **/*.test.cs'
---

# Playwright .NET Testing

## Playwright .NET Code Style and Structure

- Write idiomatic C# test code using NUnit or MSTest helpers provided by Playwright.
- Use the `Page` object model pattern for maintainability.
- Keep tests independent and deterministic.
- Use `await Expect(...)` for assertions to leverage auto-retrying.

## Naming Conventions

- Suffix test classes with `Tests`.
- Suffix test methods with `_Should[ExpectedResult]_When[Condition]`.
- Use PascalCase for Page Object Models (e.g., `LoginPage`).

## Playwright Specific Guidelines

- Use `ILocator` strictly; avoid `ElementHandle`.
- Use user-facing locators (`GetByRole`, `GetByText`) over CSS/XPath selectors.
- Use `appsettings.json` or `.runsettings` for test configuration (base URLs, browser options).
- Use `IBrowserContext` for distinct user sessions in parallel tests.

## Critical Rules (Consistency)

- NEVER use `Thread.Sleep`. Use `Page.WaitFor...` or `Expect` with timeout.
- NEVER rely on hardcoded timeouts if possible; use web assertions.
- NEVER share state between tests (variables or static members).
- NEVER use absolute paths for file uploads; use relative paths.
- NEVER check in sensitive data (passwords); use environment variables.

## Page Object Model

- Encapsulate page-specific logic and locators in dedicated classes.
- Do not expose Playwright internals (e.g., `IPage`) from Page Objects if possible; expose actions.
- Return Page Objects from navigation methods to enable fluent chaining.

## Debugging and Reporting

- Use Tracing (`RetainOnFailure`) to debug CI failures.
- Attach screenshots and videos to test reports on failure.
- Use `TestContext.WriteLine` for logging within tests.

## Parallel Execution

- Ensure tests are thread-safe.
- Configure parallel execution in `runsettings` or NUnit attributes.
- Manage resources (like database records) to avoid collision during parallel runs.
