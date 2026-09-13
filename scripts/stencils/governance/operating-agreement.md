# Agent Builder operating agreement

**Status:** Active

**Effective date:** 2026-09-08

The current phase is recorded in `governance/project-state.yaml`, not here.

## Purpose

Agent Builder gives Charles Yang Lin and his collaborators a consistent starting point for
agents that can work independently, cooperate through explicit contracts, and be understood
by humans. The template favors lean implementations and predictable behavior over large,
framework-driven abstractions.

## Workflow

{{principle:phases}}

## {{principle:decision-protocol|title}}

{{principle:decision-protocol}}

## Engineering principles

### {{principle:nokkvis-law|title}}

{{principle:nokkvis-law}}

### {{principle:use-reasoning-selectively|title}}

{{principle:use-reasoning-selectively}}

### {{principle:search-before-building|title}}

{{principle:search-before-building}}

### {{principle:work-small-fail-loudly|title}}

{{principle:work-small-fail-loudly}}

### {{principle:keep-boundaries-replaceable|title}}

{{principle:keep-boundaries-replaceable}}

### {{principle:containerize-the-deployed-agent|title}}

{{principle:containerize-the-deployed-agent}}

## {{principle:security-and-authority|title}}

{{principle:security-and-authority}}

## {{principle:communication-and-handoffs|title}}

{{principle:communication-and-handoffs}}

## v0.1 boundary (historical)

Version 0.1 supplied governance, project metadata, host-agent adapters, a machine-handoff
contract, security defaults, Python directories, and deterministic scaffold validation. It
did not supply an agent runtime, model client, MCP server, custom API, Dockerfile, or Compose
service. v0.1 was accepted on 2026-09-13 (AB-D017); v0.2 scope is recorded in
`docs/v0-2-define.md`.
