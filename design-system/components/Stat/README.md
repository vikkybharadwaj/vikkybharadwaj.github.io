A tile for one headline figure with a label and a caption on where it comes from.

The numeral uses the `stat` style in the tone colour (or `text` when untoned), with tabular figures. The tile is a `surface` card with a hairline in the tone at about 26% and lifts 4px on hover.

**You provide:** `value` (already formatted), `label` (what it counts), and `caption` (window and source, in `text-3`).

- Do show where the number came from in the caption; every figure in the source states its window.
- Do lay tiles in `repeat(auto-fill, minmax(190px, 1fr))` with a `space-4` gap.
- Don't open a page with a row of stats unless the figures are the point.

Hand-written from `index.html` (`.stat`).
