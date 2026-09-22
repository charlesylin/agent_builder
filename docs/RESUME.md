# Resume Agent Builder

Checkpoint: 2026-09-22. Agent Builder **v0.2.1** is accepted and Review is closed. The author
opened **Define** for the next iteration and confirmed its purpose, smallest deliverable, and
success evidence. The target is **v0.3.0**, with Semantic Versioning for Agent Builder. This
checkpoint records the author's explicit move to **Build** after Plan closed. The confirmed
v0.3.0 implementation scope is in
`planning/implementation-plan.md`.

## Recover context

Read these files completely, in order:

1. `AGENTS.md`
2. `governance/project-state.yaml`
3. `governance/operating-agreement.md`
4. `governance/decisions.yaml`
5. This file, then `docs/v0-2-acceptance.md` and `docs/v0-2-review-feedback.md`.

The compact machine handoff is `governance/handoff.json`. Its schema is
`skills/agent-builder/templates/kinds/agent/contracts/schemas/agent-handoff.schema.json.tmpl`.
Current governance and newer author instructions take precedence over this checkpoint. Check
Git status and recent commits before editing; preserve existing changes.

The root `CLAUDE.md` and `GEMINI.md` direct their coding hosts to `AGENTS.md`. This repository
predates Agent Builder's generated `.agent-builder.json`; the previous review records that
legacy difference. Do not fabricate the manifest or treat its absence as corruption. The
current Define answers and confirmed outcome are in `planning/definition.md`.

## Accepted releases

### v0.1.0 — accepted 2026-09-13

Governance and project scaffolding. See
`docs/v0-1-acceptance.md`. It did not include a runtime, model client, MCP server, custom API,
Dockerfile, or Compose service.

### v0.2.1 — accepted 2026-09-22

An organization-installable Agent Builder skill, deterministic seeder and checker, agent and
skill templates, single-source principles with drift checks, a Claude Code offer hook, evals,
typed consequential approvals, a parking lot for suggestions, phase-exit checks, and fuller
resume briefings. v0.2.1 incorporates the first Review feedback on top of v0.2.0.

Acceptance rested on Sean using the organization-installed v0.2.1 plugin on Windows, without
separate local setup, to reach a seeded, validated, committed Define-phase project in one
session. See `docs/v0-2-acceptance.md` for the evidence and qualifications.

## Current phase: Build for v0.3.0

The author opened Define on 2026-09-22 after accepting v0.2.1. The confirmed purpose is to
formally enact project mode and establish governance for logical versioning, reuse, modularity,
and simplicity, so Two River Bio members can build useful project increments without spaghetti
code, reinventing existing solutions, or making choices that cannot scale across the
organization, while constraining Agent Builder from proposing more than the user needs.

The smallest version is a usable, validated neutral `project` mode that guides a Two River Bio
member through one version-sized MVP. Before Build, it must require an evidence-backed
build-or-adopt decision, a standard version stepping stone, reusable modular components, and
evidence for the simplicity, robustness, and organizational scalability of technical
recommendations. Organizational-repository configuration, Grafify or skill discovery, and
formal testing or control improvements are excluded.

The main acceptance case is a DepMap-like real request in which Agent Builder documents a
suitable public solution, recommends adoption rather than a custom build, and archives the
project after typed author confirmation without entering Build. Additional evidence is concrete
Two River Bio user feedback showing at least one of: a shorter path to a useful result, more
evidence-backed reuse, or effective pushback that simplifies product sprawl. Numerical
thresholds wait for a baseline.

The project also requires structured agent-readable memory with a plain, proportionate human
experience. Human-facing interactions and documents use descriptive language; internal
identifiers are metadata rather than a vocabulary the user must learn. Governance ceremony is
justified only when it changes a real decision, authority, risk, phase, evidence requirement,
traceability, safety, or execution.

In real use, a member should understand status, important decisions, and next action without
decoding internal identifiers; each approval has a concrete consequence; and user feedback
finds the process clear and appropriately lightweight.

Agent Builder targets v0.3.0. Governed projects track their own deliverable versions, one
usable outcome per cycle. When adoption resolves a request without a build, the project records
the adopted solution's version and closes without inventing its own release.

The Define record is complete in `planning/definition.md`. The author explicitly opened Plan
on 2026-09-22. Plan may research options and draft the architecture and implementation steps.
The confirmed plan extends the existing skill, seeder, checker, and templates after
comparing GitHub Spec Kit and OpenSpec. A tagged Spec Kit v1.0.9 CLI/scaffold smoke test
subsequently found more overlap than the first draft acknowledged, especially in prior-art
research, stopping, MVP slices, and organization bundles. The revised draft records the
author's confirmed release split: a lean v0.3.0 using existing Agent Builder components,
then a separately defined v0.4.0 integrating Spec Kit as a maintained dependency
for targeted replacements. A [component map](../planning/spec-kit-component-map.md)
identifies the assessment workflow as the first candidate and explains the upstream-update
tradeoff. K-Dense was only an example of the build-or-adopt outcome, not a dependency or a
hard-coded recommendation. The author removed Windows-specific compatibility as a v0.4.0
integration gate. The release split is confirmed. On 2026-09-22 the author said "yes, close
plan, enter build"; the Plan exit check passed and Build is authorized for the v0.3.0 plan.

The full review findings are in `docs/v0-2-review-feedback.md`. The confirmed scope above is
the boundary for this version. The confirmed design, build slices, and acceptance cases are in
`planning/implementation-plan.md`; the focused Spec Kit evidence is in
`planning/spec-kit-comparison.md`.

## Items not promoted into scope

- This source repository still lacks several generated-project scaffold paths and stores its
  historical records in `docs/`.
- Cowork hook delivery and a clean desktop first run remain untested.
- Codex support beyond v0.2's accepted best-effort level.
- Runtime and environment profiles remain deferred.
- The old onboarding and existing-project proposals under `docs/`.
- Dependabot PR #1 for development-only `prek`; assess separately if it is merged.

## Verification

The accepted v0.2.1 release passed its pinned full gate on 2026-09-14. The 2026-09-22 Review
closeout passed `check.py --leaving review`, `scripts/render.py --check`, compilation, and all
54 unit and behavioral tests. Ruff 0.16.6 was not installed in the active local environment
for the documentation and governance closeout. The full generated-project scaffold check does
not apply to this legacy source repository; the previous review records its intentional
differences. The phase-specific Review exit gate passed before transition. For this Define
checkpoint, `check.py --leaving define`, all 54 tests, generated-file drift check, YAML and
JSON parsing, and whitespace validation passed.

For this Plan approval checkpoint, `check.py --leaving plan` passed with nothing unresolved;
all 54 tests, render drift, YAML/JSON syntax, and whitespace checks passed. The generic
generated-project scaffold check remains inapplicable to this source repository.

## Next action

Implement the first approved slice, a minimal neutral `project` kind, then proceed through
the remaining slices in `planning/implementation-plan.md` with a focused test and commit for
each. Do not make K-Dense part of the build or add Spec Kit to v0.3.0. v0.4.0 receives its
own Define and Plan after v0.3.0 Review.
