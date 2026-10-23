#!/usr/bin/env python3
"""Check every page against design-system/tokens.json. Exits 1 if any check fails.

  python3 scripts/check-design-conformance.py [-v] [folder]

With no folder it checks this repo; with a folder it checks that site against these tokens.
"""
import re, json, pathlib, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
tok = json.loads((ROOT / "design-system/tokens.json").read_text())
TOKENS_CSS = (ROOT / "design-system/tokens.css").read_text()
VAL = {c["name"]: c["value"] for c in tok["color"]["tokens"]}
TOKEN_NAMES = set(re.findall(r"--([a-z0-9-]+)\s*:", TOKENS_CSS))
FS = {int(t["value"][:-2]) for t in tok["fontsize"]["tokens"]}

def res(n):
    v = VAL[n]
    return res(v[1:-1]) if v.startswith("{") else v
HEX = {n: res(n) for n in VAL if res(n).startswith("#")}
RGBS = {tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) for h in HEX.values()} | {(255, 255, 255), (0, 0, 0)}

verbose = "-v" in sys.argv
args = [a for a in sys.argv[1:] if not a.startswith("-")]
SITE = pathlib.Path(args[0]).resolve() if args else ROOT

def lum(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def cr(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)
def blend(fg, bg, a):
    f = [int(fg[i:i+2], 16) for i in (1, 3, 5)]; b = [int(bg[i:i+2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(a * x + (1 - a) * y) for x, y in zip(f, b))

STYLE_ATTR = re.compile(r"""(?<!lt;body)\sstyle=(?:"([^"]*)"|'([^']*)'|([^\s>"']+))""")
def css_text(s, whole):
    if whole: return s
    parts = re.findall(r"<style[^>]*>(.*?)</style>", s, re.S)
    parts += [next(g for g in m.groups() if g is not None) for m in STYLE_ATTR.finditer(s)]
    return "\n".join(parts)

NAMED = r"white|black|red|blue|green|gray|grey|yellow|orange|purple|pink|cyan|magenta|teal|navy|lime|maroon|silver|gold|brown"
HEXRE = r"(?<![\w&#%\-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b"
HEXLONG = r"(?<![\w&#%\-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})\b"   # script data such as PR "#311" is not a colour
ALLOWED_SCALE = r"var\(--(?:radius)-[a-z]+\)|0|50%|[123]px"

def collect_pages():
    skip = {"node_modules", ".git"} | ({"design-system", "scripts"} if SITE == ROOT else set())
    return [str(p.relative_to(SITE)) for p in sorted(list(SITE.rglob("*.html")) + list(SITE.rglob("*.css")))
            if not skip & set(p.relative_to(SITE).parts)]

pages = collect_pages()
# custom properties defined anywhere on the site (for the undefined-var check)
SITE_DEFS = set()
for rel in pages:
    SITE_DEFS |= set(re.findall(r"(?:^|[;{\s])--([a-z0-9-]+)\s*:", (SITE / rel).read_text(errors="ignore"), re.M))

COLS = ["no-tokens-link", "redeclared-token", "css-hex", "color-function", "named-color", "hex-in-page", "svg-paint-attr",
        "js-color", "off-palette-rgba", "font-literal", "radius-off-scale", "font-size-off-scale", "line-height-off-scale",
        "spacing-off-scale", "stripe-border", "undefined-var", "chip-contrast<4.5", "motion-no-reduced", "img-no-alt"]
tot = collections.Counter(); rows = []
for rel in pages:
    s = (SITE / rel).read_text(errors="ignore"); whole = rel.endswith(".css")
    css = re.sub(r"/\*.*?\*/", "", css_text(s, whole), flags=re.S)
    f = collections.Counter(); notes = []

    # tokens.css linked and resolving (only for this repo; other sites cannot link the file by relative path)
    if not whole and SITE == ROOT:
        links = re.findall(r'href="([^"]*tokens\.css)[^"]*"', s)
        if not links or not any((SITE / rel).parent.joinpath(h).resolve().exists() for h in links): f["no-tokens-link"] += 1
    # redeclared tokens
    for r in re.findall(r"(?:^|[;{])\s*--([a-z0-9-]+)\s*:", css, re.M):
        if r in TOKEN_NAMES: f["redeclared-token"] += 1; notes.append(f"redeclares --{r}")
    # colour literals in CSS
    scrub = re.sub(r"url\(#[^)]*\)", "", css)
    hexes = re.findall(HEXRE, scrub); f["css-hex"] += len(hexes)
    if hexes: notes.append("hex in CSS: " + ", ".join(sorted(set(hexes)))[:80])
    f["css-hex"] += len(re.findall(r"%23[0-9a-fA-F]{3,8}\b", css))
    f["color-function"] += len(re.findall(r"\b(?:hsla?|hwb|oklch|oklab|lab|lch)\(|(?<![\w-])color\(", css))
    f["named-color"] += len(re.findall(r"(?:^|[;{\s])(?:color|background(?:-color)?|border(?:-[a-z]+)*|outline(?:-color)?|fill|stroke)\s*:[^;}]*(?<![\w-])(?:%s)(?![\w(-])" % NAMED, css))
    for m in re.finditer(r"rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)", css):
        if tuple(map(int, m.groups())) not in RGBS: f["off-palette-rgba"] += 1
    # colours in markup and JS
    if not whole:
        m1 = re.sub(r"<(code|pre)\b(?:(?!<svg).)*?</\1>", "", s, flags=re.S)
        # colours live in tags (attributes), <style> and <script>; prose such as "PR #1234" is not scanned
        scripts_ = re.findall(r"<script[^>]*>(.*?)</script>", m1, re.S)
        tags_ = re.findall(r"<(?!/?script)[^>]+>", m1)
        m2 = "\n".join(tags_)
        m2s = "\n".join(scripts_)
        m2 = re.sub(r"<meta[^>]*theme-color[^>]*>|href=\"#[^\"]*\"|url\(#[^)]*\)|&#\w+;|\sid=\"[^\"]*\"", "", m2)
        hx = re.findall(HEXRE, m2) + re.findall(HEXLONG, m2s); f["hex-in-page"] += len(hx)
        if hx: notes.append("hex in page: " + ", ".join(sorted(set(hx)))[:80])
        f["svg-paint-attr"] += len(re.findall(r'\b(?:fill|stroke|stop-color|flood-color)="(?!none|currentColor|transparent|url\(|var\(|\$\{)[^"]+"', s))
        f["js-color"] += len(re.findall(r"""\.style\.(?:color|background(?:Color)?|borderColor|fill|stroke)\s*=\s*["'](?!var\()""", s))
    # font family
    for m in re.finditer(r"font-family:\s*([^;}\"]+)", css):
        v = m.group(1).strip()
        if not (v.startswith("var(--font-mono") or v == "inherit"): f["font-literal"] += 1
    # radii (shorthand and corner longhands)
    for m in re.finditer(r"border(?:-(?:top|bottom)-(?:left|right))?-radius:\s*([^;}\"]+)", css):
        if not re.fullmatch(r"(%s)(\s+(%s))*" % (ALLOWED_SCALE, ALLOWED_SCALE), m.group(1).strip()): f["radius-off-scale"] += 1
    # font size, line height
    for m in re.finditer(r"font-size:\s*([^;}\"]+)", css):
        v = m.group(1).strip()
        if re.fullmatch(r"var\(--fs-\d+\)|inherit|[\d.]+em|[\d.]+%", v): continue
        if v.startswith("clamp("):
            if re.search(r"\d(px|rem)\b", v): f["font-size-off-scale"] += 1
            continue
        f["font-size-off-scale"] += 1
    for m in re.finditer(r"(?<![\w-])font:\s*(?:[\w.]+\s+)*?(\d+(?:\.\d+)?)(px|rem|em)", css):
        f["font-size-off-scale"] += 1
    if not whole:
        for m in re.finditer(r'\sfont-size="([\d.]+)"', s):
            if float(m.group(1)) not in FS: f["font-size-off-scale"] += 1
    for m in re.finditer(r"line-height:\s*([^;}\"]+)", css):
        v = m.group(1).strip().split("\n")[0].strip()
        if not re.fullmatch(r"var\(--lh-[a-z]+\)|inherit|normal|1|16px", v): f["line-height-off-scale"] += 1; notes.append("line-height: " + repr(v))
    # spacing
    for m in re.finditer(r"(?<![\w-])(?:padding|margin|gap|row-gap|column-gap)(?:-(?:top|bottom|left|right|inline|block)(?:-(?:start|end))?)?:\s*([^;}\"]+)", css):
        v = m.group(1)
        if re.search(r"calc\(|clamp\(|min\(|max\(", v):
            if re.search(r"\d(px|rem)\b", v): f["spacing-off-scale"] += 1
            continue
        for t in v.split():
            mm = re.fullmatch(r"(-?[\d.]+)(px|rem)", t)
            if mm and not t.startswith("-"):
                px = float(mm.group(1)) * (16 if mm.group(2) == "rem" else 1)
                if 4 <= px < 80: f["spacing-off-scale"] += 1
    # stripes
    for m in re.finditer(r"border-(?:top|right|bottom|left|inline-start|inline-end|block-start|block-end)(?:-width)?:\s*([2-9][\d.]*)px(?:\s+(?:solid|dashed))?\s*((?:[^;}\"]|\([^)]*\))*)", css):
        if re.search(r"transparent|var\(--(border|border-2|line)\)", m.group(2)): continue
        rule_start = css.rfind("{", 0, m.start()); rule_end = css.find("}", m.end())
        body = css[rule_start:rule_end]
        if "solid transparent" in body or re.search(r"(?:width|height):\s*0[;\s}]", body): continue  # CSS triangles
        f["stripe-border"] += 1; notes.append("stripe: " + m.group(0)[:60])
    for m in re.finditer(r"::(?:before|after)\s*\{([^}]*)\}", css):
        b = m.group(1)
        if "absolute" in b and re.search(r"(?:height|width):\s*[2-4]px", b) and re.search(r"inset:\s*0 0 auto|top:\s*0;[^}]*left:\s*0;[^}]*right:\s*0", b): f["stripe-border"] += 1
    # undefined custom properties
    for v in set(re.findall(r"var\(--([a-z0-9-]+)", css)):
        if v not in TOKEN_NAMES and v not in SITE_DEFS: f["undefined-var"] += 1; notes.append(f"undefined --{v}")
    # tinted chip contrast: any order, any spacing, per rule
    for rm in re.finditer(r"\{([^{}]*)\}", css):
        body = rm.group(1)
        bg = re.search(r"background(?:-color)?:\s*color-mix\(in srgb,\s*var\(--([a-z0-9-]+)\)\s*([\d.]+)%\s*,\s*transparent\)", body)
        fg = re.search(r"(?<![\w-])color:\s*var\(--([a-z0-9-]+)\)", body)
        if bg and fg and bg.group(1) in HEX and fg.group(1) in HEX:
            ground = blend(HEX[bg.group(1)], HEX["surface-solid"], float(bg.group(2)) / 100)
            c = cr(HEX[fg.group(1)], ground)
            if c < 4.5: f["chip-contrast<4.5"] += 1; notes.append(f"{fg.group(1)} on {bg.group(1)} {bg.group(2)}%: {c:.2f}")
    # motion must respect prefers-reduced-motion; images need alt text
    whole_text = s
    if re.search(r"@keyframes|(?<![\w-])animation\s*:|animation-name\s*:|IntersectionObserver", whole_text) and "prefers-reduced-motion" not in whole_text and not (SITE == ROOT and "tokens.css" in whole_text):
        f["motion-no-reduced"] += 1
    if not whole:
        for m in re.finditer(r"<img\b[^>]*>", s, re.I):
            if not re.search(r"\salt=", m.group(0), re.I): f["img-no-alt"] += 1
    # required meta
    if not whole:
        for k, pat in (("charset", r"<meta charset"), ("viewport", r'name="viewport"'), ("title", r"<title>"), ("lang", r"<html[^>]*lang=")):
            if not re.search(pat, s, re.I): f["missing-" + k] += 1
    f["font-sizes-distinct(info)"] = len(set(re.findall(r"font-size:\s*([0-9.]+px)", css)))
    rows.append((rel, f, notes)); tot.update({k: v for k, v in f.items() if not k.endswith("(info)")})

print(f"{'page':50} " + " ".join(f"{k[:6]:>6}" for k in COLS))
for rel, f, notes in rows:
    print(f"{rel[:50]:50} " + " ".join(f"{f[c]:>6}" for c in COLS))
    if verbose:
        for n in notes[:6]: print("      -", n)
print("\nTOTAL", {k: tot[k] for k in COLS})
hard = [k for k in (*COLS, "missing-title", "missing-viewport", "missing-charset", "missing-lang") if tot[k]]
sys.exit(1 if hard else 0)
