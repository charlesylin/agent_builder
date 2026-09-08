"""Command-line interface for Agent Builder."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from agent_builder.models import SUPPORTED_ADAPTERS, ProjectSpec
from agent_builder.scaffold import ScaffoldError, create_project
from agent_builder.validation import validate_project


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-builder",
        description="Create and validate governance-first agent projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="create a new project in a non-existing path")
    init.add_argument("target", type=Path)
    init.add_argument("--name", required=True, help="human-readable project name")
    init.add_argument("--purpose", required=True, help="one-sentence outcome owned by the agent")
    init.add_argument(
        "--adapter",
        action="append",
        choices=SUPPORTED_ADAPTERS,
        help="coding-agent host; repeat to select more than one (default: codex)",
    )

    validate = subparsers.add_parser("validate", help="validate an existing generated project")
    validate.add_argument("target", type=Path)
    return parser


def _run_init(arguments: argparse.Namespace) -> int:
    try:
        spec = ProjectSpec.create(
            name=arguments.name,
            purpose=arguments.purpose,
            adapters=arguments.adapter,
        )
        files = create_project(arguments.target, spec)
    except (OSError, ValueError, ScaffoldError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    target = arguments.target.expanduser().resolve()
    print(f"Created {spec.name} at {target}")
    print(f"Adapters: {', '.join(spec.adapters)}")
    print(f"Files: {len(files)}")
    print(f"Next: open {target} and begin the Define phase")
    return 0


def _run_validate(arguments: argparse.Namespace) -> int:
    issues = validate_project(arguments.target)
    if not issues:
        print(f"Scaffold valid: {arguments.target.expanduser().resolve()}")
        return 0

    for issue in issues:
        location = f" ({issue.path})" if issue.path else ""
        print(f"{issue.code}{location}: {issue.message}", file=sys.stderr)
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and return a process exit status."""

    arguments = _parser().parse_args(argv)
    if arguments.command == "init":
        return _run_init(arguments)
    if arguments.command == "validate":
        return _run_validate(arguments)
    raise AssertionError(f"unhandled command: {arguments.command}")
