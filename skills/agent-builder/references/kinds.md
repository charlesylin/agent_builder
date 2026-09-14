# Kinds

The seeder combines `templates/base/` (every project) with `templates/kinds/<kind>/`. A kind
file with the same path as a base file replaces it.

## Telling them apart

| Ask | agent | skill |
| --- | --- | --- |
| Does it call an AI model and act on the answer? | yes | no — a model runs *it* |
| Who invokes it? | a schedule, an event, or a person; may run unattended | a person, through Claude or Codex |
| What is the deliverable? | a running service, eventually a container | a `SKILL.md` folder the host loads |
| Where does repeatable logic live? | `src/<package>/` with tests | `scripts/` with tests |

Not yet supported: `mcp` (a server exposing tools or data to models) and `project` (software
with phases and a decision ledger but no AI). Say so plainly and offer the nearest kind. They
will be added when a real project in the organization needs one.

## What every kind gets (base)

`governance/` (operating agreement, project state, decisions), `planning/` (README, open
questions), `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`,
`.env.example`, `.agent-builder.json` (kind, owner, template version, adapters), a CI workflow,
Dependabot config, and one instruction file per selected host.

## agent adds

`contracts/` with the versioned handoff JSON schema and example, `deployment/README.md`
(container policy; no Dockerfile until a runtime is chosen), `src/<package>/__init__.py`,
`tests/test_scaffold.py`, `pyproject.toml`, `.dockerignore`.

## skill adds

`SKILL.md` with `name` and `description` front matter and a procedure scaffold, `scripts/`,
`references/`, `evals/` with a first trigger scenario, `.claude-plugin/plugin.json`,
`tests/test_skill.py`, and skill-flavored README, CONTRIBUTING, CI, and project state.
