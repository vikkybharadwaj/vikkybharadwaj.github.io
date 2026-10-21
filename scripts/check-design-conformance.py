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
args = [a for a in sys.argv[1:] if not a.startswith("-")]
SITE = pathlib.Path(args[0]).resolve() if args else ROOT   # optional: check another site against these tokens

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

if SITE == ROOT:
    pages = ["index.html", "playbook/index.html"] + sorted(glob.glob("projects/**/*.html", recursive=True)) + ["projects/product-cockpit/assets/styles.css"]
else:
    pages = sorted(str(p.relative_to(SITE)) for p in list(SITE.rglob("*.html")) + list(SITE.rglob("*.css")) if "node_modules" not in p.parts and ".git" not in p.parts)
tot = collections.Counter(); rows = []
for rel in pages:
    s = (SITE/rel).read_text(errors="ignore"); whole = rel.endswith(".css")
    css = re.sub(r"/\*.*?\*/", "", css_text(s, whole), flags=re.S)
    f = collections.Counter(); notes = []
    # 1 tokens linked (cockpit pages inherit via a page that links styles.css which is linked with tokens)
    if not whole and SITE == ROOT and "tokens.css" not in s: f["no-tokens-link"] += 1
    # 2 redeclared tokens
    redecl = re.findall(r"(?:^|[;{])\s*--([a-z0-9-]+)\s*:", css, re.M)
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
    # 7 font-size / line-height in scale
    for m in re.finditer(r"font-size:\s*([^;}\"]+)", css):
        v = m.group(1).strip()
        if re.fullmatch(r"var\(--fs-\d+\)|inherit|[\d.]+em|[\d.]+%", v) or v.startswith("calc"): continue
        if v.startswith("clamp("):
            if re.search(r"\d(px|rem)\b", v): f["font-size-off-scale"] += 1
            continue
        f["font-size-off-scale"] += 1
    if not whole:
        for m in re.finditer(r'\sfont-size="([\d.]+)"', s):
            if int(float(m.group(1))) not in (10, 11, 12, 13, 15, 17, 21, 30, 34, 68): f["font-size-off-scale"] += 1
    for m in re.finditer(r"line-height:\s*([^;}\"]+)", css):
        v = m.group(1).strip().split("\n")[0].strip()
        if not re.fullmatch(r"var\(--lh-[a-z]+\)|inherit|normal|1|16px", v): f["line-height-off-scale"] += 1; notes.append("line-height: " + repr(v))
    # 8 spacing in scale
    for m in re.finditer(r"(?<![\w-])(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|bottom|left|right|inline|block)(?:-(?:start|end))?)?:\s*([^;}\"]+)", css):
        v = m.group(1)
        if re.search(r"calc\(|clamp\(|min\(|max\(", v): continue
        for t in v.split():
            mm = re.fullmatch(r"(-?[\d.]+)(px|rem)", t)
            if mm and not t.startswith("-"):
                px = float(mm.group(1)) * (16 if mm.group(2) == "rem" else 1)
                if 4 <= px < 80: f["spacing-off-scale"] += 1
    # 9 stripe borders and edge stripes
    for m in re.finditer(r"border-(?:top|left|right|inline-start):\s*([2-9][\d.]*)px\s+(?:solid|dashed)\s+((?:[^;}\"]|\([^)]*\))+)", css):
        if re.search(r"transparent|var\(--(border|border-2|line)\)", m.group(2)): continue
        f["stripe-border"] += 1; notes.append("stripe: " + m.group(0)[:60])
    for m in re.finditer(r"::(?:before|after)\s*\{([^}]*)\}", css):
        b = m.group(1)
        if "position:" in b and "absolute" in b and re.search(r"(?:height|width):\s*[2-4]px", b) and re.search(r"inset:\s*0 0 auto|top:\s*0;[^}]*left:\s*0;[^}]*right:\s*0", b):
            f["stripe-border"] += 1
    # 10 hex outside allowed contexts (strip code/pre blocks, entities, theme-color meta)
    if not whole:
        m2 = re.sub(r"<(code|pre)\b.*?</\1>", "", s, flags=re.S)
        m2 = re.sub(r"<meta[^>]*theme-color[^>]*>", "", m2)
        m2 = re.sub(r"&#\d+;|&#x[0-9a-fA-F]+;", "", m2)
        hx = re.findall(r"(?<![\w&])#[0-9a-fA-F]{6}\b", m2)
        f["hex-in-page"] += len(hx)
        if hx: notes.append("hex in page: " + ", ".join(sorted(set(hx)))[:80])
    # 12 meta
    if not whole:
        for k, pat in (("charset", r"<meta charset"), ("viewport", r'name="viewport"'), ("title", r"<title>"), ("lang", r"<html[^>]*lang=")):
            if not re.search(pat, s, re.I): f["missing-" + k] += 1
    rows.append((rel, f, notes)); tot.update({k: v for k, v in f.items() if not k.endswith("(info)")})
FAILKEYS = [k for k in tot if not k.endswith("(info)")]
cols = COLS = ["redeclared-token","css-hex","hex-in-page","off-palette-rgba","font-literal","radius-off-scale","font-size-off-scale","line-height-off-scale","spacing-off-scale","stripe-border","chip-contrast<4.5"]
print(f"{'page':50} " + " ".join(f"{k[:8]:>8}" for k in cols))
for rel, f, notes in rows:
    print(f"{rel:50} " + " ".join(f"{f[c]:>8}" for c in cols))
    if verbose:
        for n in notes[:6]: print("      -", n)
print("\nTOTAL", {k: tot[k] for k in cols})
print("info: JS/SVG literal hex are covered by hex-in-page; max distinct px font-sizes on a page:", max(f["font-sizes-distinct(info)"] for _, f, _ in rows))
hard = [k for k in (*cols, "no-tokens-link", "missing-title", "missing-viewport", "missing-charset") if tot[k]]
sys.exit(1 if hard else 0)
