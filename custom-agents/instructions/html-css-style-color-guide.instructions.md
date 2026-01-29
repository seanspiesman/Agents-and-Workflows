---
description: 'Core web styling and structural guidelines'
applyTo: '**/*.html, **/*.css, **/*.scss'
---

# HTML & CSS Style Guide

## Structure and Semantics

- Use semantic HTML tags (`<nav>`, `<main>`, `<article>`, `<footer>`) instead of generic `<div>`.
- Ensure proper heading hierarchy (h1 -> h2 -> h3).
- Use `button` for actions and `a` for navigation.

## CSS Architecture

- Use a consistent naming convention (BEM is recommended).
- Prefer classes over ID selectors for styling.
- Use CSS Variables (`--custom-prop`) for theming and repeated values.

## Naming Conventions

- Use kebab-case for CSS class names (e.g., `.main-navigation`).
- Use descriptive names that reflect purpose, not appearance (e.g., `.alert-error` not `.red-box`).

## Critical Rules (Consistency)

- NEVER use inline styles (`style="..."`) unless for dynamic coordinate values.
- NEVER use `!important` unless overriding 3rd party libraries absolutely requires it.
- NEVER use generic tag selectors (e.g., `div { ... }`) in global scope.
- NEVER skip `alt` attributes on images.
- NEVER use fixed units (`px`) for font sizes; use `rem` or `em`.

## Responsive Design

- Design Mobile-First: Write base styles for mobile, use `@media (min-width)` for larger screens.
- Use Flexbox and Grid for layouts. Avoid floats.
- Ensure touch targets are at least 44x44px.

## Accessibility (A11y)

- Ensure sufficient color contrast (WCAG AA).
- Handle `:focus` states visibly.
- Use ARIA attributes only when semantic HTML is insufficient.
- Hide content accessible to screen readers using `.visually-hidden` class if needed.

## Performance

- Minify CSS in production.
- Avoid deeply nested selectors (> 3 levels).
- precise usage of animations; prefer `transform` and `opacity` changes.
