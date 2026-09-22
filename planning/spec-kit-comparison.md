# Spec Kit comparison for v0.3.0

Status: Plan-phase evidence and recommendation, not authorization to implement or migrate.
Checked: 2026-09-22. The reference implementation was GitHub Spec Kit
[v1.0.9](https://github.com/github/spec-kit/releases/tag/v1.0.9), commit
`3b895d16bd55a0cdaad16d086ffc6b10eef34614`. Its repository is MIT-licensed.
No Spec Kit source was copied into Agent Builder.

## What was tested

In a disposable directory outside this repository, I shallow-cloned the tagged release,
installed it into a temporary Python 3.14 virtual environment, checked `specify version`,
and ran:

```text
specify init depmap-adopt-trial --integration claude --script py --extension assess --ignore-agent-tools --non-interactive
specify extension list
specify preset add lean
specify bundle install <tagged-clone>/bundles/assess/bundle.yml --offline
specify workflow list
```

Initialization succeeded. It installed the bundled assessment extension v1.0.0 and created
the Claude skills and `.specify` infrastructure. The generated checkout contained 50 files
under `.claude` and `.specify`, including 15 skills. It did not initialize Git, record a
project lifecycle status, or produce an assessment decision at initialization. The latter
requires running the agent-facing assessment commands. `--ignore-agent-tools` means this was
not a test of Claude Code discovery or novice interaction. No full end-to-end assessment was
run; the workflow findings below come from the tagged commands and templates, not observed
model behavior. The bundled Lean preset and local first-party assessment bundle installed
successfully afterward; `workflow list` showed intake → research → define → shape → decide
with a verdict review gate. The catalog form of `bundle add assess --offline` could not
download its manifest, so the local tagged bundle manifest was used for this offline test.

## Test against the Two River Bio cases

| Need | Spec Kit v1.0.9 evidence | Agent Builder implication |
| --- | --- | --- |
| Recommend an existing DepMap skill and stop custom work | The optional [assessment extension](https://github.com/github/spec-kit/blob/v1.0.9/extensions/assess/README.md) researches prior art and counterevidence. Its [shape command](https://github.com/github/spec-kit/blob/v1.0.9/extensions/assess/commands/speckit.assess.shape.md) includes a smallest-workable and, when relevant, buy/do-nothing option. Its [decision command](https://github.com/github/spec-kit/blob/v1.0.9/extensions/assess/commands/speckit.assess.decide.md) permits `kill` because a better alternative exists. Research is optional when invoking stages separately, but the bundled [assessment workflow](https://github.com/github/spec-kit/blob/v1.0.9/workflows/assess/workflow.yml) runs it before the verdict. The stock decision is a stopped assessment, not an explicit `adopt` record with the selected solution's version and project archive status. | Do not claim Spec Kit lacks a no-build path. Make existing-solution research and the adopt-and-close result required, with provenance and adopted version. A configured Spec Kit workflow could also enforce the search. |
| Start a neutral S3-watcher project | The CLI initialized a general project successfully with no agent or skill product kind. | Spec Kit already serves neutral projects; this is not a unique Agent Builder capability. Agent Builder's reason to keep its project kind is compatibility with its installed skill and existing governance. |
| Deliver one usable version-sized outcome | The core [spec template](https://github.com/github/spec-kit/blob/v1.0.9/templates/spec-template.md) requires independently testable, deployable user stories and treats one story as a viable MVP. A bundled [Lean preset](https://github.com/github/spec-kit/blob/v1.0.9/presets/lean/README.md) reduces template ceremony. Neither the tested default nor assessment artifacts require a separate deliverable SemVer target or one release-sized story per cycle. | Borrow independently testable value slices and proportional templates; keep the project deliverable version distinct from the framework version. |
| Challenge a fragile novice recommendation | Assessment compares options, appetite, rabbit holes, risks, and counterevidence. The existing-project guide asks plans to reuse existing architecture. This is strong upstream guidance, but the trial did not establish that a model will reject a browser side-load in practice. | Test actual pushback with the same prompt in both systems before claiming success. |
| Organization onboarding and resumption | Spec Kit supports Claude, Codex, Gemini, bundles, catalogs, and update manifests. The tested path required a Python 3.11+ CLI install, project initialization, and opting into assessment. Its first-party assessment workflow has an approve/reject verdict gate, but the default artifacts are feature/assessment records rather than Agent Builder's explicit project phase and active/archived status. Agent Builder v0.2.1 has a confirmed organization-installed novice result. | Compare setup, migration, and lifecycle behavior in v0.4.0 planning. The author explicitly removed Windows-specific compatibility as a decision gate. |
| Organization-wide reuse and maintenance | [Bundles and catalogs](https://github.github.io/spec-kit/reference/bundles.html) provide versioned, composable, organization-curated distribution and update paths. Agent Builder does not yet have an equivalent. | This is a real Spec Kit advantage to learn from; organization-level configuration remains outside the confirmed v0.3.0 scope. |

## The three options

1. **Ignore Spec Kit.** Lowest immediate change, but knowingly miss tested patterns for
   counterevidence, stopping, thin MVP slices, Lean templates, and curated reuse. Not
   recommended.
2. **Incorporate the relevant parts into Agent Builder.** The author's confirmed release
   sequence makes this two steps: borrow useful research and MVP-slicing ideas in lean v0.3.0
   without a Spec Kit dependency or source copy; in a separately defined v0.4.0, integrate
   a maintained Spec Kit dependency and test targeted substitutions. The
   [component map](spec-kit-component-map.md) identifies the seams and upgrade tradeoffs.
3. **Stop Agent Builder and move to Spec Kit.** Plausible, not dismissed. Spec Kit overlaps
   strongly and has a larger maintained ecosystem. Do this only if a paired real-user pilot
   shows that a configured Spec Kit bundle/preset reaches the DepMap adopt-and-close case and
   neutral-project case with at least as clear a novice experience, while preserving the
   necessary approval, status, version, and upgrade behavior at lower maintenance cost.

## Decision limit

This was a CLI smoke test plus inspection of the tagged workflow, not a head-to-head novice
behavior test. It supports the confirmed release sequence but does not establish that Agent
Builder is superior. The repository already records two usable pilot prompts:
"i want to make a thing that can quickly retrieve depmap data and deploy it org wide with a
few consistent ways of presenting the output" (`docs/v0-2-skill-test.md`, Run 3), and
"help me build a little service that watches our S3 bucket for new FASTQs and kicks off the
pipeline" (`evals/triggers-help-me-build/prompt.md`).

For v0.4.0 planning, first test whether a thin Agent Builder-to-Spec Kit assessment seam
gives the required adopt-and-archive result without adding unacceptable setup or artifact
overhead. If broader replacement remains plausible, use a paired novice test with fresh
folders, the same Claude host and public-search access, and a Two River Bio member who has
not read either tool's instructions. Configure Spec Kit with the first-party assessment
bundle and Lean preset; use the accepted Agent Builder installation for the other arm.
Check whether each independently finds and verifies
a suitable DepMap solution, recommends adoption and a no-build close, scopes the S3 watcher
to one usable version, states its next action plainly, and avoids unjustified complexity.
Record elapsed time, setup steps, user confusion, and artifacts. The author's earlier
[K-Dense DepMap adoption](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/depmap)
is an illustrative historical case, not an Agent Builder dependency, integration target, or
canned expected answer. Any real comparison must assess candidate fit independently.
Keep Build closed until the author approves a release plan and phase transition.
