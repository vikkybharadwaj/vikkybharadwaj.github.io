# vikkybharadwaj.github.io

My personal portfolio — a "hub of hubs" that links to each project's own interactive HTML
documentation. Live at **https://vikkybharadwaj.github.io**.

The site is fully self-contained: each project's HTML docs are **vendored** into
`projects/<slug>/`, so nothing depends on an external host.

## Structure

```
index.html            # the portfolio landing page (hero + 3-prong "Explore my work" band
                      #   + about + experience timeline + highlights + what-I-do + contact)
.nojekyll             # tells GitHub Pages to serve every file verbatim (no Jekyll)
projects/
  tide/               # vendored Tide docs; projects/tide/index.html is the entry point
  product-cockpit/    # vendored Product Cockpit (AI-native operating system) case study
```

The homepage's three front-doors ("Explore my work"):
1. **Tide** → `projects/tide/` (in-repo)
2. **Product Cockpit — Operating System** → `projects/product-cockpit/` (in-repo)
3. **How I Learn AI** → links out to `https://vikkybharadwaj.github.io/ai_knowledgecenter/` (separate path)

## Refreshing the "How I operate" numbers

The stat strip in the **How I Operate** section is **generated**, not hand-edited. It is computed
from the git history + current file counts of the local repos listed in
`data/highlights.config.json` by `scripts/build-highlights.py`, which injects the result between
the `<!-- HIGHLIGHTS:START -->` / `<!-- HIGHLIGHTS:END -->` markers in `index.html`.

```bash
python3 scripts/build-highlights.py   # re-reads every configured repo, rewrites the strip
```

- **Why it can't run in CI.** The configured repos (Tide, ai_knowledgecenter, commandcenter, …) are
  **private and local-only**, so no GitHub Action can see them — the numbers can only be computed on
  your machine.
- **Window:** commit-history metrics (commits, cadence, Conventional %, PR count, AI-assisted %) are
  bounded to `since` in the config (**2026-01-01**). Point-in-time counts (files, docs, notes, evals,
  tools) are current snapshots. The page states this; the `git activity <first> → <last>` line in the
  strip's footer shows the real span, so a stale page is self-evident from the end date.
- **Privacy:** the script only ever emits numbers, ratios, dates, and language tallies — never file
  contents, repo names, branch names, or secrets. Toggle any insight off in the config and it is
  never computed or emitted.

### Automated daily refresh (launchd)

A local launchd agent keeps the page fresh hands-off:

- **`scripts/refresh-highlights-pr.sh`** (in this repo) regenerates the strip in a throwaway git
  worktree off the latest `origin/main`, and **only if a number changed** opens or updates a single
  evergreen PR on branch `auto/highlights-refresh`. It never merges and never touches your working
  copy — you just review and merge the PR to publish.
- **`com.vikkybharadwaj.highlights`** runs that script **daily at 5pm local time** (= 5pm EST/EDT
  when the Mac is set to US Eastern — launchd follows the wall clock, so it auto-tracks daylight
  saving). The schedule lives in **`scripts/com.vikkybharadwaj.highlights.plist`** (now versioned
  here); the *active* copy is the one you install at
  `~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist`. Logs to
  `~/Library/Logs/highlights-refresh.log`.

```bash
# install / update the schedule (run after pulling a change to the plist):
cp scripts/com.vikkybharadwaj.highlights.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist

# run it now by hand (opens/updates the PR if anything changed):
bash scripts/refresh-highlights-pr.sh
# dry run — regenerate + report, but never push or open a PR:
HIGHLIGHTS_DRY_RUN=1 bash scripts/refresh-highlights-pr.sh
# pause / resume the schedule:
launchctl unload ~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist   # pause
launchctl load   ~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist   # resume
```

## Adding a new project

1. **Vendor the HTML.** Copy the project's HTML docs into a new folder:
   ```bash
   mkdir -p projects/<slug>
   cp /path/to/that-project/docs/*.html projects/<slug>/
   ```
   Make sure there's a `projects/<slug>/index.html` that acts as the hub entry point, and
   that the docs cross-link with **relative** paths (so they work once co-located).

2. **Add a card.** In `index.html`, find a "Coming soon" card and turn it into a live one:
   ```html
   <a class="card live c-soon-1" href="projects/<slug>/index.html">
     ... logo, title, description, tags, and a "go" link (copy the Tide card) ...
   </a>
   ```
   Update the `Projects` count in the section header too.

3. **Publish.**
   ```bash
   git add -A && git commit -m "feat: add <slug> project" && git push
   ```
   GitHub Pages redeploys automatically (usually within a minute).

## Editing the bio / contact

`index.html` is a full portfolio page: hero, about, capability grid, the Tide flagship card,
and a contact block. To wire up LinkedIn, find the `LINKEDIN_SLOT` comment in the contact
section, set the real URL on that `<a>`, and remove the `soon` class + the `SOON` pill.
Email (`vikky.bharadwaj@gmail.com`) and GitHub links are already live.
