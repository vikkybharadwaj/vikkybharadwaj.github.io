A company logo in a square tile, with the company name and one short line on what it does for its customers.

Use it at the top of a role in an experience list. The logo is a single-ink SVG (or a PNG with a transparent background) shown through a mask, so it always takes `text` on the `surface` tile and never brings a brand colour. The tile is decorative (`aria-hidden`); the visible company name carries the meaning.

**You provide:** `name`, `description` (one sentence about the customer value, not the employer's history), and `logo`, the path to an SVG in `assets/logos/<company>.svg` (single colour, square-ish viewBox).

- Do use the company's own logo file, copied unmodified. Never redraw, trace or recolour a brand mark.
- Do omit `logo` when no file exists. The name and description still render, and no tile is drawn. Add the file later and the tile appears.
- Do keep the description under about 12 words and in plain customer language ("Helps people find, tour and buy homes").
- Don't use a monogram, an emoji or a letter in a circle as a stand-in for a logo.
- Pick logo files that are free to reuse or that you have the right to show, and note the source next to the file.

Hand-written for the portfolio experience section.
