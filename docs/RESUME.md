# Resume Agent Builder

Checkpoint: 2026-10-06. Agent Builder **v0.4.0** was accepted for organization use.
Review is closed and the release tag is `v0.4.0`. The next Define iteration has not
opened; the author wants members to use this version before more building.

## Recover context

Read `AGENTS.md`, `governance/project-state.yaml`, `governance/operating-agreement.md`, and
`governance/decisions.yaml`; reconcile this checkpoint with current Git state and newer
author instructions. The compact machine record is `governance/handoff.json`. This source
repository predates Agent Builder's generated `.agent-builder.json`; do not fabricate one
to make the generated-project scaffold check pass.

## Accepted releases

- **v0.4.0 — accepted 2026-10-06.** A pinned Spec Kit 1.1.0 release-build payload gives
  new Claude Code and Codex projects research and proportional specification/planning
  guidance through the single Agent Builder skill. Members do not install the Spec Kit
  CLI. See [the acceptance record](v0-4-acceptance.md) for Erico's Codex test, the
  packaging correction, and explicit untested controls.
- **v0.3.0 — accepted 2026-09-24.** Neutral `project` mode, build-or-adopt gate,
  version-sized outcomes, reuse and technical-quality evidence, and plain governance.
  See [the acceptance record](v0-3-acceptance.md).
- **v0.2.1 — accepted 2026-09-22.** Organization-installable skill and deterministic
  seeding/checking; see [the acceptance record](v0-2-acceptance.md).
- **v0.1.0 — accepted 2026-09-13.** Governance and scaffolding without a runtime;
  see [the acceptance record](v0-1-acceptance.md).

## Current project state

`governance/project-state.yaml` keeps `review` as the last phase but marks it closed;
no new phase has been authorized. The project remains active for post-release
observations, not for an unapproved next build. The v0.4.0 purpose and limits are in
the [Define record](../planning/v0-4-definition.md), approved design in the
[implementation plan](../planning/v0-4-implementation-plan.md), and completed Build
checks in [Build verification](v0-4-build-verification.md).

Erico's real Codex skill project reported sourced research, an adapt recommendation,
one feature specification, plan, tasks, and a consistency analysis. The supplied
execution record says Agent Builder read bundled Spec Kit instructions; no separate
member CLI was installed. It is an agent-authored account with supporting artifacts,
not a full transcript. A later packaging correction changed the bundled instruction
filenames, leaving their contents unchanged; a fresh Codex inventory showed only
Agent Builder as a skill. The repository checks passed, but a live project session
was not rerun after that rename.

The adopt-and-archive case, planted contradiction, full real-use host/kind matrix,
and measured v0.3 comparison were not completed before release. They are evidence
limits, not passed tests. The author explicitly accepted the release with those
limits visible so the organization can use it and report actual outcomes.

## Next action

Use the tagged v0.4.0 release in the organization and record concrete successes,
failures, and friction. Do not choose a next version or open Define until the author
explicitly requests it.
