# Agent Builder

A skill that helps people in an organization build agents, skills, and ordinary projects:
clarify the problem, check whether an existing solution is enough, then build one usable
version only when needed. It keeps phase and decision records for agents while explaining
status and consequential choices to people in plain language.

It is three things in one folder, `skills/agent-builder/`:

- **`SKILL.md`** — the instructions Claude Code or Codex follows. The judgment lives here.
- **`scripts/seed.py`** and **`scripts/check.py`** — create a project; validate one. Standard
  library only, Python 3.9+.
- **`templates/`** — what a new project gets: `base/` for every kind, kind-specific files for
  `agent`, `skill`, or neutral `project`, and one adapter file per coding host.

The principles behind all of it live once, in `principles/`, and are rendered into every place
they appear by `scripts/render.py`. A test fails if a copy drifts.

## What a colleague experiences

In an empty folder, with the skill installed: *"I want to build something that…"*. The skill
first asks about the problem, how it is solved today, its value, and its users. It then settles
the kind and purpose, proposes logistical defaults, and seeds a Git repository in **Define**.
It asks before creating a remote.

In **Plan**, it evaluates existing public solutions and any codebase the author provides.
If one meets the need, it recommends adoption and can archive the project without custom
code. Otherwise it plans one usable version with explicit exclusions and a small,
evidence-backed technical approach.

Coming back later, *"what's the status here?"* gets a briefing from the repository's own
records: purpose, phase and how long it has been there, what exists and what the phase still
owes, the important decisions in plain words, and a proposed next step — nothing done unasked.

## How it gets invoked

By name — `/agent-builder:agent-builder` in Claude Code, `$agent-builder` in Codex — or by its
description matching what someone typed. In Claude Code the plugin also ships a
`UserPromptSubmit` hook: when a prompt looks like the start of new work and the folder is not
already a seeded project, it asks Claude to offer the skill once. Declining mutes the offer for
that session. The hook is silent otherwise and never blocks a prompt; `docs/INSTALL.md`
describes exactly what it does.

## Install

See [`docs/INSTALL.md`](docs/INSTALL.md). To try it now:

```sh
claude --plugin-dir /path/to/agent_builder    # Claude Code, this session only
ln -s /path/to/agent_builder/skills/agent-builder ~/.agents/skills/agent-builder   # Codex
```

## Use the scripts directly

```sh
python3 skills/agent-builder/scripts/seed.py ../my-agent \
  --name "My Agent" --purpose "The single outcome this owns." \
  --kind agent --owner "Your Name" --adapter claude --adapter codex

python3 skills/agent-builder/scripts/check.py ../my-agent          # validate
python3 skills/agent-builder/scripts/check.py ../my-agent --since  # what changed since seeding
```

`--kind` is `agent`, `skill`, or `project`. The seeder refuses an existing path and never rewrites a seeded
project; `--since` shows a project's owner what they would be opting into.

## Development

```sh
python3 scripts/render.py --check           # generated files match principles/
python3 -m unittest discover -s tests -v    # test suite, Python 3.9+
python3 -m compileall -q scripts skills tests
python3 -m pip install "ruff==0.16.6" && ruff check . && ruff format --check .
claude plugin eval . --scaffold --judge-model sonnet   # does the skill trigger and behave? see evals/
```

How to change principles, the skill, templates, or cut a release:
[`docs/AUTHORING.md`](docs/AUTHORING.md).

## Status

**v0.3.0 accepted; in use.** The author reported all three v0.3 real-use Review
scenarios passed and accepted the release on 2026-09-24. See the
[v0.3 acceptance record](docs/v0-3-acceptance.md). Review remains current while the release
is used; v0.4.0 Define has not yet opened. Its candidate direction is a maintained Spec Kit
dependency with targeted replacements, but its exact scope is not yet defined. v0.2.1 and
v0.1.0 remain [previous accepted releases](docs/RESUME.md).

This repository is developed under its own phases; see
[`governance/`](governance/) and [`docs/RESUME.md`](docs/RESUME.md).

## License

[MIT](LICENSE).
