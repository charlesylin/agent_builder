#!/usr/bin/env python3
"""Create a new project from Agent Builder's templates.

Copies ``templates/base`` plus ``templates/kinds/<kind>`` plus one adapter directory per
selected coding-agent host, fills the ``{{PLACEHOLDER}}`` tokens, validates the result with
``check.py``, moves it into place in one step, and makes the first git commit. Refuses to
touch a path that already exists.

Usage:
    python3 seed.py PATH --name "Lab Equipment Scout" --purpose "One sentence." \
        [--kind agent|skill|project] [--owner NAME] [--adapter codex|claude|gemini]... [--no-git]
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 9):  # noqa: UP036 - deliberate guard for older interpreters
    sys.stderr.write(
        f"Agent Builder needs Python 3.9 or newer; this is "
        f"{sys.version_info[0]}.{sys.version_info[1]}. Install a newer Python and run this again.\n"
    )
    sys.exit(2)

import argparse  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import unicodedata  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from datetime import datetime, timezone  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    from check import validate_project  # noqa: E402
except ImportError as error:  # pragma: no cover - only when the skill folder is incomplete
    raise SystemExit(f"seed.py needs check.py beside it in {HERE}: {error}") from error

# Kept equal to "version" in the repository's .claude-plugin/plugin.json; a test enforces it.
TEMPLATE_VERSION = "0.3.0"
# The marker check.py looks for in planning/definition.md. Keep the two in sync.
UNANSWERED = "(not yet answered)"


def source_commit() -> str | None:
    """The builder commit these templates came from, or None for a copied skill folder."""

    git = shutil.which("git")
    if git is None:
        return None
    result = subprocess.run(
        [git, "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True, check=False
    )
    return result.stdout.strip() or None if result.returncode == 0 else None


SUPPORTED_ADAPTERS = ("codex", "claude", "gemini")
SUPPORTED_KINDS = ("agent", "skill", "project")
DEFAULT_KIND = "agent"


def _single_line(value: str, field_name: str) -> str:
    normalized = " ".join(value.strip().split())
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise ValueError(f"{field_name} must not contain control characters")
    return normalized


def _slugify(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if not slug:
        raise ValueError("name must contain at least one ASCII letter or number")
    return slug


@dataclass(frozen=True)
class ProjectSpec:
    """The small, provider-neutral input contract for a generated project."""

    name: str
    purpose: str
    slug: str
    python_package: str
    adapters: tuple[str, ...]
    kind: str = DEFAULT_KIND
    owner: str = ""
    problem: str = ""
    current_approach: str = ""
    value: str = ""
    beneficiaries: str = ""

    @classmethod
    def create(
        cls,
        *,
        name: str,
        purpose: str,
        adapters: tuple[str, ...] | list[str] | None = None,
        kind: str = DEFAULT_KIND,
        owner: str = "",
        problem: str = "",
        current_approach: str = "",
        value: str = "",
        beneficiaries: str = "",
    ) -> ProjectSpec:
        """Normalize user input and derive stable project identifiers."""

        clean_name = _single_line(name, "name")
        clean_purpose = _single_line(purpose, "purpose")
        slug = _slugify(clean_name)
        python_package = slug.replace("-", "_")
        if python_package[0].isdigit():
            python_package = f"agent_{python_package}"

        requested = ("codex",) if adapters is None else tuple(adapters)
        unknown = sorted(set(requested) - set(SUPPORTED_ADAPTERS))
        if unknown:
            supported = ", ".join(SUPPORTED_ADAPTERS)
            raise ValueError(
                f"unsupported adapter(s): {', '.join(unknown)}; choose from {supported}"
            )

        # Canonical order makes output independent of argument order and removes duplicates.
        normalized_adapters = tuple(
            adapter for adapter in SUPPORTED_ADAPTERS if adapter in requested
        )
        if not normalized_adapters:
            raise ValueError("select at least one coding-agent adapter")

        if kind not in SUPPORTED_KINDS:
            raise ValueError(f"unsupported kind {kind!r}; choose from {', '.join(SUPPORTED_KINDS)}")

        return cls(
            name=clean_name,
            purpose=clean_purpose,
            slug=slug,
            python_package=python_package,
            adapters=normalized_adapters,
            kind=kind,
            owner=" ".join(owner.split()),
            problem=" ".join(problem.split()),
            current_approach=" ".join(current_approach.split()),
            value=" ".join(value.split()),
            beneficiaries=" ".join(beneficiaries.split()),
        )


_TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
_ADAPTER_DIRECTORIES = {
    "codex": "codex",
    "claude": "claude",
    "gemini": "gemini",
}


class ScaffoldError(RuntimeError):
    """Raised when a project cannot be generated safely."""


def _template_root() -> Path:
    # Templates ship inside the skill folder so a copied skill is self-contained.
    return HERE.parent / "templates"


def _render(value: str, context: dict[str, str], *, source: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        try:
            return context[key]
        except KeyError as error:
            raise ScaffoldError(f"unknown template token {key!r} in {source}") from error

    rendered = _TOKEN.sub(replace, value)
    leftovers = sorted(set(_TOKEN.findall(rendered)))
    if leftovers:
        raise ScaffoldError(f"unrendered template token(s) in {source}: {', '.join(leftovers)}")
    return rendered


def _context(spec: ProjectSpec, generated_at: datetime) -> dict[str, str]:
    timestamp = generated_at.astimezone(timezone.utc).replace(microsecond=0)
    iso_timestamp = timestamp.isoformat().replace("+00:00", "Z")
    adapter_labels = {
        "codex": "Codex",
        "claude": "Claude Code",
        "gemini": "Gemini CLI",
    }
    return {
        "PROJECT_NAME": spec.name,
        "PROJECT_NAME_JSON": json.dumps(spec.name),
        "PROJECT_SLUG": spec.slug,
        "PROJECT_SLUG_JSON": json.dumps(spec.slug),
        "PYTHON_PACKAGE": spec.python_package,
        "PYTHON_PACKAGE_JSON": json.dumps(spec.python_package),
        "PURPOSE": spec.purpose,
        "PURPOSE_JSON": json.dumps(spec.purpose),
        "ADAPTER_LIST": ", ".join(adapter_labels[item] for item in spec.adapters),
        "ADAPTERS_JSON": json.dumps(list(spec.adapters)),
        "ADAPTERS_YAML": "\n".join(f"    - {item}" for item in spec.adapters),
        "GENERATED_AT": iso_timestamp,
        "GENERATED_AT_JSON": json.dumps(iso_timestamp),
        "GENERATED_DATE": timestamp.date().isoformat(),
        "TEMPLATE_VERSION": TEMPLATE_VERSION,
        "SOURCE_COMMIT_JSON": json.dumps(source_commit()),
        "KIND": spec.kind,
        "KIND_JSON": json.dumps(spec.kind),
        "OWNER": spec.owner,
        "OWNER_JSON": json.dumps(spec.owner),
        # Problem framing (AB-D033). Unanswered fields carry a placeholder that
        # check.py --leaving define refuses, so a project cannot leave Define without them.
        "PROBLEM": spec.problem or UNANSWERED,
        "CURRENT_APPROACH": spec.current_approach or UNANSWERED,
        "VALUE": spec.value or UNANSWERED,
        "BENEFICIARIES": spec.beneficiaries or UNANSWERED,
    }


def _collect_templates(spec: ProjectSpec, context: dict[str, str]) -> dict[Path, str]:
    template_root = _template_root()
    # base/ supplies what every kind gets; kinds/<kind>/ adds to it and may override a base
    # file; adapters/<host>/ are appended per selected host and may not collide with anything.
    layers = [(template_root / "base", False), (template_root / "kinds" / spec.kind, True)]
    layers.extend(
        (template_root / "adapters" / _ADAPTER_DIRECTORIES[item], False) for item in spec.adapters
    )

    rendered_files: dict[Path, str] = {}
    for root, may_override in layers:
        if not root.is_dir():
            raise ScaffoldError(f"template directory is missing: {root}")
        for source in sorted(root.rglob("*.tmpl")):
            relative = source.relative_to(root)
            rendered_parts = [
                _render(
                    part.replace("__PYTHON_PACKAGE__", context["PYTHON_PACKAGE"]),
                    context,
                    source=source,
                )
                for part in relative.parts
            ]
            rendered_parts[-1] = rendered_parts[-1].removesuffix(".tmpl")
            destination = Path(*rendered_parts)
            if destination in rendered_files and not may_override:
                raise ScaffoldError(f"template collision at {destination}")
            rendered_files[destination] = _render(
                source.read_text(encoding="utf-8"), context, source=source
            )
    return rendered_files


def create_project(
    target: str | Path,
    spec: ProjectSpec,
    *,
    generated_at: datetime | None = None,
) -> tuple[Path, ...]:
    """Create and validate ``target`` atomically.

    The destination must not exist. Files are first rendered and validated in a temporary
    sibling directory, then moved into place in one filesystem operation.
    """

    destination = Path(target).expanduser().resolve()
    if destination.exists():
        raise ScaffoldError(f"target already exists; refusing to overwrite: {destination}")
    if not destination.parent.is_dir():
        raise ScaffoldError(f"target parent does not exist: {destination.parent}")

    context = _context(spec, generated_at or datetime.now(timezone.utc))
    rendered_files = _collect_templates(spec, context)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.agent-builder-", dir=destination.parent)
    )

    try:
        for relative, content in rendered_files.items():
            output = temporary / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            # Path.write_text(newline=...) is Python 3.10+; open() keeps LF on every platform.
            with output.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)

        issues = validate_project(temporary)
        if issues:
            details = "; ".join(f"{issue.code}: {issue.message}" for issue in issues)
            raise ScaffoldError(f"generated project failed validation: {details}")

        os.replace(temporary, destination)
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise

    return tuple(destination / relative for relative in sorted(rendered_files))


def initialize_git(destination: Path, spec: ProjectSpec) -> str:
    """Create the repository and its first commit; return a one-line status for the user.

    Never fails the seed: a missing git or an unset identity is reported, not raised.
    """

    git = shutil.which("git")
    if git is None:
        return "git not found; repository not initialized"
    message = f"chore: seed {spec.kind} project from agent-builder {TEMPLATE_VERSION}"
    steps = (
        [git, "init", "-q"],
        # Name the first branch main on any git version (init -b needs 2.28+).
        [git, "symbolic-ref", "HEAD", "refs/heads/main"],
        [git, "add", "-A"],
        [git, "commit", "-q", "-m", message],
    )
    for command in steps:
        result = subprocess.run(command, cwd=destination, capture_output=True, text=True)
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            reason = detail[-1] if detail else f"exit {result.returncode}"
            return f"git {command[1]} failed: {reason}"
    return f"git repository initialized; first commit: {message}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="seed.py", description=__doc__.splitlines()[0])
    parser.add_argument("target", type=Path, help="new directory to create; must not exist")
    parser.add_argument("--name", required=True, help="human-readable project name")
    parser.add_argument("--purpose", required=True, help="one sentence: the outcome this owns")
    parser.add_argument(
        "--kind",
        choices=SUPPORTED_KINDS,
        default=DEFAULT_KIND,
        help=f"what is being built; selects templates/kinds/<kind> (default: {DEFAULT_KIND})",
    )
    parser.add_argument("--owner", default="", help="person accountable for the project")
    framing = parser.add_argument_group(
        "problem framing",
        "Answers from the Define conversation, written into planning/definition.md. Optional at"
        " seed time; required before leaving Define.",
    )
    framing.add_argument("--problem", default="", help="what problem this solves")
    framing.add_argument("--current", default="", help="how the problem is solved today")
    framing.add_argument("--value", default="", help="what it is worth if solved")
    framing.add_argument("--for", dest="beneficiaries", default="", help="who it is for")
    parser.add_argument(
        "--adapter",
        action="append",
        choices=SUPPORTED_ADAPTERS,
        help="coding-agent host; repeat to select more than one (default: codex)",
    )
    parser.add_argument(
        "--no-git", action="store_true", help="do not run git init and the first commit"
    )
    arguments = parser.parse_args(argv)

    try:
        spec = ProjectSpec.create(
            name=arguments.name,
            purpose=arguments.purpose,
            adapters=arguments.adapter,
            kind=arguments.kind,
            owner=arguments.owner,
            problem=arguments.problem,
            current_approach=arguments.current,
            value=arguments.value,
            beneficiaries=arguments.beneficiaries,
        )
        files = create_project(arguments.target, spec)
    except (OSError, ValueError, ScaffoldError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    target = arguments.target.expanduser().resolve()
    print(f"Created {spec.name} ({spec.kind}) at {target}")
    print(f"Adapters: {', '.join(spec.adapters)}")
    print(f"Files: {len(files)}")
    if not arguments.no_git:
        print(initialize_git(target, spec))
    print(f"Next: open {target} and begin the Define phase")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
