#!/bin/bash
#
# refresh-highlights-pr.sh — hands-off daily refresh of the "Git by the numbers" stats strip.
#
# Regenerates the strip from local git history (scripts/build-highlights.py). If any number
# changed, it commits and pushes the refresh STRAIGHT TO main — fully hands-off, no PR to merge
# (GitHub Pages then redeploys on its own). Numbers can only be computed locally (the source
# repos are private), which is why this runs on your machine, not in CI.
#
# Run by the launchd agent `com.vikkybharadwaj.highlights` (daily, 5pm local), or by hand:
#     bash scripts/refresh-highlights-pr.sh
# Dry run (regenerate + report, but never commit or push):
#     HIGHLIGHTS_DRY_RUN=1 bash scripts/refresh-highlights-pr.sh
#
set -euo pipefail

# launchd runs with a bare environment — make tool locations explicit.
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

REPO="$HOME/github-repos/vikkybharadwaj.github.io"
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

git worktree add --detach "$WT" origin/main --quiet
cd "$WT"

python3 scripts/build-highlights.py

if git diff --quiet; then
  log "no changes — numbers already current, nothing to do"
  exit 0
fi

log "numbers changed:"
git --no-pager diff --stat

if [ "$DRY_RUN" = "1" ]; then
  log "DRY RUN — skipping commit/push"
  exit 0
fi

git add -A
git commit -m "chore(highlights): daily refresh of Git by the numbers" --quiet

# Publish straight to main — no PR, no merge step. If main moved under us between the fetch
# above and now (e.g. a doc-sync landed), rebase the single refresh commit onto the latest
# origin/main and retry. Never force-pushes main.
for attempt in 1 2 3; do
  if git push origin HEAD:main --quiet; then
    log "published refresh straight to main (attempt $attempt) — Pages will redeploy"
    exit 0
  fi
  log "push rejected — main advanced; rebasing onto latest origin/main (attempt $attempt)"
  git fetch origin main --quiet
  git rebase origin/main --quiet || { log "rebase conflict — aborting, will retry next run"; git rebase --abort >/dev/null 2>&1 || true; exit 1; }
done
log "could not publish to main after 3 attempts — will retry next run"
exit 1
