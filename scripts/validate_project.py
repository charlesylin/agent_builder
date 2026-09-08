#!/usr/bin/env python3
"""Validate a generated project without installing Agent Builder."""

from __future__ import annotations

import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main(("validate", *sys.argv[1:])))
