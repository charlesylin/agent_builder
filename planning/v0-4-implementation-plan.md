# Agent Builder v0.4.0 — implementation plan

**Status:** Approved by the author on 2026-10-05; Build is authorized with the
first-slice host handoff as a stop/go gate.

The approved outcome and exclusions are in [`v0-4-definition.md`](v0-4-definition.md);
the build-or-adopt recommendation is in
[`v0-4-solution-evaluation.md`](v0-4-solution-evaluation.md). One release-sized result:
after one Agent Builder installation, a member on Claude Code or Codex can use a
Spec Kit-backed, evidence-led adopt-or-build judgment and, when building is justified,
reach one coherent version-sized spec, plan, and task set without a second lifecycle.

## Evidence that fixes the dependency boundary

Pin [Spec Kit v1.1.0](https://github.com/github/spec-kit/releases/tag/v1.1.0) at
`f1d3a4f8337ebbd3ae22760a9c12e3352b93a175` (MIT). The CLI runs only in an isolated
release-build environment with Python 3.11+. It generates assets for both `claude` and
`codex` with `--script sh --extension assess --non-interactive`; a deterministic allowlist
packages the selected output inside the Agent Builder skill. Member machines neither
install nor invoke `specify`, and seeding makes no network request.

In disposable Plan probes on macOS arm64, the v1.1.0 CLI generated the seven selected
host skills, Bash helpers, and templates for both hosts. A repeated Claude generation
produced identical selected files. Manually copying a filtered payload into fresh
Agent Builder `agent`, `skill`, and `project` seeds with both host adapters left all three
scaffolds valid. Without `specify` on the member command path, the bundled Bash helpers
created a feature and resolved paths, plan, tasks template, and analysis prerequisites.
The copied Agent Builder operating agreement was byte-identical to the Spec Kit
constitution view. See the exact probe record in
[`v0-4-spec-kit-feasibility.md`](v0-4-spec-kit-feasibility.md).

These are **packaging and script** results, not proof of model-mediated handoff or a clean
organization installation. Codex file-reading produced the expected research artifact
shape in an earlier v1.0.13 probe, but public web research was disabled. Claude Code's CLI
is not authenticated on this machine, so its live handoff is unobserved. The first Build
slice below is a stop/go integration test, not permission to claim host parity from the
structural probe.

## Smallest integration design

1. **One member-facing entry point.** Keep Agent Builder's existing skill, offer hook,
   Define → Plan → Build → Review phases, typed approvals, project status, SemVer target,
   and deterministic checker. The seven upstream-generated instruction files are bundled
   under `skills/agent-builder/vendor/spec-kit/`, not installed as additional top-level
   member-facing skills. Agent Builder reads the host-specific upstream file, binds its
   `$ARGUMENTS` explicitly, follows it for the selected step, and checks the expected
   artifact before continuing. This avoids relying on unproven skill-to-skill native
   invocation or asking the member to run Spec Kit as a second workflow.
2. **Selected upstream steps.** Always use `assess-research` to challenge a proposed
   build with prior art and counterevidence. Agent Builder still completes its existing
   fit/use/maintenance/tests/security/license/setup evaluation and obtains author
   confirmation of adopt, adapt, or build; a sufficient public solution ends the project
   in Plan. On an approved build path, use `specify` for one feature-sized specification,
   `clarify` for material ambiguity, `checklist` where requirement quality needs a check,
   then `plan`, `tasks`, and `analyze` to surface inconsistencies before implementation.
   Do not run every optional step ceremonially. Do not ship or invoke Spec Kit's intake,
   define, shape, decide, constitution, implement, converge, or taskstoissues workflows.
3. **One owner per fact.** `planning/definition.md` owns the problem, users, purpose,
   release-sized outcome, and exclusions. `governance/project-state.yaml` and
   `governance/decisions.yaml` own phase/status/version/approvals. The short
   `planning/solution-evaluation.md` owns the final adopt/adapt/build judgment and links
   to `.specify/assessments/<slug>/research.md` as evidence. Only on the build path,
   `specs/<feature>/spec.md` owns detailed requirements and acceptance scenarios;
   adjacent `plan.md` and `tasks.md` own implementation detail. These files must reference,
   not independently redefine, the approved outcome. If clarification changes purpose,
   scope, authority, or version target, pause and obtain the corresponding Agent Builder
   approval before continuing.
4. **Constitution as a checked view.** Seed `.specify/memory/constitution.md` from the
   project's `governance/operating-agreement.md`; it is never independently edited.
   `check.py` checks equality (or a deterministic rendered equivalent) for v0.4 seeds.
   Spec Kit analysis may treat the constitution as binding without creating a second
   source of governance. Preserve existing projects unchanged; any upgrade is opt-in.
5. **Only the necessary project assets.** Newly seeded v0.4 projects receive the six
   upstream Bash helpers and four used templates (`spec`, `plan`, `tasks`, `checklist`),
   the generated constitution view, an upstream version/provenance marker, and the MIT
   notice. The release bundle also carries the two host-specific sets of seven selected
   instruction files. It does not install the CLI or create an upstream placeholder
   constitution, integration manifest, workflow registry, or visible excluded skills.
   Existing Gemini seeding keeps its v0.3 behavior, without claiming these v0.4
   augmentations on that host. A missing file, unsupported Spec Kit host, missing Bash,
   invalid feature path, stale constitution, or absent expected artifact fails clearly
   rather than silently falling back to an unreviewed workflow.

The release refresh command must fetch/verify the full upstream commit, run the pinned
CLI in an isolated environment, extract an explicit allowlist, preserve the license, and
write a manifest of version, commit, source commands, and hashes. A repository test checks
the committed payload against that manifest and forbids extra upstream workflows. Updating
the pin requires regenerating the payload and reviewing the asset diff; it never silently
rewrites an existing project. The normal test suite should not require network access.

## Build sequence, each slice independently reversible

1. **Stop/go host handoff.** In disposable projects, implement the smallest Agent Builder
   adapter that reads a bundled upstream research step, binds a substantive idea, and
   verifies `research.md`. Exercise it through authenticated Claude Code and Codex with
   Agent Builder as the only member-invoked skill. Check that the host does not merely
   mention or file-read the upstream step without producing the artifact, and that
   uncertainty is explicit when public research is unavailable. If either host cannot
   provide equivalent behavior without a second member invocation, stop Build and return
   to Plan before implementing the rest. The author approved moving this
   remaining live-host uncertainty into the bounded first Build slice.
2. **Reproducible release payload.** Add the pinned generator/allowlist, version and hash
   manifest, MIT notice, and drift/exclusion tests. The released Agent Builder skill must
   contain everything needed for the selected steps. A clean install requires no Spec Kit
   CLI or first-use download.
3. **Seed and validate one owner.** Extend `seed.py`, templates, and `check.py` to place the
   selected Bash helpers/templates and generated constitution in new `agent`, `skill`,
   and `project` seeds. Keep old seeds valid and untouched. Verify no host-specific asset
   is required in the project's core governance contract.
4. **Route the two outcomes.** Update the single-source Agent Builder skill instructions
   to use upstream research before its existing build-or-adopt gate; then, only for a
   justified build, guide the proportional specify/clarify/checklist/plan/tasks/analyze
   path. Verify artifact postconditions, approval boundaries, failure behavior, and
   no duplicated normative record. Do not add another user-facing phase or a parallel
   decision ledger.
5. **Prepare Review.** Update installation/upgrade guidance and run the full repository
   tests, render-drift check, lint, and new fixture tests. Run the clean-install matrix
   below. Do not tag or claim v0.4.0 acceptance inside Build.

## Review tests and controls

- **Six host/kind cases:** a fresh Agent Builder install on each of Claude Code and Codex,
  each seeding `agent`, `skill`, and `project`. The member installs Agent Builder once,
  never runs or installs `specify`, and can use the same adopt-or-build and build-detail
  capabilities. The installed payload exposes no `implement` or `converge` step.
- **Adopt control:** a request with a demonstrably suitable public solution produces
  sourced research, the complete Agent Builder quality comparison, a recommendation to
  adopt, and (only after typed confirmation) an archived project with no invented release
  or Spec Kit build artifacts. Keep the candidate generic; no favored repository is
  hard-coded.
- **Build control:** a request without a suitable public solution reaches one usable
  version, a concise feature spec, plan, and tasks. Seed an intentional contradiction
  between requirement and task; `analyze` must report it before Build. Check that
  optional clarification/checklist steps are used for a real gap, not every time.
- **Regression and authority:** the v0.3.0 scenarios still work, older projects stay
  unchanged, Gemini seeding retains its existing behavior, the project phase and release
  target have one owner, and neither target host can
  bypass Agent Builder's typed adopt/build and phase approvals by following an upstream
  next-step suggestion. `check.py` catches missing or divergent required assets.
- **Human outcome:** a Two River Bio member reports whether this made the decision and
  version-sized plan more useful without appreciable extra ceremony. Record failures and
  net regression as Review findings, not automatic acceptance.

There is no Windows-specific acceptance gate (the author's earlier direction), no Claude
Chat/Cowork path, no Spec Kit runtime CLI, no upstream implementation/convergence
workflow, and no automated migration of existing projects in this version.

## Approved Build boundary

The author approved this scoped adaptation and its first-slice stop/go test after
the complete plan was read back. This is Build authorization for the sequence above,
not evidence that the live host handoff works or that v0.4.0 is accepted.
