# Changelog

All notable changes to Agent Builder are documented here.

## [Unreleased]

### Added

- `check.py --since [VERSION]` prints the Agent Builder changelog sections newer than the
  project's pinned `template_version` (or a given version). Deliberately that simple: the
  changelog is the upgrade guide, and Agent Builder never rewrites a seeded project
  (AB-D012, AB-D030). `.agent-builder.json` now records `source_commit`, the builder commit
  the templates came from, or `null` when seeded from a copied skill folder.
- `skills/agent-builder/` — Agent Builder as a skill (AB-D019, AB-D026). `SKILL.md` carries the
  authored procedure (orient, Define conversation, seed, resume, phase rules, decisions,
  closeout) and the generated short form of every principle. `scripts/seed.py` and
  `scripts/check.py` are self-contained, standard-library files; the seeder gains `--owner`,
  makes the first commit on `main`, and soft-fails when git or an identity is missing.
  `templates/` lives inside the skill folder so a copied folder is complete.
  `references/` holds the full operating agreement (generated), a kinds guide, and the
  closeout template. Root `.claude-plugin/plugin.json` and `marketplace.json` make this
  repository its own plugin marketplace (AB-D027).
- `skill` kind (AB-D023): `init --kind skill` seeds a project whose `SKILL.md` carries `name`
  and `description` front matter, plus `scripts/`, `references/`, `evals/` with a first
  scenario, a `.claude-plugin/plugin.json` manifest, its own tests, and skill-specific README,
  CONTRIBUTING, CI, and project state via kind overrides. `.agent-builder.json` and
  `project-state.yaml` now record `kind`. The validator reads the kind and requires the right
  files for it; manifests without a kind (v0.1 projects) validate as agents unchanged.
- `principles/`: one file per principle, the single source for every copy of the operating
  principles (AB-D020). `scripts/render.py` fills `{{principle:<id>}}` tokens in
  `scripts/stencils/` to produce root `AGENTS.md`, this repository's operating agreement, the
  template operating agreement, and the three coding-agent adapter templates. A test and a CI
  step fail when a generated file is edited directly. Nokkvi's law now exists in one file
  instead of six; the root and template operating agreements no longer differ.
- CI `lint` job running pinned Ruff check and format.

### Removed

- The `agent_builder` Python package, `scripts/new_agent.py`, `scripts/validate_project.py`,
  the `agent-builder` console script, and the wheel build. Nothing is installed with pip;
  the skill folder is the product. `pyproject.toml` keeps metadata and Ruff config only.

### Changed

- Seeded default decisions now match the kind: skill projects no longer inherit "deploy the
  eventual agent as an OCI container" (F-008). `SKILL.md` requires the purpose sentence to be
  read back in full, never offered as a menu.
- Every summarized principle in `SKILL.md`, the adapters, and root `AGENTS.md` is now prefixed
  with its name, so a session can answer "what is Nokkvi's law?" without opening the full
  agreement (F-005).
- Seeded adapter files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay substantive and now open
  by telling the host to invoke the `agent-builder` skill when it is available, and to answer
  a status question with a briefing rather than a summary. The skill's `description` covers
  returning to a project ("what's the status here", "where did we leave off", "catch me up")
  as well as starting one; its resume step specifies the briefing; its Define step asks kind
  and purpose one at a time and batches logistics with defaults. All from the 2026-09-14 skill
  test (F-003, F-004, AB-D030).
- Templates moved out of the Python package to `templates/` at the repository root and split
  into `base/` (every project), `kinds/agent/` (contracts, deployment policy, Python package
  skeleton, pyproject, `.dockerignore`), and `adapters/<host>/`. A kind layer may override a
  base file; adapters may not collide with anything. `init --kind` is wired with `agent` as the
  only kind so far. Generated output for `agent` is byte-identical to before the move. The
  wheel no longer carries templates; the scaffolder must run from a checkout, which is the only
  supported way to run it until the skill ships in B5.
- Python floor lowered from 3.11 to 3.9 for the builder's own scripts (AB-D025). Entry points
  now fail with a one-sentence message and exit code 2 on an older interpreter instead of a
  stdlib traceback (closes finding F-002). CI runs on Python 3.9 and 3.12 on Ubuntu and 3.12 on
  Windows. Generated projects still declare `requires-python >= 3.11` for their own future code;
  that default is theirs to change.

## [0.1.0] - 2026-09-13

Governance and project scaffolding only. No agent runtime, model client, MCP server, custom
API, Dockerfile, or Compose service is included. Accepted by the project author on 2026-09-13
under AB-D017; see [the acceptance record](docs/v0-1-acceptance.md).

### Added

- Governance-first project initializer.
- Selectable Codex, Claude Code, and Gemini CLI adapters.
- Compact machine-handoff contract and project validator.
- Container, compatibility, and secret-handling policies.
- Nokkvi's law: a silent per-turn encouragement cue in builder instructions and generated
  Codex, Claude Code, and Gemini CLI adapters. Performance impact remains unmeasured.
- Practical persistence guidance: try a concrete alternative when difficulty causes premature
  stopping, while respecting blockers, permissions, phase gates, stop requests, and budgets.
- Repository restart guide and compact handoff for resuming across accounts and hosts.
- Sean's Windows test packet and proposed onboarding/existing-project adoption review notes.
