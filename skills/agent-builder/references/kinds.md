# Kinds

The seeder combines `templates/base/` (every project) with `templates/kinds/<kind>/`. A kind
file with the same path as a base file replaces it.

## Telling them apart

| Ask | agent | skill | project |
| --- | --- | --- | --- |
| Does it call an AI model and act on the answer? | yes | no — a model runs *it* | not assumed |
| Who invokes it? | a schedule, an event, or a person; may run unattended | a person, through Claude or Codex | depends on what is built |
| What is the deliverable? | a running service, eventually a container | a `SKILL.md` folder the host loads | defined by the project author |
| Where does repeatable logic live? | `src/<package>/` with tests | `scripts/` with tests | chosen after Define and Plan |

Not yet supported: `mcp` (a server exposing tools or data to models). A neutral `project`
does not assume an agent runtime, skill manifest, application language, or deployment model.

## What every kind gets (base)

`governance/` (operating agreement, project state, decisions), `planning/` (README, open
questions), `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `.gitignore`,
`.env.example`, `.agent-builder.json` (kind, owner, template version, adapters), a CI workflow,
Dependabot config, and one instruction file per selected host.
The base planning layer also seeds a short build-or-adopt evidence record for the Plan gate.

## agent adds

`contracts/` with the versioned handoff JSON schema and example, `deployment/README.md`
(container policy; no Dockerfile until a runtime is chosen), `src/<package>/__init__.py`,
`tests/test_scaffold.py`, `pyproject.toml`, `.dockerignore`.

## skill adds

`SKILL.md` with `name` and `description` front matter and a procedure scaffold, `scripts/`,
`references/`, `evals/` with a trigger case and a negative case in `claude plugin eval`
format, `.claude-plugin/plugin.json`,
`tests/test_skill.py`, and skill-flavored README, CONTRIBUTING, CI, and project state.

## project adds

A neutral project state, README, planning questions, and scaffold tests. It overrides the
common CI to check only its current scaffold and keeps Dependabot limited to GitHub Actions.
It does not seed agent contracts, an agent runtime, deployment policy, skill manifest, or
application code.
