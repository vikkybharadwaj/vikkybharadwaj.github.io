#!/usr/bin/env python3
"""Generate design-system/tokens.css from design-system/tokens.json (the single source of truth)."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent / "design-system"
t = json.loads((root / "tokens.json").read_text())
out = ["/* Vik Bharadwaj — generated from tokens.json. Edit tokens.json, then run scripts/build-design-tokens.py */", ":root {"]
for fam in ("color", "spacing", "radius", "shadow", "gradient"):
    for tok in t[fam]["tokens"]:
        out.append(f"  --{tok['name']}: {tok['value']};")
out.append(f"  --font-mono: {t['type']['families']['mono']};")
out.append("}")
(root / "tokens.css").write_text("\n".join(out) + "\n")
print("wrote", root / "tokens.css")
