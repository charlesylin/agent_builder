#!/usr/bin/env python3
"""Create a generated agent project without installing Agent Builder."""

from __future__ import annotations

import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main(("init", *sys.argv[1:])))
