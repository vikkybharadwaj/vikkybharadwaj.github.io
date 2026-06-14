#!/bin/bash
#
# refresh-highlights-pr.sh — hands-off daily refresh of the "Git by the numbers" stats strip.
#
# Regenerates the strip from local git history (scripts/build-highlights.py). If any number
# changed, it opens — or updates — a single evergreen PR (branch: auto/highlights-refresh) for
# review. It NEVER merges; you stay in control of what goes live. Numbers can only be computed
# locally (the source repos are private), which is why this runs on your machine, not in CI.
#
# Run by the launchd agent `com.vikkybharadwaj.highlights` (daily, 5pm local), or by hand:
#     bash scripts/refresh-highlights-pr.sh
# Dry run (regenerate + report, but never push or open a PR):
#     HIGHLIGHTS_DRY_RUN=1 bash scripts/refresh-highlights-pr.sh
#
set -euo pipefail

# launchd runs with a bare environment — make tool locations explicit.
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO="$HOME/github-repos/vikkybharadwaj.github.io"
BRANCH="auto/highlights-refresh"
DRY_RUN="${HIGHLIGHTS_DRY_RUN:-0}"

log() { echo "[highlights $(date '+%Y-%m-%d %H:%M:%S')] $*"; }

cd "$REPO"
git fetch origin --quiet
git worktree prune

# Work in a throwaway worktree off the latest origin/main, so the user's working copy and
# current branch are never touched.
WT="$(mktemp -d)"
cleanup() { git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true; rm -rf "$WT"; }
trap cleanup EXIT

git worktree add -B "$BRANCH" "$WT" origin/main --quiet
cd "$WT"

python3 scripts/build-highlights.py

if git diff --quiet; then
  log "no changes — numbers already current, nothing to do"
  exit 0
fi

log "numbers changed:"
git --no-pager diff --stat

if [ "$DRY_RUN" = "1" ]; then
  log "DRY RUN — skipping commit/push/PR"
  exit 0
fi

git add -A
git commit -m "chore(highlights): daily refresh of Git by the numbers" --quiet
git push -f -u origin "$BRANCH" --quiet

# One evergreen PR: if it's already open, the force-push above just updated it; otherwise open it.
if gh pr view "$BRANCH" --json state --jq '.state' 2>/dev/null | grep -qx OPEN; then
  log "updated existing PR on $BRANCH"
else
  gh pr create --base main --head "$BRANCH" \
    --title "chore(highlights): daily refresh of Git by the numbers" \
    --body "Automated daily refresh of the **Git by the numbers** stats strip from local git history (\`scripts/build-highlights.py\`). One or more numbers changed since the last refresh — review and merge to publish.

Counts are 2026-to-date; the section footer shows the exact span. Opened by the \`com.vikkybharadwaj.highlights\` launchd agent."
  log "opened PR on $BRANCH"
fi
