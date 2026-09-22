---
id: keep-boundaries-replaceable
title: Keep boundaries replaceable
---
Reuse suitable existing code and make new code modular where a real reuse or change boundary
exists. Core project contracts remain independent of Codex, Claude, Gemini, any model provider,
agent runtime, API framework, MCP implementation, data source, storage engine, or delivery
channel. Provider-specific capabilities are optional adapters that declare their coupling.
Do not add layers merely to look scalable; explain the smaller boundary and its maintenance
cost for the organization.

## Short form

Reuse suitable code and keep genuine provider or integration boundaries replaceable. Avoid
speculative layers; core contracts depend on no one host or runtime.
