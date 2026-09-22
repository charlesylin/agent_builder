# Resume Agent Builder

Checkpoint: 2026-09-22. Agent Builder v0.2 is accepted at release **v0.2.1** under AB-D039.
Review is closed. The project author explicitly opened **Define** for the next iteration; its
version number and scope are not yet decided. This checkpoint authorizes Define work only: no
Plan, Build, or implementation.

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
predates Agent Builder's generated `.agent-builder.json`; F-016 records that legacy difference.
Do not fabricate the manifest or treat its absence as corruption.

## Accepted releases

### v0.1.0 — accepted 2026-09-13

Governance and project scaffolding, accepted under AB-D017. See
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

## Current phase: Define for the next iteration

The author opened Define on 2026-09-22 after accepting v0.2.1. Define must establish one
problem and one version-sized outcome before Plan. No version number, scope, architecture,
configuration mechanism, new project kind, or implementation has been approved.

F-018 through F-025 in `docs/v0-2-review-feedback.md` are unprioritized inputs:

- a required build-or-adopt gate after public-solution discovery;
- one minimum viable outcome per versioned cycle;
- discovery and reuse of organizational code plus reusable new modules;
- discovery of available or configured skills and capabilities;
- a neutral `project` kind, now supported by real-use evidence;
- an evidence-backed technical-quality gate for novice recommendations;
- standard versions as useful, testable stepping stones; and
- author-defined expected results, cases, hypotheses, and controls.

They are evidence, not confirmed scope. The first Define question is: **What single problem
should the next iteration solve?** After that, establish how it is handled today, its value,
who benefits, the smallest version-sized outcome, exclusions, and success evidence.

## Items not promoted into scope

- F-016: this source repository uses `docs/` where generated projects use `planning/`.
- Remaining F-017 observations: Cowork hook delivery and a clean desktop first run.
- Codex support beyond v0.2's accepted best-effort level.
- Runtime and environment profiles deferred by AB-D008.
- The old onboarding and existing-project proposals under `docs/`.
- Dependabot PR #1 for development-only `prek`; assess separately if it is merged.

## Verification

The accepted v0.2.1 release passed its pinned full gate on 2026-09-14. The 2026-09-22 Review
closeout passed `check.py --leaving review`, `scripts/render.py --check`, compilation, and all
54 unit and behavioral tests. Ruff 0.16.6 was not installed in the active local environment
for the documentation and governance closeout. The full generated-project scaffold check does
not apply to this legacy source repository; F-016 records its intentional differences. The
phase-specific Review exit gate passed before transition.

## Next action

Ask the author what single problem the next iteration should solve. Continue the Define
conversation without selecting solutions or treating F-018 through F-025 as a bundled scope.
Entering Plan requires a separate explicit author decision.
