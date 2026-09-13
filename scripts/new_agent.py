#!/usr/bin/env python3
"""Create a generated agent project without installing Agent Builder."""

import sys

if sys.version_info < (3, 9):  # noqa: UP036 - deliberate guard for older interpreters
    sys.stderr.write(
        f"Agent Builder needs Python 3.9 or newer; this is "
        f"{sys.version_info[0]}.{sys.version_info[1]}. Install a newer Python and run this again.\n"
    )
    sys.exit(2)

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main(("init", *sys.argv[1:])))
