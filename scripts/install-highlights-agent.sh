#!/bin/bash
#
# install-highlights-agent.sh — one-time (re)install of the launchd agent that refreshes the
# "Git by the numbers" strip daily at 5pm local time. Run this once on your Mac after cloning
# or whenever scripts/com.vikkybharadwaj.highlights.plist changes:
#
#     bash scripts/install-highlights-agent.sh
#
# After this, everything is hands-off: the agent runs the refresh daily and publishes straight
# to main — you never open Terminal again for it. (The numbers must still be COMPUTED on this
# machine, because the source repos are private and local-only — but that now happens
# automatically in the background; you don't type anything.)
#
set -euo pipefail

PLIST="com.vikkybharadwaj.highlights.plist"
SRC="$(cd "$(dirname "$0")" && pwd)/$PLIST"
DEST="$HOME/Library/LaunchAgents/$PLIST"

[ -f "$SRC" ] || { echo "error: $SRC not found" >&2; exit 1; }

mkdir -p "$HOME/Library/LaunchAgents"
cp "$SRC" "$DEST"
launchctl unload "$DEST" 2>/dev/null || true
launchctl load "$DEST"

echo "installed + loaded: $DEST"
echo "schedule: daily at 17:00 local time (5pm EST/EDT on an Eastern Mac)"
echo "next: it will publish straight to main; logs at ~/Library/Logs/highlights-refresh.log"
echo
echo "to refresh + publish right now without waiting for 5pm:"
echo "    bash \"$(cd "$(dirname "$0")" && pwd)/refresh-highlights-pr.sh\""