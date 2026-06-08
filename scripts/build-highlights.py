#!/usr/bin/env python3
"""build-highlights.py — generate the "How I operate" highlights strip on index.html.

Scans a configured list of LOCAL repos (data/highlights.config.json) and computes a fixed allowlist
of AGGREGATE, non-sensitive metrics from git history + file counts. Renders stat tiles + a stack bar
and injects them into index.html between the HIGHLIGHTS markers. Also writes data/highlights.json
(the computed values, for transparency). Honors config: only ENABLED insights are computed/emitted,
so a disabled insight never reaches the public page.

PRIVACY: this only ever emits numbers, ratios, dates, and language tallies. It never emits file
contents, branch names, feature names, secrets, repo names, or anything from docs-private/. It only
reads files to COUNT (lines / matches), never to surface text — except `latest_ship`, which (only
when explicitly enabled + allowlisted in config) emits a single plain-English changelog headline.

Runs locally only (the private repos exist on Vik's machine). Re-run after any repo changes:
    python3 scripts/build-highlights.py
Idempotent: same repo state -> no diff.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
CONFIG = ROOT / "data" / "highlights.config.json"
DATA_OUT = ROOT / "data" / "highlights.json"
START = "<!-- HIGHLIGHTS:START -->"
END = "<!-- HIGHLIGHTS:END -->"

CONV_RE = re.compile(r"^(feat|fix|docs|chore|refactor|style|test|perf|build|ci)(\([^)]*\))?!?:")
PR_RE = re.compile(r"\(#\d+\)\s*$")

# extension -> display language for the stack bar
LANG = {
    "ts": "TypeScript", "tsx": "TypeScript", "js": "JavaScript", "jsx": "JavaScript",
    "py": "Python", "html": "HTML", "css": "CSS", "md": "Markdown", "sh": "Shell",
    "tf": "Terraform", "json": "JSON", "yml": "YAML", "yaml": "YAML",
}


def git(repo: Path, *args) -> str:
    try:
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, text=True).stdout
    except Exception:
        return ""


def is_repo(repo: Path) -> bool:
    return git(repo, "rev-parse", "--is-inside-work-tree").strip() == "true"


def count_lines(p: Path) -> int:
    try:
        with open(p, "rb") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def count_matches(p: Path, needle: str) -> int:
    try:
        return open(p, encoding="utf-8", errors="ignore").read().count(needle)
    except Exception:
        return 0


def scan(repos, since=None):
    """Compute the full aggregate metric bag across all repos. Numbers only.

    `since` (ISO date, e.g. "2026-01-01") bounds all COMMIT-history metrics —
    commits, cadence, Conventional %, PR count, AI-assisted % — to that window.
    Point-in-time counts (tracked files, docs, notes, evals, tools…) are
    current-state snapshots and are not date-bounded.
    """
    since_args = ["--since", since] if since else []
    m = dict(commits=0, conv=0, pr=0, ai=0, files=0, md=0, html=0, projects=0,
             notes=0, concepts=0, evals=0, learnings=0, changelog=0,
             skills=0, commands=0, agents=0, hooks=0)
    ext = {}            # extension -> count
    dates = []          # in-window commit short-dates, for span + cadence

    for raw in repos:
        repo = Path(os.path.expanduser(raw))
        if not repo.exists() or not is_repo(repo):
            continue
        m["projects"] += 1

        n = git(repo, "rev-list", "--count", *since_args, "HEAD").strip()
        m["commits"] += int(n) if n.isdigit() else 0

        for d in git(repo, "log", *since_args, "--format=%cd", "--date=short").split():
            if re.match(r"\d{4}-\d{2}-\d{2}", d):
                dates.append(d)

        subjects = [s for s in git(repo, "log", *since_args, "--format=%s").splitlines() if s.strip()]
        m["conv"] += sum(1 for s in subjects if CONV_RE.match(s))
        m["pr"] += sum(1 for s in subjects if PR_RE.search(s))

        ai = git(repo, "log", *since_args, "-i", "--grep=claude", "--format=%H").splitlines()
        m["ai"] += sum(1 for x in ai if x.strip())

        files = [f for f in git(repo, "ls-files").splitlines() if f.strip()]
        m["files"] += len(files)
        for f in files:
            e = f.rsplit(".", 1)[-1].lower() if "." in f.rsplit("/", 1)[-1] else ""
            if e:
                ext[e] = ext.get(e, 0) + 1
            if e == "md":
                m["md"] += 1
            elif e == "html":
                m["html"] += 1
            if f.startswith("knowledge/notes/") and e == "md":
                m["notes"] += 1
            elif f.startswith("knowledge/concepts/") and e == "md":
                m["concepts"] += 1
            if "evals/" in f and e == "json":
                m["evals"] += 1
            if re.match(r"\.claude/skills/[^/]+/SKILL\.md$", f):
                m["skills"] += 1
            elif re.match(r"\.claude/commands/[^/]+\.md$", f):
                m["commands"] += 1
            elif re.match(r"\.claude/agents/[^/]+\.md$", f):
                m["agents"] += 1

        # LEARNINGS lines (count only, never content)
        for cand in ("LEARNINGS.md", "docs/LEARNINGS.md"):
            p = repo / cand
            if p.exists():
                m["learnings"] += count_lines(p)
        # changelog entries (HTML cards / JS-array rows) — published, count only
        cl = repo / "docs" / "changelog.html"
        if cl.exists():
            m["changelog"] += count_matches(cl, "cl-item")
        os_html = repo / "docs" / "operating-system.html"
        if os_html.exists():
            m["changelog"] += count_matches(os_html, "num:")
        # hook command entries from PROJECT settings (no secrets there; never ~/.claude)
        sj = repo / ".claude" / "settings.json"
        if sj.exists():
            try:
                hk = json.load(open(sj)).get("hooks", {})
                m["hooks"] += sum(len(g.get("hooks", [])) for ev in hk.values() for g in ev)
            except Exception:
                pass

    # language rollup for the stack bar
    langs = {}
    for e, c in ext.items():
        if e in LANG:
            langs[LANG[e]] = langs.get(LANG[e], 0) + c
    m["languages"] = sorted(langs.items(), key=lambda kv: -kv[1])
    m["dates"] = sorted(dates)
    return m


def gh_contributions(since=None):
    """Total GitHub contributions (commits + PRs + issues + reviews, public + private) from the
    contribution calendar — the exact number GitHub shows as "N contributions in the last year".

    Sourced from the GitHub GraphQL API via the authenticated `gh` CLI, bounded by the same
    `since` date as the commit-history metrics so it stays consistent with the rest of the strip
    (GraphQL defaults the `to` bound to now). Returns an int, or None if `gh` is unavailable /
    unauthenticated / errors — in which case the tile is simply not emitted and the build never
    breaks. This is the one metric that can't come from local git: GitHub aggregates it server-side.
    """
    frm = f"{since}T00:00:00Z" if since else "2026-01-01T00:00:00Z"
    query = ("query($from:DateTime!){viewer{contributionsCollection(from:$from)"
             "{contributionCalendar{totalContributions}}}}")
    try:
        out = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}", "-f", f"from={frm}"],
            capture_output=True, text=True, timeout=20)
        if out.returncode != 0:
            return None
        n = json.loads(out.stdout)["data"]["viewer"]["contributionsCollection"][
            "contributionCalendar"]["totalContributions"]
        return int(n) if isinstance(n, int) else None
    except Exception:
        return None


def latest_ship(repos, sources):
    """Only for the opt-in latest_ship card: newest published changelog headline + date.
    `sources` is an allowlist of 'repo_path::doc' the user marked public. Headline only."""
    best = None
    for src in sources or []:
        try:
            repo_raw, doc = src.split("::", 1)
        except ValueError:
            continue
        p = Path(os.path.expanduser(repo_raw)) / doc
        if not p.exists():
            continue
        text = open(p, encoding="utf-8", errors="ignore").read()
        # AIKC-style: <h2 class="cl-date">June 7, 2026</h2> ... <span class="cl-text">Headline</span>
        m = re.search(r'cl-text">([^<]+)<', text)
        d = re.search(r'cl-date">([^<]+)<', text)
        if m:
            best = {"headline": m.group(1).strip(), "date": (d.group(1).strip() if d else "")}
            break
    return best


# ── insight registry: key -> (accent, label, caption, value-fn) ─────────────────────────
def pct(n, d):
    return f"{round(100*n/d)}%" if d else "0%"


def make_insights(m):
    span_days = 0
    if m["dates"]:
        from datetime import date
        a = date.fromisoformat(m["dates"][0]); b = date.fromisoformat(m["dates"][-1])
        span_days = max((b - a).days, 1)
    cadence = m["commits"] / span_days if span_days else 0
    reg = {
        "commits":         ("g", f'{m["commits"]:,}', "commits shipped", f'across {m["projects"]} repos · 2026 to date'),
        "cadence":         ("g", f"{cadence:.1f}", "commits a day", "steady, iterative cadence"),
        "conventional":    ("b", pct(m["conv"], m["commits"]), "Conventional Commits", "structured, readable history"),
        "pr_driven":       ("b", f'{m["pr"]:,}', "changes shipped via PR", "reviewed — never straight to main"),
        "ai_assisted":     ("p", pct(m["ai"], m["commits"]), "AI-built commits", "I build with AI, and keep the receipts"),
        "tools_built":     ("p", str(m["skills"] + m["commands"] + m["agents"]), "custom AI tools", "skills & commands I built to extend my own workflow"),
        "guardrails":      ("a", str(m["hooks"]), "automated guardrails", "hooks that enforce my own discipline"),
        "evals":           ("p", str(m["evals"]), "eval fixtures", "AI quality measured, not guessed"),
        "knowledge_atoms": ("b", str(m["notes"] + m["concepts"]), "knowledge atoms", "notes + concepts wired into one map"),
        "learnings":       ("g", f'{m["learnings"]:,}', "lessons captured", "institutional memory, written as I go"),
        "changelog":       ("g", str(m["changelog"]), "documented changes", "every ship explained in plain English"),
        "docs":            ("a", str(m["md"] + m["html"]), "docs & diagrams", "documentation as a living spec"),
        "tracked_files":   ("t", f'{m["files"]:,}', "files under version control", "full-stack breadth"),
        "projects":        ("t", str(m["projects"]), "active projects", "public + private"),
    }
    # GitHub contributions: server-side aggregate, only present when `gh` resolved it.
    if m.get("gh_contributions") is not None:
        reg["github_contributions"] = (
            "g", f'{m["gh_contributions"]:,}', "GitHub contributions",
            "commits, PRs & reviews · public + private · 2026 to date")
    return reg


ACCENT_HEX = {"g": "#00D26A", "b": "#4F8CFF", "p": "#a855f7", "a": "#f59e0b", "t": "#94a3b8"}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render(cfg, m):
    insights = make_insights(m)
    tiles, emitted = [], []
    overrides = {i["key"]: i for i in cfg["insights"]}
    for item in cfg["insights"]:
        key = item["key"]
        if not item.get("enabled"):
            continue
        if key == "stack":
            tiles.append(render_stack(m))
            emitted.append({"key": "stack", "languages": m["languages"][:6]})
            continue
        if key == "latest_ship":
            opt = cfg.get("options", {}).get("latest_ship", {})
            ls = latest_ship(cfg["repos"], opt.get("sources")) if opt.get("enabled") else None
            if ls:
                tiles.append(render_latest(ls))
                emitted.append({"key": "latest_ship", **ls})
            continue
        if key not in insights:
            continue
        accent, value, label, caption = insights[key]
        o = overrides.get(key, {})
        accent = o.get("accent", accent); label = o.get("label", label); caption = o.get("caption", caption)
        tiles.append(
            f'      <div class="stat {accent}">\n'
            f'        <div class="stat-num">{esc(value)}</div>\n'
            f'        <div class="stat-label">{esc(label)}</div>\n'
            f'        <div class="stat-cap">{esc(caption)}</div>\n'
            f'      </div>'
        )
        emitted.append({"key": key, "value": value, "label": label, "caption": caption, "accent": accent})

    first = m["dates"][0] if m["dates"] else ""
    updated = m["dates"][-1] if m["dates"] else ""
    window = (f'Counts 2026 to date · git activity {first} → {updated}'
              if first else 'Counts 2026 to date')
    grid = ('    <div class="stat-grid">\n' + "\n".join(tiles) + "\n    </div>\n") if tiles else ""
    meta = (f'    <p class="stat-meta">{esc(window)} · commit history only; file/tooling counts are a '
            f'current snapshot · no private code or content. '
            f'<a href="https://github.com/vikkybharadwaj" target="_blank" rel="noopener">See the work →</a></p>')
    block = grid + meta
    return block, {"updated": updated, "first": first, "window": window, "insights": emitted}


def render_stack(m):
    langs = m["languages"][:6]
    total = sum(c for _, c in langs) or 1
    palette = ["#00D26A", "#4F8CFF", "#a855f7", "#f59e0b", "#22d3ee", "#94a3b8"]
    segs, legend = [], []
    for i, (name, c) in enumerate(langs):
        w = round(100 * c / total, 1)
        col = palette[i % len(palette)]
        segs.append(f'<span style="width:{w}%;background:{col}" title="{esc(name)} {w}%"></span>')
        legend.append(f'<i><b style="background:{col}"></b>{esc(name)} {w}%</i>')
    return (
        '      <div class="stat t stat-wide">\n'
        '        <div class="stat-label">the stack</div>\n'
        '        <div class="stat-cap">what I actually build with, across every repo</div>\n'
        f'        <div class="stackbar">{"".join(segs)}</div>\n'
        f'        <div class="stack-legend">{"".join(legend)}</div>\n'
        '      </div>'
    )


def render_latest(ls):
    when = f' · {esc(ls["date"])}' if ls.get("date") else ""
    return (
        '      <div class="stat g stat-wide">\n'
        '        <div class="stat-label">most recent ship' + when + '</div>\n'
        f'        <div class="stat-cap" style="font-size:13px;color:var(--text-2)">“{esc(ls["headline"])}”</div>\n'
        '      </div>'
    )


def main():
    cfg = json.load(open(CONFIG))
    m = scan(cfg["repos"], cfg.get("since"))
    # Only hit the GitHub API when the tile is actually enabled (avoids a needless network call).
    if any(i["key"] == "github_contributions" and i.get("enabled") for i in cfg["insights"]):
        m["gh_contributions"] = gh_contributions(cfg.get("since"))
    block, data = render(cfg, m)

    text = INDEX.read_text(encoding="utf-8")
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pat.search(text):
        raise SystemExit(f"error: {START}/{END} markers not found in {INDEX}")
    new = pat.sub(f"{START}\n{block}\n    {END}", text)
    if new != text:
        INDEX.write_text(new, encoding="utf-8")
        print(f"highlights: injected {len(data['insights'])} insights into index.html")
    else:
        print("highlights: index.html already up to date")

    DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
    DATA_OUT.write_text(json.dumps({"section": cfg.get("section", {}), **data}, indent=2) + "\n",
                        encoding="utf-8")
    print(f"highlights: wrote {DATA_OUT.relative_to(ROOT)} (updated {data['updated']})")


if __name__ == "__main__":
    raise SystemExit(main())
