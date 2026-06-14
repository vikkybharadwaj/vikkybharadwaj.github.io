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

- **Where it runs.** The configured repos (Tide, ai_knowledgecenter, commandcenter, …) are
  **private**. Two refresh paths exist: a **scheduled GitHub Action** (recommended — fully in the
  cloud, no machine needed; see below) or a **local launchd agent** (computes on your Mac). Pick one
  — don't run both, or they'll race to publish the same numbers.
- **Window:** commit-history metrics (commits, cadence, Conventional %, PR count, AI-assisted %) are
  bounded to `since` in the config (**2026-01-01**). Point-in-time counts (files, docs, notes, evals,
  tools) are current snapshots. The page states this; the `git activity <first> → <last>` line in the
  strip's footer shows the real span, so a stale page is self-evident from the end date.
- **Privacy:** the script only ever emits numbers, ratios, dates, and language tallies — never file
  contents, repo names, branch names, or secrets. Toggle any insight off in the config and it is
  never computed or emitted.

### Recommended: automated daily refresh (GitHub Action — no machine needed)

`.github/workflows/highlights-refresh.yml` does the whole job **in the cloud**: every day at **5pm
US Eastern** it clones the private source repos onto an ephemeral GitHub runner, runs
`build-highlights.py`, and **publishes straight to `main`** (Pages redeploys). Your Mac is never
involved.

**One-time setup — add a single secret:**

1. Create a **classic** Personal Access Token (github.com → Settings → Developer settings → Tokens
   (classic)) owned by your account, with scopes **`repo`** (clone the private repos + push to
   `main`) and **`read:user`** (read the contribution-calendar total for the "GitHub contributions"
   tile).
2. Add it to this repo as a secret named **`HIGHLIGHTS_PAT`** (repo → Settings → Secrets and
   variables → Actions → New repository secret).

That's it — no further action ever. Trigger a run immediately from the **Actions** tab → *Refresh
"Git by the numbers"* → **Run workflow** (manual runs ignore the time gate).

- **DST-correct timing.** GitHub cron is UTC with no DST, so the workflow fires at both 21:00 and
  22:00 UTC and runs the job only when it's actually 17:00 in `America/New_York` — exactly once a day
  year-round.
- **Repo-name assumption.** The workflow clones `vikkybharadwaj/<folder-name>` for each source repo.
  If a repo is named differently on GitHub than its local folder, edit the clone lines in the
  workflow.
- **Privacy.** It clones private repos onto GitHub-hosted runners (ephemeral) and stores a broad
  classic PAT as a secret. Only aggregate numbers ever reach the public page — same as the local
  script. If you prefer nothing private to touch GitHub's infra, use the launchd path below instead.

### Alternative: automated daily refresh on your Mac (launchd)

A local launchd agent keeps the page fresh **fully hands-off** — after a one-time install you never
touch Terminal for it again:

- **`scripts/refresh-highlights-pr.sh`** (despite the legacy name) regenerates the strip in a
  throwaway git worktree off the latest `origin/main`, and **only if a number changed** commits and
  pushes the refresh **straight to `main`** — no PR, no merge step. GitHub Pages redeploys on its
  own. It never force-pushes and never touches your working copy.
- **`com.vikkybharadwaj.highlights`** runs that script **daily at 5pm local time** (= 5pm EST/EDT
  when the Mac is set to US Eastern — launchd follows the wall clock, so it auto-tracks daylight
  saving). The schedule lives in **`scripts/com.vikkybharadwaj.highlights.plist`** (versioned here);
  the *active* copy is the one installed at
  `~/Library/LaunchAgents/com.vikkybharadwaj.highlights.plist`. Logs to
  `~/Library/Logs/highlights-refresh.log`.

> **When to use this instead of the Action.** Choose launchd if you'd rather your private repos never
> be cloned onto GitHub's runners — the computation then happens entirely on your Mac and only the
> numbers are pushed. The trade-off: your Mac must be on/awake around 5pm. The only manual step is
> installing the agent once.

```bash
# one-time install (or after the plist changes) — copies + loads the agent:
bash scripts/install-highlights-agent.sh

# refresh + publish to main right now, without waiting for 5pm:
bash scripts/refresh-highlights-pr.sh
# dry run — regenerate + report, but never commit or push:
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
