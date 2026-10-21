# Resume Agent Builder

Checkpoint: 2026-10-21. Agent Builder **v0.5.0** is accepted and untagged.
The author closed Review and opened **Define**, with **v0.6.0** as the working
next target. Scope remains open. See the [acceptance record](v0-5-acceptance.md)
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

`governance/project-state.yaml` records **Define** for a working v0.6.0 target.
The author reports that the latest tests exposed new issues for this cycle;
those issues have not yet been described. Purpose, scope, smallest outcome,
exclusions, and success evidence remain open. No implementation is approved.

The accepted v0.5.0 outcome and amendments remain in the
[Define record](../planning/v0-5-definition.md) and
[implementation plan](../planning/v0-5-implementation-plan.md).
The prior resume note saying the candidate commits were unpushed was stale:
local and live remote `main` both pointed to `6cd6958` before this closeout.
The author authorized committing and pushing the governance transition.

## Next action

Capture the newly exposed issues from the author, then define the smallest
useful v0.6.0 outcome, exclusions, and success evidence. No tag was requested.
