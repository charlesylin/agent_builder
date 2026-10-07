# v0.4.1 Build verification

Checkpoint: 2026-10-07. The approved patch is implemented locally at
`ea4581d769e0da4910ade491633330ad6242731a`. Build remains the current
phase; Review, acceptance, push, and a v0.4.1 tag have not been authorized.

## What changed

- The Agent Builder repository now marks its pinned Spec Kit bundle `-text`
  in `.gitattributes`, so Git does not rewrite any manifest-hashed file at
  checkout.
- New Claude Code and Codex projects receive narrow `.gitattributes` rules
  for their six pinned Bash helpers, four templates, and MIT notice. A
  Gemini-only project receives no new Spec Kit files or attributes.
- The plugin, Python metadata, seeder, and changelog identify the candidate
  as v0.4.1. The pinned Spec Kit v1.1.0 payload and its hashes are unchanged;
  existing generated projects are not modified.
- Regression tests commit and reclone the bundle and a generated project with
  `core.autocrlf=true`, then verify the hashes. A deliberate byte change still
  produces `spec-kit-asset-drift`.

## Checks performed

- A fresh `git -c core.autocrlf=true clone` of the committed Agent Builder
  repository passed `python3 scripts/refresh_spec_kit.py --check` and all 77
  unit tests. Representative pinned files reported `i/lf w/lf attr/-text`.
- `python3 -m unittest discover -s tests -v`: 77 passed on Python 3.14.0.
  `/usr/bin/python3 -m unittest discover -s tests -q`: 77 passed on Python 3.9.6.
- `python3 scripts/render.py --check`,
  `python3 scripts/refresh_spec_kit.py --check`,
  `python3 -m compileall -q scripts skills tests`, and `git diff --check`
  passed.
- Ruff 0.16.6, installed temporarily outside the repository, passed
  `ruff check .` and `ruff format --check .`.
- `python3 skills/agent-builder/scripts/check.py . --leaving build` reported
  nothing unresolved. The generic `check.py .` scaffold check remains
  inapplicable to this legacy source repository because it has no generated
  `.agent-builder.json` and intentionally contains template tokens. The
  generated-project checker passed after the simulated Windows checkout.

## Remaining verification

The real GitHub Windows job has not run on this patch because no push was
requested. Local Git simulation reproduces the original failure without the
attributes and passes with them; it is not a substitute for a green Windows
CI run. Review should confirm that job after an authorized push. Do not move
the existing v0.4.0 tag.
