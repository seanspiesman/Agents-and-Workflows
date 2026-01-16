# Handoff Template

When defining an agent in `custom-agents/agents/*.agent.md`, the `handoffs` block in the YAML frontmatter MUST following this schema.

## Schema

```yaml
handoffs:
  - label: [Action Verb] [Goal]
    agent: [Target Agent Name]
    prompt: [Context of what is done]. [Request for what needs to be done].
    send: true
```

## Rules

1.  **Label**: 3-5 words, clear Action Verb (e.g., "Request Analysis", "Submit for Critique").
2.  **Prompt**:
    - **Context**: State what triggered the handoff (e.g., "Plan approved", "Bug found").
    - **Request**: State clear instruction for the next agent.
    - **NO Greetings**: Do not start with "Hi" or "Hello".
3.  **Send**: Always `true` for automated workflows.

## Standard Handoffs (Zero to Hero)

### Critique
```yaml
  - label: Submit for Critique
    agent: Critic
    prompt: Please review my output ([Artifact Name]) for the Zero to Hero workflow.
    send: true
```

### Roadmap (Return to Strategy)
```yaml
  - label: Return to Strategy
    agent: Roadmap
    prompt: [Task] complete. Returning findings for strategy alignment.
    send: true
```
