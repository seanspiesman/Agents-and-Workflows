---
description: 'Markdown formatting and usage guidelines'
applyTo: '**/*.md'
---

# Markdown Style Guide

## Markdown Editing and Structure

- Use standard Markdown (CommonMark/GFM).
- Use H1 (`#`) for the document title (one per file).
- Use H2 (`##`) for major sections.
- Use backticks for code literals (e.g., `variableName`).

## Naming and Links

- Use descriptive link text: `[Implementation Plan](./impl.md)` not `[here](./impl.md)`.
- Use relative paths for internal links.

## Critical Rules (Consistency)

- NEVER use H1 for anything other than top-level title.
- NEVER break lists with unindented newlines (breaks rendering).
- NEVER use raw HTML unless Markdown doesn't support the feature (and even then, sparingly).
- NEVER leave trailing whitespace on lines.

## Special Features

- Use Alerts (GitHub style) for important notes:
  > [!NOTE]
  > This is a note.
- Use Mermaid diagrams for flows and charts.
- Use tables for structured data comparison.
