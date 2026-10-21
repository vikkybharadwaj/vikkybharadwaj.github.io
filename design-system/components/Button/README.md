A gradient or ghost action button that is the main call to action in a row.

Use `variant="primary"` once per row: green-to-blue `grad-brand` fill with `on-accent` text, lifting 2px on hover with `glow-button`. Use `variant="ghost"` for the secondary action: transparent with a `border` hairline that brightens to `border-2`. Pass `href` to render an anchor.

**You provide:** the label as children (sentence case, start with a verb: "Explore my work"), and `href` or `onClick`.

- Do put the primary button first in the row, with a 14px gap.
- Don't put two primary buttons side by side.
- Don't put the button on a light surface: `on-accent` text is tuned for the dark ground.

Hand-written from `index.html` (`.btn`).
