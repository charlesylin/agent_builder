# Resume Agent Builder

Checkpoint: 2026-10-05. Agent Builder **v0.3.0** is accepted and tagged. The author approved
the v0.4.0 Define record and explicitly opened **v0.4.0 Plan**. The v0.4.0 Plan proposal
awaits author confirmation; no Build work is authorized.

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
install the CLI separately. A filtered v1.1.0 payload passed disposable structural and
helper-script probes, but the exact integration design is not approved for Build and live
host behavior remains unverified. The proposed design, Build slices, and Review tests are in
`planning/v0-4-implementation-plan.md`; evidence is in
`planning/v0-4-spec-kit-feasibility.md`; the earlier comparison is in
`planning/spec-kit-comparison.md` and `planning/spec-kit-component-map.md`.

The [build-or-adopt evaluation](../planning/v0-4-solution-evaluation.md) recommends a
targeted adaptation rather than wholesale Spec Kit adoption or a custom rewrite. Plan
proposes a single Agent Builder entry point, a filtered upstream asset bundle, one owner
per artifact, and a first Build-slice stop/go test for model-mediated handoff. That last
choice explicitly moves remaining live-host uncertainty across the phase boundary and
requires author approval. If it fails, return to Plan rather than weaken v0.4.0.

## Verification and limits

The v0.3.0 Build passed 64 tests, rendering drift, compilation, and the phase-specific Build
exit check. The Review exit check found nothing unresolved. The acceptance sessions are
author-reported without transcripts, project links, host details, or tested source commits.
The v0.4.0 Define exit check reported nothing unresolved on 2026-09-29.
The 2026-10-05 v0.4.0 Plan draft passed 64 repository tests, render-drift, YAML/JSON
parsing, and diff checks. The phase exit check now correctly refuses its two proposed
architecture/risk decisions until the author resolves them.
The generic generated-project scaffold check does not apply to this legacy source repository:
it intentionally lacks `.agent-builder.json` and contains template tokens. It does pass on
projects generated from the new templates.

## Next action

Read the author the short version of `planning/v0-4-implementation-plan.md`, especially
the non-discoverable upstream-file adapter and the first-slice live-host stop/go gate.
Ask for confirmation or correction of those choices and the Build sequence. Do not
transition solely because the source repository's generated-project checker reports
"nothing unresolved"; it does not validate this Plan's architecture or tests.
