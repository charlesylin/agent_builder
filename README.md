# Agent Builder

A skill that helps people in an organization build agents, skills, and projects the same
way: a short Define conversation first, a repository seeded from templates by a script, work
kept inside a recorded phase, decisions written down with IDs, and a closeout in a fixed shape.

It is three things in one folder, `skills/agent-builder/`:

- **`SKILL.md`** — the instructions Claude Code or Codex follows. The judgment lives here.
- **`scripts/seed.py`** and **`scripts/check.py`** — create a project; validate one. Standard
  library only, Python 3.9+.
- **`templates/`** — what a new project gets: `base/` for every kind, `kinds/agent/` and
  `kinds/skill/`, one adapter file per coding host.

The principles behind all of it live once, in `principles/`, and are rendered into every place
they appear by `scripts/render.py`. A test fails if a copy drifts.

## What a colleague experiences

In an empty folder, with the skill installed: *"I want to build something that…"*. The skill
asks what kind of thing it is, settles a one-sentence purpose and reads it back, proposes
name, owner, hosts, and destination as defaults, then runs the seeder. Twenty-odd files, a git
repository on `main` with its first commit, phase **Define**, purpose and decisions already in
the ledger. It asks before creating a remote.

Coming back later, *"what's the status here?"* gets a briefing from the repository's own
records: purpose, phase and how long it has been there, what exists and what the phase still
owes, every decision with its ID, a proposed next step — and nothing done unasked.

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

`--kind` is `agent` or `skill`. The seeder refuses an existing path and never rewrites a seeded
project; `--since` shows a project's owner what they would be opting into.

## Development

```sh
python3 scripts/render.py --check           # generated files match principles/
python3 -m unittest discover -s tests -v    # 47 tests, Python 3.9+
python3 -m compileall -q scripts skills tests
python3 -m pip install "ruff==0.16.6" && ruff check . && ruff format --check .
claude plugin eval . --scaffold --judge-model sonnet   # does the skill trigger and behave? see evals/
```

How to change principles, the skill, templates, or cut a release:
[`docs/AUTHORING.md`](docs/AUTHORING.md).

## Status

**In Review.** v0.2.0 shipped 2026-09-14; the first colleague's feedback is in
[`docs/v0-2-review-feedback.md`](docs/v0-2-review-feedback.md) and is incorporated in **v0.2.1**
(see [`CHANGELOG.md`](CHANGELOG.md)). The org opt-in install is the acceptance test.
v0.1 (governance and scaffolding only) was accepted on 2026-09-13 and is tagged `v0.1.0`. The v0.2 vision is in
[`docs/v0-2-define.md`](docs/v0-2-define.md), the plan in
[`docs/v0-2-plan.md`](docs/v0-2-plan.md), and the evidence from three rounds of hands-on testing
in [`docs/v0-2-skill-test.md`](docs/v0-2-skill-test.md).

This repository is developed under its own phases; see
[`governance/`](governance/) and [`docs/RESUME.md`](docs/RESUME.md).

## License

[MIT](LICENSE).
