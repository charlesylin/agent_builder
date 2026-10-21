# Resume Agent Builder

Checkpoint: 2026-10-21. Agent Builder **v0.5.0** is accepted and untagged.
The author approved v0.6.0 Define and opened **Plan**. The next target is
**v0.6.0**. See the [acceptance record](v0-5-acceptance.md)
for reported test success and evidence limits.

## Recover context

Read `AGENTS.md`, `governance/project-state.yaml`, `governance/operating-agreement.md`, and
`governance/decisions.yaml`; reconcile this checkpoint with current Git state and newer
author instructions. The compact machine record is `governance/handoff.json`. This source
repository predates Agent Builder's generated `.agent-builder.json`; do not fabricate one
to make the generated-project scaffold check pass.

## Accepted releases

- **v0.5.0 — accepted 2026-10-21, untagged.** Lean-cycle guidance, repository
  cleanup, behavior-focused testing, and a proportionate maintenance stopping
  rule. The author reports successful latest tests; detailed scenario results
  were not supplied. See [acceptance and limits](v0-5-acceptance.md).
- **v0.4.1 — accepted 2026-10-07, untagged.** Fixes Windows Git checkout
  conversion of pinned Spec Kit files in both Agent Builder and newly
  generated projects. Windows, Ubuntu, and lint CI passed; separate member
  Windows workstation use was not observed. See [Review evidence](v0-4-1-review.md).
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

`governance/project-state.yaml` records **Plan** for v0.6.0.
The five approved requirements, smallest outcome, and success evidence are in the
[v0.6.0 Define record](../planning/v0-6-definition.md). They cover Build size,
useful tests, visible deferrals, lean shared governance, and session version
status. Change-size reporting includes additions and removals by category and
language. Implementation choices remain open; Build is not approved.

The accepted v0.5.0 outcome and amendments remain in the
[Define record](../planning/v0-5-definition.md) and
[implementation plan](../planning/v0-5-implementation-plan.md).

## Next action

Evaluate existing solutions and select the smallest implementation. Resolve
measurement and enforcement, local/shared governance, and version authority.
Present estimated additions/removals by category, purposeful verification, and
flagged-for-later items before seeking Build approval. No push or tag is requested.
