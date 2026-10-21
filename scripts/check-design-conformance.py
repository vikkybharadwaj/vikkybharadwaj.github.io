#!/usr/bin/env python3
"""Check every page against design-system/tokens.json. Exit 1 if any FAIL. Run: python3 scripts/check-design-conformance.py [-v]"""
import re, json, glob, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
tok = json.loads((ROOT/"design-system/tokens.json").read_text())
VAL = {c["name"]: c["value"] for c in tok["color"]["tokens"]}
def res(n, d=0):
    v = VAL[n]
    return res(v[1:-1], d+1) if v.startswith("{") else v
HEX = {n: res(n) for n in VAL if res(n).startswith("#")}
RGBS = {tuple(int(h[i:i+2], 16) for i in (1,3,5)) for h in HEX.values()} | {(255,255,255), (0,0,0)}
RADII = {t["name"]: t["value"] for t in tok["radius"]["tokens"]}
verbose = "-v" in sys.argv

def lum(h):
    r, g, b = [int(h[i:i+2], 16)/255 for i in (1,3,5)]
    f = lambda c: c/12.92 if c <= .03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def cr(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb)+.05)/(min(la, lb)+.05)
def blend(fg, bg, a):
    f = [int(fg[i:i+2], 16) for i in (1,3,5)]; b = [int(bg[i:i+2], 16) for i in (1,3,5)]
    return "#%02x%02x%02x" % tuple(round(a*x+(1-a)*y) for x, y in zip(f, b))

def css_text(s, whole):
    if whole: return s
    parts = re.findall(r"<style[^>]*>(.*?)</style>", s, re.S) + re.findall(r'(?<!lt;body)\sstyle="([^"]*)"', s)
    return "\n".join(parts)

pages = ["index.html", "playbook/index.html"] + sorted(glob.glob("projects/**/*.html", recursive=True)) + ["projects/product-cockpit/assets/styles.css"]
tot = collections.Counter(); rows = []
for rel in pages:
    s = (ROOT/rel).read_text(); whole = rel.endswith(".css")
    css = re.sub(r"/\*.*?\*/", "", css_text(s, whole), flags=re.S)
    f = collections.Counter(); notes = []
    # 1 tokens linked (cockpit pages inherit via a page that links styles.css which is linked with tokens)
    if not whole and "tokens.css" not in s: f["no-tokens-link"] += 1
    # 2 redeclared tokens
    redecl = re.findall(r"^\s*--([a-z0-9-]+)\s*:", css, re.M)
    for r in redecl:
        if r in VAL or r in RADII: f["redeclared-token"] += 1; notes.append(f"redeclares --{r}")
    # 3 palette hex literals inside CSS
    hexes = re.findall(r"(?<![&\w])#[0-9a-fA-F]{6}\b", css)
    f["css-hex"] += len(hexes)
    if hexes: notes.append("hex in CSS: " + ", ".join(sorted(set(hexes)))[:80])
    # 3b hex in markup/JS (info only)
    f["svg-js-hex(info)"] += len(re.findall(r"(?<![&\w])#[0-9a-fA-F]{6}\b", s)) - len(hexes)
    # 4 off-palette rgba
    for m in re.finditer(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", css):
        if tuple(map(int, m.groups())) not in RGBS: f["off-palette-rgba"] += 1
    # 5 font-family literal
    for m in re.finditer(r"font-family:\s*([^;}\"]+)", css):
        v = m.group(1).strip()
        if not (v.startswith("var(--font-mono") or v == "inherit"): f["font-literal"] += 1
    # 6 radii
    for m in re.finditer(r"border-radius:\s*([^;}\"]+)", css):
        v = m.group(1).strip()
        if not re.fullmatch(r"(var\(--radius-[a-z]+\)|0|50%|[123]px)(\s+(var\(--radius-[a-z]+\)|0|50%|[123]px))*", v): f["radius-off-scale"] += 1
    # 7 font sizes (info)
    f["font-sizes-distinct(info)"] = len(set(re.findall(r"font-size:\s*([0-9.]+px)", css)))
    # 8 contrast of tinted chips: background color-mix(var(--A) N%) + color var(--B) on surface-solid
    for m in re.finditer(r"background:\s*color-mix\(in srgb, var\(--([a-z0-9-]+)\) ([\d.]+)%, transparent\)[^;}]*;\s*color:\s*var\(--([a-z0-9-]+)\)", css):
        a, n, b = m.group(1), float(m.group(2))/100, m.group(3)
        if a in HEX and b in HEX:
            ground = blend(HEX[a], HEX["surface-solid"], n); c = cr(HEX[b], ground)
            if c < 4.5: f["chip-contrast<4.5"] += 1; notes.append(f"{b} on {a} {n:.0%}: {c:.2f}")
    # 9 stripe pattern (info)
    f["stripe-borders(info)"] = len(re.findall(r"border-(?:left|top):\s*[2-6]px", css))
    # 12 meta
    if not whole:
        for k, pat in (("charset", r"<meta charset"), ("viewport", r'name="viewport"'), ("title", r"<title>"), ("lang", r"<html[^>]*lang=")):
            if not re.search(pat, s, re.I): f["missing-" + k] += 1
    rows.append((rel, f, notes)); tot.update({k: v for k, v in f.items() if not k.endswith("(info)")})
FAILKEYS = [k for k in tot if not k.endswith("(info)")]
print(f"{'page':58} " + " ".join(f"{k[:11]:>11}" for k in ["no-tokens-link","redeclared-token","css-hex","off-palette-rgba","font-literal","radius-off-scale","chip-contrast<4.5"]))
cols = ["no-tokens-link","redeclared-token","css-hex","off-palette-rgba","font-literal","radius-off-scale","chip-contrast<4.5"]
for rel, f, notes in rows:
    print(f"{rel:58} " + " ".join(f"{f[c]:>11}" for c in cols))
    if verbose:
        for n in notes[:6]: print("      -", n)
print("\nTOTAL", {k: tot[k] for k in cols})
print("info: svg/js hex literals", sum(f["svg-js-hex(info)"] for _, f, _ in rows), "| stripe borders", sum(f["stripe-borders(info)"] for _, f, _ in rows), "| max distinct font sizes on a page", max(f["font-sizes-distinct(info)"] for _, f, _ in rows))
hard = [k for k in ("redeclared-token", "css-hex", "off-palette-rgba", "font-literal", "radius-off-scale", "chip-contrast<4.5", "missing-title", "missing-viewport", "missing-charset") if tot[k]]
sys.exit(1 if hard else 0)
