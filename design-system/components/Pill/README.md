A rounded chip for tags, topics and links.

`variant="outline"` (default) is a hairline chip in `text-2`; given `href` it lifts 1px and takes its `tone` border on hover. `variant="tint"` is a small uppercase badge filled with 15% of its tone, used for document-type tags on cards (ARCHITECTURE, DATA FLOW, MATH).

**You provide:** short text as children, and a `tone` for the tint variant. Map tones by topic, not decoration: blue for architecture, purple for data flow and AI, cyan for pipelines, green for evals, amber for math.

- Do wrap pills in a flex row with `gap: 7px` to `8px`.
- Don't use more than two tones in one row.

Hand-written from `index.html` (`.pill`, `.xtag`) and `projects/tide/index.html` (`.tag`).
