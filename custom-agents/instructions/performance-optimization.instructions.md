---
description: 'General performance optimization guidelines'
applyTo: '**/*.cs, **/*.js, **/*.ts, **/*.tsx'
---

# Performance Optimization

## Core Performance Principles

- Measure before optimizing. Don't correct premature optimizations.
- Focus on the "Critical Rendering Path" for UI apps.
- Optimize hot paths in backend services.

## Critical Rules (Consistency)

- NEVER block the main thread (UI or Node.js event loop).
- NEVER fetch all columns (`SELECT *`) if only a few are needed.
- NEVER optimize without a benchmark or profile trace.
- NEVER ignore memory leaks; dispose resources.

## Frontend Optimization

- Implementation lazy loading for routes/heavy components.
- Optimize images (WebP/AVIF, proper sizing).
- Minimize bundle size (Tree shaking).

## Backend Optimization

- Use caching (Redis, In-Memory) for frequent reads.
- Optimize database queries (Indexing, N+1 problem).
- Use asynchronous I/O parallelization.

## Network Optimization

- Use compression (Gzip/Brotli).
- Minimize round trips.
- Use CDNs for static assets.
