# Agent Builder

Agent Builder creates governance-first project scaffolds for lean, predictable agents.
It keeps model reasoning focused on orchestration and decisions while reserving repeatable
work for deterministic, testable Python.

Version 0.1 intentionally provides the project contract and scaffold only. It does not
select an agent runtime, model provider, API framework, or MCP implementation.

## What it creates

- an explicit Define → Plan → Build → Review workflow;
- human-readable governance plus machine-readable project state and decisions;
- selectable Codex, Claude Code, and Gemini CLI instruction adapters;
- a compact JSON Schema for agent-to-agent handoffs;
- security rules for credentials, tools, data, and logs;
- Python-first source and test directories without a runtime dependency; and
- container and compatibility policies ready for a later runtime profile.

## Quick start

Agent Builder has no runtime dependencies and requires Python 3.11 or newer.

```sh
python3 scripts/new_agent.py ../my-agent \
  --name "My Agent" \
  --purpose "Describe the single outcome this agent owns." \
  --adapter codex \
  --adapter gemini
```

Codex is selected when no `--adapter` option is supplied. Repeat `--adapter` to enable
more than one coding-agent host.

Validate a generated project with:

```sh
python3 scripts/validate_project.py ../my-agent
```

For the installed CLI equivalent:

```sh
agent-builder init ../my-agent --name "My Agent" --purpose "..."
agent-builder validate ../my-agent
```

The initializer refuses to write to an existing path. This makes generation predictable
and prevents accidental overwrites.

## Development

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q src scripts tests
```

Optional development tools are isolated in the `dev` extra:

```sh
python3 -m pip install -e '.[dev]'
ruff check .
ruff format --check .
prek run --all-files
```

See [the architecture](docs/architecture.md),
[the operating agreement](governance/operating-agreement.md),
[the open-source evaluation](docs/open-source-evaluation.md), and
[the validation record](docs/validation.md) for the design rationale and evidence.

## Status

Version 0.1 is in the Review phase. Mechanical validation has passed; user acceptance will
come from building the first real agent with the scaffold. Generated projects record the
Agent Builder version they came from; later releases never silently rewrite them.

## License

Agent Builder is available under the [MIT License](LICENSE).
