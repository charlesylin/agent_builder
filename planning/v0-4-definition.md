# Agent Builder v0.4.0 — Define record

The author approved this Define record and explicitly opened Plan on 2026-09-29. It states
the desired outcome and limits, not an implementation design.

## Author's statement

> We want to maintain agent builder core functionality and process which is quite popular but
> align with the concepts of reuse and best practices. we think that bringing in spec kit as a
> dependency and using as much of that as possible will keep our agents/code/skills more
> consistent and able to be used internally or in the real world as part of a full stack

## Clarification from the author

> v0.3 has actually worked fine so we want to understand whether spec kit can either:
>
> 1) seamlessly replace something
> 2) improve upon something in agent-builder without too drastically changing the user
> experience. If there is a change that would improve AND change user experience, propose it
> and we can evaluate
>
> we don't want to degrade agent-builder just in the name of reuse

## Further direction from the author (2026-09-29)

> ok in this build cycle, i'm in favor of:
>
> Idea assessment - partial replacement
> Specify, clarify, checklist - augmentation
> Plan, tasks, analyze - augmentation
>
> to do this we need to make spec kit a dependency and make sure that when agent-builder is
> installed, spec kit comes along for the ride

The approved direction is one coherent path: assess whether to adopt an existing solution;
if building is justified, clarify one version-sized outcome and expose inconsistencies
between its requirements, plan, and tasks before implementation. A member should not need
to install Spec Kit separately or maintain duplicate records. The installation mechanism
and whether each supported host can satisfy that experience remain to be tested in Plan.
Agent Builder retains its project lifecycle, approvals, versioning, and deterministic
checks unless separately changed with author approval.

## Coverage direction from the author (2026-09-29)

> i think we need to have it for everything whether it's claude/codex and
> agent/project/skill for builds because the idea assessment is broadly useful as are the
> additional features

The author confirmed that the v0.4.0 release requirement is consistent member-facing
capability in Claude Code and Codex, across all three kinds (`agent`, `project`, `skill`).
The organization-installed Claude Code plugin alone is not sufficient. A member should not
have to install or configure Spec Kit separately after installing Agent Builder. This means
equivalent outcomes, not necessarily identical packaging or running every Spec Kit step for
every project: assess reuse for every kind; apply specification, clarification, checks,
planning, tasks, and analysis proportionately on the build path; and stop when adoption
makes a build unnecessary.

Claude Chat, Cowork, and claude.ai plugin installation paths are not v0.4.0 targets; the
author reports that no one uses them. This changes the proposed coverage scope, not any
existing deployment or historical release claim. Plan must verify the installation and
dependency path for Claude Code and Codex. Review should exercise clean-install coverage
for both hosts and all three kinds, and check for duplicate governance records.

## Purpose and smallest useful outcome

For Two River Bio members using Claude Code or Codex to build an agent, skill, or project,
v0.4.0 should make the adopt-or-build judgment and a single version-sized build plan more
consistent and reusable, using a maintained Spec Kit dependency without degrading Agent
Builder's working governance or requiring separate member setup.

The smallest useful result is the selected partial replacement of idea assessment and
proportional augmentation of specification, clarification, checklist, plan, tasks, and
analysis. A suitable existing solution should still end the proposed build. When a build
is justified, the member should reach coherent requirements and tasks for one usable
version, with meaningful inconsistencies surfaced before implementation. This is a
prospective improvement; the author reports that v0.3.0 works well, not that it needs repair.

## Limits and success evidence

Do not replace Agent Builder's phase control, approvals, project status, versioning, or
deterministic checks merely to maximize Spec Kit use. Do not add Spec Kit's implementation
or convergence workflows, or Claude Chat/Cowork/claude.ai coverage, to v0.4.0. If an
experience-changing improvement or unavoidable regression emerges, return to the author
for a separate decision. Keeping a working component unchanged is valid.

Plan should make the acceptance test precise. At minimum, Review needs evidence that a
fresh Agent Builder installation on each target host exposes the agreed capability without
a second member-managed Spec Kit install; each of the three kinds can reach an evidence-led
adopt-or-build decision; a justified build can produce one version-sized specification and
plan/tasks with relevant inconsistencies surfaced; and the experience preserves Agent
Builder's governance without parallel records. Member feedback should check for a net
improvement over v0.3.0, not just successful execution of Spec Kit commands.
