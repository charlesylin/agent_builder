#!/usr/bin/env bash
# Shared scaffold for resume cases. Seeds an agent project into the run's workspace (cwd).
# Runs only when `claude plugin eval` is invoked with --scaffold. seed.py refuses an existing
# destination, so seed into a subfolder and hoist its contents into the workspace root.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_root="$(cd "$here/.." && pwd)"
python3 "$plugin_root/skills/agent-builder/scripts/seed.py" ./seeded \
  --name "Lab Deal Scout" \
  --purpose "Watch secondhand marketplaces for equipment on a configured shopping list and alert a designated recipient when a listing meets the deal criteria." \
  --kind agent --owner "eval-fixture" --adapter claude >/dev/null
shopt -s dotglob
mv seeded/* .
rmdir seeded
