# Where Spec Kit could fit Agent Builder

Status: Plan-phase component audit, not a dependency or migration decision. Checked
2026-09-22 against [Spec Kit v1.0.9](https://github.com/github/spec-kit/releases/tag/v1.0.9)
(`3b895d16bd55a0cdaad16d086ffc6b10eef34614`) and Agent Builder v0.2.1.
The tagged CLI was smoke-tested in a disposable directory, but no novice ran the
assessment workflow. See [the comparison](spec-kit-comparison.md) for test limits.

The real DepMap example used [K-Dense's DepMap skill](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/depmap),
as confirmed by the author. The installed revision and its suitability for a new user's
requirements have not been independently verified here. It is a reference case, not an
automatic adoption recommendation for every DepMap request.

## Component-level fit

| Agent Builder responsibility today or in the v0.3.0 draft | Spec Kit counterpart | Fit and boundary |
| --- | --- | --- |
| Organization-installed skill, Claude offer hook, pre-seed novice conversation | Per-project `specify init` and a coding-agent integration | **Keep Agent Builder's entry point for now.** The accepted Windows test began without a separate local setup. Spec Kit's tested path needed CLI installation, initialization, and explicit assessment enablement. Central installation might close the gap, but has not been tested. |
| Seed and commit agent/skill projects with base, kind, and host-adapter layers | General project initializer, coding-agent integrations, optional [Git extension](https://github.com/github/spec-kit/tree/v1.0.9/extensions/git) | **Possible later replacement for neutral project scaffolding**, not a drop-in for all kinds. Spec Kit can seed a neutral project. Its Git extension can initialize and commit, but auto-commit is disabled by default and the tested `init` did neither. Agent/skill-specific files and the one-session seeded/validated/committed outcome still need a mapping and Windows test. |
| Require a public-solution search, compare alternatives, and stop custom work when one fits | Optional [assess extension](https://github.github.io/spec-kit/reference/agentic-assessment.html), including research, counterevidence, options, and a `kill` verdict; bundled workflow can order the steps | **Strongest direct-reuse candidate.** A configured assessment workflow could supplant much of the planned bespoke research dialogue. Agent Builder would still need to make the gate unavoidable before Build and represent an explicit adopt/version/archive outcome. Invoking assessment stages individually does not force research. Five assessment artifacts may be too much for a small project; test the actual user experience before replacing the proposed short record. |
| One useful deliverable version per cycle and explicit exclusions | Independently testable user stories in the [spec template](https://github.com/github/spec-kit/blob/v1.0.9/templates/spec-template.md), plus a [Lean preset](https://github.com/github/spec-kit/tree/v1.0.9/presets/lean) | **Augment.** Use the independently testable slice and leaner wording. Keep Agent Builder's separate project-deliverable version and adopt-without-new-release rule; the smoke test did not find those as stock lifecycle fields. |
| Project phase, status, decisions, author approvals, and resumption | Assessment verdicts; [workflows](https://github.github.io/spec-kit/reference/workflows.html) with human gates and resumable runs; project constitution | **Keep Agent Builder's lifecycle contract.** Spec Kit has useful checkpoints, but a workflow run state is not the same as a project's active/archived status, typed consequential approval, or cross-cycle decision ledger. A future bridge could call Spec Kit within these boundaries. |
| Deterministic scaffold, phase, and secret-pattern checks | `specify check` checks tooling; agentic `analyze` checks artifact consistency | **Keep the checker.** These checks answer different questions. Spec Kit analysis could add a quality review; it should not silently replace deterministic validation. |
| Single-source principles rendered to multiple host instructions | Live constitution, [presets](https://github.github.io/spec-kit/reference/presets.html), extension overlays, one active integration at a time | **Keep until ownership is redesigned.** Spec Kit's composition avoids editing managed files and permits upgrades, but migrating only some host files would create two instruction owners. Multiple integrations may be installed, though only one is active at a time. |
| Distribute and update Agent Builder for organization use | [Bundles/catalogs](https://github.github.io/spec-kit/reference/bundles.html), managed integrations and [upgrade path](https://github.github.io/spec-kit/upgrade.html), [artifact provenance](https://github.github.io/spec-kit/reference/artifacts.html) | **Candidate platform replacement later.** These are stronger distribution/update primitives than Agent Builder currently has. Organization-repository configuration is outside v0.3.0; do not add this machinery solely for the first MVP. |

## What the upstream-lag concern changes

Borrowing a prompt or pattern from Spec Kit, as Agent Builder borrowed from rewrites.bio,
creates a **manual tracking obligation**: future Spec Kit improvements do not arrive
automatically. Copying source is even more expensive because it adds a local fork and
license/attribution maintenance. A thin integration using Spec Kit's published extension,
preset, workflow, and bundle surfaces offers a genuine update path while keeping Agent
Builder's distinctive entry point and lifecycle. That is the preferred *shape* of any
future dependency, not a decision to add one now.

The update path is controlled, not automatic. Spec Kit separates CLI upgrades from project
file upgrades; the latter use manifest-aware integration and extension updates. Locally
modified managed files may block updates or require manual merging. Bundle pins are
enforced when a component is installed or explicitly refreshed, not when an already-present
component is skipped by an ordinary install. If we use it, pin a tested release, keep local
behavior in overlays rather than edits to managed files, inspect artifact provenance, and
run compatibility tests before updating. A periodic upstream review is still needed for
the parts we only borrow as ideas.

## Recommendation for this Plan

Do not replace Agent Builder's front door, lifecycle, seeder, or deterministic checker in
v0.3.0 on the current evidence. Keep direct reuse of Spec Kit's **assessment workflow** open
as the first, bounded substitution to test against the proposed short Agent Builder
build-or-adopt record. The comparison should measure setup and time to a trustworthy
adopt-and-archive outcome for the K-Dense DepMap case, not just the number of features or
artifacts. If that substitution does not make the novice path simpler, borrow its research
and counterevidence pattern and explicitly review upstream at subsequent release planning.
No Build-phase work is authorized by this map.
