#!/usr/bin/env python3
"""Generate design-system/tokens.css from design-system/tokens.json (the single source of truth)."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent / "design-system"
t = json.loads((root / "tokens.json").read_text())
COLOURS = {c["name"]: c["value"] for c in t["color"]["tokens"] if c["value"].startswith("#")}
out = ["/* Vik Bharadwaj — generated from tokens.json. Edit tokens.json, then run scripts/build-design-tokens.py */", ":root {"]
for fam in ("color", "spacing", "radius", "shadow", "gradient", "fontsize", "lineheight", "duration", "zindex"):
    for tok in t[fam]["tokens"]:
        v = tok["value"]
        if v.startswith("{") and v.endswith("}"):
            v = f"var(--{v[1:-1]})"
        if fam == "gradient":   # keep the gradient linked to the colour tokens
            for n, hv in COLOURS.items():
                v = re.sub(re.escape(hv), f"var(--{n})", v, flags=re.I)
        out.append(f"  --{tok['name']}: {v};")
out.append(f"  --font-mono: {t['type']['families']['mono']};")
out.append("}")
out.append(":focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }")
(root / "tokens.css").write_text("\n".join(out) + "\n")
print("wrote", root / "tokens.css")
