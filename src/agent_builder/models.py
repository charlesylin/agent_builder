"""Validated inputs for deterministic project generation."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

SUPPORTED_ADAPTERS = ("codex", "claude", "gemini")


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


@dataclass(frozen=True, slots=True)
class ProjectSpec:
    """The small, provider-neutral input contract for a generated project."""

    name: str
    purpose: str
    slug: str
    python_package: str
    adapters: tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        name: str,
        purpose: str,
        adapters: tuple[str, ...] | list[str] | None = None,
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

        return cls(
            name=clean_name,
            purpose=clean_purpose,
            slug=slug,
            python_package=python_package,
            adapters=normalized_adapters,
        )
