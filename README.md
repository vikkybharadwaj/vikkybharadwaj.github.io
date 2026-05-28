# vikkybharadwaj.github.io

My personal portfolio — a "hub of hubs" that links to each project's own interactive HTML
documentation. Live at **https://vikkybharadwaj.github.io**.

The site is fully self-contained: each project's HTML docs are **vendored** into
`projects/<slug>/`, so nothing depends on an external host.

## Structure

```
index.html            # the portfolio landing page (hero + project cards)
.nojekyll             # tells GitHub Pages to serve every file verbatim (no Jekyll)
projects/
  tide/               # vendored Tide docs; projects/tide/index.html is the entry point
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

## Editing the bio

The hero in `index.html` has three spots marked `<!-- EDIT -->`: the headline, the blurb,
and the LinkedIn URL. Swap those for your own wording/links.
