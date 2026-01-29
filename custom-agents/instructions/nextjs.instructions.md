---
description: 'Next.js development standards (App Router)'
applyTo: '**/*.tsx, **/*.ts, **/*.js, **/*.jsx'
---

# Next.js Development

## Next.js Code Style and Structure

- Use the App Router (`app/` directory) for all new projects.
- Prefer Server Components (RSC) by default; add `"use client"` only when interactivity is needed.
- Use `next/image` for image optimization.
- Use `next/font` for font loading.

## Naming Conventions

- Route folders define URL structure (e.g., `app/dashboard/page.tsx`).
- Use kebab-case for URL segments.
- Use PascalCase for component names.

## Next.js Specific Guidelines

- Use `layout.tsx` for shared UI across routes.
- Use `loading.tsx` for suspense boundaries.
- Use `error.tsx` for handling errors in route segments.
- Use `route.ts` for Route Handlers (API endpoints).

## Critical Rules (Consistency)

- NEVER access `window` or `document` in Server Components.
- NEVER start a component name with specific implementations (e.g., `RedButton`), describe intent (`SubmitButton`).
- NEVER ignore `eslint-config-next` warnings.
- NEVER import heavy client libraries in Server Components if not needed.
- NEVER export a component as `default` and named export simultaneously from the same file (pattern consistency).

## Data Fetching

- Fetch data directly in Server Components using `async/await`.
- Use `generateStaticParams` for static site generation (SSG) of dynamic routes.
- Use `fetch` with `cache` options for caching and revalidation control.

## State Management

- Keep client state local to the leaf components that need it.
- Use URL search params for state that should be shareable (filters, pagination).

## Optimization

- Use `Link` component for client-side navigation.
- Implement Metadata API for SEO (`generateMetadata`).
- Configure `next.config.js` for image domains and optimizations.

## Styling

- Use Tailwind CSS or CSS Modules as preferred by the project.
- Keep global styles minimal in `globals.css`.
