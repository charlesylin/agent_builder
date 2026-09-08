"""Deterministic structural and secret-safety checks for generated projects."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

_ADAPTER_FILES = {
    "codex": Path("AGENTS.md"),
    "claude": Path("CLAUDE.md"),
    "gemini": Path("GEMINI.md"),
}
_REQUIRED_FILES = (
    Path(".agent-builder.json"),
    Path(".dockerignore"),
    Path(".env.example"),
    Path(".gitignore"),
    Path("README.md"),
    Path("SECURITY.md"),
    Path("contracts/examples/agent-handoff.example.json"),
    Path("contracts/schemas/agent-handoff.schema.json"),
    Path("governance/decisions.yaml"),
    Path("governance/operating-agreement.md"),
    Path("governance/project-state.yaml"),
    Path("planning/README.md"),
    Path("planning/open-questions.md"),
)
_SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai-style-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "google-api-key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
}
_FORBIDDEN_SECRET_FILES = {".env", ".env.local", ".env.production"}
_TOKEN = re.compile(r"\{\{[A-Z0-9_]+\}\}")


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """One actionable scaffold validation failure."""

    code: str
    message: str
    path: Path | None = None


def _load_json(path: Path, issues: list[ValidationIssue]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        issues.append(ValidationIssue("invalid-json", str(error), path))
        return None


def _validate_contract(root: Path, issues: list[ValidationIssue]) -> None:
    schema_path = root / "contracts/schemas/agent-handoff.schema.json"
    example_path = root / "contracts/examples/agent-handoff.example.json"
    if not schema_path.is_file() or not example_path.is_file():
        return

    schema = _load_json(schema_path, issues)
    example = _load_json(example_path, issues)
    if not isinstance(schema, dict) or not isinstance(example, dict):
        return

    required = schema.get("required")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        issues.append(
            ValidationIssue(
                "invalid-schema", "handoff schema must declare string required fields", schema_path
            )
        )
        return

    missing = sorted(set(required) - set(example))
    if missing:
        issues.append(
            ValidationIssue(
                "invalid-example",
                f"handoff example is missing required fields: {', '.join(missing)}",
                example_path,
            )
        )


def _scan_text_files(root: Path, issues: list[ValidationIssue]) -> None:
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root)
        if relative.name in _FORBIDDEN_SECRET_FILES:
            issues.append(
                ValidationIssue("secret-file", "secret file must not be generated", relative)
            )
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        if _TOKEN.search(content):
            issues.append(ValidationIssue("template-token", "unrendered template token", relative))
        for name, pattern in _SECRET_PATTERNS.items():
            if pattern.search(content):
                issues.append(ValidationIssue("possible-secret", f"matched {name}", relative))


def validate_project(root: str | Path) -> tuple[ValidationIssue, ...]:
    """Return structural and secret-safety issues without mutating the project."""

    project_root = Path(root).expanduser().resolve()
    issues: list[ValidationIssue] = []
    if not project_root.is_dir():
        return (
            ValidationIssue("missing-project", "project directory does not exist", project_root),
        )

    for relative in _REQUIRED_FILES:
        if not (project_root / relative).is_file():
            issues.append(
                ValidationIssue("missing-file", "required scaffold file is missing", relative)
            )

    manifest_path = project_root / ".agent-builder.json"
    manifest = _load_json(manifest_path, issues) if manifest_path.is_file() else None
    if isinstance(manifest, dict):
        adapters = manifest.get("coding_agent_adapters")
        if (
            not isinstance(adapters, list)
            or not adapters
            or not all(isinstance(adapter, str) for adapter in adapters)
        ):
            issues.append(
                ValidationIssue(
                    "invalid-manifest",
                    "coding_agent_adapters must be a non-empty list of strings",
                    manifest_path,
                )
            )
        else:
            unknown = sorted(set(adapters) - set(_ADAPTER_FILES))
            if unknown:
                issues.append(
                    ValidationIssue(
                        "invalid-manifest",
                        f"unknown coding-agent adapters: {', '.join(unknown)}",
                        manifest_path,
                    )
                )
            for adapter in adapters:
                adapter_path = _ADAPTER_FILES.get(adapter)
                if adapter_path and not (project_root / adapter_path).is_file():
                    issues.append(
                        ValidationIssue(
                            "missing-adapter",
                            f"{adapter} adapter entry point is missing",
                            adapter_path,
                        )
                    )
            if len(adapters) != len(set(adapters)):
                issues.append(
                    ValidationIssue(
                        "invalid-manifest",
                        "coding_agent_adapters must not contain duplicates",
                        manifest_path,
                    )
                )
            for adapter, adapter_path in _ADAPTER_FILES.items():
                if adapter not in adapters and (project_root / adapter_path).exists():
                    issues.append(
                        ValidationIssue(
                            "unexpected-adapter",
                            f"{adapter} entry point exists but is not declared",
                            adapter_path,
                        )
                    )

    state_path = project_root / "governance/project-state.yaml"
    if state_path.is_file() and "  current: define\n" not in state_path.read_text(encoding="utf-8"):
        issues.append(
            ValidationIssue("invalid-phase", "new projects must start in Define", state_path)
        )

    gitignore_path = project_root / ".gitignore"
    if gitignore_path.is_file():
        gitignore = gitignore_path.read_text(encoding="utf-8")
        for required_pattern in (".env", "*.pem", "*.key", "secrets/"):
            if required_pattern not in gitignore:
                issues.append(
                    ValidationIssue(
                        "unsafe-ignore",
                        f".gitignore does not cover {required_pattern}",
                        gitignore_path,
                    )
                )

    _validate_contract(project_root, issues)
    _scan_text_files(project_root, issues)
    return tuple(issues)
