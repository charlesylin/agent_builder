# Resume Agent Builder

Checkpoint: 2026-10-08. Agent Builder **v0.4.1** is accepted but untagged.
The author returned v0.5.0 from Review to **Plan** after reporting an
overbuilt fix in Project Aurora. The previous candidate is built but not accepted;
two further guidance amendments are proposed, not implemented.
The confirmed outcome is in the [Define record](../planning/v0-5-definition.md);
the original Build scope and approved amendments are in the
[implementation plan](../planning/v0-5-implementation-plan.md).

## Recover context

Read `AGENTS.md`, `governance/project-state.yaml`, `governance/operating-agreement.md`, and
`governance/decisions.yaml`; reconcile this checkpoint with current Git state and newer
author instructions. The compact machine record is `governance/handoff.json`. This source
repository predates Agent Builder's generated `.agent-builder.json`; do not fabricate one
to make the generated-project scaffold check pass.

## Accepted releases

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

`governance/project-state.yaml` records **Plan**. The earlier v0.5.0 amendments remove
four historical files (2,702 lines) from the active tree; their exact contents
remain in Git history, and the two transcript links now give retrieval commands.
The machine handoff is compact. New neutral projects have no placeholder tests
or CI job; skill and agent projects retain continuing contract checks. Test
guidance now separates expected behavior, temporary feasibility checks, and
lasting regression tests for supported guarantees.

The amended candidate passed 79 repository tests on Python 3.9 and 3.14,
rendered-file and pinned Spec Kit checks, and Ruff 0.16.6 lint and formatting.
These checks establish packaging and deterministic behavior, not real-use
acceptance. The source repository itself predates `.agent-builder.json`, so
`check.py .` still reports its documented scaffold/template baseline warnings;
do not fabricate generated-project files to silence them. v0.5.0 is not
accepted or tagged. Prior release evidence and limits remain in the linked
acceptance records above, especially [v0.4.0](v0-4-acceptance.md) and
[v0.4.1](v0-4-1-review.md).

## Next action

Ask the author to approve or correct the two narrow
[Plan amendments](../planning/v0-5-implementation-plan.md): evidence of a
remaining failure before adding machinery to a direct fix, and current
first-party Codex/Claude Code documentation before host-specific setup guidance.
Do not implement them, enter Build, push, tag, or accept v0.5.0 without
separate direction.
