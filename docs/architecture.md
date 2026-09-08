# Architecture

## v0.1 shape

Agent Builder is a deterministic scaffold renderer, not an agent runtime.

```text
project inputs
  name + purpose + selected coding-agent adapters
                         │
                         ▼
              stdlib-only Python renderer
                         │
                         ▼
  governance + contracts + security + Python project skeleton
```

The templates are the single source of truth. The renderer substitutes a small, validated
set of project values, writes through a temporary directory, validates the result, and only
then moves it to the requested destination. Existing targets are never overwritten.

## Three independent adapter layers

1. **Coding-agent adapter:** instructions for Codex, Claude Code, or Gemini CLI while humans
   develop the project.
2. **Runtime adapter:** a future boundary between the project contract and PydanticAI,
   OpenAI Agents SDK, Google Gen AI, another framework, or direct model APIs.
3. **Deployment profile:** a future OCI image and Docker Compose definition for local use,
   with portable configuration for other container hosts.

Selecting a coding-agent adapter does not select a model provider or runtime. A project may
be developed with Codex, run Gemini, and expose tools through independently deployed MCP
servers.

## Framework-independent contract

The following remain outside every runtime adapter:

- purpose, scope, authority, and phase state;
- domain inputs, outputs, validation, and failure policy;
- agent-to-agent handoff schema;
- API and MCP payload schemas;
- configuration and secret references;
- persisted data and migration versions; and
- provenance, audit events, and acceptance fixtures.

This boundary allows an agent to change runtime without changing what collaborators consume.

## Upgrade policy

Every generated project records the template version and selected adapters in
`.agent-builder.json`. New template versions affect new projects only. Existing projects may
compare changes and opt in later; no background or automatic rewriting occurs.

Internal changes can break freely inside a standalone agent. Boundary changes require a
new contract version and a migration or coordinated rollout. Base images and dependencies
still require security review and rebuilds even when pinned.

## Deferred deliberately

Version 0.1 does not generate a Dockerfile or `compose.yaml` because a non-runnable placeholder
would imply runtime decisions that have not been made. The approved default—OCI containers
with Docker Compose locally—is recorded now and will be emitted with the first runtime profile.
