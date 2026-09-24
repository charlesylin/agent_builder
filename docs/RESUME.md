# Resume Agent Builder

Checkpoint: 2026-09-24. Agent Builder **v0.3.0** is accepted and tagged locally. The author
reported all three agreed real-use Review scenarios passed and asked to use this release for
a while before advancing to v0.4.0. **Review remains the current phase** for post-release
observations. No v0.4.0 Define transition has been made.

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

## Current phase: Review, v0.3.0 accepted and in use

Collect any friction from using v0.3.0. The prior confirmed release split names a maintained
Spec Kit dependency and targeted replacements as the candidate direction for v0.4.0. The
comparison is in `planning/spec-kit-comparison.md` and
`planning/spec-kit-component-map.md`. Those records do not predetermine the exact v0.4.0
scope. No new architecture or implementation work is authorized by this release closeout.

A quick existing-solution screen before seeding was discussed during v0.3.0 Review; v0.3.0
requires the full documented decision in Plan, not an early screen in Define. Whether an
earlier screen materially shortens the path to an adopt decision is an open Define input.
Organizational-repository configuration, Grafify or skill discovery, and formal test/control
improvements were excluded from v0.3.0; none is automatically v0.4.0 scope.

## Verification and limits

The v0.3.0 Build passed 64 tests, rendering drift, compilation, and the phase-specific Build
exit check. The Review exit check found nothing unresolved. The acceptance sessions are
author-reported without transcripts, project links, host details, or tested source commits.
The generic generated-project scaffold check does not apply to this legacy source repository:
it intentionally lacks `.agent-builder.json` and contains template tokens. It does pass on
projects generated from the new templates.

## Next action

The author may push the release commit and `v0.3.0` tag, then use the release and report
observations. Enter v0.4.0 Define only after renewed explicit direction.
