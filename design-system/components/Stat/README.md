A tile for one headline figure with a label and a caption on where it comes from.

The numeral uses the `stat` style in the tone colour (or `text` when untoned), with tabular figures. The tile is a `surface` card with a hairline in the tone at about 26% and lifts 4px on hover.

**Give every figure a reference.** A big number alone raises the question "is that a lot?". Set `context` to one line that answers it with a comparison you can source, a rate ("about 5 a day") or a before and after. Lead with the comparison when the figure is the point. If no honest reference exists, say what the number counts and over what window instead of leaving it bare.

**You provide:** `value` (already formatted), `label` (what it counts), `context` (the reference line) and `caption` (window and source, in `text-3`).

- Do show where the number came from in the caption; every figure in the source states its window.
- Do lay tiles in `repeat(auto-fill, minmax(190px, 1fr))` with a `space-4` gap.
- Don't open a page with a row of stats unless the figures are the point.

Hand-written from `index.html` (`.stat`).
