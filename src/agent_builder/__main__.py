"""Run Agent Builder as ``python -m agent_builder``."""

import sys

if sys.version_info < (3, 9):
    sys.stderr.write(
        "Agent Builder needs Python 3.9 or newer; this is %d.%d. "
        "Install a newer Python and run this again.\n" % sys.version_info[:2]
    )
    sys.exit(2)

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main())
