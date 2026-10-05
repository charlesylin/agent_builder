# v0.4.0 Spec Kit feasibility — first Plan investigation

Checked 2026-09-29. This is evidence for a Plan decision, not an approved implementation
design or Build authorization. The exploratory upstream release was
[Spec Kit v1.0.13](https://github.com/github/spec-kit/releases/tag/v1.0.13), commit
`f1a548a39dba4e5e8600de1d2e0d3ff0c468d2a9`. The earlier v1.0.9 comparison remains
historical evidence in `planning/spec-kit-comparison.md`.

## Question and result

Can a single Agent Builder installation expose the selected Spec Kit capabilities on Claude
Code and Codex, across agent, skill, and project builds, without separate member setup,
duplicate governance, or a v0.3.0 regression?

**Not yet proven.** Spec Kit's own Claude Code and Codex integrations initialized and
coexisted with Agent Builder's three scaffolds in isolated tests. Agent Builder's current
distribution does not bring along the `specify-cli` Python package, and a direct use of
Spec Kit commands would create a second set of assessment, constitution, requirements,
and plan files. Those are Plan design problems, not reasons to change the approved outcome
silently.

## Upstream and local evidence

- [Official installation guidance](https://github.github.io/spec-kit/installation.html)
  distributes `specify-cli` as a Python package or source install, requires Python 3.11+,
  and calls for `specify init` in each project. The tagged package declares Python 3.11+
  and eight direct dependencies in `pyproject.toml`. Agent Builder v0.3.0 is a skill folder,
  not an installed Python package; its scripts support Python 3.9+ and its project
  `pyproject.toml` does not install runtime dependencies.
- [Spec Kit integrations](https://github.github.io/spec-kit/reference/integrations.html)
  install Claude Code skills under `.claude/skills` and Codex skills under
  `.agents/skills`. Both integrations are declared safe to coexist, but optional extension
  skills register to the active integration. The active integration can be changed with
  `specify integration use`.
- [Claude Code's plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies)
  refer to other plugins, not Python packages. The checked Spec Kit v1.0.13 source contains
  no Claude plugin manifest. Therefore adding `specify-cli` to Agent Builder's Claude
  plugin `dependencies` is not a working installation route.
- [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins) can ship
  skills, scripts, and connections, but does not automatically install a local Python
  package as an installation lifecycle step. Agent Builder's documented Codex path today
  is a skill-folder copy or symlink, not a dependency-installing package.

An isolated macOS arm64 / Python 3.14.0 test used a temporary virtual environment, not a
global installation. `specify version` reported 1.0.13. With the host CLIs present, these
non-interactive operations succeeded:

```text
specify init claude-trial --integration claude --script py --extension assess --non-interactive
specify init codex-trial --integration codex --script py --extension assess --non-interactive
specify bundle install <v1.0.13 checkout>/bundles/assess/bundle.yml --offline
```

The local bundle command installed the assessment workflow in both fresh trials. A
Claude-initialized, Agent Builder-seeded `project` accepted `specify init --here --force`,
then `specify integration install codex` without changing tracked Agent Builder files.
The Codex core skills appeared immediately; its assessment skills appeared after
`specify integration use codex`. The Agent Builder scaffold checker still passed.
Separately, Agent Builder-seeded `agent` and `skill` projects accepted Codex initialization
and passed the same checker. The tested Claude-initialized project gained about 50 new
`.specify/` and `.claude/` files. These are structural smoke tests, not tests of agent
discovery, novice interaction, clean organization installation, or all six host/kind pairs.

## Fit of the selected capabilities

| Selected area | Spec Kit v1.0.13 behavior | Agent Builder boundary |
| --- | --- | --- |
| Idea assessment | The optional [assessment extension](https://github.github.io/spec-kit/reference/agentic-assessment.html) produces intake, research, problem, concept, and decision artifacts. Its verdict is `go`, `needs-clarification`, or `kill`; research seeks counterevidence. | Partial replacement is credible, but `kill` is not an explicit `adopt` record with a chosen component/version, author confirmation, and archived project status. Keep those Agent Builder obligations. |
| Specify, clarify, checklist | [SDD commands](https://github.github.io/spec-kit/reference/agentic-sdd.html) create `spec.md`, ask targeted questions, and check requirement quality. | Agent Builder already owns `planning/definition.md` and the version-sized outcome. Assign each fact one authoritative home before exposing both flows. |
| Plan, tasks, analyze | Spec Kit produces feature `plan.md` and `tasks.md`; `analyze` reads those with `spec.md` and the Spec Kit constitution. It does not analyze Agent Builder's current files directly. | Keep phase approvals and deterministic checks. Decide whether Spec Kit feature artifacts become the authoritative build detail or whether a supported adapter maps them to Agent Builder records; do not maintain two editable copies. |
| Project principles | Spec Kit initializes `.specify/memory/constitution.md`. | Agent Builder already has `governance/operating-agreement.md`; leaving both independently normative risks contradictory instructions. |

The stock initialization also exposes `implement` and `converge` skills even though they
are excluded from the approved v0.4.0 scope. The Plan must prevent these from appearing
to be Agent Builder's recommended next step.

## Distribution routes compared

1. **Organization-managed CLI prerequisite.** Administrators provision a pinned
   `specify-cli` alongside Agent Builder on both hosts. This is simple for members but is
   two deployment operations and does not make a personal Agent Builder install complete.
2. **Agent Builder-managed isolated runtime.** A small, deterministic bootstrap checks
   Python 3.11+, installs a pinned upstream package into an Agent Builder-owned location,
   verifies its version, and reports network or package failures plainly. This could meet
   the no-*manual*-setup requirement, but first-run network access, the higher Python floor,
   cache ownership, upgrades, and Codex/Claude permissions need explicit tests.
3. **Ship a pinned upstream-built artifact with the plugin.** This removes first-run network
   dependence but increases release size and cross-platform dependency packaging work. It
   must preserve upstream provenance and a tested update path, not become a hand-maintained
   local fork disguised as a dependency.

The CLI smoke test alone approved no route. The author subsequently selected the
release-time-generated dependency payload described below. The host/kind acceptance
matrix and single-source artifact mapping still need Plan evidence. If the selected route
cannot meet the approved one-install experience without net regression, return the tradeoff
to the author before requesting Build.

## Follow-up: the handoff seam (2026-10-05)

The author agreed with using the CLI *behind* Agent Builder, rather than making members run
Spec Kit as a second workflow. This is direction to continue Plan investigation, not approval
of a packaging route or permission to enter Build. The source check below used the same
v1.0.13 commit named above; the installed host CLIs on this machine reported Claude Code
2.1.271 and Codex CLI 0.159.2. Read-only invocation probes are described below.

- The tagged [`speckit.assess.research` command](https://github.com/github/spec-kit/blob/v1.0.13/extensions/assess/commands/speckit.assess.research.md)
  explicitly permits research to be the first
  assessment step. Without `intake.md`, it requires substantive idea text in the invocation;
  a slug alone is insufficient. It writes only
  `.specify/assessments/<slug>/research.md`, including prior art and counterevidence, and
  expressly does **not** render a verdict. Agent Builder can supply the already-confirmed
  problem from `planning/definition.md`, use this upstream step for research, then retain
  its own adopt/adapt/build decision and author-confirmed archive behavior. Running all five
  assessment steps by default would repeat Agent Builder's Define and decision records.
- Spec Kit renders each agent-facing step as a project skill: Claude Code under
  `.claude/skills/` and Codex under `.agents/skills/`, with names such as
  `speckit-assess-research`. [Spec Kit's integration guide](https://github.github.io/spec-kit/reference/integrations.html)
  distinguishes these in-agent steps from terminal setup. [Claude Code's skill guide](https://code.claude.com/docs/en/skills)
  documents model invocation; [official OpenAI documentation](https://developers.openai.com/plugins/concepts/skills)
  describes metadata-based loading when a request matches or the user invokes a skill. Neither
  establishes a deterministic, cross-host API by which one skill executes another. Reading
  `SKILL.md` as an ordinary file is not automatically equivalent to native invocation:
  generated Spec Kit skills use argument placeholders such as `$ARGUMENTS`.
- The narrow Plan hypothesis is for Agent Builder to remain the member-facing entry point,
  arrange the pinned upstream CLI and project skills, direct the active host to the selected
  upstream skill, and verify the expected artifact before proceeding. A behavioral trial must
  show that this actually activates the upstream skill on **both** hosts without asking the
  member to invoke it manually. If that fails, do not claim the dependency is integrated.
- Proposed artifact ownership: Agent Builder remains authoritative for problem/purpose,
  project phase and status, approvals, version target, and final build-or-adopt decision.
  Spec Kit's `research.md` is supporting evidence linked from the short Agent Builder
  solution evaluation. On a justified build, Spec Kit's `spec.md`, `plan.md`, and `tasks.md`
  can be the detailed delivery artifacts. Its constitution cannot be a second editable
  authority: `analyze` treats that file as binding, so Plan must test a generated view of
  Agent Builder's operating agreement or another single-source mapping.

This narrows the behavioral test but not the distribution problem. Spec Kit v1.0.13 still
requires Python 3.11+ for its CLI, while Agent Builder's shipped scripts support 3.9+.
The plugin/skill installation paths still have no demonstrated way to install that Python
package automatically. A release-time vendored artifact would reduce member setup but must
be evaluated against the author's preference for a maintained dependency rather than a
copied fork. It is not automatically Python-free: the tested `--script py` output has
project scripts using Python 3.10+ syntax, and `speckit-plan` calls one of those scripts.
A managed first-use installation or unified organization deployment could keep
the CLI upstream-pinned, but neither has yet passed a clean one-install trial.

A fresh disposable repeat on 2026-10-05 installed the tagged source into an isolated
Python 3.14 virtual environment, seeded an Agent Builder `project` with both host adapters,
and ran `specify init --here --force --non-interactive --integration claude --script py
--extension assess`, followed by `specify integration install codex --script py` and
`specify integration use codex`. Both host directories then contained
`speckit-assess-research/SKILL.md`; Agent Builder's scaffold check still passed. This is
an installation/structure result, not proof of a live handoff. Initialization also exposed
`speckit-implement` and `speckit-converge` in both host directories, and its next-step text
advertised them. If v0.4.0 must not present these excluded workflows, Plan needs a supported
way to suppress them or an explicit author decision about their incidental presence.

Read-only Codex CLI 0.159.2 probes in that disposable project found a sharper boundary:
an initial plain-language request to use `speckit-assess-research` led Codex to read the
`SKILL.md` as a file; a direct user `$speckit-assess-research` invocation loaded it natively
as a skill message. Adding a test-only Agent Builder-style instruction to the project
`AGENTS.md` to load that upstream skill, then asking without the skill name, again produced
an ordinary file read rather than observed native skill activation. These are single probes,
not reliability measurements, and none ran the research step or wrote an artifact. They
rule out treating skill-to-skill native invocation on Codex as already solved. A deliberate
file-reading adapter could still use the pinned upstream instructions, but it would need to
bind `$ARGUMENTS` explicitly and pass behavior tests; it is not the same as native skill
invocation. A Claude Code 2.1.271 live probe could not start because that CLI was not logged
in on this machine. Its documented model-invocation support remains a claim to verify in an
authenticated session, not an observed pass.

One further disposable Codex probe read the upstream research `SKILL.md` as a file, bound
`$ARGUMENTS` to a supplied CSV-date-formatting idea, and followed its instructions without
native skill activation. It produced only the expected `research.md`, with prior-art gaps,
counterevidence hypotheses, explicit `ASSUMPTION` labels, and low overall confidence.
Web access was deliberately excluded, so this proves that file-based instruction reuse can
produce the expected *shape* on Codex, not that it finds real public solutions or improves
the adoption judgment. The upstream research step also does not itself cover every Agent
Builder gate field (utilization, maintenance, tests, security history, license, setup burden)
and its URL trust policy prompts or skips many non-allowlisted sites. Agent Builder must keep
those evidence obligations rather than treating the upstream artifact as a complete gate.

## Distribution decision and remaining tests

The isolated `specify-cli` installation needed network access to resolve its Python
dependencies, but `specify init` subsequently ran from its bundled assets in the network-
restricted sandbox. A stock init is too broad for the approved v0.4.0 experience: it
installs and advertises `implement` and `converge`, and leaves a placeholder constitution.
No selective-core-skill option appeared in v1.0.13's `init` or `integration install` help.

The author confirmed a **release-time generated dependency payload** on 2026-10-05,
over a separate member-machine CLI install. In this direction, Agent Builder's release
process would pin and run the unmodified upstream CLI, preserve its provenance and license,
and package only the upstream-generated skills and infrastructure needed for the selected
v0.4.0 steps.
Agent Builder's seeder would copy that immutable payload and create a single-source
constitution view. Members would install Agent Builder once and need no Spec Kit CLI or
network download at first use. This is build-time vendoring of generated dependency output,
not a runtime `specify-cli` installation or automatic upstream updates. To honor the
preference for a maintained dependency over lifted code, the release process must keep
the upstream pin, provenance, license, and refresh test visible. It also needs a
script-variant and upgrade test; the tested Python script variant would raise the
project-script floor above Agent Builder's 3.9 baseline.

The competing **runtime CLI** route preserves upstream's own project initialization and
update machinery, but the current Claude plugin and Codex skill installation surfaces do
not install Python 3.11+ or `specify-cli` automatically. A first-use bootstrap would require
those prerequisites and possibly network or an offline wheel bundle; an organization-wide
installer would change the installation path. Neither is yet a proven one-install result.
The selected release-time route remains a Plan direction, not a proven packaging
implementation or Build authorization. Next, test a reproducible filtered payload,
Python-script compatibility, single-source constitution, and the selected handoffs across
Claude Code and Codex and all three build kinds. Do not claim a pass solely from the
successful local virtual-environment test.
