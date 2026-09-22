# Agent Builder v0.3.0 plan

Status: proposed for author review. This plan does not authorize Build.
Scope and success evidence: [definition.md](definition.md).
The focused [Spec Kit comparison](spec-kit-comparison.md) and
[component map](spec-kit-component-map.md) update the provisional build-or-adopt
recommendation below after a tagged-release CLI smoke test. In particular, direct use of
Spec Kit's assessment workflow remains an open alternative to building the proposed short
Agent Builder evidence record; no dependency choice has been confirmed.

## Build or adopt Agent Builder itself?

Checked 2026-09-22 against the approved outcome, using the projects' own documentation and
release records. GitHub stars indicate interest, not verified active use. No third-party
source or runtime dependency is proposed for the Agent Builder release; MIT notice
obligations would apply if source is copied later.

| Candidate | Evidence | Fit for this version | Recommendation |
| --- | --- | --- | --- |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | MIT; about 138k stars; tests and active releases ([v1.0.9, 2026-09-21](https://github.com/github/spec-kit/releases)). Its optional [assessment extension](https://github.github.io/spec-kit/guides/assessment.html) researches prior art, includes counterevidence, and can stop when a better alternative exists. Its core spec template supports independently testable MVP slices; Lean presets and organization-curated bundles reduce ceremony and support reuse. The [tagged-release smoke test](spec-kit-comparison.md) succeeded. | Substantial overlap, including neutral projects and a no-build outcome. The first-party assessment workflow can require research, although separate stage use does not; the stock decision does not record a distinct adopt-and-archive result. The tested CLI path adds installation and initialization to the accepted organization-plugin path. Its extension system could close these gaps, but that needs a comparative novice pilot. | Provisionally incorporate the relevant parts into Agent Builder. Test direct use of the assessment workflow before deciding whether to build the short evidence record; keep broader replacement open until a novice pilot. |
| [OpenSpec](https://github.com/Fission-AI/OpenSpec) | MIT; about 70k stars; tests and active [releases](https://github.com/Fission-AI/OpenSpec/releases), including recent archive and security fixes. | Useful short spec and archive workflow. Its documented [setup](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md) requires Node.js 20.19+ and a CLI install; its archive follows a change workflow. The documented default does not require an existing-solution decision before Build or represent adoption as a completed project without a custom release. | Do not replace Agent Builder or add it as a dependency for v0.3.0. |
| Agent Builder v0.2.1 | Organization-installed skill already passed the Windows novice acceptance test without separate setup; seeder, checker, template layers, project status, and single-source principles are in this repo and tested. | The missing behavior is bounded: a neutral kind, a decision before Build, a project release target, and a plainer human interface. | Extend the existing system. Recommend public tools directly to future project authors when they satisfy that project's need. |

This is a recommendation for this version, not a claim that either public tool is generally
inferior. Spec Kit v1.0.9 was installed in a disposable environment for CLI and scaffold
testing; OpenSpec was not installed. The Spec Kit trial did not run the agent-facing assessment
or test a novice user. Published tests and security history were inspected at repository
level; no independent security audit was performed.

## Design

1. Add a neutral `project` template layer to the existing seeder and checker. It receives the
   common governance and planning files, plus a project-specific state file without agent
   runtime, deployment, contracts, skill manifest, or generated application code. The S3
   watcher that motivated the kind is the realistic seed example.
2. Give every newly seeded kind one short `planning/solution-evaluation.md`. It records the
   need, search date and sources, suitable public candidates and any user-provided codebase,
   evidence of fit, utilization, maintenance, tests, security history, licensing, and setup
   burden, then a reasoned `adopt`, `adapt`, or `build` recommendation. If none qualifies, say
   what was searched and why. The skill must recommend adoption and ending the custom project
   when a candidate meets the need. After typed author confirmation, it records the adopted
   component and version, archives the project, and does not enter Build. No repository or
   skill registry is hard-coded.
3. For work that continues, store a separate deliverable version target in project state;
   keep it distinct from `generated_by.version`. The skill asks what would make v0.1.0 usable,
   or what the next appropriate SemVer stepping stone is for an existing project, and records
   its explicit exclusions. The Plan exit check requires a recorded build-or-adopt decision
   and valid target for an `adapt` or `build` outcome. An `adopt` outcome has no new project
   release. Existing pre-0.3 projects keep validating unchanged; upgrades remain opt-in.
4. Use that same evidence record for technical-quality judgment. For an `adapt` or `build`
   choice, state which existing components are reused, what small boundary makes new code
   replaceable, the failure behavior, and why the proposed design is simpler and sufficiently
   robust for the version-sized outcome. Compare credible alternatives and organizational
   maintenance costs; challenge a fragile shortcut, especially for a novice user, without
   adding speculative abstraction. The checker can verify required fields and the decision;
   it cannot certify the truth or quality of the reasoning. Real-use review provides that test.
5. Keep stable IDs and structured state for agents. Render plain human-facing status,
   decisions, and next action without requiring people to learn local IDs. Ask for typed
   approval only when it changes a consequential choice or authority. Remove the mandatory
   four-part closeout when its empty sections add no value. Change source principles and
   skill stencils, then regenerate adapters and agreements with `scripts/render.py`.

## Build sequence if the author later authorizes Build

Each slice should leave the existing suite green and have a focused test that proves its
behavior. No version bump or release tag occurs until the result is ready for Review.

1. **Neutral kind:** add `project` to `seed.py` and `check.py`, a minimal kind template, and
   seeding/validation tests. Confirm old agent and skill projects still validate.
2. **Decision before Build:** add the common solution-evaluation template, skill guidance,
   and the Plan exit check for projects seeded at 0.3.0 or later. Test adopt-and-archive,
   adapt, build, missing evidence, and old-template compatibility.
3. **Version-sized work and quality:** add independent deliverable targets, SemVer checks,
   guidance that challenges overscoped or fragile proposals, and realistic behavioral cases.
4. **Plain human interface:** revise the single-source principle and skill instructions,
   render generated instructions, and test that human briefings avoid internal IDs while
   machine records retain them.
5. **Review readiness:** run the S3-watcher neutral-kind case and a DepMap-like adoption case;
   record commands, outputs, and unknowns. Collect Two River Bio user feedback in Review.
   Bump release metadata together only when cutting v0.3.0 in the authorized release workflow.

## Acceptance and limits

- A `project` seed is validated and committed, with no agent or skill-specific files.
- A DepMap-like skill request yields an evidence-backed adoption recommendation and, after
  author confirmation, an archived project with no Build or invented project release.
- A proposed browser side-load or similarly fragile shortcut is challenged with evidence and
  a simpler version-sized route.
- A novice can explain status and next action without decoding IDs; the internal ledger remains
  intact. Feedback records whether the process felt clear and appropriately lightweight.
- The existing 54 tests, new focused tests, render drift check, and generated-project checker
  pass. This source repository's generic scaffold check remains inapplicable to its own tree.

Organizational-repository configuration, Grafify/skill discovery, and formal hypothesis or
control-data work remain outside v0.3.0.
