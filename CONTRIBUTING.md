# Contributing

Start by reading `AGENTS.md`, `governance/operating-agreement.md`, and
`governance/project-state.yaml`.

Changes should be small, justified by a real generated-agent need, and validated with:

```sh
python3 -m unittest discover -s tests -v
python3 -m compileall -q src scripts tests
ruff check .
ruff format --check .
```

Do not add a framework, service, or dependency until existing open-source options have
been assessed and the choice has been approved. Never include real credentials in issues,
fixtures, examples, commits, or logs.
