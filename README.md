# Agent Builder

A Python-first project template for building lean, predictable agents that can
work together under a shared set of engineering and operating standards.

## Status

Initial repository scaffold. The agent-building conventions, templates, and
validation tooling will be designed collaboratively before implementation.

## Workflow

1. **Define** the agent's purpose, scope, boundaries, and success criteria.
2. **Plan and discuss** the architecture, integrations, and substantive decisions.
3. **Build** the approved design with deterministic Python wherever practical.
4. **Review and test** behavior, integrations, simulations, and acceptance criteria.

Stage transitions require explicit approval from the project author.

## Guiding principles

- Reserve model reasoning for orchestration and decisions.
- Use deterministic, testable code for repeatable execution.
- Prefer Python, focused modules, explicit interfaces, and minimal dependencies.
- Keep agent state, provenance, permissions, and failure behavior visible.
- Design APIs, MCP servers, models, and data providers as replaceable integrations.
- Preserve confirmed decisions and provide clear handoffs between collaborating agents.
