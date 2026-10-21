Dark, monospace, and technical with a green-to-blue gradient as its single signature. Every page of the portfolio (landing, Tide docs, Product Cockpit, playbook) is built from the same tokens: one font, one dark ground, glass cards, coloured hairlines. Build new pages from the tokens in `tokens.json` and the components in `components/`.

## Content fundamentals

- **Voice.** First person, plain, builder-forward. A product manager who ships. Lead with what was built and the result: "A product manager who builds — across the app, the AI pipeline, the data model, and the evals."
- **Casing.** Sentence case for titles, buttons and nav ("Explore my work", "Career Highlights" is the one title-case exception in nav). Eyebrows, card subtitles and callout titles are uppercase through CSS, not in the source text.
- **Pronouns.** "I" for first-person claims on case studies ("What I'd do differently"); imperative "you" in the playbook ("Build me a one-page portfolio...").
- **Length.** Card copy is two to four lines; section subtitles one or two sentences, max 720px wide.
- **Numbers.** Every figure states its window and source ("Last 90 days across 4 repos").
- **Punctuation.** The source uses em-dashes in titles; new copy should prefer a colon or two short sentences.
- **Emoji.** The source uses single emoji as card icons and callout markers. Treat that as legacy: prefer none in new work.

## Visual foundations

- **Ground.** `bg` is the page. Two blurred blobs (a 520px `green` one top-left, a 560px `blue` one right, 120px blur, 16% to 18% opacity) sit fixed behind everything. There is no light theme.
- **Surfaces.** Cards are `surface` (translucent navy) with `backdrop-filter: blur(8px)`, a 1px `border` hairline and `radius-lg` (14px), or `radius-xl` (18px) for feature cards and figure frames. No opaque white or grey panels.
- **Colour.** `text` for headings, `text-2` for paragraphs, `text-3` for metadata. `green` is primary, `blue` is the link colour. `purple`, `amber`, `teal` and `cyan` each carry a topic or a note type; use one accent per card.
- **Gradient.** `grad-brand` (green to blue, 100deg) appears on the primary button, the active nav link and one highlighted word in the hero h1. Nowhere else.
- **Type.** JetBrains Mono at weights 400 to 800 for everything. Headlines are 800 with negative tracking (`display` -2px, `title` -1px, `heading` -0.5px); eyebrows are 11px, 700, 2px tracking, uppercase. Body copy is 13px to 15px with line-height 1.7 to 1.9, capped near 760px wide.
- **Spacing.** Page gutter `space-6` (24px), card padding `space-5`/`space-6`, grid gap `space-gap` (18px), section padding `space-8` (58px). Content sits in a 1040px wrapper (1080px on case-study pages).
- **Borders and shadows.** Borders do the separating. Shadows appear only as coloured glows on hover (`glow-green`, `glow-blue`...), never as neutral drop shadows.
- **Motion.** Hover lifts only: cards `translateY(-4px)` to `-6px`, buttons `-2px`, pills `-1px`, timeline rows `translateX(3px)`, in 0.15s to 0.2s ease. Arrows slide 5px right on card hover. Nothing animates on load.
- **States.** Hover raises and strengthens the border to the full tone. Focus: the source defines none; use a 2px `cyan` outline with 2px to 3px offset (about 10.8:1 on `bg`).
- **Layout.** Left-aligned. Grids use `repeat(auto-fill, minmax(280px, 1fr))` for cards and `minmax(190px, 1fr)` for stats; three-up bands collapse to one column at 880px. Sticky blurred nav at the top.

## Iconography

There is no icon set. The source uses single emoji as card icons, the arrow glyphs `→` and `↗` for links, and `›` as a list bullet in `green`/accent. Diagrams are inline SVG drawn in the same palette. No logo file exists: the mark is the wordmark "Vik" + green period + "Bharadwaj" set in `heading` weight 800.

## Using the tokens

- Set every colour from a token; never write a hex in a page. Use `color-mix(in srgb, var(--green) 30%, transparent)` for tinted borders and fills, as the components do.
- Text on `green` or `blue` fills is `on-accent`; text on `amber` is `on-amber`.
- Load JetBrains Mono from Google Fonts (400 to 800) and keep `ui-monospace, SFMono-Regular, Menlo, monospace` as the fallback; `var(--font-mono)` carries both.
- Components need React 18 and the `VikDS` bundle; styles are in `components/bundle.css`.

## Known gaps in the source

- `text-3` (4.0:1) fails the 4.5:1 text floor and `purple` is marginal on `surface` (4.65:1); both are kept exact. Keep `text-3` to metadata.
- The Tide data-flow and architecture maps hard-code their own reds and blues (for example `#ef4444` section numbers); those are page-local and not tokenised here.
- No focus styles, no light theme and no mobile menu exist in the source.
