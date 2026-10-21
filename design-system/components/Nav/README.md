A sticky top bar with the wordmark at left and section links at right.

Translucent `bg` at 70% with a 12px backdrop blur and a `border` hairline underneath. The wordmark is "Vik" + green period + "Bharadwaj". The link flagged `active` gets the `grad-brand` fill with `on-accent` text and `aria-current="page"`. Links hide under 680px; the source has no mobile menu.

**You provide:** `links` as `{label, href, active}` and optionally `brand`, `brandTail`, `homeHref`.

- Do keep to six links or fewer, in sentence case ("Career Highlights").
- Do give the page `scroll-padding-top: 76px` so anchors clear the bar.
- Don't add a mobile menu without one in the source; if you need one, flag it as an addition.

Hand-written from `index.html` (`nav`) and `projects/product-cockpit/assets/styles.css` (`.nav`).
