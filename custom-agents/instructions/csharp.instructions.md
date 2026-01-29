---
description: 'Guidelines for building C# applications'
applyTo: '**/*.cs, agent-output/**/*.md'
---

# C# Development

## C# Code Style and Structure

- Always use the latest version C#, currently C# 14 features.
- Write clear and concise comments for each function.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- For libraries or external dependencies, mention their usage and purpose in comments.

## Naming Conventions

- Follow PascalCase for component names, method names, and public members.
- Use camelCase for private fields and local variables.
- Prefix interface names with "I" (e.g., IUserService).
- Use `nameof` instead of string literals when referring to member names.

## Critical Rules (Consistency)

- NEVER use `== null` or `!= null`. Use `is null` or `is not null`.
- NEVER ignore the type system; don't add null checks if the type is non-nullable.
- NEVER emit "Act", "Arrange" or "Assert" comments in tests.
- NEVER hardcode secrets in code; use `SecureStorage` or environment variables.
- NEVER use implicit `any` via `object` unless strictly necessary; prefer strong types.

## Formatting

- Apply code-formatting style defined in `.editorconfig`.
- Prefer file-scoped namespace declarations and single-line using directives.
- Insert a newline before the opening curly brace of any code block.
- Ensure that the final return statement of a method is on its own line.
- Use pattern matching and switch expressions wherever possible.
- Ensure that XML doc comments are created for any public APIs.

## Project Setup and Structure

- Organize code using feature folders or domain-driven design principles.
- Show proper separation of concerns with models, services, and data access layers.
- Explain the Program.cs and configuration system in ASP.NET Core 10 including environment-specific settings.

## Nullable Reference Types

- Declare variables non-nullable, and check for `null` at entry points.
- Always use `is null` or `is not null` instead of `== null` or `!= null`.
- Trust the C# null annotations.

## Data Access Patterns

- Implement data access layers using Entity Framework Core.
- Use efficient query patterns to avoid common performance issues.
- Implement database migrations and data seeding.

## Authentication and Authorization

- Implement authentication using JWT Bearer tokens or OAuth 2.0.
- Secure both controller-based and Minimal APIs consistently.
- Implement role-based and policy-based authorization.

## Validation and Error Handling

- Implement model validation using data annotations and FluentValidation.
- Use a global exception handling strategy using middleware.
- Use problem details (RFC 7807) for standardized error responses.

## API Versioning and Documentation

- Implement API versioning strategies (controller-based or Minimal APIs).
- specific Swagger/OpenAPI implementation with proper documentation.

## Logging and Monitoring

- Implement structured logging using Serilog or other providers.
- Integrate with Application Insights for telemetry collection.

## Testing

- Always include test cases for critical paths.
- Copy existing style in nearby files for test method names and capitalization.
- Mock dependencies using Moq or NSubstitute.

## Performance Optimization

- Implement caching strategies (in-memory, distributed).
- Use asynchronous programming patterns.
- Implement pagination, filtering, and sorting for large data sets.

## Deployment and DevOps

- Containerize APIs using .NET's built-in container support.
- Implement health checks and readiness probes.
