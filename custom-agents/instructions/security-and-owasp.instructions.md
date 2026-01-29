---
description: 'Security best practices and OWASP Top 10 mitigation'
applyTo: '*'
---

# Security & OWASP Guidelines

## Core Security Principles

- Least Privilege: Grant only necessary permissions.
- Defense in Depth: Layered security controls.
- Secure by Design: Integrate security from the start.

## Critical Rules (Consistency)

- NEVER commit secrets (API keys, passwords) to Git.
- NEVER trust user input. Validate and sanitize EVERYTHING.
- NEVER implement your own crypto. Use standard libraries (e.g., bcrypt, Argon2).
- NEVER expose stack traces to end users in production.
- NEVER disable security features (CORS, CSRF) for "convenience".

## Common Vulnerability Mitigation

- **Injection**: Use parameterized queries (SQL) and ORMs.
- **XSS**: Escape output context-appropriately; use CSP.
- **Auth Flaws**: Use established identity providers; enforce MFA.
- **Insecure Design**: Threat model critical features.
- **Misconfiguration**: Automate and audit infrastructure config.

## Data Protection

- Encrypt sensitive data at rest and in transit (TLS).
- redact PII in logs.
- Implement strict access controls.
