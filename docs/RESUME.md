# Resume Agent Builder

Checkpoint: 2026-10-05. Agent Builder **v0.3.0** is accepted and tagged. The author approved
the v0.4.0 Define record and explicitly opened **v0.4.0 Plan**. No Build work is authorized.

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

## Current phase: Plan for v0.4.0

The approved [Define record](../planning/v0-4-definition.md) targets a maintained Spec Kit
dependency for a partial replacement of idea assessment and proportionate augmentation of
specification, clarification, checklist, plan, tasks, and analysis. The member-facing result
must work after one Agent Builder installation on Claude Code or Codex, for agent, skill, and
project builds. Claude Chat, Cowork, and claude.ai are not v0.4.0 targets. Preserve Agent
Builder's lifecycle, approvals, versioning, and deterministic checks; avoid duplicate records
and a net regression from v0.3.0. The author chose a pinned Spec Kit CLI as a release-build
dependency that generates a filtered payload bundled with Agent Builder, so members do not
install the CLI separately. The exact packaging and integration design is not yet proven or
approved for Build. Evidence and remaining tests are in
`planning/v0-4-spec-kit-feasibility.md`; the earlier comparison is in
`planning/spec-kit-comparison.md` and `planning/spec-kit-component-map.md`.

Plan should test Spec Kit dependency/distribution feasibility on both hosts; compare the
selected functions with Agent Builder's current flow; record a build-or-adopt evaluation;
and propose only the integration boundaries and acceptance tests needed for v0.4.0. If a
maintained dependency cannot deliver the agreed outcome without regression, return to the
author for a decision rather than silently weakening the release criterion.

## Verification and limits

The v0.3.0 Build passed 64 tests, rendering drift, compilation, and the phase-specific Build
exit check. The Review exit check found nothing unresolved. The acceptance sessions are
author-reported without transcripts, project links, host details, or tested source commits.
The v0.4.0 Define exit check reported nothing unresolved on 2026-09-29.
The generic generated-project scaffold check does not apply to this legacy source repository:
it intentionally lacks `.agent-builder.json` and contains template tokens. It does pass on
projects generated from the new templates.

## Next action

Test that the release-build payload is reproducible, preserves upstream provenance and
license, excludes out-of-scope skills, and works without a member CLI. Resolve script
compatibility and single-source artifact ownership, then test the intended handoffs on
Claude Code and Codex across all three build kinds before proposing the v0.4.0
implementation plan or seeking Build approval.
