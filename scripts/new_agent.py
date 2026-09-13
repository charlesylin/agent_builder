#!/usr/bin/env python3
"""Create a generated agent project without installing Agent Builder."""

import sys

if sys.version_info < (3, 9):
    sys.stderr.write(
        "Agent Builder needs Python 3.9 or newer; this is %d.%d. "
        "Install a newer Python and run this again.\n" % sys.version_info[:2]
    )
    sys.exit(2)

from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE))

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main(("init", *sys.argv[1:])))
