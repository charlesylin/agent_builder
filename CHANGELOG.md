# Changelog

All notable changes to Agent Builder are documented here.

## [Unreleased]

### Changed

- Python floor lowered from 3.11 to 3.9 for the builder's own scripts (AB-D025). Entry points
  now fail with a one-sentence message and exit code 2 on an older interpreter instead of a
  stdlib traceback (closes finding F-002). CI runs on Python 3.9 and 3.12 on Ubuntu and 3.12 on
  Windows. Generated projects still declare `requires-python >= 3.11` for their own future code;
  that default is theirs to change.

## [0.1.0] - 2026-09-13

Governance and project scaffolding only. No agent runtime, model client, MCP server, custom
API, Dockerfile, or Compose service is included. Accepted by the project author on 2026-09-13
under AB-D017; see [the acceptance record](docs/v0-1-acceptance.md).

### Added

- Governance-first project initializer.
- Selectable Codex, Claude Code, and Gemini CLI adapters.
- Compact machine-handoff contract and project validator.
- Container, compatibility, and secret-handling policies.
- Nokkvi's law: a silent per-turn encouragement cue in builder instructions and generated
  Codex, Claude Code, and Gemini CLI adapters. Performance impact remains unmeasured.
- Practical persistence guidance: try a concrete alternative when difficulty causes premature
  stopping, while respecting blockers, permissions, phase gates, stop requests, and budgets.
- Repository restart guide and compact handoff for resuming across accounts and hosts.
- Sean's Windows test packet and proposed onboarding/existing-project adoption review notes.
