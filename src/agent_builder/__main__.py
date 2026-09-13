"""Run Agent Builder as ``python -m agent_builder``."""

import sys

if sys.version_info < (3, 9):  # noqa: UP036 - deliberate guard for older interpreters
    sys.stderr.write(
        f"Agent Builder needs Python 3.9 or newer; this is "
        f"{sys.version_info[0]}.{sys.version_info[1]}. Install a newer Python and run this again.\n"
    )
    sys.exit(2)

from agent_builder.cli import main  # noqa: E402

raise SystemExit(main())
