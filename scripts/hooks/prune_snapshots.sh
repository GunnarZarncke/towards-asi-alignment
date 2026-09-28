#!/usr/bin/env bash
# Delete snapshot refs older than 90 days whose timestamp is at or before the
# ledger cursor (so prune never drops an unrecorded interval).
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"
python3 "$root/scripts/human_delta.py" prune-snapshots
