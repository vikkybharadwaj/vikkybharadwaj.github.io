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
