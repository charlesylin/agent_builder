---
id: containerize-the-deployed-agent
title: Containerize the deployed agent
---
Generated agents are intended to run as standalone OCI images. Once a runtime is selected,
use a minimal trusted base, multi-stage build, locked dependencies, a non-root user, explicit
health checks, resource limits, and a read-only filesystem where feasible. Keep durable data
outside the container. Docker Compose is the default local orchestration format.

Containers isolate implementation dependencies; they do not make boundaries compatible.
Version messages, APIs, MCP contracts, configuration, persisted state, and exchanged files.
Internal code may change without backward compatibility. A breaking boundary change requires
an explicit version change and either a migration or a coordinated rollout.

Generated projects pin their own dependencies and record their template version. Agent
Builder does not silently update existing projects. Security maintenance is the exception to
indefinite freezing: vulnerable dependencies and base images must be assessed and rebuilt.

## Short form

Deployed agents are standalone OCI containers; Docker Compose is the local default once a
runtime is selected. Containers isolate implementations, not interfaces: version every
external contract, and require an explicit version change plus migration or coordinated
rollout for a breaking one. Template upgrades never silently rewrite an existing project.
