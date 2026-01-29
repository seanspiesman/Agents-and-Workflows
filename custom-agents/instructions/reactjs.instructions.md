---
description: 'ReactJS development standards and best practices'
applyTo: '**/*.jsx, **/*.tsx, **/*.js, **/*.ts, **/*.css, **/*.scss, agent-output/**/*.md'
---

# ReactJS Development

## ReactJS Code Style and Structure

- Use functional components with hooks as the primary pattern.
- Follow React's official style guide and best practices (React 19+).
- Implement component composition over inheritance.
- Keep components small and focused on a single concern.
- Use TypeScript for type safety whenever possible.

## Naming Conventions

- Follow PascalCase for component names (e.g., `UserProfile`).
- Use camelCase for functions, hooks, and variables (e.g., `useAuth`, `handleSubmit`).
- Use PascalCase for TypeScript interfaces and types.

## React Specific Guidelines

- Use custom hooks for reusable stateful logic.
- Use `useEffect` with proper dependency arrays to avoid infinite loops and stale closures.
- Use `useMemo` and `useCallback` judiciously for performance optimization.
- Implement cleanup functions in effects to prevent memory leaks.
- Use `useRef` for accessing DOM elements and storing mutable values without re-renders.

## Critical Rules (Consistency)

- NEVER mutate state directly. Always use setters or reducers.
- NEVER use class components (unless strictly required by legacy dependencies).
- NEVER call hooks conditionally or within loops/nested functions.
- NEVER use index as a key in lists if the order can change. Use unique IDs.
- NEVER prop-drill more than 2-3 levels. Use Context or Composition.
- NEVER put side effects directly in the render body. Use `useEffect` or event handlers.
- NEVER leave `console.log` in production code.

## State Management

- Use `useState` for local component state.
- Leverage `useContext` for sharing state across component trees.
- Consider external state management (Redux Toolkit, Zustand) for complex applications.
- Use React Query or SWR for server state management.

## Component Design

- Separate presentational and container components clearly.
- Use composition patterns (render props, children as functions).
- Implement proper prop validation with TypeScript or PropTypes.

## Styling

- Use CSS Modules, Styled Components, or modern CSS-in-JS solutions as per project setup.
- Implement responsive design with mobile-first approach.
- Ensure accessibility with proper ARIA attributes and semantic HTML.

## Performance Optimization

- Use `React.memo` for component memoization when appropriate.
- Implement code splitting with `React.lazy` and `Suspense`.
- Optimize bundle size with tree shaking.
- Implement virtual scrolling for large lists.

## Data Fetching

- Use modern data fetching libraries (React Query, SWR, Apollo Client).
- Implement proper loading, error, and success states.
- Handle race conditions, request cancellation, and caching strategies.

## Error Handling

- Implement Error Boundaries for component-level error handling.
- Handle async errors in effects and event handlers.
- Provide meaningful error messages to users.

## Testing

- Write unit tests using React Testing Library.
- Test component behavior, not implementation details.
- Mock external dependencies and API calls appropriately.
- Test accessibility features and keyboard navigation.

## Security

- Sanitize user inputs to prevent XSS attacks.
- Use HTTPS for all external API calls.
- Avoid storing sensitive data in localStorage or sessionStorage.
