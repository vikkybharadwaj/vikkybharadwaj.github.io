A company logo on a light plate, with one short line on what the company does for its customers.

Use it at the top of a role in an experience list. Brand marks are drawn for light backgrounds (Trustly's is black), so the logo sits unmodified, in its own colours, on a plate in `text` colour. The plate is `size-mark-tile` high and the logo `size-mark` high; width follows the logo's proportions.

**You provide:** `name`, `description` (one sentence about the customer value, not the employer's history), `logo` (path to a PNG with a transparent background or an SVG in `assets/logos/`) and `logoHasName`.

- Set `logoHasName` when the logo already spells the company name. The name is then not repeated as text and the logo's `alt` carries it for screen readers. For an icon-only mark leave it off, and the name shows beside the plate.
- Do use the company's own file, in its original colours. Never redraw, trace or recolour a mark, and trim only transparent margins.
- Do omit `logo` when no file exists: the name and description still render, without a plate.
- Do keep the description under about 12 words and in plain customer language ("Helps people find, tour and buy homes").
- Don't use a monogram, an emoji or a letter in a circle as a stand-in for a logo.
- Keep logo files small: export at 3x the display height (96px) and note each file's source in `assets/logos/README.md`.

Hand-written for the portfolio experience section.
