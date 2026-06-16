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
  **private**, so the numbers can only be computed where those repos can be cloned. A **scheduled
  GitHub Action** does this fully in the cloud — no machine needed (see below). `scripts/refresh-highlights-pr.sh`
  remains for running a refresh by hand from your Mac, but nothing is scheduled locally anymore.
- **Window:** commit-history metrics (commits, cadence, Conventional %, PR count, AI-assisted %) are
  bounded to `since` in the config (**2026-01-01**). Point-in-time counts (files, docs, notes, evals,
  tools) are current snapshots. The page states this; the `git activity <first> → <last>` line in the
  strip's footer shows the real span, so a stale page is self-evident from the end date.
- **Privacy:** the script only ever emits numbers, ratios, dates, and language tallies — never file
  contents, repo names, branch names, or secrets. Toggle any insight off in the config and it is
  never computed or emitted.

### Recommended: automated daily refresh (GitHub Action — no machine needed)

`.github/workflows/highlights-refresh.yml` does the whole job **in the cloud**: every day around **5pm
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
"Git by the numbers"* → **Run workflow** (manual runs always publish, ignoring the daily gate).

- **Robust to GitHub's loose scheduling.** GitHub's scheduled runners have no timing guarantee and
  routinely fire 1–2h late. The workflow fires at both 21:00 and 22:00 UTC (= 17:00 EDT / EST), and
  instead of demanding the clock read *exactly* 5pm — which a delayed run would miss, silently
  skipping for days — it publishes on the **first trigger of each Eastern day** that finds the strip
  not-yet-refreshed-today; the day's later trigger detects today's refresh commit and no-ops. So a
  late run still publishes, just a little after 5pm.
- **Repo-name assumption.** The workflow clones `vikkybharadwaj/<folder-name>` for each source repo.
  If a repo is named differently on GitHub than its local folder, edit the clone lines in the
  workflow.
- **Privacy.** It clones private repos onto GitHub-hosted runners (ephemeral) and stores a broad
  classic PAT as a secret. Only aggregate numbers ever reach the public page.

### Manual local refresh (optional)

There is **no scheduled job on your Mac** — the GitHub Action above is the only scheduler. (A local
launchd agent used to do this; it was retired in favor of the Action so the two can't race.) To
regenerate and publish the strip by hand from your Mac:

```bash
# refresh + publish to main right now:
bash scripts/refresh-highlights-pr.sh
# dry run — regenerate + report, but never commit or push:
HIGHLIGHTS_DRY_RUN=1 bash scripts/refresh-highlights-pr.sh
```

`scripts/refresh-highlights-pr.sh` regenerates the strip in a throwaway git worktree off the latest
`origin/main` and, **only if a number changed**, commits and pushes straight to `main`. It never
force-pushes and never touches your working copy. Logs to `~/Library/Logs/highlights-refresh.log`.

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
