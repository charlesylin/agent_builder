# Resume Agent Builder

Checkpoint: 2026-10-05. Agent Builder **v0.3.0** is accepted and tagged. The author approved
the v0.4.0 Define record, then approved the scoped implementation plan and explicitly
closed Plan and opened **v0.4.0 Build**. The scoped Build implementation is ready for an
author-approved Review transition; the phase has **not** changed yet.

## Recover context

Read `AGENTS.md`, `governance/project-state.yaml`, `governance/operating-agreement.md`, and
`governance/decisions.yaml`; then reconcile this checkpoint with current Git state and newer
author instructions. The compact machine handoff is `governance/handoff.json`. This source
repository predates Agent Builder's generated `.agent-builder.json`; do not fabricate one to
make the generated-project scaffold check pass.

## Accepted releases

- **v0.3.0 — accepted 2026-09-24.** Neutral `project` mode, a required Plan-stage
  build-or-adopt gate, version-sized outcomes, reuse and technical-quality evidence, and
  plainer human-facing governance. The author reported passing adopt-instead-of-build,
  small-project, and cold-resume sessions. See `docs/v0-3-acceptance.md` for what was and was
  not independently observed. Mechanical results are in `docs/v0-3-build-verification.md`.
- **v0.2.1 — accepted 2026-09-22.** Organization-installable skill and deterministic
  seeding/checking. Sean reached a seeded, validated, committed Define project from the
  organization-installed plugin on Windows; see `docs/v0-2-acceptance.md`.
- **v0.1.0 — accepted 2026-09-13.** Governance and scaffolding without a runtime; see
  `docs/v0-1-acceptance.md`.

## Current phase: Build for v0.4.0

The approved [Define record](../planning/v0-4-definition.md) targets a maintained Spec Kit
dependency for a partial replacement of idea assessment and proportionate augmentation of
specification, clarification, checklist, plan, tasks, and analysis. The member-facing result
must work after one Agent Builder installation on Claude Code or Codex, for agent, skill, and
project builds. Claude Chat, Cowork, and claude.ai are not v0.4.0 targets. Preserve Agent
Builder's lifecycle, approvals, versioning, and deterministic checks; avoid duplicate records
and a net regression from v0.3.0. The author chose a pinned Spec Kit CLI as a release-build
dependency that generates a filtered payload bundled with Agent Builder, so members do not
install the CLI separately. The pinned v1.1.0 payload is generated, bundled, seeded, and
validated in the v0.4.0 Build candidate. Both live hosts produced the expected research
artifact in disposable first-slice tests, though neither verified public sources in that
environment. The approved design, Build slices, and Review tests are in
`planning/v0-4-implementation-plan.md`; evidence is in
`docs/v0-4-build-verification.md` and `planning/v0-4-spec-kit-feasibility.md`; the earlier comparison is in
`planning/spec-kit-comparison.md` and `planning/spec-kit-component-map.md`.

The [build-or-adopt evaluation](../planning/v0-4-solution-evaluation.md) recommends a
targeted adaptation rather than wholesale Spec Kit adoption or a custom rewrite. The
approved plan keeps a single Agent Builder entry point, a filtered upstream asset bundle,
and one owner per artifact. The first Build-slice handoff gate passed on both hosts; a
sourced real-use adopt/build test remains for Review. Do not treat low-confidence pilot
research as a validated public-solution recommendation.

## Verification and limits

The v0.3.0 Build passed 64 tests, rendering drift, compilation, and the phase-specific Build
exit check. The Review exit check found nothing unresolved. The acceptance sessions are
author-reported without transcripts, project links, host details, or tested source commits.
The v0.4.0 Define exit check reported nothing unresolved on 2026-09-29.
The 2026-10-05 v0.4.0 Plan passed 64 repository tests, render-drift, YAML/JSON
parsing, and diff checks. After the author confirmed the architecture and risk choices,
the Plan exit check found nothing unresolved. Build passed 74 tests under Python 3.9.6
and 3.14.0, Ruff lint/format, render and vendor drift checks, and the six clean-copy
host/kind seeding cases. The live pilot proved artifact-producing handoff, not sourced
public research or full organization-plugin installation.
The generic generated-project scaffold check does not apply to this legacy source repository:
it intentionally lacks `.agent-builder.json` and contains template tokens. It does pass on
projects generated from the new templates.

## Next action

Ask the author to explicitly close Build and enter Review. Once authorized, have them
refresh/install this v0.4.0 candidate and run Agent Builder on a separate project. A
suitable-public-solution case must produce sourced research and an adopt recommendation;
a novel-build case must produce one version-sized spec, plan, tasks, and an analysis of
contradictions. See `docs/v0-4-build-verification.md` for exactly what passed and what
remains. No v0.4.0 tag or push has been authorized by the Build phase alone.
