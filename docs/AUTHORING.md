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

## Change the offer hook

`hooks/agent_builder_offer.py` decides when Claude is asked to offer the skill.
`looks_like_new_work` is a pure function over the prompt text, so tuning it is cheap and
offline: add the phrasing to `EVAL_PROMPTS` or `NOT_NEW_WORK` in `tests/test_hook.py`, adjust
`POSITIVE` or `NEGATIVE`, and run the tests. `NEGATIVE` wins over `POSITIVE` by design — work
on something that already exists should never be interrupted.

Testing it is not like testing the skill: `--plugin-dir` does not load hooks, only an
installed plugin's hooks run. Unit tests cover the matcher offline; for a live check, install
the plugin from a local path, verify with `/hooks`, and use `claude --debug` to see the hook's
exit code and output. Re-installing or bumping the version is required to pick up an edit.

Keep the hook silent by default and always exiting 0. It runs on every prompt; a hook that is
noisy, slow, or capable of failing loudly is worse than no hook.

## Change what gets seeded

Templates live in `skills/agent-builder/templates/`: `base/` for every kind, `kinds/<kind>/`
for one kind (a same-path file there replaces the base one), `adapters/<host>/` per coding
host. Seed-time placeholders are `{{UPPER_CASE}}`; the list is `_context()` in
`scripts/seed.py`. Add a test in `tests/test_agent_builder.py` for anything a kind must or
must not contain — F-008 was a skill project inheriting an agent default.

Adding a lifecycle status: extend `_PROJECT_STATUSES` in `check.py`, the comment in the
project-state templates, and the table in `SKILL.md` §6. Keep it orthogonal to the phases.

Adding a kind: create `kinds/<name>/`, add it to `SUPPORTED_KINDS` in `seed.py` and
`_KIND_REQUIRED_FILES` in `check.py`, add its row to `references/kinds.md` and the §1 table in
the `SKILL.md` stencil, and seed one real project with it before shipping (AB-D023).

## Refresh the Spec Kit bundle

The v0.4 bundle is generated from the pinned upstream commit, not hand-edited. The
approved version, commit, host steps, and project asset allowlist live in
`scripts/refresh_spec_kit.py`. The source checkout and a Python 3.11+ environment with
Spec Kit's release dependencies are needed only when refreshing. For example:

```sh
python3 scripts/refresh_spec_kit.py --source /path/to/pinned/spec-kit \
  --python /path/to/isolated/python
python3 scripts/refresh_spec_kit.py --check
```

The first command verifies the checkout commit, runs Spec Kit's unmodified CLI for
Claude Code and Codex, copies only the approved outputs and MIT notice, and writes
their hashes to `vendor/spec-kit/manifest.json`. Upstream instruction bytes are unchanged,
but the bundled filename is `instructions.md` rather than `SKILL.md` so they remain internal
references instead of separately discoverable skills. The second command is offline and
must pass in CI. A pin change requires an upstream and license review, regeneration,
inspection of the asset diff, and a corresponding test update. Never modify a seeded
project's `.specify/` files as a side effect of a bundle refresh.

## Release

1. Update `CHANGELOG.md`: move `[Unreleased]` into a dated version section.
2. Set the same version in `.claude-plugin/plugin.json`, `pyproject.toml`, and
   `TEMPLATE_VERSION` in `skills/agent-builder/scripts/seed.py` (a test keeps the first and
   last equal).
3. Run the full gate: `scripts/render.py --check`, `scripts/refresh_spec_kit.py --check`,
   tests under 3.9 and a current Python, `ruff check .`, `ruff format --check .`, and
   the evals. Exercise both hosts' member-facing flow for a changed integration.
4. Commit, tag `vX.Y.Z`, push with `--follow-tags`.

Installed copies update only when `plugin.json` `version` changes. Seeded projects never
update themselves; `check.py --since` shows their owners what changed.

## This repository's own governance

Agent Builder is developed under its own phases. `governance/project-state.yaml` records the
phase; `governance/decisions.yaml` the decisions; `docs/RESUME.md` how to pick it up. Follow
them — the skill is only as credible as the repository that ships it.
