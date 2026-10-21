A glass card with a 3px tone stripe on its top edge, used for the major "doors" into a body of work.

Fill is `surface` over the ambient glow with `radius-lg`; border and stripe take the `tone`. On hover it lifts 6px and gains a glow in that tone. With `href` the whole card is a link and ends in an "Open →" line pinned to the bottom.

**You provide:** `title`, and optionally `number` ("01"), `subtitle` (uppercase tone line), `tags` (strings), and body text as children. Use one tone per card and a different tone for each sibling: green, teal, cyan for three siblings.

- Do lay cards in a grid with `space-gap` (18px), three across, one column under 880px.
- Do keep body text under about four lines.
- Don't nest cards.
- Don't add emoji; the source's emoji icons are an exception, not the rule.

Hand-written from `index.html` (`.xcard`). The top stripe is how the source marks tone; if you extend this component, keep it to one edge.
