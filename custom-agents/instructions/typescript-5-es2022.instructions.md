---
description: 'Guidelines for TypeScript Development targeting TypeScript 5.x and ES2022 output'
applyTo: '**/*.ts'
---

# TypeScript Development

## TypeScript Code Style and Structure

- Target TypeScript 5.x / ES2022 and prefer native features over polyfills.
- Use pure ES modules; never emit `require`, `module.exports`, or CommonJS helpers.
- Accept the existing architecture and coding standards; prefer readable, explicit solutions.
- Prioritize maintainability and clarity, short methods and classes, clean code.

## Naming Conventions

- Use PascalCase for classes, interfaces, enums, and type aliases.
- Use camelCase for variables, functions, and methods.
- Use kebab-case for filenames (e.g., `user-session.ts`).
- Name things for their behavior or domain meaning, not implementation.

## TypeScript Specific Guidelines

- Use discriminated unions for realtime events and state machines.
- Express intent with TypeScript utility types (e.g., `Readonly`, `Partial`, `Record`).
- Avoid `any` (implicit or explicit); prefer `unknown` plus narrowing.
- Centralize shared contracts instead of duplicating shapes.

## Critical Rules (Consistency)

- NEVER use `any`. Use `unknown` and type narrowing.
- NEVER use `var`. Use `const` or `let`.
- NEVER use `I` prefix for interfaces (unless project convention strictly dictates otherwise, but generally avoid).
- NEVER use `module.exports` or `require` in new code. Use `export` and `import`.
- NEVER ignore linter errors; fix them.
- NEVER check in `console.log` statements.

## Project Organization

- Follow the repository's folder and responsibility layout for new code.
- Keep tests, types, and helpers near their implementation.
- Reuse or extend shared utilities before adding new ones.

## Formatting

- Run the repository's lint/format scripts (e.g., `npm run lint`) before submitting.
- Match the project's indentation, quote style, and trailing comma rules.
- Favor immutable data and pure functions when practical.

## Async, Events & Error Handling

- Use `async/await`; wrap awaits in try/catch with structured errors.
- Guard edge cases early to avoid deep nesting.
- Surface user-facing errors via the repository's notification pattern.

## External Integrations

- Instantiate clients outside hot paths and inject them for testability.
- Never hardcode secrets; load them from secure sources.
- Apply retries, backoff, and cancellation to network or IO calls.

## Security Practices

- Validate and sanitize external input with schema validators or type guards.
- Encode untrusted content before rendering HTML.
- Use parameterized queries or prepared statements to block injection.
- Favor immutable flows and defensive copies for sensitive data.

## Testing Expectations

- Add or update unit tests with the project's framework and naming style.
- Avoid brittle timing assertions; prefer fake timers or injected clocks.
- Run targeted test scripts for quick feedback before submitting.
