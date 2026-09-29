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

## Distribution routes to compare, not yet chosen

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
   must remain an upstream package with provenance and a tested update path, not a copied
   local fork disguised as a dependency.

No route is approved merely because the CLI smoke test succeeded. The smallest next Plan
step is to compare these routes against the actual Claude Code and Codex installation
surfaces, then define one authoritative artifact mapping and a six-case host/kind acceptance
matrix. If none can meet the approved one-install experience without net regression, return
the tradeoff to the author before requesting Build.
