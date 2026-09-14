# Changing Agent Builder

The rule that makes everything else work: **a principle's text lives in one file**, under
`principles/`. Everything that states a principle — root `AGENTS.md`, this repository's
operating agreement, the template operating agreement, the three adapter templates,
`skills/agent-builder/SKILL.md`, and its `references/operating-agreement.md` — is generated
from stencils in `scripts/stencils/`. A test fails if you edit a generated copy directly.

## Change a principle

1. Edit the one file in `principles/` (front matter `id` and `title`, full text, then a
   `## Short form` section).
2. `python3 scripts/render.py` — regenerates every copy.
3. `python3 -m unittest discover -s tests` — the drift test now passes again.
4. Commit the source and the generated files together.

Add a principle by adding a file and referencing it from at least one stencil as
`{{principle:<id>}}`, `{{principle:<id>|short}}`, or `{{principle:<id>|title}}`; the renderer
refuses unused principles and unknown ids.

## Change the skill's procedure

`scripts/stencils/skills/agent-builder/SKILL.md` is the source; the principles section in it is
generated, the rest is authored. Edit, render, test. The `description` line in its front matter
is the whole trigger surface: change it only with the evals (`evals/README.md`) run before and
after, and keep the version that measures better.

## Change what gets seeded

Templates live in `skills/agent-builder/templates/`: `base/` for every kind, `kinds/<kind>/`
for one kind (a same-path file there replaces the base one), `adapters/<host>/` per coding
host. Seed-time placeholders are `{{UPPER_CASE}}`; the list is `_context()` in
`scripts/seed.py`. Add a test in `tests/test_agent_builder.py` for anything a kind must or
must not contain — F-008 was a skill project inheriting an agent default.

Adding a kind: create `kinds/<name>/`, add it to `SUPPORTED_KINDS` in `seed.py` and
`_KIND_REQUIRED_FILES` in `check.py`, add its row to `references/kinds.md` and the §1 table in
the `SKILL.md` stencil, and seed one real project with it before shipping (AB-D023).

## Release

1. Update `CHANGELOG.md`: move `[Unreleased]` into a dated version section.
2. Set the same version in `.claude-plugin/plugin.json`, `pyproject.toml`, and
   `TEMPLATE_VERSION` in `skills/agent-builder/scripts/seed.py` (a test keeps the first and
   last equal).
3. Run the full gate: `scripts/render.py --check`, tests under 3.9 and a current Python,
   `ruff check .`, `ruff format --check .`, and the evals.
4. Commit, tag `vX.Y.Z`, push with `--follow-tags`.

Installed copies update only when `plugin.json` `version` changes. Seeded projects never
update themselves; `check.py --since` shows their owners what changed.

## This repository's own governance

Agent Builder is developed under its own phases. `governance/project-state.yaml` records the
phase; `governance/decisions.yaml` the decisions; `docs/RESUME.md` how to pick it up. Follow
them — the skill is only as credible as the repository that ships it.
