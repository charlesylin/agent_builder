---
id: keep-boundaries-replaceable
title: Keep boundaries replaceable
---
Core project contracts remain independent of Codex, Claude, Gemini, any model provider,
agent runtime, API framework, MCP implementation, data source, storage engine, or delivery
channel. Provider-specific capabilities are optional adapters that declare their coupling.

## Short form

Keep model providers, agent runtimes, APIs, MCP servers, storage, and delivery systems behind
replaceable adapters. Core contracts depend on none of them.
