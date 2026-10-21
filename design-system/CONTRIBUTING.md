# Working with the design system

`tokens.json` is the single source of truth. `tokens.css` is generated from it: never edit `tokens.css` by hand.

## Before you add or change a page
1. Link the tokens in `<head>`: `<link rel="stylesheet" href="…/design-system/tokens.css">`, plus the JetBrains Mono link from Google Fonts. Every page also needs `charset`, `viewport`, `<title>` and `lang`.
2. Read "Rules for pages" in `design-system/README.md`: no coloured edge stripes, no hex, scales only, distinct dimensions.
3. Use tokens, never literals: colours `var(--green)`, sizes `var(--fs-13)`, line heights `var(--lh-normal)`, spacing `var(--space-4)`, radii `var(--radius-md)`, font `var(--font-mono)`. In SVG use `style="fill:var(--green)"`; in JavaScript read `getComputedStyle(document.documentElement).getPropertyValue('--green')`.
4. Pick a tone for the page or card and carry it with a label or dot, not an edge.

## Check before you push
```bash
python3 scripts/check-design-conformance.py -v   # must exit 0
python3 scripts/tests/run_tests.py               # tests for the gate itself
```
CI runs both on every pull request.

## Proposing a token
Add it to `design-system/tokens.json` with a `usage` note (and a contrast figure for colours), then run `python3 scripts/build-design-tokens.py`. Text colours must reach 4.5:1 on the grounds named in the note. Bump `version` when a token's value changes or a token is removed.

## Generated HTML
`scripts/build-highlights.py` writes the stat strip in `index.html` every day. Its output must pass the gate: tests cover it in `scripts/tests/run_tests.py`.
