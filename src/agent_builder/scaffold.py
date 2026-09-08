"""Render a new agent project without overwriting user files."""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from agent_builder import __version__
from agent_builder.models import ProjectSpec
from agent_builder.validation import validate_project

_TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
_ADAPTER_DIRECTORIES = {
    "codex": "codex",
    "claude": "claude",
    "gemini": "gemini",
}


class ScaffoldError(RuntimeError):
    """Raised when a project cannot be generated safely."""


def _template_root() -> Path:
    return Path(__file__).resolve().parent / "templates"


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
    timestamp = generated_at.astimezone(UTC).replace(microsecond=0)
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
        "TEMPLATE_VERSION": __version__,
    }


def _collect_templates(spec: ProjectSpec, context: dict[str, str]) -> dict[Path, str]:
    template_root = _template_root()
    roots = [template_root / "base"]
    roots.extend(template_root / "adapters" / _ADAPTER_DIRECTORIES[item] for item in spec.adapters)

    rendered_files: dict[Path, str] = {}
    for root in roots:
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
            if destination in rendered_files:
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

    context = _context(spec, generated_at or datetime.now(UTC))
    rendered_files = _collect_templates(spec, context)
    temporary = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.agent-builder-", dir=destination.parent)
    )

    try:
        for relative, content in rendered_files.items():
            output = temporary / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding="utf-8", newline="\n")

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
