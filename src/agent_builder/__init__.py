"""Governance-first scaffolding for agent projects."""

__version__ = "0.1.0"

from agent_builder.models import ProjectSpec
from agent_builder.scaffold import ScaffoldError, create_project
from agent_builder.validation import ValidationIssue, validate_project

__all__ = [
    "ProjectSpec",
    "ScaffoldError",
    "ValidationIssue",
    "create_project",
    "validate_project",
]
