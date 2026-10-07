# Agent Builder v0.4.1 — Define record

The author explicitly closed Define and entered Plan for this patch on 2026-10-07.

## Problem

The published v0.4.0 repository passes its Linux checks but fails its Windows CI job.
Git can rewrite the line endings of the pinned Spec Kit files at checkout, so their
working-tree bytes no longer match the SHA-256 values in the bundle manifest. A generated
project has the same problem after a Windows-style Git checkout: its copied Spec Kit
assets no longer match the hashes in `.specify/spec-kit-provenance.json`.

This was reproduced locally with `git -c core.autocrlf=true clone` for both the Agent
Builder repository and a newly seeded project. The former failed
`python3 scripts/refresh_spec_kit.py --check`; the latter reported drift for all six
helpers, four templates, and the MIT notice with `check.py .`.

## Smallest useful outcome

Treat v0.4.1 as a patch release for the Windows checkout/hash failure. A checkout of
Agent Builder and a checkout of a newly seeded Claude Code or Codex project must retain
the exact bytes of the pinned Spec Kit assets while preserving the existing hash checks.
The fix must not change the pinned Spec Kit version, asset contents, or Agent Builder's
member-facing workflow.

## Outside this patch

No new Spec Kit steps, host coverage, project kinds, governance changes, or alterations
to existing projects. Do not move the published v0.4.0 tag.

## Success evidence

- A checkout configured to convert text to CRLF still passes the bundle verifier.
- A newly seeded project's Git round-trip under the same configuration still passes
  its project checker for the selected Claude Code or Codex adapter.
- The normal Linux test and lint checks remain green, and Windows CI passes when run
  on the proposed patch.

The exact implementation belongs in Plan. The author has requested that the assistant
handle the fix; Build still requires explicit approval under this project's operating
agreement.
